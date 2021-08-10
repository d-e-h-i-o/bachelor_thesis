import os
import sqlite3
from datetime import datetime
from random import choice
from typing import Generator, Tuple, List

import numpy as np
from numpy.typing import NDArray
from sklearn.model_selection import KFold

from preprocessing.models import Reference, parse_references, Act

LawMatchingSample = Tuple[str, Reference, datetime.date, bool]


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

    def __init__(self, rows, folds):
        self.kf = KFold(n_splits=folds)
        self.acts = self.load_legislation()
        self.X = self.parse_rows(rows)

    @property
    def folds(self) -> Generator:
        return self.kf.split(self.X)

    def parse_rows(self, rows) -> NDArray[LawMatchingSample]:
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

    def sample_reference(
        self, negative_list: List[Reference], date: datetime.date
    ) -> Reference:
        """Samples a random reference, that is not included in the negative list.
        If the date is from a date with no valid acts, it will go into an eternal loop.
        """
        while True:
            act = choice(
                list(filter(lambda act: act.has_sections_for(date), self.acts))
            )
            valid_sections = act.all_sections_for(date)
            if not valid_sections:
                continue

            section = choice(valid_sections)
            subsection = choice(section.subsections)
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
        return acts
