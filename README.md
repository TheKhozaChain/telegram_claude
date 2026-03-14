# Telegram-Claude Bridge

A personal tool that gives you Claude Code CLI access from Telegram. Send a message from your phone, and Claude Code executes it on your machine — reading files, writing code, running commands, managing projects.

> **Note:** This is a personal power tool designed for solo use on your own machine. It is not a production-grade multi-user system.

## Features

- **Claude Code from Telegram** — every message runs through the Claude Code CLI
- **Conversation continuity** — follow-up messages continue the same CLI session via `--continue`
- **Full file system access** — works across all your projects (configurable working directory)
- **Security** — whitelisted Telegram user IDs, rate limiting, concurrent request protection
- **Long responses** automatically split into multiple messages (Telegram's 4096 char limit)
- **Flexible auth** — works with Claude.ai subscription (Pro/Max) or API credits

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
   | `ALLOWED_USER_IDS` | Yes | Comma-separated Telegram user IDs (whitelist) |
   | `ANTHROPIC_API_KEY` | No | Set to use API credits; leave empty to use your Claude.ai subscription |
   | `CLAUDE_CLI_PATH` | No | Path to `claude` binary (default: `claude`) |
   | `WORKING_DIR` | No | Root working directory for Claude Code (default: your home directory) |
   | `RATE_LIMIT_CODE` | No | Max requests per minute (default: `10`) |

5. **Run the bot:**

   ```bash
   source venv/bin/activate
   python run.py
   ```

### Auto-start on login (macOS)

To have the bot start automatically when you log in and restart if it crashes:

```bash
cp com.thekhozachain.telegramclaude.plist ~/Library/LaunchAgents/
```

**Edit the plist file first** — replace `/PATH/TO/telegram_claude` with your actual install path.

```bash
launchctl load ~/Library/LaunchAgents/com.thekhozachain.telegramclaude.plist
```

Manage the service:

```bash
# Stop the bot
launchctl unload ~/Library/LaunchAgents/com.thekhozachain.telegramclaude.plist

# Start the bot
launchctl load ~/Library/LaunchAgents/com.thekhozachain.telegramclaude.plist

# Check logs
tail -f ~/telegram_claude/bot.log
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

Follow-up messages maintain context via Claude Code's `--continue` flag, so you can have back-and-forth conversations. Use `/new` when you want to start a fresh topic.

## Project Structure

```
telegram_claude/
├── run.py                                      # Entry point
├── .env.example                                # Environment variable template
├── requirements.txt                            # Python dependencies
├── com.thekhozachain.telegramclaude.plist       # macOS launch agent template
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
- **`--dangerously-skip-permissions`** — required because there is no TTY for interactive permission prompts. The security boundary is the Telegram user whitelist. Only add your own user ID.

> **Important:** This bot gives Claude Code full access to your file system. Only add your own Telegram user ID to the whitelist. Never share your `.env` file or bot token.

## Authentication

The bot supports two authentication methods for the Claude Code CLI:

| Method | How | When to use |
|---|---|---|
| **Subscription** (default) | Run `claude login` before starting the bot | You have a Claude Pro or Max plan |
| **API credits** | Set `ANTHROPIC_API_KEY` in `.env` | You want to use pay-per-token billing |

If `ANTHROPIC_API_KEY` is set, it takes priority. If empty or unset, the CLI uses whatever auth was configured via `claude login`.

## License

MIT
