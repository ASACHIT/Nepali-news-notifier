import random
import time
import webbrowser
from functools import partial

import requests
from bs4 import BeautifulSoup
from win10toast_click import ToastNotifier

baseurl = "https://kathmandupost.com"
notification = ToastNotifier()


class News:
    def __init__(self):
        htmlcontent = requests.get("https://kathmandupost.com/").text
        soup = BeautifulSoup(htmlcontent, "html.parser")
        self.content = soup.find_all(
            "div",
            class_="col-xs-12 col-sm-6 col-md-4 grid-first divider-right order-2--sm",
        )

    def get_random_news(self):
        for news in self.content:
            all_anchors = news.find_all("a")
            random_news = random.choice(all_anchors)
            random_news_href = baseurl + random_news["href"]
            return random_news.text, random_news_href


def open_link_in_browser(link):
    webbrowser.open_new_tab(link)
    print("Opened Link In NEw Tab")


def push_notification():
    news, href = News().get_random_news()
    callback_open = partial(open_link_in_browser, href)
    notification.show_toast(
        title=news,
        msg=href,
        duration=10,
        threaded=True,
        callback_on_click=callback_open,
    )
    print("Notification pushed")


if __name__ == "__main__":
    while True:
        push_notification()
        time.sleep(10)  # Change this according to your preference
