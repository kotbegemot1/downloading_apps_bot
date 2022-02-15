import requests
import json
import time
import os
from dotenv import load_dotenv, find_dotenv

from get_url_selenium import get_url_by_selenium
from bs4 import BeautifulSoup

load_dotenv(find_dotenv())

def get_page_of_app(app_name):
    """Получаем список прриложений по параметру поиска {app_name}"""
    session = requests.Session()
    session.headers.update({
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
                })
    url = f"https://apkcombo.com/ru/search?q={app_name}#gsc.tab=0&gsc.q={app_name}&gsc.page=1"
    req = session.get(url=url)

    soup = BeautifulSoup(req.text, "lxml")

    links = soup.find(id="main").find("div", class_="content").find_all("a")


    result_list = []
    for link in links[0:6]:

        #получаем инфу на приложение
        url = "https://apkcombo.com" + link.get("href")
        print(url)
        req = session.get(url=url) #, proxies=proxies, auth=auth
        soup = BeautifulSoup(req.text, 'lxml')
        apps_list = soup.find("section", class_="info").find_all("tr")

        # добавляем в словарь информацию и приложении 
        app_add = {}
        for app_info in apps_list:
            app_add[app_info.find("td").text] = app_info.find("td").find_next().text

        # получаем ссылку на скачивание
        url += "download/apk"
        # req = session.get(url=url) # , verify=False , proxies=proxies, auth=auth
        # with open(f"{app_name}.html", "w") as file:
        #     file.write(req.text)
        try:
            soup = BeautifulSoup(get_url_by_selenium(url), 'lxml')
            # soup = BeautifulSoup(req.text, 'lxml')
            item = soup.find("div", id="download-tab").find("ul", class_="file-list").find("a").get("href").replace("amp;", "")
        
            # добавляем в словарь ссылку на скачивание
            app_add["ссылка"] = item
        except Exception as ex:
            print(ex)
            continue
        # break
        result_list.append(app_add)
        print(f"[+] page")
        
        
    with open(f"{app_name}.json", 'w', encoding="utf-8") as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)

def get_page_of_app_2(app_name):
    """Получаем список прриложений по параметру поиска {app_name}"""
    start_time = time.time()
    session = requests.Session()
    session.headers.update({
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
                    })
    url = f"https://apkcombo.com/ru/search?q={app_name}#gsc.tab=0&gsc.q={app_name}&gsc.page=1"
    req = session.get(url=url)

    soup = BeautifulSoup(req.text, "lxml")

    apps_list = soup.find(id="main").find("div", class_="content").find_all("a")
    apps_info = []
    for app in apps_list[0:3]:
        app_icon = app.find("img").get("data-src")
        app_name_ = app.find(class_="name").text
        app_author, app_category = app.find(class_="author").text.split(" · ")
        app_link = "https://apkcombo.com" + app.get("href") + "download/apk"
        # print(app_name, app_author, app_category, app_link)
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
    # return json.dumps(apps_info, indent=4, ensure_ascii=False) # ПРОВЕРИТЬ ПОЧЕМУ НЕ РАБОТАЕТ ЕСЛИ НЕ СОХРАНЯТЬ В ДОКУМЕНТ
    # print(js)
    # return apps_info




def main():
    # get_page_of_app("банк")
    print(get_page_of_app_2("vk"))

if __name__ == '__main__':
    main()

