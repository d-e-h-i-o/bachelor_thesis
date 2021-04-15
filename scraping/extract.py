import json
import re
import os
from typing import Tuple
from unicodedata import normalize

from bs4 import BeautifulSoup

ABSATZ = re.compile('\(\d\d?\)')
class LawSoup:
    @staticmethod
    def construct_paragraph(title_tag):
        title = normalize("NFKD", title_tag.contents[0])
        print(title)
        if not title.startswith('§'):
            return
        paragraph = {
            "titleText": title_tag.contents[2].strip(),
        }
        for sibling in title_tag.next_siblings:
            if sibling.name == 'p' and sibling.contents:
                if absatz := ABSATZ.match(sibling.contents[0]):
                    paragraph[absatz.group(0)] = normalize('NFKD', sibling.contents[0])
                    last_num = absatz.group(0)
            elif sibling.name == 'dl':
                for num, text in zip(sibling.find_all('dt'), sibling.find_all('p')):
                    paragraph[last_num] += normalize('NFKD', ' '.join(num.contents) + ' '.join(text.contents))

        return title, paragraph

    def __init__(self, soup):
        self.soup = soup

    def extract_name_and_date(self) -> Tuple[str, str]:
        """<span class="h3_titel">SARS-CoV-2-Infektionsschutzverordnung<br/> Vom 23. Juni 2020</span>"""
        name_and_date = self.soup.find("span", ["h3_titel"]).contents
        name, date = name_and_date[0], name_and_date[2]
        return name, date

    def extract_paragraphs(self):
        potential_paragraphs = self.soup.find_all("h4") + self.soup.find_all("h5")
        paras = {}
        for potential_paragraph in potential_paragraphs:
            if p := LawSoup.construct_paragraph(potential_paragraph):
                paras[p[0]] = p[1]
        return paras


if __name__ == "__main__":

    html_file_names = os.listdir("data/html_pages")

    extracted_laws = {}

    for file_name in html_file_names:
        if file_name.startswith("."):
            continue
        print(file_name)
        with open("data/html_pages/" + file_name, "r") as file:
            soup = LawSoup(BeautifulSoup(file.read(), "html.parser"))
            extracted_laws[file_name.split('.')[0]] = soup.extract_paragraphs()

    with open("laws.json", "w+", encoding='utf8') as file:
        json.dump(extracted_laws, file, ensure_ascii=False)
