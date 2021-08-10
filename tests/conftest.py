import pytest

from preprocessing.datasets import LawMatchingDatasets


@pytest.fixture(scope="session")
def law_matching_datasets():
    return LawMatchingDatasets.load_from_database(
        database="tests/fixtures/database_fixture.db"
    )
