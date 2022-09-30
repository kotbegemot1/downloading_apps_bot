import requests
import json
import time
import os

from bs4 import BeautifulSoup

def get_page_of_app(app_name):
    start_time = time.time()
    """Получаем список прриложений по параметру поиска {app_name}"""
    os.system(f"curl -o web_pages_apps/{app_name}.html https://apkcombo.com/ru/search/{app_name}")
    time.sleep(2)
    with open(f"web_pages_apps/{app_name}.html", "r") as f:
        src = f.read()

    soup = BeautifulSoup(src, "lxml")

    apps_list = soup.find(id="main").find("div", class_="content").find_all("a")
    apps_info = []
    for app in apps_list[0:3]:
        app_icon = app.find("img").get("data-src")
        app_name_ = app.find(class_="name").text
        app_author, app_category = app.find(class_="author").text.split(" · ")
        app_link = "https://apkcombo.com" + app.get("href") + "download/apk"
        apps_info.append({
            "app_icon": app_icon,
            "app_name": app_name_,
            "app_author": app_author,
            "app_category": app_category,
            "app_link": app_link
        })
        # break
    with open(f"JSONs/{app_name}-data.json", "w") as file:
        json.dump(apps_info, file, indent=4, ensure_ascii=False)
    print("--- %s seconds ---" % (time.time() - start_time))


def main():
    """Для теста"""
    print(get_page_of_app("ok"))

if __name__ == '__main__':
    main()