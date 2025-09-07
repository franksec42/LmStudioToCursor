# LM Studio Connector for Cursor & VS Code

A powerful, OpenAI-compatible API server that connects Cursor and VS Code to LM Studio, enabling you to use local open-source models with the same interface as GPT-4.

## ✨ Features

- **OpenAI-Compatible API**: Full compatibility with OpenAI's chat completions API
- **Streaming Support**: Real-time response streaming for better user experience  
- **Multiple Model Support**: Automatic discovery and switching between LM Studio models
- **Health Monitoring**: Built-in health checks and connection monitoring
- **Easy Configuration**: Simple JSON configuration and automatic setup
- **Dual Server Options**: Choose between FastAPI (recommended) or Flask implementations
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** (tested with Python 3.10 and 3.11)
- **LM Studio** (latest version)
- **Cursor** or **VS Code**

### Installation

1. **Clone or download this repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Setup & Usage

#### Option 1: Automated Setup (Recommended)

1. **Start LM Studio:**
   - Open LM Studio
   - Load your desired model
   - Click "Start Server" in the Local Server tab
   - Note the server URL (usually `http://localhost:1234`)

2. **Start the connector:**
   ```bash
   python start_server.py
   ```

   if not starting use
   ```bash
   uvicorn llm_server:app --reload --host 0.0.0.0 --port 8000
   ```


   start ngrok
   ```bash
   ngrok http http://127.0.0.1:1234
   ```
   
   The script will:
   - Check all dependencies
   - Verify LM Studio connection
   - Start the API server on `http://localhost:8000`
   - Show you the API documentation URL

3. **Configure Cursor/VS Code:**
   - Copy settings from `vscode_settings.json` to your editor's settings
   - Or manually configure:
     - API Key: `lm-studio-key` (any value)
     - API Base URL: `http://localhost:8000/v1`
     - Model: Use any name (will auto-detect from LM Studio)

#### Option 2: Manual Setup

1. **Start LM Studio server** (as above)

2. **Start the FastAPI server:**
   ```bash
   uvicorn llm_server:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Configure your editor** (as above)

## 🔧 Configuration

### Server Configuration

Edit `config.json` to customize the server behavior:

```json
{
  "lm_studio": {
    "url": "http://localhost:1234",
    "timeout": 300,
    "default_model": "lm-studio-model"
  },
  "server": {
    "host": "0.0.0.0",
    "port": 8000,
    "reload": true
  }
}
```

### Editor Configuration

#### For Cursor

Add to your Cursor settings (`Cmd/Ctrl + ,` → Open Settings JSON):

```json
{
  "openai.apiKey": "lm-studio-key",
  "openai.apiBase": "http://localhost:8000/v1",
  "openai.model": "lm-studio-model"
}
```

#### For VS Code with AI Extensions

Different extensions may require different settings. Check `vscode_settings.json` for examples.

## 📡 API Endpoints

The connector provides a full OpenAI-compatible API:

- **Chat Completions**: `POST /v1/chat/completions`
- **Models List**: `GET /v1/models`
- **Health Check**: `GET /health`
- **Configuration**: `GET/POST /config`
- **API Docs**: `http://localhost:8000/docs` (when running)

### Example Usage

```bash
# Check health
curl http://localhost:8000/health

# List available models
curl http://localhost:8000/v1/models

# Chat completion
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "lm-studio-model",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": false
  }'
```

## 🚨 Troubleshooting

### Common Issues

**"Cannot connect to LM Studio"**
- Ensure LM Studio is running and the local server is started
- Check that the URL in `config.json` matches LM Studio's server URL
- Try accessing `http://localhost:1234/v1/models` in your browser

**"No models found"**
- Make sure a model is loaded in LM Studio
- Verify the model is showing as "Loaded" in LM Studio
- Try restarting both LM Studio and the connector

**"Connection timeout"**
- Increase the timeout value in `config.json`
- Check your firewall settings
- Try using `127.0.0.1` instead of `localhost`

**Editor not using the local model**
- Verify the API key is set (can be any value)
- Check that the API base URL is correct
- Restart your editor after changing settings
- Look for error messages in the editor's developer console

### Advanced Configuration

**Custom LM Studio URL:**
```bash
python start_server.py --config custom_config.json
```

**Different Port:**
```bash
python start_server.py --port 9000
```

**Skip Connection Checks:**
```bash
python start_server.py --skip-checks
```

## 🔄 Switching Between Models

1. **In LM Studio**: Load a different model
2. **Restart the connector**: The new model will be auto-detected
3. **In your editor**: The model name will update automatically

To use multiple models simultaneously, run multiple instances of the connector on different ports.

## 🏛️ Legacy Flask Server

The repository includes a Flask-based server (`v1.py`) for compatibility. To use it:

```bash
python v1.py
```

The Flask server runs on port 5000 and provides similar functionality with a different implementation.

## ⚡ Performance Tips

- **Use streaming**: Enable streaming in your editor for faster response times
- **Adjust temperature**: Lower values (0.1-0.3) for code, higher (0.7-1.0) for creative tasks
- **Model selection**: Choose appropriate model size for your hardware
- **Memory management**: Monitor RAM usage, especially with larger models

## 🔐 Security Notes

- The connector runs locally and doesn't send data to external servers
- Use `127.0.0.1` instead of `0.0.0.0` if you don't need network access
- Consider firewall rules if running on a network
- The API key can be any value - it's not validated for security

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/improvement`
3. **Make your changes**: Follow the existing code style
4. **Test thoroughly**: Ensure compatibility with different LM Studio versions
5. **Commit changes**: `git commit -am 'Add new feature'`
6. **Push to branch**: `git push origin feature/improvement`
7. **Create Pull Request**: Describe your changes clearly

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/LmStudioToCursor.git
cd LmStudioToCursor

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
python -m pytest

# Format code
black *.py

# Lint code
flake8 *.py
```

## 📋 Dependencies

Current dependencies installed via `requirements.txt`:

- **FastAPI 0.115.6**: Modern web framework for the API server
- **Uvicorn 0.34.0**: ASGI server for running FastAPI
- **HTTPX 0.28.1**: Async HTTP client for LM Studio communication
- **Requests 2.32.3**: HTTP library for synchronous requests
- **Flask 3.1.2 + Flask-CORS 6.0.1**: Alternative server implementation
- **OpenAI 1.106.1**: OpenAI Python client for compatibility
- **Pydantic**: Data validation and settings management

## 🆚 FastAPI vs Flask

| Feature | FastAPI (Recommended) | Flask (Legacy) |
|---------|----------------------|----------------|
| **Performance** | ⚡ Async, faster | 🐌 Sync, slower |
| **Streaming** | ✅ Native support | ✅ Supported |
| **Documentation** | ✅ Auto-generated | ❌ Manual |
| **Type Safety** | ✅ Pydantic models | ❌ Basic |
| **Modern Features** | ✅ Latest async/await | ❌ Traditional |
| **Port** | 8000 | 5000 |

## 🔄 Version History

- **v2.0.0**: Complete rewrite with FastAPI, OpenAI compatibility, streaming support
- **v1.0.0**: Initial Flask-based implementation

## 📞 Support & Contact

- **GitHub Issues**: [Report bugs or request features](https://github.com/olweraltuve/LmStudioToCursor/issues)
- **Discussions**: [Community discussions and Q&A](https://github.com/olweraltuve/LmStudioToCursor/discussions)
- **LinkedIn**: [Oliver Altuve](https://www.linkedin.com/in/olwer-altuve-santaromita-97824518a/)
- **Email**: olwerjose33@hotmail.com

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **LM Studio Team**: For creating an excellent local LLM platform
- **Cursor Team**: For building an amazing AI-powered code editor
- **OpenAI**: For establishing the API standards we follow
- **FastAPI**: For providing a modern, fast web framework

---

⭐ **Star this repository if it helps you use local LLMs with Cursor/VS Code!**