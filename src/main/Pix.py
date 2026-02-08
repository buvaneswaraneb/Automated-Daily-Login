from seleniumbase import SB
from Accounts import getEmailPair,getLength
from pathlib import Path
import time

img_dir = Path("logs/images")
img_dir.mkdir(parents=True, exist_ok=True)
close_button = "span:contains('Close')"
toast_close_btn = "button[aria-label='close']"
reward_selector = "span:contains('Claim 10,000 daily credits')"


def login(email:str , password:str , i):
    with SB(
    uc=True,        
    headless=False,
    incognito=False,
    locale="en-US"
    ) as sb:
        try: 
            sb.open("https://pixai.art/en/login")
            sb.wait_for_text("Continue with Email", timeout=20)
            sb.click("span:contains('Continue with Email')")
            sb.type("#email-input",email)
            sb.type("#password-input",password)
            sb.wait_for_element_clickable(
                "span:contains('Login')",
                timeout=20
            )
            sb.sleep(0.5)
            sb.click("span:contains('Login')")
            sb.sleep(1)
            if (sb.is_element_visible("span:contains('Login')")):
                sb.click("span:contains('Login')")
                sb.sleep(1.5)
                if (sb.is_element_visible("span:contains('Login')")):
                    try : 
                         sb.click("span:contains('Login')")
                         sb.sleep(2)
                    except:
                         pass
            
                sb.sleep(2.3)   
            if sb.is_element_visible(reward_selector):
                clickRewards(sb) 
                print(f"✅ Reward available on Email: {email}")
                if sb.is_element_visible(reward_selector):
                    try:
                        sb.sleep(4)
                        clickRewards()
                        if sb.is_element_visible(reward_selector):
                            sb.sleep(2)
                            clickRewards()
                            sb.sleep(2)
                    except:
                        pass

                # Collects the Reward
                closeRewards(sb)
                logout(sb)
            else:
                print(f"❌ Reward already claimed today on Email: {email}")
                logout(sb) #logs out
            
        except:
            print(f"Error Founded on Email: {email}")
            sb.save_screenshot(str(img_dir / f"Error{i}.png"))


def clickRewards(sb:SB):
        sb.sleep(1)
        sb.wait_for_element_clickable(reward_selector, timeout=30)
        sb.click(reward_selector)

def closeRewards(sb:SB):
        sb.click(close_button)
        sb.wait_for_element_visible(toast_close_btn, timeout=15)
        sb.click(toast_close_btn)
     
def logout(sb:SB):
            try: 
                sb.click("header button[aria-haspopup='true']")
                print("Logged Out")
                sb.click("div:contains('Log out')")
            except:
                if sb.is_element_visible("header button[aria-haspopup='true']"):
                    logout(sb)

def reAttemptReward(sb:SB):
    sb.sleep(2)
    clickRewards(sb)
    if (sb.is_element_visible(reward_selector)):
        sb.sleep(4)
        clickRewards(sb) #clicks the Rewards


def main():
    start = time.time()
    for i in range(0,getLength()):
        data = getEmailPair(i)
        login(data["email"],data["password"],i)
    end = time.time()
    print(f"Time taken: {end - start:.4f} seconds")
    print("sucessfully Completed")



if __name__ == "__main__":
    main() 
