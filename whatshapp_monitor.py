# whatsapp_message_monitor.py
import asyncio
import time


async def get_current_chat_state(page):
    """Scrape visible chat names, last message, and unread counts."""
    chat_state = {}
    chat_rows = await page.query_selector_all('div[role="row"]')

    for row in chat_rows:
        try:
            name_el = await row.query_selector('div[role="gridcell"][aria-colindex="2"] span[title]')
            chat_name = await name_el.get_attribute('title') if name_el else None
            if not chat_name:
                continue

            msg_el = await row.query_selector('span.x78zum5.x1cy8zhl[title]')
            last_message = await msg_el.get_attribute('title') if msg_el else ""
            last_message = last_message.strip()

            unread_el = await row.query_selector('span[aria-label*="unread message"]')
            unread_text = await unread_el.inner_text() if unread_el else "0"
            unread_count = int(''.join(filter(str.isdigit, unread_text)))

            chat_state[chat_name] = {
                "last_message": last_message,
                "unread_count": unread_count,
            }
        except Exception:
            pass

    return chat_state


async def detect_new_messages(page, on_new_message,app):
    """
    Watches for new messages forever.
    Calls `on_new_message(chat_name, last_message, unread_count)` when detected.
    """
    print("\n[INFO] Starting WhatsApp message watcher...")
    previous_state = await get_current_chat_state(page)
    print(f"[INIT] Captured {len(previous_state)} chats.")

    while True:
        await asyncio.sleep(5)
        current_state = await get_current_chat_state(page)

        for chat_name, current in current_state.items():
            prev = previous_state.get(chat_name)

            # New chat entirely
            if chat_name not in previous_state and current["unread_count"] > 0:
                await on_new_message(page,chat_name, current["last_message"], current["unread_count"],app)
                continue

            # Existing chat: check if unread count or message changed
            if prev:
                is_new = (
                    current["unread_count"] > prev["unread_count"] or
                    (current["unread_count"] >
                     0 and current["last_message"] != prev["last_message"])
                )
                if is_new:
                    await on_new_message(page,chat_name, current["last_message"], current["unread_count"],app)

        previous_state = current_state
