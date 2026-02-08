from seleniumbase import SB


def login():
    with SB(
    uc=True,        
    headless=False,
    incognito=False,
    locale="en-US"
    ) as sb:
         sb.open("http://127.0.0.1:5500/test/index.html")
         closeRewards(sb)



def closeRewards(sb:SB):
    close_button = "span:contains('Close')"
    sb.click(close_button)
    sb.save_screenshot("clicked.png")

login()
