"""
Orchestrator — Main entry point for the AI Development Team.

Polls GitHub Issues for tasks assigned to each agent role,
dispatches them to Claude API, and manages the workflow.

Usage:
    python agents/orchestrator.py
"""

import os
import sys
import time
import json
import logging
from datetime import datetime

from dotenv import load_dotenv
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
import anthropic

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.tools.github_tools import (
    get_issues_by_label, create_issue, add_comment, update_issue_labels,
    close_issue, create_branch, create_or_update_file, create_pull_request,
    get_pr_diff, merge_pull_request, create_release, get_file_content,
)
from agents.tools.telegram_tools import (
    send_message_sync, notify_spec_ready, notify_pr_created,
    notify_test_passed, notify_test_failed, notify_release,
    notify_release_verified, notify_error,
)
from agents.architect import ARCHITECT_SYSTEM_PROMPT
from agents.developer import DEVELOPER_SYSTEM_PROMPT
from agents.tester import TESTER_SYSTEM_PROMPT

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

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


# ── Tool Definitions for Claude ─────────────────────

TOOL_DEFINITIONS = [
    {
        "name": "get_issues_by_label",
        "description": "Fetch open GitHub issues with a specific label. Returns list of issues with number, title, body, labels, url.",
        "input_schema": {
            "type": "object",
            "properties": {
                "label": {"type": "string", "description": "Label name, e.g. 'role:architect'"}
            },
            "required": ["label"]
        }
    },
    {
        "name": "create_issue",
        "description": "Create a new GitHub issue with title, body, and labels.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Issue title"},
                "body": {"type": "string", "description": "Issue body in markdown"},
                "labels": {"type": "array", "items": {"type": "string"}, "description": "List of label names"}
            },
            "required": ["title", "body", "labels"]
        }
    },
    {
        "name": "add_comment",
        "description": "Add a comment to an existing GitHub issue.",
        "input_schema": {
            "type": "object",
            "properties": {
                "issue_number": {"type": "integer", "description": "Issue number"},
                "body": {"type": "string", "description": "Comment body in markdown"}
            },
            "required": ["issue_number", "body"]
        }
    },
    {
        "name": "update_issue_labels",
        "description": "Add or remove labels from a GitHub issue.",
        "input_schema": {
            "type": "object",
            "properties": {
                "issue_number": {"type": "integer", "description": "Issue number"},
                "add_labels": {"type": "array", "items": {"type": "string"}, "description": "Labels to add"},
                "remove_labels": {"type": "array", "items": {"type": "string"}, "description": "Labels to remove"}
            },
            "required": ["issue_number"]
        }
    },
    {
        "name": "close_issue",
        "description": "Close a GitHub issue.",
        "input_schema": {
            "type": "object",
            "properties": {
                "issue_number": {"type": "integer", "description": "Issue number"}
            },
            "required": ["issue_number"]
        }
    },
    {
        "name": "create_branch",
        "description": "Create a new git branch from base branch.",
        "input_schema": {
            "type": "object",
            "properties": {
                "branch_name": {"type": "string", "description": "New branch name, e.g. 'feature/2-hello-api'"},
                "base": {"type": "string", "description": "Base branch name, default 'main'"}
            },
            "required": ["branch_name"]
        }
    },
    {
        "name": "create_or_update_file",
        "description": "Create or update a file in the GitHub repository on a specific branch.",
        "input_schema": {
            "type": "object",
            "properties": {
                "branch": {"type": "string", "description": "Branch name"},
                "path": {"type": "string", "description": "File path in repo, e.g. 'src/main.py'"},
                "content": {"type": "string", "description": "File content"},
                "message": {"type": "string", "description": "Commit message"}
            },
            "required": ["branch", "path", "content", "message"]
        }
    },
    {
        "name": "create_pull_request",
        "description": "Create a pull request from head branch to base branch.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "PR title"},
                "body": {"type": "string", "description": "PR body in markdown"},
                "head": {"type": "string", "description": "Source branch name"},
                "base": {"type": "string", "description": "Target branch name, default 'main'"}
            },
            "required": ["title", "body", "head"]
        }
    },
    {
        "name": "get_pr_diff",
        "description": "Get the diff content of a pull request.",
        "input_schema": {
            "type": "object",
            "properties": {
                "pr_number": {"type": "integer", "description": "Pull request number"}
            },
            "required": ["pr_number"]
        }
    },
    {
        "name": "merge_pull_request",
        "description": "Merge a pull request.",
        "input_schema": {
            "type": "object",
            "properties": {
                "pr_number": {"type": "integer", "description": "PR number"},
                "commit_message": {"type": "string", "description": "Merge commit message"}
            },
            "required": ["pr_number"]
        }
    },
    {
        "name": "create_release",
        "description": "Create a GitHub release with a tag.",
        "input_schema": {
            "type": "object",
            "properties": {
                "tag": {"type": "string", "description": "Tag name, e.g. 'v1.0.0'"},
                "name": {"type": "string", "description": "Release name"},
                "body": {"type": "string", "description": "Release notes in markdown"}
            },
            "required": ["tag", "name", "body"]
        }
    },
    {
        "name": "get_file_content",
        "description": "Read a file from the GitHub repository.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path in repo"},
                "branch": {"type": "string", "description": "Branch name, default 'main'"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "send_telegram",
        "description": "Send a notification message to the user via Telegram.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Message text (HTML formatting supported)"}
            },
            "required": ["text"]
        }
    },
]


# ── Tool Executor ───────────────────────────────────

TOOL_MAP = {
    "get_issues_by_label": get_issues_by_label,
    "create_issue": create_issue,
    "add_comment": add_comment,
    "update_issue_labels": update_issue_labels,
    "close_issue": close_issue,
    "create_branch": create_branch,
    "create_or_update_file": create_or_update_file,
    "create_pull_request": create_pull_request,
    "get_pr_diff": get_pr_diff,
    "merge_pull_request": merge_pull_request,
    "create_release": create_release,
    "get_file_content": get_file_content,
    "send_telegram": lambda text: send_message_sync(text),
}


def execute_tool(name: str, input_data: dict) -> str:
    """Execute a tool and return the result as a string."""
    log.info(f"  🔧 Tool call: {name}({json.dumps(input_data, ensure_ascii=False)[:200]})")
    
    try:
        func = TOOL_MAP.get(name)
        if not func:
            return json.dumps({"error": f"Unknown tool: {name}"})
        
        result = func(**input_data)
        result_str = json.dumps(result, ensure_ascii=False, default=str)
        log.info(f"  ✅ Tool result: {result_str[:200]}")
        return result_str
    except Exception as e:
        error_msg = f"Tool error ({name}): {str(e)}"
        log.error(f"  ❌ {error_msg}")
        return json.dumps({"error": error_msg})


# ── Agent Runner ────────────────────────────────────

def run_agent(role: str, system_prompt: str, user_message: str, max_turns: int = 15) -> str:
    """
    Run an agent with Claude API in an agentic loop.
    
    The agent can call tools, receive results, and continue
    until it produces a final text response or hits max_turns.
    
    Args:
        role: Agent role name (for logging)
        system_prompt: System prompt for the agent
        user_message: Initial user message
        max_turns: Maximum number of tool-use turns
    
    Returns:
        Final text response from the agent
    """
    messages = [{"role": "user", "content": user_message}]
    
    for turn in range(max_turns):
        log.info(f"  [{role.upper()}] Turn {turn + 1}/{max_turns}")
        
        try:
            response = client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=8000,
                system=system_prompt,
                tools=TOOL_DEFINITIONS,
                messages=messages,
            )
        except Exception as e:
            log.error(f"  Claude API error: {e}")
            notify_error(role, str(e))
            return f"Error: {e}"
        
        # Process response blocks
        assistant_content = response.content
        messages.append({"role": "assistant", "content": assistant_content})
        
        # Check if agent wants to use tools
        tool_use_blocks = [b for b in assistant_content if b.type == "tool_use"]
        
        if not tool_use_blocks:
            # No tool calls — agent is done
            text_blocks = [b.text for b in assistant_content if b.type == "text"]
            final_text = "\n".join(text_blocks)
            log.info(f"  [{role.upper()}] Done: {final_text[:200]}")
            return final_text
        
        # Execute each tool call and collect results
        tool_results = []
        for tool_block in tool_use_blocks:
            result = execute_tool(tool_block.name, tool_block.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_block.id,
                "content": result,
            })
        
        messages.append({"role": "user", "content": tool_results})
    
    log.warning(f"  [{role.upper()}] Reached max turns ({max_turns})")
    return "Agent reached maximum number of turns."


# ── Agent Dispatcher ────────────────────────────────

AGENT_CONFIG = {
    "architect": {
        "system_prompt": ARCHITECT_SYSTEM_PROMPT,
        "prompt_template": (
            "New task received. Analyze and create a specification.\n\n"
            "Issue #{number}: {title}\n\n"
            "Description:\n{body}\n\n"
            "Instructions:\n"
            "1. Create a detailed spec file at specs/{slug}.md using create_or_update_file on branch 'main'\n"
            "2. Create subtasks as GitHub issues with appropriate labels (role:developer, role:tester)\n"
            "3. Comment on issue #{number} with a summary\n"
            "4. Send a Telegram notification that the spec is ready\n"
            "5. Update labels: remove role:architect, add role:developer on the parent issue"
        ),
    },
    "developer": {
        "system_prompt": DEVELOPER_SYSTEM_PROMPT,
        "prompt_template": (
            "New development task assigned to you.\n\n"
            "Issue #{number}: {title}\n\n"
            "Description:\n{body}\n\n"
            "Instructions:\n"
            "1. Read the spec file referenced in the issue description\n"
            "2. Create a feature branch: feature/{number}-{slug}\n"
            "3. Write the code and commit files to the branch\n"
            "4. Create a Pull Request\n"
            "5. Comment on issue #{number} that the PR is ready\n"
            "6. Update labels: remove role:developer, add role:tester\n"
            "7. Send a Telegram notification about the PR"
        ),
    },
    "tester": {
        "system_prompt": TESTER_SYSTEM_PROMPT,
        "prompt_template": (
            "New task for testing.\n\n"
            "Issue #{number}: {title}\n\n"
            "Description:\n{body}\n\n"
            "Instructions:\n"
            "1. Read the spec file referenced in the issue\n"
            "2. Review the PR diff using get_pr_diff\n"
            "3. Write tests and push them to the PR branch\n"
            "4. If code matches spec: comment approval, update labels (remove role:tester, add role:architect), send Telegram\n"
            "5. If code has issues: comment with details, update labels (remove role:tester, add role:developer), send Telegram"
        ),
    },
}


def dispatch_to_agent(role: str, issue: dict) -> None:
    """Dispatch an issue to the appropriate agent via Claude API."""
    
    config = AGENT_CONFIG.get(role)
    if not config:
        log.error(f"Unknown role: {role}")
        return
    
    # Build slug from title
    slug = issue["title"].lower()
    for char in "[](){}!@#$%^&*":
        slug = slug.replace(char, "")
    slug = slug.strip().replace(" ", "-")[:40]
    
    # Build prompt
    prompt = config["prompt_template"].format(
        number=issue["number"],
        title=issue["title"],
        body=issue["body"],
        slug=slug,
    )
    
    log.info(f"[{role.upper()}] Processing #{issue['number']}: {issue['title']}")
    send_message_sync(
        f"🤖 <b>{role.upper()}</b> начал работу над #{issue['number']}\n"
        f"<b>{issue['title']}</b>"
    )
    
    # Run the agent
    result = run_agent(role, config["system_prompt"], prompt)
    
    log.info(f"[{role.upper()}] Finished #{issue['number']}")
    
    # Mark as processed
    processed_issues.add(issue["number"])


# ── Polling Loop ────────────────────────────────────

def poll_cycle() -> int:
    """Run one polling cycle: check for tasks for each agent role."""
    dispatched = 0
    
    roles = [
        ("role:architect", "architect"),
        ("role:developer", "developer"),
        ("role:tester", "tester"),
    ]
    
    for label, role in roles:
        try:
            log.info(f"Polling for {label}...")
            issues = get_issues_by_label(label)
            log.info(f"Found {len(issues)} issue(s) for {label}")
            for issue in issues:
                if issue["number"] not in processed_issues:
                    dispatch_to_agent(role, issue)
                    dispatched += 1
        except Exception as e:
            log.error(f"Error polling {label}: {e}", exc_info=True)
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
        send_message_sync("🚀 <b>Orchestrator started (Claude API connected)</b>\nWaiting for tasks...")
    except Exception as e:
        log.warning(f"Could not send Telegram notification: {e}")
    
    # ── Polling loop ──
    try:
        while True:
            dispatched = poll_cycle()
            if dispatched > 0:
                log.info(f"Dispatched {dispatched} task(s)")
            else:
                log.info("No new tasks")
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        console.print("\n[yellow]Shutting down...[/yellow]")
        try:
            send_message_sync("⏹ <b>Orchestrator stopped</b>")
        except Exception:
            pass


if __name__ == "__main__":
    main()
