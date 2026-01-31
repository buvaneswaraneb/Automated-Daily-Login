from seleniumbase import SB

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
            sb.sleep(4)
            sb.wait_for_element_clickable(
                "span:contains('Login')",
                timeout=20
            )
            sb.click("span:contains('Login')")
            sb.sleep(2)
            reward_selector = "span:contains('Claim 10,000 daily credits')"
            close_button = "span:contains('Close')"
            if sb.is_element_visible(reward_selector):
                sb.sleep(3)
                print("✅ Reward available")
                sb.save_screenshot(f"reward{i}.png")
                sb.wait_for_element_clickable(reward_selector, timeout=30)
                sb.click(reward_selector)
                sb.click(close_button)
                sb.sleep(3)
            else:
                print("❌ Reward already claimed today")
            sb.wait(3)
            sb.click("header button[aria-haspopup='true']")
            print("clicked tthe icon")
            sb.click("div:contains('Log out')")
            sb.save_screenshot(f"log{i}.png")
        except :
            print("Error Founded")





data = [ #add a dictonary of Email and Password
]
for i in range(len(data)):
    login(data[i]["email"],data[i]["password"],i)
print("sucessfully Completed")
