import sqlite3
from operator import itemgetter
from itertools import groupby
from typing import List, Tuple, Generator

import numpy as np
from numpy.typing import NDArray
from sklearn.model_selection import KFold, ShuffleSplit

ClaimExtractionSample = Tuple[str, List[Tuple[int, int]]]


class ClaimExtractionDatasets:
    """Loads the claim extraction data from the db, groups it, and returns folds
    Usage:
        datasets = ClaimExtractionDatasets.load_from_database()
        for train, test in datasets.folds:
            # preprocess train and test set

    or (without folds):
        datasets = ClaimExtractionDatasets.load_from_database()
        train = datasets.train
        test = datasets.test
    """

    TASK = "claim_extraction"

    def __init__(self, rows, folds):
        self.kf = KFold(n_splits=folds)
        self.X = self.group_rows(rows)
        self.train_split, self.test_split = next(
            ShuffleSplit(n_splits=1, test_size=0.25).split(self.X)
        )

    @property
    def folds(self):
        for train_split, test_split in self.kf.split(self.X):
            yield self.X[train_split], self.X[test_split]

    @property
    def train(self) -> NDArray[ClaimExtractionSample]:
        return self.X[self.train_split]

    @property
    def test(self) -> NDArray[ClaimExtractionSample]:
        return self.X[self.test_split]

    @classmethod
    def group_rows(cls, rows) -> NDArray[ClaimExtractionSample]:
        """Takes the db rows (url, fulltext, claim), groups them by url, and returns for every
        url a tuple (fulltext, [(start, end)]) with the claim offsets."""
        sorted_rows = sorted(rows, key=itemgetter(0))
        groups = groupby(sorted_rows, key=itemgetter(0))
        return_list = []
        for url, group in groups:
            group = list(group)
            fulltext: str = group[0][1]
            article = (fulltext, [])
            for _, _, claim in group:
                claim = claim.strip()
                if claim in fulltext:
                    start: int = fulltext.find(claim)
                    end: int = start + len(claim)
                    article[1].append((start, end))
            if article[1]:
                return_list.append(article)

        return np.array(return_list, dtype=object)

    @classmethod
    def load_from_database(cls, database="database.db", folds=5):
        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT f.url, plaintext, claim FROM fulltext f INNER JOIN claims c on f.url=c.url"
        )
        rows = cursor.fetchall()
        cursor.close()
        return cls(rows, folds=folds)
