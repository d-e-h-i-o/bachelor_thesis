import pytest
from unittest.mock import MagicMock

import numpy as np

from preprocessing.datasets import ClaimExtractionDatasets
from preprocessing import Preprocessor


@pytest.fixture(scope="session")
def claim_extraction_sample():
    datasets = ClaimExtractionDatasets.load_from_database(
        database="tests/fixtures/database_fixture.db"
    )
    return datasets.X[0]


def test_preprocessor_chunking_works(claim_extraction_sample):
    tokenizer = MagicMock()
    preprocessor = Preprocessor(tokenizer)

    fulltext, claim_offsets = claim_extraction_sample[0], claim_extraction_sample[1]

    chunks = preprocessor.chunk_fulltext(fulltext, claim_offsets)
    assert (
        len([claim for chunk, chunk_claims in chunks for claim in chunk_claims]) == 18
    )  # all claims are still here

    assert (
        "".join([chunk_text for chunk_text, chunk_claims in chunks]) == fulltext
    )  # all chunks together form the fulltext

    for chunk_text, _ in chunks:
        assert len(chunk_text) <= 2550


def test_preprocessor_align_claim_label_works():
    tokenizer = MagicMock()
    preprocessor = Preprocessor(tokenizer)

    input_ids = [102, 8862, 818, 7679, 16300, 30881, 1420, 28237, 103]
    offset_mapping = [
        (0, 0),
        (0, 2),
        (2, 3),
        (4, 6),
        (7, 10),
        (10, 11),
        (12, 14),
        (15, 21),
        (0, 0),
    ]
    claim_offsets = [(4, 11), (15, 21)]

    expected_labels = np.array([0, 0, 0, 1, 2, 2, 0, 1, 0])

    labels = preprocessor.align_claim_labels(input_ids, offset_mapping, claim_offsets)
    assert (labels == expected_labels).all()
