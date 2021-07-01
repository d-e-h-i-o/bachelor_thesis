import re
from dataclasses import dataclass
from datetime import date
from typing import List

SECTION_DELIMITER = re.compile(r"\n\n\(\d\)")
SECTION = re.compile(r"(\n\n\(\d\)) (.+?)(?=(\n\n\(\d\)|$))", re.DOTALL)


@dataclass
class Subsection:
    subsection_number: str
    text: str
    section_number: str
    act: str


@dataclass
class Section:
    act: str
    section_number: str
    section_title: str
    text: str
    valid_from: date
    valid_to: date

    @property
    def subsections(self) -> List[Subsection]:
        if SECTION_DELIMITER.search(self.text):
            subsections = []
            for subsection_match in SECTION.finditer(self.text):
                subsection_number = subsection_match.group(1)
                text = subsection_match.group(2)
                subsections.append(
                    Subsection(subsection_number, text, self.section_number, self.act)
                )
        else:
            """Some laws are not split up in subsections, e.g. § 5 3. PflegeM-Cov-19-V
            (https://gesetze.berlin.de/bsbe/document/jlr-CoronaVPflege5VBEpP3)
            For those, we assign the subsection with the number 'full_section'"""
            subsections = [
                Subsection("full_section", self.text, self.section_number, self.act)
            ]
        return subsections
