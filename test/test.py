from seleniumbase import SB
from Accounts import getEmailPair, getLength
from pathlib import Path
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from db import DateDataBase

# ── Constants ────────────────────────────────────────────────────────────────
img_dir = Path("logs/images")
img_dir.mkdir(parents=True, exist_ok=True)

CLOSE_BTN       = "span:contains('Close')"
TOAST_CLOSE_BTN = "button[aria-label='close']"
REWARD_SEL      = "span:contains('Claim 10,000 daily credits')"
LOGIN_SPAN      = "span:contains('Login')"
EMAIL_INPUT     = "#email-input"
PASSWORD_INPUT  = "#password-input"
LOGOUT_BTN      = "header button[aria-haspopup='true']"
LOGOUT_SEL      = "div:contains('Log out')"
TURNSTILE_INPUT = 'input[name="cf-turnstile-response"]'
LOGIN_URL       = "https://pixai.art/en/login"

MAX_WORKERS     = 3   # Tune based on your machine / site limits
HEADLESS        = False

# ── Core Actions ─────────────────────────────────────────────────────────────
def click_rewards(sb: SB):
    sb.click(REWARD_SEL)

def close_rewards(sb: SB):
    sb.click(CLOSE_BTN)
    sb.wait_for_element_visible(TOAST_CLOSE_BTN, timeout=15)
    sb.click(TOAST_CLOSE_BTN)

def logout(sb: SB, depth: int = 0):
    if depth > 2:
        print("⚠️  Logout recursion limit hit — skipping.")
        return
    try:
        sb.click(LOGOUT_BTN)
        sb.click(LOGOUT_SEL)
        print("🔓 Logged out.")
    except Exception:
        if sb.is_element_visible(LOGOUT_BTN):
            logout(sb, depth + 1)

# ── Login & Claim ─────────────────────────────────────────────────────────────
def login(email: str, password: str, index: int):
    with SB(
        uc=True,
        headless=HEADLESS,
        incognito=False,
        locale="en-US",
    ) as sb:
        try:
            sb.open(LOGIN_URL)
            sb.wait_for_text("Continue with Email", timeout=20)
            sb.click("span:contains('Continue with Email')")

            sb.type(EMAIL_INPUT, email)
            sb.type(PASSWORD_INPUT, password)
            sb.wait_for_element_clickable(LOGIN_SPAN, timeout=20)
            sb.click(LOGIN_SPAN)

            # Wait for page reaction instead of a fixed sleep
            sb.sleep(2)

            # Retry login click once if still on login page
            if sb.is_element_visible(LOGIN_SPAN):
                try:
                    sb.click(LOGIN_SPAN)
                    sb.sleep(2)
                except Exception:
                    print(f"⚠️  Re-click login failed for {email}")

            # Turnstile check
            if sb.is_element_present(TURNSTILE_INPUT):
                print(f"🔒 Turnstile detected for {email} — waiting for resolve…")
                sb.sleep(3)

            # Claim reward if available
            if sb.is_element_visible(REWARD_SEL):
                sb.sleep(0.5)
                click_rewards(sb)
                sb.sleep(1.5)
                close_rewards(sb)
                DateDataBase().AddValue(email)
                print(f"✅ Reward claimed — {email}")
            else:
                print(f"❌ Already claimed today — {email}")

        except Exception as e:
            print(f"💥 Error on {email}: {e}")
            sb.save_screenshot(str(img_dir / f"Error_{index}.png"))

        finally:
            logout(sb)

# ── Worker (for thread pool) ──────────────────────────────────────────────────
def process_account(args):
    index, email, password = args
    login(email, password, index)

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    start    = time.time()
    db       = DateDataBase()
    visited  = set(db.getclaimed())
    print(f"📋 Already claimed today: {len(visited)} account(s)")

    # Build work list — skip already-claimed accounts up front
    tasks = []
    for i in range(getLength()):
        data = getEmailPair(i)
        tasks.append((i, data["email"], data["password"]))

    print(f"🚀 Processing {len(tasks)} account(s) with {MAX_WORKERS} parallel workers…")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(process_account, t): t for t in tasks}
        for future in as_completed(futures):
            exc = future.exception()
            if exc:
                idx, email, _ = futures[future]
                print(f"💥 Thread error for {email} (index {idx}): {exc}")

    elapsed = time.time() - start
    print(f"\n✅ All done in {elapsed:.2f}s")

if __name__ == "__main__":
    main()