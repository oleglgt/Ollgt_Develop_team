"""
Orchestrator — Main entry point for the AI Development Team.

Polls GitHub Issues for tasks assigned to each agent role,
dispatches them to the appropriate agent, and manages the workflow.

Usage:
    python agents/orchestrator.py
"""

import os
import sys
import time
import logging
from datetime import datetime

from dotenv import load_dotenv
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.tools.github_tools import get_issues_by_label
from agents.tools.telegram_tools import send_message_sync, notify_error
from agents.architect import ARCHITECT_SYSTEM_PROMPT, ARCHITECT_TOOLS
from agents.developer import DEVELOPER_SYSTEM_PROMPT, DEVELOPER_TOOLS
from agents.tester import TESTER_SYSTEM_PROMPT, TESTER_TOOLS

load_dotenv()

# ── Configuration ───────────────────────────────────

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250929")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "30"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

console = Console()

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(message)s",
    handlers=[RichHandler(console=console, rich_tracebacks=True)],
)
log = logging.getLogger("orchestrator")

# Track processed issues to avoid duplicate processing
processed_issues: set[int] = set()


# ── Agent Dispatcher ────────────────────────────────

def dispatch_to_agent(role: str, issue: dict) -> None:
    """
    Dispatch an issue to the appropriate agent.
    
    This is where the Claude Agent SDK integration will happen.
    For now, this is a placeholder that logs the dispatch.
    
    TODO: Replace with actual Claude Agent SDK calls:
    
    ```python
    from anthropic import Anthropic
    
    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    
    # For Architect (leader):
    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=8000,
        system=ARCHITECT_SYSTEM_PROMPT,
        tools=[...tool_definitions...],
        messages=[{
            "role": "user",
            "content": f"Process this task:\\n\\nTitle: {issue['title']}\\nDescription: {issue['body']}\\nIssue: #{issue['number']}"
        }]
    )
    ```
    
    Args:
        role: Agent role ('architect', 'developer', 'tester')
        issue: Issue dict from GitHub
    """
    log.info(f"[{role.upper()}] Processing #{issue['number']}: {issue['title']}")
    
    # ── Placeholder: log what would happen ──
    # In production, this calls Claude Agent SDK
    
    prompts = {
        "architect": (
            f"New task received. Analyze and create a specification.\n\n"
            f"Issue #{issue['number']}: {issue['title']}\n\n"
            f"Description:\n{issue['body']}"
        ),
        "developer": (
            f"New development task. Read the spec and write code.\n\n"
            f"Issue #{issue['number']}: {issue['title']}\n\n"
            f"Description:\n{issue['body']}"
        ),
        "tester": (
            f"New task for testing. Review the PR and run tests.\n\n"
            f"Issue #{issue['number']}: {issue['title']}\n\n"
            f"Description:\n{issue['body']}"
        ),
    }
    
    console.print(Panel(
        f"[bold]{role.upper()}[/bold] would process:\n"
        f"Issue #{issue['number']}: {issue['title']}\n\n"
        f"Prompt:\n{prompts.get(role, 'Unknown role')[:200]}...",
        title=f"🤖 Agent Dispatch — {role}",
        border_style="blue",
    ))
    
    # Mark as processed
    processed_issues.add(issue["number"])


# ── Polling Loop ────────────────────────────────────

def poll_cycle() -> int:
    """
    Run one polling cycle: check for tasks for each agent role.
    
    Returns:
        Number of tasks dispatched
    """
    dispatched = 0
    
    roles = [
        ("role:architect", "architect"),
        ("role:developer", "developer"),
        ("role:tester", "tester"),
    ]
    
    for label, role in roles:
        try:
            issues = get_issues_by_label(label)
            for issue in issues:
                if issue["number"] not in processed_issues:
                    dispatch_to_agent(role, issue)
                    dispatched += 1
        except Exception as e:
            log.error(f"Error polling {label}: {e}")
            try:
                notify_error(role, str(e))
            except Exception:
                pass
    
    return dispatched


def main():
    """Main entry point — start the polling loop."""
    
    # ── Validate configuration ──
    missing = []
    if not ANTHROPIC_API_KEY:
        missing.append("ANTHROPIC_API_KEY")
    if not os.getenv("GITHUB_TOKEN"):
        missing.append("GITHUB_TOKEN")
    if not os.getenv("TELEGRAM_BOT_TOKEN"):
        missing.append("TELEGRAM_BOT_TOKEN")
    if not os.getenv("TELEGRAM_CHAT_ID"):
        missing.append("TELEGRAM_CHAT_ID")
    
    if missing:
        console.print(f"[red]Missing environment variables: {', '.join(missing)}[/red]")
        console.print("Copy .env.example to .env and fill in your values.")
        sys.exit(1)
    
    # ── Startup banner ──
    console.print(Panel(
        f"[bold green]AI Development Team — Orchestrator[/bold green]\n\n"
        f"Model: {CLAUDE_MODEL}\n"
        f"Repo: {os.getenv('GITHUB_OWNER')}/{os.getenv('GITHUB_REPO')}\n"
        f"Poll interval: {POLL_INTERVAL}s\n"
        f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        title="🚀 Starting",
        border_style="green",
    ))
    
    # Notify on Telegram
    try:
        send_message_sync("🚀 <b>Orchestrator started</b>\nWaiting for tasks...")
    except Exception as e:
        log.warning(f"Could not send Telegram notification: {e}")
    
    # ── Polling loop ──
    try:
        while True:
            dispatched = poll_cycle()
            if dispatched > 0:
                log.info(f"Dispatched {dispatched} task(s)")
            else:
                log.debug("No new tasks")
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        console.print("\n[yellow]Shutting down...[/yellow]")
        try:
            send_message_sync("⏹ <b>Orchestrator stopped</b>")
        except Exception:
            pass


if __name__ == "__main__":
    main()
