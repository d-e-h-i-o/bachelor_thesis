import sqlite3
from datetime import datetime

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

today = datetime.today().date().strftime("%d.%m.%y")


def not_yet_processed(annotation) -> bool:
    """Returns false if the annotations is already in the database."""
    cursor.execute("SELECT * FROM claims WHERE id = ?", (annotation["id"],))
    return not bool(cursor.fetchone())


def _save_extraction_data(_id, claim, url, plaintext) -> None:
    cursor.execute(
        "INSERT INTO fulltext VALUES(?, ?, ?)",
        (url, plaintext, today),
    )
    cursor.execute(
        "INSERT INTO claims VALUES(?, ?, ?, ?)",
        (_id, claim, url),
    )


def _save_matching_data(_id, reference, date) -> None:
    cursor.execute(
        "INSERT INTO references VALUES(?, ?, ?)",
        (_id, reference, date),
    )


def save_to_database(annotation, plaintext) -> None:
    claim = annotation["target"][0]["selector"][2]["exact"]
    if plaintext.find(claim) == -1:
        print(
            f"For url {annotation['uri']}: Claim not found in plaintext. Plaintext has to be manually added to fulltext"
            f"table."
        )
        plaintext = ""

    _save_extraction_data(
        annotation["id"], annotation["text"], annotation["uri"], plaintext
    )
    _save_matching_data(annotation["id"], annotation["text"], annotation["tags"][0])
    connection.commit()
