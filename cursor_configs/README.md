# Cursor Configuration Files for Different LM Studio Models

This directory contains pre-configured settings.json files for each of your LM Studio models. Simply copy the content of the desired model configuration to your Cursor settings.json file.

## 🚀 How to Use

1. **Choose your model** from the configurations below
2. **Copy the entire JSON content** from the corresponding file
3. **Replace your Cursor settings.json** with the copied content
4. **Restart Cursor**
5. **Test with Cmd+K** (Mac) or Ctrl+K (Windows/Linux)

## 📋 Available Model Configurations

| Model | Size | Best For | File |
|-------|------|----------|------|
| **qwen/qwen3-30b-a3b-2507** | 30B | General AI tasks, complex reasoning | `qwen3-30b.json` |
| **qwen/qwen2.5-coder-14b** | 14B | **Coding, programming** | `qwen2.5-coder-14b.json` |
| **qwen/qwen3-coder-480b** | 480B | **Large-scale coding** | `qwen3-coder-480b.json` |
| **deepseek-r1-distill-llama-8b** | 8B | **Reasoning, math, logic** | `deepseek-r1-8b.json` |
| **meta-llama-3.1-8b-instruct** | 8B | General tasks, fast responses | `llama-3.1-8b.json` |
| **mistral-nemo-instruct-2407** | 12B | Balanced performance | `mistral-nemo.json` |
| **llama-3.2-3b-instruct** | 3B | **Fast, lightweight** | `llama-3.2-3b.json` |
| **hermes-3-llama-3.2-3b** | 3B | Chat, creative writing | `hermes-3-3b.json` |
| **devstral-small-2507-mlx** | 22B | **Code generation** | `devstral-small.json` |
| **claude2-alpaca-13b** | 13B | Instruction following | `claude2-alpaca.json` |
| **openai/gpt-oss-20b** | 20B | GPT-like responses | `gpt-oss-20b.json` |

## 💡 **Recommended Models by Use Case**

### 🧑‍💻 **For Coding:**
- **Primary**: `qwen/qwen2.5-coder-14b` (Best balance of speed/quality)
- **Heavy**: `qwen/qwen3-coder-480b` (Most capable but slower)
- **Fast**: `devstral-small-2507-mlx` (Quick code suggestions)

### 🧠 **For Reasoning/Math:**
- **Primary**: `deepseek-r1-distill-llama-8b` (New reasoning model)
- **Alternative**: `qwen/qwen3-30b-a3b-2507` (General reasoning)

### ⚡ **For Speed:**
- **Fastest**: `llama-3.2-3b-instruct` (3B parameters)
- **Balanced**: `meta-llama-3.1-8b-instruct` (8B parameters)

### 📝 **For Writing/Chat:**
- **Creative**: `hermes-3-llama-3.2-3b`
- **General**: `mistral-nemo-instruct-2407`

## 🔧 **Quick Switch Commands**

```bash
# Copy a model configuration to Cursor settings
cp cursor_configs/qwen2.5-coder-14b.json "/Users/$(whoami)/Library/Application Support/Cursor/User/settings.json"

# Or manually copy the content and paste into Cursor settings
```

## ⚠️ **Important Notes**

1. **Load the model in LM Studio first** before switching in Cursor
2. **Restart Cursor** after changing the model configuration
3. **Only one model can be active** in LM Studio at a time
4. **Larger models require more RAM** and are slower
5. **The connector must be running** (`uvicorn llm_server:app --reload --host 0.0.0.0 --port 8000`)
