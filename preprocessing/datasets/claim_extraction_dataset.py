import sqlite3
from operator import itemgetter
from itertools import groupby
from typing import List, Tuple, Generator

import numpy as np
from numpy.typing import NDArray
from sklearn.model_selection import KFold


class ClaimExtractionDatasets:
    """Loads the claim extraction data from the db, groups it, and returns folds
    Usage:
        datasets = ClaimExtractionDatasets.load_from_database()
        for fold in datasets.folds:
            train = datasets.X[fold[0]]
            test = datasets.X[fold[1]]
    """

    def __init__(self, rows, folds):
        self.kf = KFold(n_splits=folds)
        self.X = self.group_rows(rows)

    @property
    def folds(self) -> Generator:
        return self.kf.split(self.X)

    @classmethod
    def group_rows(cls, rows) -> NDArray[Tuple[str, List[Tuple[int, int]]]]:
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
                if claim in fulltext:
                    start: int = fulltext.find(claim)
                    end: int = start + len(claim)
                    article[1].append((start, end))
            if article[1]:
                return_list.append(article)

        return np.array(return_list)

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
