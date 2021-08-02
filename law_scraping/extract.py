import json
import re
import os
from typing import Tuple, Dict, List
from unicodedata import normalize

from bs4 import BeautifulSoup

ABSATZ = re.compile("\(\d\d?\)")

law_abbr_mapping = {
    "SARS-CoV-2-EindV": "SARS-CoV-2-Eindämmungsverordnung",
    "SARS-CoV-2-Eindma\u00dfnV": "SARS-CoV-2-Eindämmungsmaßnahmenverordnung",
    "Gro\u00dfveranstVerbV": "Großveranstaltungsverbotsverordnung",
    "SARS-CoV-2-Infektionsschutzverordnung": "SARS-CoV-2-Infektionsschutzverordnung",
    "InfSchMV": "SARS-CoV-2-Infektionsschutzmaßnahmenverordnung",
    "2. InfSchMV": "Zweite SARS-CoV-2-Infektionsschutzmaßnahmenverordnung",
    "3. InfSchMV": "Dritte SARS-CoV-2-Infektionsschutzmaßnahmenverordnung",
    "Zweite Krankenhaus-Covid-19-Verordnung": "Zweite Krankenhaus-Covid-19-Verordnung",
    "Zweite Pflegemaßnahmen-Covid-19-Verordnung": "Zweite Pflegemaßnahmen-Covid-19-Verordnung)",
}


class LawStore:
    def __init__(self, law_name):
        self.filename = law_name + ".json"
        law_files = os.listdir("data/parsed_laws")
        if self.filename in law_files:
            with open("data/parsed_laws/" + self.filename, "r") as file:
                self.data = json.load(file)
        else:
            self.data = {
                "name": law_abbr_mapping[law_name],
                "abbreviation": law_name,
                "sections": [],
            }

    def save(self):
        with open("data/parsed_laws/" + self.filename, "w+") as file:
            json.dump(self.data, file)


def get_table_of_contents(soup) -> Dict[str, str]:
    table_html = [
        table for table in soup.find_all("table") if table.find("thead")
    ].pop()
    return parse_table(table_html)


def parse_table(table_html: str) -> Dict[str, str]:
    table = {}

    tbody = table_html.find("tbody")
    rows = tbody.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        table[cols[0].replace("\xa0", " ")] = cols[1]
    return table


class LawSoup:
    def __init__(self, soup):
        self.soup = soup
        self.table_of_contents = get_table_of_contents(soup)

    def construct_section(self, title_tag):
        title = normalize(
            "NFKD", title_tag.contents[0]
        )  # to remove unicode sign like protected spaces

        if not title.startswith("§"):
            return

        for name, dates in self.table_of_contents.items():
            if name.startswith(name):
                valid_from, valid_to = dates.split(" bis ")

        section = {
            "sectionNumber": title.split(" ")[1],  # '§ 1' => '1'
            "sectionTitle": title_tag.contents[2].strip(),
            "valid_from": valid_from,
            "valid_to": valid_to,
            "text": "",
        }
        for sibling in title_tag.next_siblings:
            if sibling.name == "p" and sibling.contents:
                section["text"] += "\n\n" + sibling.contents[0]
            elif sibling.name == "dl":
                for num, text in zip(sibling.find_all("dt"), sibling.find_all("p")):
                    section["text"] += (
                        "\n" + " ".join(num.contents) + " ".join(text.contents)
                    )
        return section

    def extract_name_and_date(self) -> Tuple[str, str]:
        """<span class="h3_titel">SARS-CoV-2-Infektionsschutzverordnung<br/> Vom 23. Juni 2020</span>"""
        name_and_date = self.soup.find("span", ["h3_titel"]).contents
        name, date = name_and_date[0], name_and_date[2]
        return name, date

    def extract_sections(self) -> List[Dict[str, str]]:
        potential_sections = self.soup.find_all("h4") + self.soup.find_all("h5")
        sections = [
            self.construct_section(potential_section)
            for potential_section in potential_sections
        ]
        return [section for section in sections if section]


if __name__ == "__main__":

    html_file_names = [
        filename for filename in os.listdir("data/html_pages") if "#" in filename
    ]  # only the new filename format contains '#'

    extracted_laws = {}

    for file_name in html_file_names:
        if file_name.startswith("."):
            continue
        print(file_name)
        law_name = file_name.split("#")[0]
        with open("data/html_pages/" + file_name, "r") as file:
            soup = LawSoup(BeautifulSoup(file.read(), "html.parser"))
            store = LawStore(law_name)
            store.data["sections"] += soup.extract_sections()
            store.save()
