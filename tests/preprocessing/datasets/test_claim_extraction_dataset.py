import sqlite3

import pytest

from training.preprocessing.datasets_ import ClaimExtractionDatasets


@pytest.fixture
def sample_from_database():
    connection = sqlite3.connect("tests/fixtures/database_fixture.db")
    sample = connection.execute(
        "SELECT f.url, plaintext, claim FROM fulltext f INNER JOIN claims c on f.url=c.url"
    ).fetchone()
    return sample


def test_claim_extraction_dataset_should_load_from_database():
    datasets = ClaimExtractionDatasets.load_from_database(
        database="tests/fixtures/database_fixture.db"
    )
    assert datasets.X is not None


def test_claim_extraction_dataset_should_group_rows():
    datasets = ClaimExtractionDatasets.load_from_database(
        database="tests/fixtures/database_fixture.db"
    )
    assert len(datasets.X) == 158
    assert isinstance(datasets.X[0][0], str)  # fulltext
    assert isinstance(datasets.X[0][1], list)  # list of (claim_start, claim_end) tuples
    assert isinstance(datasets.X[0][1][0], tuple)  # (claim_start, claim_end) tuple
    assert isinstance(datasets.X[0][1][1][0], int)  # claim_start, or claim_end


def test_claim_extraction_dataset_folds():
    datasets = ClaimExtractionDatasets.load_from_database(
        database="tests/fixtures/database_fixture.db", folds=5
    )
    for train, test in datasets.folds:
        assert 124 <= len(train) <= 127
        assert 30 <= len(test) <= 34

    assert len(datasets.train) == 134
    assert len(datasets.test) == 24


@pytest.mark.skip
def test_claim_extracion_datasets_chunking_works(sample_from_database):
    datasets = ClaimExtractionDatasets.load_from_database(
        database="tests/fixtures/database_fixture.db", folds=5
    )

    fulltext, claim_offsets = sample_from_database[0], sample_from_database[1]

    chunks = datasets.chunk_fulltext(fulltext, claim_offsets)

    assert (
        len([claim for chunk, chunk_claims in chunks for claim in chunk_claims]) == 19
    )  # all claims are still here

    assert (
        "".join([chunk_text for chunk_text, chunk_claims in chunks]) == fulltext
    )  # all chunks together form the fulltext

    for chunk_text, _ in chunks:
        assert len(chunk_text) <= 2550
