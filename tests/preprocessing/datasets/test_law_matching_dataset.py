import datetime

from preprocessing.datasets import LawMatchingDataset
from preprocessing import Reference, Act


def test_law_matching_dataset_should_load_from_database():
    datasets = LawMatchingDataset.load_from_database(
        database="tests/fixtures/database_fixture.db"
    )
    assert datasets.X is not None


def test_law_matching_dataset_should_parse_rows():
    datasets = LawMatchingDataset.load_from_database(
        database="tests/fixtures/database_fixture.db"
    )
    assert len(datasets.X) == 315
    assert isinstance(datasets.X[0][0], str)  # claim
    assert isinstance(datasets.X[0][1], list)  # list of references
    assert isinstance(datasets.X[0][1][0], Reference)
    assert isinstance(datasets.X[0][2], datetime.date)


def test_law_matching_dataset_should_load_legislation():
    datasets = LawMatchingDataset.load_from_database(
        database="tests/fixtures/database_fixture.db"
    )
    assert datasets.acts
    assert isinstance(datasets.acts[0], Act)
