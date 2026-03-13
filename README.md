# Telegram-Claude Bridge

A Telegram bot that gives you Claude Code CLI access from your phone. Send a message, and Claude Code executes it on your machine — reading files, writing code, running commands, managing projects.

## Features

- **Claude Code from Telegram** — every message runs through the Claude Code CLI
- **Conversation continuity** — follow-up messages keep context from prior exchanges
- **Full file system access** — works across all your projects under your home directory
- **Security** — whitelisted Telegram user IDs, rate limiting, concurrent request protection
- **Long responses** automatically split into multiple messages (Telegram's 4096 char limit)
- **Pro/Max subscription support** — uses your Claude.ai subscription, no API credits needed

## Prerequisites

- Python 3.9+
- A Telegram bot token (from [@BotFather](https://t.me/BotFather))
- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed and authenticated (`claude login`)

## Setup

1. **Clone and install dependencies:**

   ```bash
   git clone https://github.com/TheKhozaChain/telegram_claude.git
   cd telegram_claude
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Authenticate Claude Code CLI** (if not already done):

   ```bash
   claude login
   ```

   Sign in with your Claude.ai account (Pro or Max subscription).

3. **Get your Telegram user ID** by messaging [@userinfobot](https://t.me/userinfobot).

4. **Configure environment variables:**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your values:

   | Variable | Required | Description |
   |---|---|---|
   | `TELEGRAM_BOT_TOKEN` | Yes | Bot token from [@BotFather](https://t.me/BotFather) |
   | `ANTHROPIC_API_KEY` | No | Only needed if using API credits instead of subscription |
   | `ALLOWED_USER_IDS` | Yes | Comma-separated Telegram user IDs (whitelist) |
   | `CLAUDE_CLI_PATH` | No | Path to `claude` binary (default: `claude`) |
   | `RATE_LIMIT_CODE` | No | Max requests per minute (default: `10`) |

5. **Run the bot:**

   ```bash
   source venv/bin/activate
   python run.py
   ```

## Usage

Open your bot in Telegram and send any message. Claude Code handles it.

| Command | Description |
|---|---|
| `/start` | Welcome message |
| `/new` | Start a fresh conversation (resets context) |

### Examples

- `Create a React project called my-app in my home directory`
- `Show me the file structure of my-app`
- `Add a login page component to my-app`
- `Delete the old-project directory`
- `Read the README in my crypto-analyst project and summarize it`

Follow-up messages maintain context, so you can have back-and-forth conversations. Use `/new` when you want to start a fresh topic.

## Project Structure

```
telegram_claude/
├── run.py                # Entry point
├── .env.example          # Environment variable template
├── requirements.txt      # Python dependencies
└── bot/
    ├── main.py           # Application setup and handler registration
    ├── config.py         # Environment variable loading and validation
    ├── security.py       # Auth decorator and rate limiter
    ├── handlers.py       # Telegram command and message handlers
    ├── code_backend.py   # Claude CLI subprocess integration
    └── utils.py          # Message chunking and sending
```

## Security

- **User whitelist** — only Telegram IDs listed in `ALLOWED_USER_IDS` can use the bot
- **No secrets in code** — all credentials loaded from `.env` (gitignored)
- **No shell injection** — CLI invoked via `create_subprocess_exec` (no shell mode)
- **Rate limiting** — prevents abuse (configurable per-minute limit)
- **`CLAUDECODE` env var stripped** — allows CLI subprocess invocation without conflicts

> **Important:** This bot gives Claude Code full access to your file system. Only add your own Telegram user ID to the whitelist. Never share your `.env` file or bot token.

## Using API Credits Instead of Subscription

By default, the bot uses your Claude.ai subscription (via `claude login`). To use API credits instead, set `ANTHROPIC_API_KEY` in your `.env` file — the bot will pass it to the CLI.

## License

MIT
