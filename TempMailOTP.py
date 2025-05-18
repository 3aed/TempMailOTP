from playwright.sync_api import sync_playwright
import re
import time
# 3aed Hany FarajAllah


headless_input = input("Do you want to run the browser in headless mode? (yes/no): ").strip().lower()

headless = True if headless_input in ["yes", "y", "true"] else False

def get_microsoft_otp():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        
        # go to emailnator
        page.goto("https://www.emailnator.com/")
        
        try:
            page.locator("button.fc-cta-consent").click(timeout=3000)
        except:
            pass
        
        # 2. create a temporary email
        page.get_by_role("button", name="Go !").click()
        time.sleep(3)
        
        # 4. wait for the new message
        page.get_by_role("button", name="Reload").click()
        
        page.wait_for_selector('a.text-decoration-none >> nth=1', timeout=10000)
        page.get_by_role("button", name="Reload").click()
        time.sleep(3)

        # the massege u want to click on it
        # replace it ( with what u need )
        page.get_by_role("link", name="Microsoft on behalf of MSC").click()

        # To remove ads
        page.evaluate("""
        () => {
            document.querySelectorAll('.ad, .popup, .overlay, .fc-dialog, .fc-banner').forEach(el => el.remove());
        }
        """)
        
        time.sleep(2)
        try:
            
            code_text = page.get_by_text("Your code is:").inner_text()
            otp = re.search(r'\d{4,8}', code_text).group()
        except:
            # the second way to get the code
            otp_element = page.locator("text=Your code is: >> xpath=following-sibling::*[1]")
            otp = otp_element.inner_text()
        
        # save the screenshot and the content of the page
        page.screenshot(path='email_debug.png', full_page=True)
        with open('email_content.html', 'w', encoding='utf-8') as f:
            f.write(page.content())
        
        browser.close()
        return otp

# the run
otp = get_microsoft_otp()
print(f"the code is: {otp}")