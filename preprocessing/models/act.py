import json
from dataclasses import dataclass
from typing import List
import datetime

from preprocessing.models.section import Section


@dataclass
class Act:
    abbreviation: str
    full_name: str
    sections: List[Section]

    @classmethod
    def from_file(cls, filepath):
        with open(filepath, "r") as file:
            data = json.load(file)
        sections = [
            Section.from_dict(data=section_dict, act=data["abbreviation"])
            for section_dict in data["sections"]
        ]
        return cls(
            abbreviation=data["abbreviation"], full_name=data["name"], sections=sections
        )

    def all_sections_for(self, date: datetime.date) -> List[Section]:
        return list(
            filter(
                lambda section: section.valid_from >= date <= section.valid_to,
                self.sections,
            )
        )

    def __repr__(self):
        return f"Act({self.full_name} ({self.abbreviation}))"
