from seleniumbase import SB

def login(email:str , password:str , i):
    with SB(
    uc=True,        
    headless=False,
    incognito=False,
    locale="en-US"
    ) as sb:
        sb.open("https://pixai.art/en/login")
        sb.wait_for_text("Continue with Email", timeout=15)
        sb.click("span:contains('Continue with Email')")
        sb.type("#email-input",email)
        sb.type("#password-input",password)
        sb.sleep(4)
        sb.wait_for_element_clickable(
            "span:contains('Login')",
            timeout=20
        )
        sb.click("span:contains('Login')")
        sb.sleep(2)
        reward_selector = "span:contains('Claim 10,000 daily credits')"
        if sb.is_element_visible(reward_selector):
            sb.sleep(3)
            print("✅ Reward available")
            sb.save_screenshot(f"reward{i}.png")
            sb.wait_for_element_clickable(reward_selector, timeout=30)
            sb.click(reward_selector)
        else:
            print("❌ Reward already claimed today")
        
        sb.click("header button[aria-haspopup='true']")
        sb.click("div:contains('Log out')")
        sb.save_screenshot(f"log{i}.png")



for i in range(len(data)):
    login(data[i]["email"],data[i]["password"],i)
print("sucessfull pergant")
