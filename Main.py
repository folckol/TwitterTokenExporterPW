import time
import traceback

import ua_generator
from playwright.sync_api import sync_playwright


class twitter_unlock_v2:
    def __init__(self, proxies):

        # print(1)

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=False,
            proxy={
               "server": f"{proxies.split(':')[0]}:{proxies.split(':')[1]}",
               "username": f"{proxies.split(':')[2]}",
               "password": f"{proxies.split(':')[3]}",
            }, devtools=True
        )
        self.context = self.browser.new_context(user_agent=ua_generator.generate().text)

        self.page = self.context.new_page()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.page.close()
        self.context.close()
        self.browser.close()
        self.playwright.stop()


    def script(self, username, password, email, phone):

        self.page.goto("https://twitter.com/i/flow/login")

        try:
            self.page.wait_for_selector('input[autocomplete="username"]', timeout=15000).fill(username if username != "None" else email if email else phone )
        except:
            try:
                self.page.reload()
                self.page.wait_for_selector('input[autocomplete="username"]', timeout=15000).fill(username if username != "None" else email if email else phone )
            except:
                self.page.reload()
                self.page.wait_for_selector('input[autocomplete="username"]', timeout=15000).fill(
                    username if username != "None" else email if email else phone)


        self.page.wait_for_selector('input[autocomplete="username"]').click()
        self.page.wait_for_timeout(timeout=2000)
        self.page.keyboard.press("Tab")
        self.page.keyboard.press("Space")

        try:
            self.page.wait_for_selector('input[autocomplete="current-password"]').fill(password, timeout=10000)
        except:
            try:
                self.page.wait_for_selector('input[autocomplete="username"]', timeout=5000).fill(email if email else phone)

                self.page.wait_for_selector('input[autocomplete="username"]').click()
                self.page.wait_for_timeout(timeout=2000)
                self.page.keyboard.press("Tab")
                self.page.keyboard.press("Space")

                try:
                    self.page.wait_for_selector('input[autocomplete="current-password"]').fill(password, timeout=10000)
                except:
                    with open("res.txt", "a+") as file:
                        file.write("auth_token={}; ct0={}\n".format("", ""))
                    return False

            except:

                with open("res.txt", "a+") as file:
                    file.write("auth_token={}; ct0={}\n".format("", ""))
                return False

        self.page.wait_for_selector('div[data-testid="LoginForm_Login_Button"]').click()

        try:

            try:
                self.page.wait_for_selector('div[role="alert"]', timeout=3000)

                with open("res.txt", "a+") as file:
                    file.write("auth_token={}; ct0={}\n".format("", ""))

            except:
                pass

            try:
                self.page.wait_for_selector('input[inputmode="email"]', timeout=10000).fill(email)
                self.page.keyboard.press("Enter")
            except:
                pass

            self.page.wait_for_selector('a[href="/explore"]', timeout=20000)

            try:
                self.page.wait_for_selector('div[role="alert"]', timeout=5000)

                with open("res.txt", "a+") as file:
                    file.write("auth_token={}; ct0={}\n".format("", ""))

            except:

                cookies = self.context.cookies()

                auth = ""
                ct0 = ""
                for i in cookies:
                    if i['name'] == "auth_token":
                        auth = i['value']
                    if i['name'] == "ct0":
                        ct0 = i['value']

                with open("res.txt", "a+") as file:
                    file.write("auth_token={}; ct0={}\n".format(auth, ct0))

        except:



            print("Ошибка")


        print("Изи")
        # self.page.wait_for_timeout(10000000)

if __name__ == '__main__':

    proxies = []
    data = []


    with open("data.txt", "r") as file:
        for i in file:
            data.append(i.rstrip().split('	'))

    with open("proxy.txt", "r") as file:
        for i in file:
            proxies.append(i.rstrip())

    count = 32
    for index, item in enumerate(proxies[count-1:]):
        # print(count)
        index = count-1

        print(index, item)

        a = twitter_unlock_v2(item)

        username = data[index][0]
        try:
            password = data[index][1]
        except:

            a.__exit__(None, None,None)
            time.sleep(2)

            count+=1

            with open("res.txt", "a+") as file:
                file.write("auth_token={}; ct0={}\n".format("", ""))
            continue

        try:
            email = data[index][2]
        except:
            email = None

        try:
            email_pass = data[index][3]
        except:
            email_pass = None

        try:
            phone = data[index][4]
        except:
            phone = None

        try:
            a.script(username, password, email, phone)

            a.__exit__(None, None, None)
            time.sleep(5)
        except:
            traceback.print_exc()

            with open("res.txt", "a+") as file:
                file.write("auth_token={}; ct0={}\n".format("", ""))

            a.__exit__(None, None, None)
            time.sleep(5)

        count+=1




