from dataclasses import dataclass
from typing import List
from datetime import date

from .section import Section


@dataclass
class Act:
    abbreviation: str
    full_name: str
    sections = List[Section]

    def all_sections_for(self, from_date: date, to_date: date):
        return filter(
            lambda section: section.valid_from >= from_date
            and section.valid_to <= to_date,
            self.sections,
        )
