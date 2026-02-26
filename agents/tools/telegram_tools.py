"""
Telegram Tools — Send notifications to Telegram chat.

Used by agents to notify the user about key events:
- Spec ready
- PR created  
- Test results
- Release published
"""

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


async def send_message(text: str, parse_mode: str = "HTML") -> dict:
    """
    Send a message to the configured Telegram chat.
    
    Args:
        text: Message text (supports HTML formatting)
        parse_mode: 'HTML' or 'Markdown'
    
    Returns:
        Dict with message_id and success status
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/sendMessage",
            json={
                "chat_id": CHAT_ID,
                "text": text,
                "parse_mode": parse_mode,
            },
        )
        data = response.json()
        return {
            "ok": data.get("ok", False),
            "message_id": data.get("result", {}).get("message_id"),
        }


def send_message_sync(text: str, parse_mode: str = "HTML") -> dict:
    """
    Synchronous version of send_message.
    """
    response = httpx.post(
        f"{BASE_URL}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": parse_mode,
        },
    )
    data = response.json()
    return {
        "ok": data.get("ok", False),
        "message_id": data.get("result", {}).get("message_id"),
    }


# ── Pre-formatted notification helpers ──────────────

def notify_spec_ready(issue_number: int, title: str, subtasks: list[int]):
    """Notify that a spec is ready."""
    subtask_list = ", ".join(f"#{n}" for n in subtasks)
    send_message_sync(
        f"📋 <b>Архитектор:</b> ТЗ готово для #{issue_number}\n"
        f"<b>{title}</b>\n"
        f"Подзадачи: {subtask_list}"
    )


def notify_pr_created(issue_number: int, pr_number: int, title: str):
    """Notify that a PR was created."""
    send_message_sync(
        f"🛠 <b>Программист:</b> PR #{pr_number} готов\n"
        f"Для задачи #{issue_number}: <b>{title}</b>"
    )


def notify_test_passed(issue_number: int, title: str):
    """Notify that tests passed."""
    send_message_sync(
        f"✅ <b>Тестировщик:</b> Approved #{issue_number}\n"
        f"<b>{title}</b>"
    )


def notify_test_failed(issue_number: int, title: str, reason: str):
    """Notify that tests failed."""
    send_message_sync(
        f"❌ <b>Тестировщик:</b> Возврат #{issue_number}\n"
        f"<b>{title}</b>\n"
        f"Причина: {reason}"
    )


def notify_release(tag: str, name: str, url: str):
    """Notify about a new release."""
    send_message_sync(
        f"🚀 <b>Архитектор:</b> Релиз {tag}\n"
        f"<b>{name}</b>\n"
        f"{url}"
    )


def notify_release_verified(tag: str):
    """Notify that release was verified."""
    send_message_sync(
        f"✅ <b>Тестировщик:</b> Релиз {tag} верифицирован ✔"
    )


def notify_error(agent: str, error: str):
    """Notify about an error."""
    send_message_sync(
        f"⚠️ <b>Ошибка ({agent}):</b>\n{error}"
    )
