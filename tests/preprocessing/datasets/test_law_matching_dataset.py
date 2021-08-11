import datetime

from preprocessing import Reference, Act
from preprocessing.datasets import resolve_reference_to_subsection_text


def test_law_matching_dataset_should_load_from_database(law_matching_datasets):

    assert law_matching_datasets.X is not None


def test_law_matching_dataset_should_parse_rows(law_matching_datasets):

    assert len(law_matching_datasets.X) == 890  # both positive and negative samples
    assert isinstance(law_matching_datasets.X[0][0], str)  # claim
    assert isinstance(law_matching_datasets.X[0][1], str)  # list of references
    assert isinstance(law_matching_datasets.X[0][2], bool)  # label


def test_law_matching_dataset_should_load_legislation(law_matching_datasets):

    assert law_matching_datasets.acts


def test_law_matching_dataset_is_balanced(law_matching_datasets):

    positive_samples = filter(lambda sample: sample[2] is True, law_matching_datasets.X)
    negative_samples = filter(
        lambda sample: sample[2] is False, law_matching_datasets.X
    )

    assert len(list(positive_samples)) == len(list(negative_samples))


def test_resolve_reference(law_matching_datasets):
    acts = law_matching_datasets.acts
    reference = Reference(
        act="SARS-CoV-2-EindmaßnV",
        section_number="14",
        subsection_number="1",
        sentences="",
    )
    text = resolve_reference_to_subsection_text(
        reference, acts, datetime.date(2020, 4, 30)
    )
    assert (
        text
        == "\n\nWissenschaftliche Bibliotheken und Archive dürfen unter Beachtung der Hygieneregeln nach §\xa02 "
        "Absatz\xa01 ab dem 27. April 2020 für den Leihbetrieb geöffnet werden."
    )
