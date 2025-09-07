# llm_server.py - LM Studio Connector for Cursor/VS Code
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
import requests
import json
import time
import logging
from datetime import datetime
import asyncio
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="LM Studio Connector",
    description="Connect Cursor and VS Code to LM Studio with OpenAI-compatible API",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LM Studio configuration
class Config:
    def __init__(self):
        self.lm_studio_url = "http://localhost:1234"
        self.api_base = f"{self.lm_studio_url}/v1"
        self.timeout = 300
        
    def update_url(self, url: str):
        self.lm_studio_url = url.rstrip('/')
        self.api_base = f"{self.lm_studio_url}/v1"

config = Config()

# Pydantic models for OpenAI compatibility
class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None
    top_p: Optional[float] = 1.0
    frequency_penalty: Optional[float] = 0.0
    presence_penalty: Optional[float] = 0.0
    stream: Optional[bool] = False
    stop: Optional[Union[str, List[str]]] = None

class ModelInfo(BaseModel):
    id: str
    object: str = "model"
    created: int = Field(default_factory=lambda: int(time.time()))
    owned_by: str = "lm-studio"

class ModelsResponse(BaseModel):
    object: str = "list"
    data: List[ModelInfo]

# Health check endpoint
@app.get("/health")
async def health_check():
    """Check if the server and LM Studio connection are healthy"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{config.api_base}/models")
            if response.status_code == 200:
                return {"status": "healthy", "lm_studio_connected": True}
            else:
                return {"status": "unhealthy", "lm_studio_connected": False, "error": f"LM Studio returned {response.status_code}"}
    except Exception as e:
        return {"status": "unhealthy", "lm_studio_connected": False, "error": str(e)}

# Configuration endpoint
@app.post("/config")
async def update_config(request: Dict[str, Any]):
    """Update LM Studio server configuration"""
    if "lm_studio_url" in request:
        config.update_url(request["lm_studio_url"])
        logger.info(f"Updated LM Studio URL to: {config.lm_studio_url}")
    return {"status": "updated", "config": {"lm_studio_url": config.lm_studio_url}}

@app.get("/config")
async def get_config():
    """Get current configuration"""
    return {"lm_studio_url": config.lm_studio_url, "api_base": config.api_base}

# OpenAI-compatible models endpoint
@app.get("/v1/models")
async def list_models():
    """List available models from LM Studio"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{config.api_base}/models")
            
            if response.status_code == 200:
                lm_studio_models = response.json()
                # Convert LM Studio format to OpenAI format
                models = []
                if "data" in lm_studio_models:
                    for model in lm_studio_models["data"]:
                        models.append(ModelInfo(id=model["id"]))
                else:
                    # Fallback for different LM Studio API versions
                    models = [ModelInfo(id="lm-studio-model")]
                
                return ModelsResponse(data=models)
            else:
                logger.error(f"Failed to fetch models: {response.status_code}")
                # Return default model if LM Studio is not responding
                return ModelsResponse(data=[ModelInfo(id="lm-studio-model")])
                
    except Exception as e:
        logger.error(f"Error fetching models: {str(e)}")
        # Return default model on error
        return ModelsResponse(data=[ModelInfo(id="lm-studio-model")])

# OpenAI-compatible chat completions endpoint
@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """Handle chat completions with streaming support"""
    try:
        # Prepare request for LM Studio
        lm_studio_request = {
            "model": request.model,
            "messages": [{"role": msg.role, "content": msg.content} for msg in request.messages],
            "temperature": request.temperature,
            "stream": request.stream,
        }
        
        # Add optional parameters if provided
        if request.max_tokens:
            lm_studio_request["max_tokens"] = request.max_tokens
        if request.top_p != 1.0:
            lm_studio_request["top_p"] = request.top_p
        if request.stop:
            lm_studio_request["stop"] = request.stop

        if request.stream:
            return StreamingResponse(
                stream_chat_completion(lm_studio_request),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Access-Control-Allow-Origin": "*",
                }
            )
        else:
            return await non_stream_chat_completion(lm_studio_request)
            
    except Exception as e:
        logger.error(f"Error in chat completion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def stream_chat_completion(lm_studio_request: dict):
    """Stream chat completion responses"""
    try:
        async with httpx.AsyncClient(timeout=config.timeout) as client:
            async with client.stream(
                "POST",
                f"{config.api_base}/chat/completions",
                json=lm_studio_request,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status_code != 200:
                    error_msg = f"LM Studio error: {response.status_code}"
                    yield f"data: {json.dumps({'error': {'message': error_msg, 'type': 'api_error'}})}\n\n"
                    return

                async for chunk in response.aiter_lines():
                    if chunk.startswith("data: "):
                        data = chunk[6:]  # Remove "data: " prefix
                        if data.strip() == "[DONE]":
                            yield f"data: [DONE]\n\n"
                            break
                        try:
                            # Forward the chunk as-is (LM Studio should already be OpenAI compatible)
                            yield f"data: {data}\n\n"
                        except json.JSONDecodeError:
                            continue
                            
    except Exception as e:
        logger.error(f"Streaming error: {str(e)}")
        yield f"data: {json.dumps({'error': {'message': str(e), 'type': 'connection_error'}})}\n\n"

async def non_stream_chat_completion(lm_studio_request: dict):
    """Handle non-streaming chat completion"""
    try:
        async with httpx.AsyncClient(timeout=config.timeout) as client:
            response = await client.post(
                f"{config.api_base}/chat/completions",
                json=lm_studio_request,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                error_msg = f"LM Studio error: {response.status_code} - {response.text}"
                raise HTTPException(status_code=response.status_code, detail=error_msg)
                
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request timeout")
    except Exception as e:
        logger.error(f"Non-streaming error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Legacy endpoint for backward compatibility
@app.post("/ask")
async def ask_llm_legacy(request: Dict[str, Any]):
    """Legacy endpoint for backward compatibility"""
    try:
        # Convert legacy format to OpenAI format
        messages = [{"role": "user", "content": request.get("prompt", "")}]
        model = request.get("model", "lm-studio-model")
        
        chat_request = ChatCompletionRequest(
            model=model,
            messages=[Message(role="user", content=request.get("prompt", ""))],
            stream=False
        )
        
        response = await non_stream_chat_completion({
            "model": model,
            "messages": messages,
            "temperature": 0.7,
            "stream": False
        })
        
        # Extract content from OpenAI format response
        if "choices" in response and len(response["choices"]) > 0:
            content = response["choices"][0]["message"]["content"]
            return {"response": content}
        else:
            return {"error": "No response generated"}
            
    except Exception as e:
        return {"error": str(e)}

# Root endpoint with API information
@app.get("/")
async def root():
    """API information and status"""
    return {
        "name": "LM Studio Connector",
        "version": "2.0.0",
        "description": "OpenAI-compatible API for LM Studio integration with Cursor/VS Code",
        "endpoints": {
            "health": "/health",
            "models": "/v1/models", 
            "chat": "/v1/chat/completions",
            "config": "/config"
        },
        "lm_studio_url": config.lm_studio_url,
        "status": "running"
    }

# Run with: uvicorn llm_server:app --reload --host 0.0.0.0 --port 8000
