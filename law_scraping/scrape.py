from time import sleep
from typing import Optional
from random import randint
import json

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from retry import retry
import typer

random_sleep = lambda: sleep(randint(2, 7))


@retry(tries=3, delay=2, jitter=(1, 3))
def fetch_page(driver, url: str) -> Optional[str]:
    driver.get(url)
    sleep(10)
    return driver.page_source


def save_page(html: str, url: str, law: str) -> None:
    if "%" in url:
        filename = law + "#" + url.split("%")[-1]
    else:
        filename = law + "#"

    with open(f"data/html_pages/{filename}.html", "w+") as file:
        file.write(html)


def main(
    url: str = typer.Option(None, help="Specify if a singe url should be scraped"),
    law: str = typer.Option(None, help="Name of the law"),
    file_with_urls: str = typer.Option(
        None, help="File in data/urls/{file} with urls to scrape"
    ),
):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    failed = []

    file_name = file_with_urls or "all_urls.json"

    if not url:
        with open(f"data/urls/{file_name}", "r") as file:
            to_scrape = json.load(file)

        for law in to_scrape:
            for version_url in to_scrape[law]:
                if html := fetch_page(driver, version_url):
                    save_page(html, version_url, law)
                else:
                    failed.append(version_url)
                random_sleep()
    else:
        save_page(fetch_page(driver, url), url, law)

    driver.close()
    print("Failed: ", failed)


if __name__ == "__main__":
    typer.run(main)
