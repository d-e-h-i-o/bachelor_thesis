import pytest

from preprocessing.datasets import ClaimExtractionDatasets


def test_claim_extraction_dataset_should_load_from_database():
    datasets = ClaimExtractionDatasets.load_from_database(
        database="tests/fixtures/database_fixture.db"
    )
    assert datasets.X is not None


def test_claim_extraction_dataset_should_group_rows():
    datasets = ClaimExtractionDatasets.load_from_database(
        database="tests/fixtures/database_fixture.db"
    )
    assert len(datasets.X) == 44
    assert isinstance(datasets.X[0][0], str)  # fulltext
    assert isinstance(datasets.X[0][1], list)  # list of (claim_start, claim_end) tuples
    assert isinstance(datasets.X[0][1][0], tuple)  # (claim_start, claim_end) tuple
    assert isinstance(datasets.X[0][1][1][0], int)  # claim_start, or claim_end


def test_claim_extraction_dataset_folds():
    datasets = ClaimExtractionDatasets.load_from_database(
        database="tests/fixtures/database_fixture.db", folds=5
    )
    for train_split, test_split in datasets.folds:
        train = datasets.X[train_split]
        test = datasets.X[test_split]
        assert 35 <= len(train) <= 36
        assert 8 <= len(test) <= 9
