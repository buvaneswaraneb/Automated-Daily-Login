from seleniumbase import SB
import time
from Accounts import getEmailPair,getLength
from db import DateDataBase


class Pix:
    def __init__(self,sb:SB ,testmode=False):
        self.sb = sb
        # login url
        self.loginUrl = "https://www.typing.com/" if testmode else "https://pixai.art/en/login"
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
            self.sb.type("#password-input",passwrd)
            self.sb.click(self.login_ele)
            self.sb.wait_for_element_not_present("button[disabled]", timeout=30)
            self.sb.wait_for_element_not_present
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
                self.date.AddValue(self.email)
                print("++++Program exited++++ ")
                return False# reward not found
            
            if self.sb.is_element_present('input[name="cf-turnstile-response"]'):
                self.sb.solve_captcha()
            self.sb.click(self.reward_selector_ele)
            print("Reward Sucessfuly Claimed ✅")
            self.date.AddValue(EMAIL=self.email)
            self.closeRewards()
            return True
        except Exception as e:
            print(e)
            print("Exited")
            return False
        
    def closeRewards(self):
            self.sb.wait_for_element("//*[normalize-space()='Close']", by="xpath", timeout=15)
            self.sb.click("//*[normalize-space()='Close']", by="xpath")
            self.sb.wait_for_element_visible(self.toast_close_btn, timeout=15)
            self.sb.click(self.toast_close_btn)

    def logout(self):
        try:
            self.sb.wait_for_element_present("header button[aria-haspopup='true']")
            self.sb.click("header button[aria-haspopup='true']")
            self.sb.click("//div[@role='menuitem']//div[text()='Log out']", by="xpath")
            self.sb.wait_for_text_visible("Sign in",timeout=10)
            print("Sucessfully logged out")
            return True

        except Exception as e:
            print(e)
            print("logout failed")
            return False




def main(headles=True):
    start = time.time()
    with SB(uc=True,headless=headles,incognito=False) as sb:
        pix = Pix(sb=sb,testmode=False)
        date = DateDataBase()
        visted = date.getclaimedToday()
        for i in range(0,getLength()):
            data = getEmailPair(i)
            if (data["email"] in visted):
                continue
            if (not pix.visitWebpage()):
                print("failed on visiting")
            if( not pix.login(data["email"],data["password"])):
                print("failed on logging in")
                continue
            log = pix.collect_reward()
            if(log == False):
                print("failed on logged out")
                continue
            pix.logout()
    end = time.time()
    print(f"Total Time :: {end-start:.2f} seconds")
        
        


main(headles=True)