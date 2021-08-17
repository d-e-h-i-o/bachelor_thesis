import sqlite3
import pickle
from operator import itemgetter
from itertools import groupby
from typing import List, Tuple

import numpy as np
from numpy.typing import NDArray
from sklearn.model_selection import KFold, ShuffleSplit

ClaimExtractionSample = Tuple[str, List[Tuple[int, int]]]
Offset = Tuple[int, int]


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
        self.X: List[ClaimExtractionSample] = []
        grouped_rows = self.group_rows(rows)
        for sample_text, claim_offsets in grouped_rows:
            chunks = self.chunk_fulltext(sample_text, claim_offsets)
            for sample in chunks:
                self.X.append(sample)

        self.X = np.array(self.X)
        self.train_split, self.test_split = next(
            ShuffleSplit(n_splits=1, test_size=0.15).split(self.X)
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

    @staticmethod
    def chunk_fulltext(
        fulltext: str, claims: List[Offset]
    ) -> List[Tuple[str, List[Offset]]]:
        """Split article fulltext into smaller chunks (max. 512 tokens), with the condition that
        every claim is fully contained in one chunk."""
        length = 2300  # this is a heuristic
        offset = 0
        chunks = []

        for i in range(0, len(fulltext), length):
            chunk_last = i + length
            chunk = fulltext[i - offset : chunk_last]
            chunk_claims = []

            next_offset = None
            for claim_start, claim_end in claims:
                if claim_start < chunk_last < claim_end:
                    # overlapping claim
                    next_offset = chunk_last - claim_start
                    chunk_last = claim_start
                    chunk = fulltext[(i - offset) : chunk_last]
                    break

            for claim_start, claim_end in claims:
                # add claims that are fully contained in chunk
                claim = fulltext[claim_start:claim_end]
                if claim in chunk:
                    # offsets have to be newly calculated for the chunk
                    new_start: int = chunk.find(claim)
                    new_end: int = new_start + len(claim)
                    chunk_claims.append((new_start, new_end))

            offset = next_offset or 0
            chunks.append((chunk, chunk_claims))

        return chunks

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

    def save_to_disk(self, file_path):
        with open(file_path, "w") as file:
            pickle.dump(self, file)
