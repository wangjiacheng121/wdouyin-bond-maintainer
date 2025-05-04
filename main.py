import traceback
from playwright.sync_api import sync_playwright
from config import get_config
from runner import run

try:
    with sync_playwright() as playwright:
        run(playwright,get_config())
except Exception as e:
    # error_msg = str(e)
    error_details = traceback.format_exc()
    print(error_details)
