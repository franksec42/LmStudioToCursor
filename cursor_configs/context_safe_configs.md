# Context-Safe Model Configurations

## 🚨 **Issue**: Context Length Error

LM Studio is reporting: "The number of tokens to keep from the initial prompt is greater than the context length"

## 🔧 **Solution**: Reduced Token Limits

These configurations use much smaller `maxTokens` values to prevent context overflow:

### ⚡ **Quick Fix Settings**

Add these to your Cursor settings.json (replace existing OpenAI settings):

```json
{
    "openai.apiKey": "lm-studio-key",
    "openai.apiBase": "http://localhost:8000/v1",
    "openai.model": "qwen/qwen3-30b-a3b-2507",
    "openai.temperature": 0.7,
    "openai.maxTokens": 512
}
```

### 📋 **Context-Safe Token Limits by Model**

| Model | Safe Max Tokens | Context Window |
|-------|----------------|----------------|
| **qwen/qwen3-30b-a3b-2507** | 512 | Small context |
| **qwen/qwen2.5-coder-14b** | 256 | Very small |
| **deepseek-r1-distill-llama-8b** | 384 | Small |
| **meta-llama-3.1-8b-instruct** | 512 | Medium |
| **llama-3.2-3b-instruct** | 256 | Small |
| **mistral-nemo-instruct-2407** | 768 | Medium |

### 🎯 **Recommended Settings for Different Tasks**

#### **For Coding (Short responses):**
```json
{
    "openai.model": "qwen/qwen2.5-coder-14b",
    "openai.temperature": 0.2,
    "openai.maxTokens": 256
}
```

#### **For General Chat:**
```json
{
    "openai.model": "qwen/qwen3-30b-a3b-2507", 
    "openai.temperature": 0.7,
    "openai.maxTokens": 512
}
```

#### **For Quick Responses:**
```json
{
    "openai.model": "llama-3.2-3b-instruct",
    "openai.temperature": 0.8, 
    "openai.maxTokens": 256
}
```

## 🔍 **Why This Happens**

1. **Small Context Window**: The model was loaded with limited context
2. **Large Token Request**: Cursor requested too many tokens
3. **Prompt + Response**: Combined size exceeded available context

## 💡 **Solutions**

### **Option 1: Reduce Token Limits (Recommended)**
- Use the configurations above with smaller `maxTokens`
- Responses will be shorter but won't error

### **Option 2: Increase LM Studio Context**
1. In LM Studio, go to model settings
2. Increase "Context Length" (e.g., 4096, 8192)
3. Reload the model
4. Use larger `maxTokens` values

### **Option 3: Use Smaller Models**
- Switch to 3B or 8B models (they need less context)
- Use `llama-3.2-3b-instruct` or `meta-llama-3.1-8b-instruct`
