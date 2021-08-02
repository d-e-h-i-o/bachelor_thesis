from datetime import date

from preprocessing import Act


def test_act_from_file_constructor():
    file_path = "tests/fixtures/InfSchMV_fixture.json"
    act = Act.from_file(file_path)


def test_act_should_return_valid_sections():
    file_path = "tests/fixtures/InfSchMV_fixture.json"
    act = Act.from_file(file_path)

    valid_date = date(2021, 2, 13)
    assert len(act.all_sections_for(valid_date)) == 32
