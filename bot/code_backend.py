import os
import asyncio
import subprocess
from bot import config


def _snapshot_git_repos(working_dir: str) -> list[str]:
    """Auto-commit uncommitted changes in git repos under working_dir as a safety snapshot.

    Returns list of directories where snapshots were created.
    """
    snapped = []
    dirs_to_check = [working_dir]

    # Also check immediate subdirectories (for when WORKING_DIR is ~)
    try:
        for entry in os.scandir(working_dir):
            if entry.is_dir() and not entry.name.startswith('.'):
                if os.path.isdir(os.path.join(entry.path, '.git')):
                    dirs_to_check.append(entry.path)
    except OSError:
        pass

    for d in dirs_to_check:
        if not os.path.isdir(os.path.join(d, '.git')):
            continue
        try:
            # Check if there are any uncommitted changes
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=d, capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0 and result.stdout.strip():
                subprocess.run(
                    ['git', 'add', '-A'],
                    cwd=d, capture_output=True, timeout=10,
                )
                subprocess.run(
                    ['git', 'commit', '-m', '[teleclaude] auto-snapshot before new task'],
                    cwd=d, capture_output=True, timeout=10,
                )
                snapped.append(d)
        except Exception:
            pass

    return snapped


async def send(user_id: int, message_text: str, is_continuation: bool = False) -> str:
    """Send a prompt to Claude Code CLI and return the response."""
    # Snapshot git repos before making changes
    if not is_continuation:
        await asyncio.to_thread(_snapshot_git_repos, config.WORKING_DIR)

    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

    # Use API key if configured, otherwise fall back to CLI's own auth (subscription)
    if config.ANTHROPIC_API_KEY:
        env["ANTHROPIC_API_KEY"] = config.ANTHROPIC_API_KEY
    else:
        env.pop("ANTHROPIC_API_KEY", None)

    cmd = [
        config.CLAUDE_CLI_PATH,
        "-p", message_text,
        "--output-format", "text",
        "--max-turns", "50",
        "--dangerously-skip-permissions",
    ]

    if is_continuation:
        cmd.append("--continue")

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=config.WORKING_DIR,
            env=env,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await proc.communicate()

        if proc.returncode != 0:
            error_msg = stderr.decode("utf-8", errors="replace").strip()
            # If --continue failed, retry without it
            if is_continuation and error_msg:
                return await send(user_id, message_text, is_continuation=False)
            return f"Error (exit {proc.returncode}):\n{error_msg or '(no output)'}"

        result = stdout.decode("utf-8", errors="replace").strip()
        return result or "(empty response)"

    except FileNotFoundError as e:
        if not os.path.isdir(config.WORKING_DIR):
            return f"Working directory not found: {config.WORKING_DIR}"
        return f"Claude CLI not found at: {config.CLAUDE_CLI_PATH}"
    except Exception as e:
        return f"Error: {e}"
