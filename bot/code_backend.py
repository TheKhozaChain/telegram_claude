import os
import asyncio
from bot import config

TIMEOUT_SECONDS = 300
WORKING_DIR = "/Users/siphokhoza"


async def send(user_id: int, message_text: str, is_continuation: bool = False) -> str:
    """Send a prompt to Claude Code CLI and return the response."""
    env = {k: v for k, v in os.environ.items() if k not in ("CLAUDECODE", "ANTHROPIC_API_KEY")}

    cmd = [
        config.CLAUDE_CLI_PATH,
        "-p", message_text,
        "--output-format", "text",
        "--max-turns", "10",
        "--dangerously-skip-permissions",
    ]

    if is_continuation:
        cmd.append("--continue")

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=WORKING_DIR,
            env=env,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await asyncio.wait_for(
            proc.communicate(),
            timeout=TIMEOUT_SECONDS,
        )

        if proc.returncode != 0:
            error_msg = stderr.decode("utf-8", errors="replace").strip()
            # If --continue failed, retry without it
            if is_continuation and error_msg:
                return await send(user_id, message_text, is_continuation=False)
            return f"Error (exit {proc.returncode}):\n{error_msg or '(no output)'}"

        result = stdout.decode("utf-8", errors="replace").strip()
        return result or "(empty response)"

    except asyncio.TimeoutError:
        proc.kill()
        await proc.wait()
        return f"Timed out after {TIMEOUT_SECONDS}s. Try a simpler request."
    except FileNotFoundError:
        return f"Claude CLI not found at: {config.CLAUDE_CLI_PATH}"
    except Exception as e:
        return f"Error: {e}"
