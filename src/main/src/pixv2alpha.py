from seleniumbase import SB
import time
from Accounts import getEmailPair,getLength
from db import DateDataBase


class Pix:
    def __init__(self,sb:SB):
        self.sb = sb
        # login url
        self.loginUrl = "https://pixai.art/en/login"
        self.start = time.time()
        self.conti_email_ele = "span:contains('Continue with Email')"
        self.login_ele = "span:contains('Login')"
        self.reward_selector_ele = "span:contains('Claim 10,000 daily credits')"
        self.close_button = "span:contains('Close')"
        self.toast_close_btn = "button[aria-label='close']"
        self.date = DateDataBase()
    
    def visitWebpage(self):
        try:
            print("Entering the Webpage")
            self.sb.open(self.loginUrl)
            self.sb.solve_captcha()
            self.sb.wait_for_ready_state_complete()
            self.sb.wait_for_text_visible("Sign in",timeout=10)
            print("Passed Ready state")
            if(self.sb.is_text_visible("Sign in")):
                print("sucesfully signin Spotted")
                print(f"Time taken to Enter Webpage: {time.time() - self.start:.4f} seconds")
                return True
        except Exception as e:
            print("Error Occuried! While Entering the Login Page falied")
            print(e)
            return False
    
    def login(self,email,passwrd):
        try:
            self.email = email
            self.sb.wait_for_text_visible("Sign in",timeout=10)
            self.sb.wait_for_text("Continue with Email", timeout=20)
            self.sb.click(self.conti_email_ele)
            self.sb.wait_for_ready_state_complete()
            self.sb.type("#email-input",email)
            print("Email Sucessfully Entered")
            self.sb.type("#password-input",passwrd)
            print("Password Sucessfully Entered")
            self.sb.click(self.login_ele)
            print("login Button Clicked ")
            self.sb.wait_for_element_not_present("button[disabled]", timeout=30)
            print("Button is now enabled!")
            print(f"Time taken to Enter Webpage: {time.time() - self.start:.4f} seconds")
            self.sb.wait_for_text_not_visible("Sign in")
            return True
        except Exception as e :
            print("Error while loggin in")
            print(e)
            return False
    
    def collect_reward(self):
        try:
            self.sb.wait_for_ready_state_complete()
            try:
                self.sb.wait_for_text_visible("Daily Claim",timeout=5)
                print('Daily Login Visible')
            except Exception as e:
                pass 

            if not self.sb.is_element_visible(self.reward_selector_ele):
                print("Reward Not Found")
                print(f"Time taken to Reward Not Found: {time.time() - self.start:.4f} seconds")
                print("++++Program exited++++ ")
                return False# reward not found
            
            if self.sb.is_element_visible("#cf-turnstile"):
                self.sb.solve_captcha()
                print("Cloudflare widget found!")

            self.sb.click(self.reward_selector_ele)
            print("Reward Sucessfuly Claimed ✅")
            print(f"Time taken to Claim reward: {time.time() - self.start:.4f} seconds")
            self.date.AddValue(EMAIL=self.email)
            self.closeRewards()
            return True
        except Exception as e:
            print(e)
            print("Exited")
            return False
        
    def closeRewards(self):
            print("Closing the Reward Page")
            self.sb.wait_for_element("//*[normalize-space()='Close']", by="xpath", timeout=15)
            self.sb.click("//*[normalize-space()='Close']", by="xpath")
            self.sb.wait_for_element_visible(self.toast_close_btn, timeout=15)
            self.sb.click(self.toast_close_btn)
            print("Closed reward ")
            print(f"Time taken to close Reward: {time.time() - self.start:.4f} seconds")

    def logout(self):
        try:
            print("Entered for logout")
            self.sb.wait_for_element_present("header button[aria-haspopup='true']")
            self.sb.click("header button[aria-haspopup='true']")
            self.sb.click("//div[@role='menuitem']//div[text()='Log out']", by="xpath")
            self.sb.wait_for_text_visible("Sign in",timeout=10)
            print("signupspotted")
            print("Sucessfully logged out")
            print(f"Time taken to Logout: {time.time() - self.start:.4f} seconds")
            return True

        except Exception as e:
            print(e)
            print("logout failed")
            return False




def main(headles=True):
    start = time.time()
    with SB(uc=True,headless=headles,incognito=False) as sb:
        pix = Pix(sb=sb)
        date = DateDataBase()
        visted = date.getclaimedToday()

        testmode = True
        testmail = [
            {
                "email":"tempsoul@duck.com",
                "password":"opklnmuihjvb"
            }
        ]


        for i in range(0,getLength()):
            data = getEmailPair(i)
            if (data["email"] in visted and not testmode):
                continue
            if (not pix.visitWebpage()): 
                print("failed on visiting")
            if( not pix.login(data["email"],data["password"])):
                print("failed on logging in")
            log = pix.collect_reward()
            if(log == False):
                print("m failed on logged out")
            pix.logout()
    end = time.time()
    print(f"Total Time :: {end-start:.2f} seconds")

def test(headles=False):
    start = time.time()
    with SB(uc=True,headless=headles,incognito=False) as sb:
        pix = Pix(sb=sb)
        testmail = [
            {
                "email":"bhuvaneshgg01@gmail.com",
                "password":"opklnmuihjvb"
            }
        ]
        for data in testmail:
            if (not pix.visitWebpage()): 
                print("failed on visiting")
            if( not pix.login(data["email"],data["password"])):
                print("failed on logging in")
            log = pix.collect_reward()
            if(log == False):
                print("m failed on logged out")
            pix.logout()
    end = time.time()
    print(f"Total Time :: {end-start:.2f} seconds")
        
        

#test(headles=False)
main(headles=False)