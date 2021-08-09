import sqlite3
from datetime import datetime
from typing import Generator, Tuple, List

import numpy as np
from numpy.typing import NDArray
from sklearn.model_selection import KFold

from preprocessing.models import Reference, parse_references

LawMatchingSample = Tuple[str, List[Reference], datetime.date]


class LawMatchingDataset:
    """Loads the law matching data from the db, parses the references and dates, and returns folds.
    Usage:
        datasets = LawMatchingDataset.load_from_database()
        for train_split, test_split in datasets.folds:
            train = datasets.X[train_split]
            test = datasets.X[test_split]
    """

    TASK = "law_matching"

    def __init__(self, rows, folds):
        self.kf = KFold(n_splits=folds)
        self.X = self.parse_rows(rows)

    @property
    def folds(self) -> Generator:
        return self.kf.split(self.X)

    @classmethod
    def parse_rows(cls, rows) -> NDArray[LawMatchingSample]:
        samples = []

        for claim, reference_string, date_string in rows:
            claim = claim.strip()
            references = parse_references(reference_string)
            date = datetime.strptime(date_string, "%d.%m.%y").date()
            samples.append((claim, references, date))

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
