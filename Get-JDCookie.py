#!/usr/bin/env python3

# -*- coding:utf-8 -*-
import asyncio
import pyperclip
from playwright.async_api import async_playwright


def find_cookie(cookies) -> str:
    """提取pt_key和pt_pin"""
    pt_pin = None
    pt_key = None
    for key, value in cookies.items():
        if key == "pt_pin":
            pt_pin = value
        elif key == "pt_key":
            pt_key = value
    if not pt_pin or not pt_key:
        print("cookies:", cookies)
        print("提取失败，请手动提取pt_key和pt_pin")
        return None
    jd_cookie = f"pt_pin={pt_pin};pt_key={pt_key};"
    pyperclip.copy(jd_cookie)  # 拷贝JDcookie到剪切板
    print("Cookie:", jd_cookie)
    print("已拷贝Cookie到剪切板、直接黏贴即可。")
    return jd_cookie


async def main():
    """使用pyppeteer库来登录京东、并获取cookie"""
    print("请在弹出的网页中登录账号、推荐使用账户短信验证码的形式登录。")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--no-sandbox", "--window-size=1000,800", "--disable-infobars"],
        )  # 进入有头模式
        context = await browser.new_context()  # 隐身模式
        page = await context.new_page()  # 打开新的标签页
        await page.set_viewport_size({"width": 1000, "height": 800})  # 页面大小一致
        await page.goto(
            "https://home.m.jd.com", timeout=1000 * 60
        )  # 访问主页、增加超时解决Navigation Timeout Exceeded: 30000 ms exceeded报错

        while True:
            cookie = await context.cookies()
            # print(cookie)
            # 格式化cookie
            cookies = {}
            for i in cookie:
                cookies[i["name"]] = i["value"]
            if find_cookie(cookies):
                break
            else:
                print("未提取到cookie，重试中...")
                await page.wait_for_timeout(1000)
        await context.close()
        await browser.close()
        # print("cookies:{}".format(await page.cookies()))


if __name__ == "__main__":
    asyncio.run(main())  # 调用
