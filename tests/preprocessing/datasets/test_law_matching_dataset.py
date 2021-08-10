import datetime


from preprocessing import Reference, Act


def test_law_matching_dataset_should_load_from_database(law_matching_datasets):

    assert law_matching_datasets.X is not None


def test_law_matching_dataset_should_parse_rows(law_matching_datasets):

    assert len(law_matching_datasets.X) == 862  # both positive and negative samples
    assert isinstance(law_matching_datasets.X[0][0], str)  # claim
    assert isinstance(law_matching_datasets.X[0][1], Reference)  # list of references
    assert isinstance(law_matching_datasets.X[0][2], datetime.date)  # date of the claim
    assert isinstance(law_matching_datasets.X[0][3], bool)  # label


def test_law_matching_dataset_should_load_legislation(law_matching_datasets):

    assert law_matching_datasets.acts
    assert isinstance(law_matching_datasets.acts[0], Act)


def test_law_matching_dataset_is_balanced(law_matching_datasets):

    positive_samples = filter(lambda sample: sample[3] is True, law_matching_datasets.X)
    negative_samples = filter(
        lambda sample: sample[3] is False, law_matching_datasets.X
    )

    assert len(list(positive_samples)) == len(list(negative_samples))
