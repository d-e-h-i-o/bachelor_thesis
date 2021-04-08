from time import sleep
from typing import Optional
from random import randint
import json

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

random_sleep = lambda: sleep(randint(1, 5))


def fetch_page(driver, url: str) -> Optional[str]:
    try:
        driver.get(url)
        sleep(5)
        return driver.page_source
    except Exception as e:
        print(e)


def save_page(html: str, url: str) -> None:
    filename = url.split("-")[-1].replace("%", "_")

    with open(f"data/html_pages/{filename}.html", "w+") as file:
        file.write(html)


if __name__ == "__main__":

    driver = webdriver.Chrome(ChromeDriverManager().install())
    failed = []

    with open("data/urls/urls_berliner_verordnungen.json", "r") as file:
        to_scrape = json.load(file)

    for law in to_scrape:
        for version_url in to_scrape[law]:
            if html := fetch_page(driver, version_url):
                save_page(html, version_url)
            else:
                failed.append(version_url)
            random_sleep()

    driver.close()
    print("Failed: ", failed)
