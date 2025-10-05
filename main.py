# main_async.py
import asyncio
import time
from login_whatshapp import get_logged_in_page
from whatshapp_monitor import detect_new_messages
from actions import click_chat_by_name , send_message
from chat_reply_ai import bot, build_app

async def handle_new_message(page,chat_name, message, unread_count,app):
    """Callback for new messages — here you can reply, log, or trigger AI."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print("\n" + "="*40)
    print(f"🚨 NEW MESSAGE DETECTED ({timestamp}) 🚨")
    print(f"Chat: {chat_name}")
    print(f"Unread: {unread_count}")
    print(f"Message: {message}")
    print("="*40 + "\n")

    response = await bot(app, message, thread_id=chat_name)
    if response:
        response = f"[Automated Reply] : {response}"
        print(f"[AI REPLY] : {response}")
        # Click the chat to ensure it's active
        clicked = await click_chat_by_name(page, chat_name)
        if clicked:
            await asyncio.sleep(1)  # Wait a moment for the chat to load
            await send_message(page, response)
        else:
            print(f"[ERROR] Could not find chat '{chat_name}' to send reply.")
    else:
        print("[AI REPLY] No response generated.")
    
    try:
        await page.keyboard.press("Escape")
        print("[INFO] Returned to chat list to allow unread detection.")
    except Exception:
        print("[WARN] Could not return to chat list — may affect future detections.")



async def main():
    app = await build_app()  # Ensure the app is built before use
    playwright, browser, page = await get_logged_in_page()
    if not page:
        print("❌ Login failed.")
        return

    await detect_new_messages(page, handle_new_message ,app)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[EXIT] Stopped by user.")
