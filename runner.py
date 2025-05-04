from playwright.sync_api import Playwright
from utils import parse_to_playwright_cookies

def run(playwright: Playwright, config) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    context.add_cookies(parse_to_playwright_cookies(config['cookies']))

    page = context.new_page()

    page.goto("https://www.douyin.com/?recommend=1")

    print('等待弹窗1')
    # 询问是否保存登陆信息 关闭
    page.get_by_text("取消").click(timeout=100000)

    print('点击私信按钮')
    page.get_by_role("paragraph").filter(has_text="私信").click(timeout=100000)
    print('点击续火花用户')
    page.get_by_text(f"{config['nickname']}").click(timeout=100000)
    print('输入文本并回车')
    page.locator("#douyin-header-menuCt").get_by_role("textbox").locator("div").nth(2).click(timeout=100000)
    page.locator("#douyin-header-menuCt").get_by_role("textbox").fill(f"{config['msg']}")
    page.locator("#douyin-header-menuCt").get_by_role("textbox").press("Enter")

    page.wait_for_timeout(30000)

    print('关闭浏览器')
    context.close()
    browser.close()
