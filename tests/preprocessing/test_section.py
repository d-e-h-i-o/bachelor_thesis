def test_subsection_numbers_contain_no_newlines(law_matching_datasets):

    section = law_matching_datasets.acts["SARS-CoV-2-EindV"].sections[1]

    for subsection in section.subsections.values():
        assert "\n" not in subsection.subsection_number
