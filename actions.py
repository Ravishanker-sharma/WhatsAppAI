from playwright.async_api import Page, Error


async def click_chat_by_name(page: Page, name: str):
    """
    Finds a chat by its name in the chat list and clicks on it.
    """
    print(f"\n[ACTION] Trying to find and click chat: '{name}'")
    try:
        chat_selector = f'div[role="row"]:has(span[title="{name}"])'
        chat_element = page.locator(chat_selector)
        count = await chat_element.count()

        if count == 0:
            print(f"[ERROR] Chat '{name}' not found in the visible list.")
            return False

        await chat_element.first.click()
        print(f"[SUCCESS] Clicked on chat: '{name}'")
        return True
    except Error as e:
        print(f"[ERROR] Could not click on chat '{name}'. Reason: {e}")
        return False


async def send_message(page: Page, message: str):
    """
    Finds the active chat's message input box, types a message, and presses Enter.
    
    Args:
        page: The Playwright page object.
        message (str): The text message you want to send.
    """
    print(f"\n[ACTION] Attempting to send message: '{message}'")
    try:
        # This selector targets the content-editable div that serves as the message box.
        # It's highly reliable as it uses the role and placeholder text.
        textbox_selector = 'div[role="textbox"][aria-placeholder="Type a message"]'

        # Using .locator() is the modern Playwright approach
        textbox = page.locator(textbox_selector)

        # Check if the textbox is visible before interacting with it
        await textbox.wait_for(state="visible", timeout=5000)

        # Fill the message into the textbox
        await textbox.fill(message)

        # Press Enter to send the message
        await textbox.press("Enter")

        print(f"[SUCCESS] Message sent: '{message}'")

    except Error as e:
        print(
            f"[ERROR] Could not send the message. The message box might not be visible.")
        print(f"        Details: {e}")
