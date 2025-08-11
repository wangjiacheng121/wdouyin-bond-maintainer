import sys
from time import  time
import traceback
from playwright.sync_api import sync_playwright , TimeoutError
from config import get_config
from utils import parse_to_playwright_cookies

print('开始执行...')
start_time = time()
with sync_playwright() as playwright:
    try:
        config = get_config()
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        context.add_cookies(parse_to_playwright_cookies(config['cookies']))

        page = context.new_page()

        page.goto("https://www.douyin.com/?recommend=1")

        print('等待弹窗1')
        # 询问是否保存登陆信息 关闭
    try:
        # 创建定位器：匹配class和文本内容（处理可能的空格）
        login_button = page.locator("div.ZkNVpl8h", has_text="登录")
        
        # 方法1：快速检查元素是否存在（不等待）
        if login_button.count() > 0:
            print("⚠️ 未登录状态：检测到登录按钮")
            return False
        
        # 方法2：严格检查元素可见性（等待1000ms）
        if login_button.is_visible(timeout=1000):
            print("⚠️ 未登录状态：登录按钮可见")
            return False
        
        print("✅ 已登录状态")
        return True
        
    except Exception as e:
        # 当元素不存在时会抛出错误
        print(f"✅ 已登录状态（未找到登录按钮）")
        return True
    try:
            page.get_by_text("取消").click(timeout=600000)
            print('点击私信按钮')
            page.get_by_role("paragraph").filter(has_text="私信").click()
        except TimeoutError:
            print('点击私信按钮')
            page.get_by_role("paragraph").filter(has_text="私信").click()

        print('点击续火花用户')
        page.get_by_text(f"{config['nickname']}",exact=True).first.click()
        print('输入文本并回车')
        page.locator("#douyin-header-menuCt").get_by_role("textbox").locator("div").nth(2).click()
        page.locator("#douyin-header-menuCt").get_by_role("textbox").fill(f"{config['msg']}")
        page.locator("#douyin-header-menuCt").get_by_role("textbox").press("Enter")

        try:
            page.locator("text=发送失败").wait_for(timeout=10000)
            print('发送失败！')
            raise RuntimeError('发送失败!')
        except TimeoutError as e:
            print('发送成功！')

        print("耗时："+str(int(time() - start_time)))
        # sleep(10)

        print('关闭浏览器')

        context.close()
        browser.close()
    except Exception as e:
    # error_msg = str(e)
        error_details = traceback.format_exc()
        print(error_details)

        try :
            screenshot = page.screenshot(path='error.png',full_page=True)
        except Exception as e:
            print(e)

        sys.exit(1)
