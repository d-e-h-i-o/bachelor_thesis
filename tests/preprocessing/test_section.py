def test_subsection_numbers_contain_no_newlines(law_matching_datasets):

    section = law_matching_datasets.acts[0].sections[0]
    for subsection in section.subsections:
        assert "\n" not in subsection.subsection_number
