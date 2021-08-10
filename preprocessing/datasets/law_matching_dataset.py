import os
import sqlite3
import csv
from datetime import datetime
from random import choice
from typing import Generator, Tuple, List, Union, Optional, Dict

import numpy as np
from numpy.typing import NDArray
from sklearn.model_selection import KFold

from preprocessing.models import Reference, parse_references, Act

LawMatchingSample = Tuple[str, Reference, datetime.date, bool]
DBRow = Tuple[str, str, str]


def resolve_reference_to_subsection_text(
    reference: Reference, acts: Dict[str, Act], date: datetime.date
) -> Optional[str]:
    """Returns the subsection text of a reference."""
    if act := acts.get(reference.act):
        if section := act.all_sections_for(date).get(reference.section_number):
            subsections = section.subsections
            if subsection := subsections.get("full_section"):
                # section has no split into subsections
                return subsection.text
            if subsection := subsections.get(reference.subsection_number):
                return subsection.text

    return None


class LawMatchingDatasets:
    """The dataset has the following functions.
    1. Either loads data from the database and
        a. Parses the data and create positive samples
        b. Creates negative samples
        c. Saves the dataset to a csv file
    2. Or loads a prepared dataset from a csv file

    Usage:
        datasets = LawMatchingDataset.load_from_database()
        for train_split, test_split in datasets.folds:
            train = datasets.X[train_split]
            test = datasets.X[test_split]
    """

    TASK = "law_matching"

    def __init__(
        self,
        input: Union[List[DBRow], NDArray[LawMatchingSample]],
        folds,
        needs_preprocessing=True,
    ):
        self.kf = KFold(n_splits=folds)
        self.acts = self.load_legislation()
        if needs_preprocessing:
            self.X = self.parse_rows(input)
        else:
            self.X = input

    @property
    def folds(self) -> Generator:
        return self.kf.split(self.X)

    def parse_rows(self, rows: List[DBRow]) -> NDArray[LawMatchingSample]:
        """Parse the raw rows from the database, and adds a negative sample for every positive."""
        samples = []

        for claim, reference_string, date_string in rows:
            claim = claim.strip()
            references = parse_references(reference_string)
            date = datetime.strptime(date_string, "%d.%m.%y").date()
            used_references = references.copy()  # those are already in an sample
            for reference in references:
                positive_sample = (claim, reference, date, True)
                wrong_reference = self.sample_reference(used_references, date)
                negative_sample = (claim, wrong_reference, date, False)
                used_references.append(wrong_reference)

                samples.append(positive_sample)
                samples.append(negative_sample)

        return np.array(samples, dtype=object)

    @classmethod
    def load_from_database(cls, database="database.db", folds=5):
        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT c.claim, r.reference, r.date FROM claims c "
            "INNER JOIN 'references' r on c.annotation_id=r.annotation_id "
        )
        rows = cursor.fetchall()
        cursor.close()
        return cls(rows, folds=folds)

    @classmethod
    def load_from_csv(cls, file_name, folds=5):
        pass  # TODO

    def save_to_csv(self, file_name):
        with open(file_name, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=";")

            for sample in self.X:
                writer.writerow(sample)

    def sample_reference(
        self, negative_list: List[Reference], date: datetime.date
    ) -> Reference:
        """Samples a random reference, that is not included in the negative list.
        If the date is from a date with no valid acts, it will go into an eternal loop.
        """
        while True:
            act = choice(
                list(
                    filter(
                        lambda act: act.has_sections_for(date), list(self.acts.values())
                    )
                )
            )
            valid_sections = list(act.all_sections_for(date).values())
            if not valid_sections:
                continue

            section = choice(valid_sections)
            subsection = choice(list(section.subsections.values()))
            reference = Reference(
                act=act.abbreviation,
                section_number=section.section_number,
                subsection_number=subsection.subsection_number,
                sentences="",
            )
            if reference not in negative_list:
                return reference

    @classmethod
    def load_legislation(cls, path="legislation"):
        acts = []
        for file_name in os.listdir(path):
            acts.append(Act.from_file(f"{path}/{file_name}"))
        return {act.abbreviation: act for act in acts}
