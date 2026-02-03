from seleniumbase import SB
from Accounts import getEmailPair,getLength
from pathlib import Path

img_dir = Path("logs/images")
img_dir.mkdir(parents=True, exist_ok=True)


def login(email:str , password:str , i):
    with SB(
    uc=True,        
    headless=False,
    incognito=False,
    locale="en-US"
    ) as sb:
        try: 
            sb.open("https://pixai.art/en/login")
            sb.wait_for_text("Continue with Email", timeout=15)
            sb.click("span:contains('Continue with Email')")
            sb.type("#email-input",email)
            sb.type("#password-input",password)
            sb.wait_for_element_clickable(
                "span:contains('Login')",
                timeout=20
            )
            sb.sleep(0.5)
            sb.click("span:contains('Login')")
            reward_selector = "span:contains('Claim 10,000 daily credits')"
            close_button = "span:contains('Close')"
            toast_close_btn = "button[aria-label='close']"
            sb.sleep(2)

            if sb.is_element_visible(reward_selector):
                sb.sleep(2)
                print(f"✅ Reward available on Email: {email}")
                #sb.save_screenshot(f"reward{i}.png")
                sb.wait_for_element_clickable(reward_selector, timeout=30)
                sb.click(reward_selector)
                if (sb.is_element_visible(reward_selector)):
                    sb.sleep(1)
                    if (sb.is_element_visible(reward_selector)):
                        sb.sleep(4)
                        sb.click(reward_selector)

                sb.click(close_button)
                sb.wait_for_element_visible(toast_close_btn, timeout=15)
                sb.click(toast_close_btn)
            else:
                print(f"❌ Reward already claimed today on Email: {email}")
            sb.click("header button[aria-haspopup='true']")
            print("clicked tthe icon")
            sb.click("div:contains('Log out')")
            
        except:
            print(f"Error Founded on Email: {email}")
            sb.save_screenshot(str(img_dir / f"Error{i}.png"))

def main():
    for i in range(0,getLength()):
        data = getEmailPair(i)
        login(data["email"],data["password"],i)
    print("sucessfully Completed")



main()
