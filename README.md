# Gemini Discord AI Bot

An AI agent powered by Google's Gemini API that can reason about a task, call tools, and act on a local codebase. It runs either as a command-line tool or as a Discord bot with per-channel conversation memory.

## Features

- **Gemini-powered agent** with function calling to plan and execute multi-step tasks.
- **File system tools**: list files/directories, read file contents, write/overwrite files, and execute Python files — all sandboxed to a working directory for safety.
- **Web search** via the Tavily API for looking up definitions and information.
- **Two interfaces**: a CLI (`main.py`) and a Discord bot (`bot.py`).
- **Conversation memory** per Discord channel so the bot keeps context.

## Project Structure

```
.
├── agent.py            # Core agent loop used by the Discord bot
├── bot.py              # Discord bot entry point (per-channel memory)
├── main.py             # CLI entry point
├── functions/          # Tool implementations + schemas
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── run_python_file.py
│   ├── write_file.py
│   ├── search_web.py
│   └── schema_all_functions.py
├── calculator/         # Sample project the agent can operate on
├── tests.py
├── pyproject.toml
└── .python-version
```

## Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) for dependency management
- A Google Gemini API key
- A Discord bot token (only for the Discord interface)
- A Tavily API key (only for the web search tool)

## Installation

```bash
git clone https://github.com/Yhangzzz12/aiagent.git
cd aiagent
uv sync
```

## Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
DISCORD_TOKEN=your_discord_bot_token
API_KEY=your_tavily_api_key
```

For the Discord bot, enable the **Message Content Intent** in the Discord Developer Portal.

## Usage

### CLI

```bash
uv run main.py "your prompt here"
```

Add `--verbose` to see the function-call plan and token details:

```bash
uv run main.py "list the files in the calculator directory" --verbose
```

### Discord bot

```bash
uv run bot.py
```

Once running and invited to your server, the bot responds to messages and keeps conversation history per channel.

## Tools Available to the Agent

| Tool | Description |
|------|-------------|
| `get_files_info` | List files and directories |
| `get_file_content` | Read the contents of a file |
| `write_file` | Write or overwrite a file |
| `run_python_file` | Execute a Python file with optional arguments |
| `web_search` | Search the web via the Tavily API |

All file paths are relative to the working directory, which is injected automatically for security.

## Notes

Never commit your `.env` file or API keys — the included `.gitignore` already excludes `.env`.
