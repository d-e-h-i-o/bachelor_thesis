import sqlite3
from datetime import datetime

from annotation import Annotation

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

today = datetime.today().date().strftime("%d.%m.%y")


def not_yet_processed(raw_annotation) -> bool:
    """Returns false if the annotations is already in the database."""
    cursor.execute("SELECT * FROM claims WHERE id = ?", (raw_annotation["id"],))
    return not bool(cursor.fetchone())


def _save_extraction_data(annotation, plaintext) -> None:
    cursor.execute(
        "INSERT INTO fulltext VALUES(?, ?, ?)",
        (annotation.url, plaintext, today),
    )
    cursor.execute(
        "INSERT INTO claims VALUES(?, ?, ?, ?)",
        (annotation.id, annotation.claim, annotation.url),
    )


def _save_matching_data(annotation) -> None:
    cursor.execute(
        "INSERT INTO references VALUES(?, ?, ?)",
        (annotation.id, annotation.reference, annotation.date),
    )


def save_to_database(raw_annotation, plaintext) -> None:
    annotation = Annotation(raw_annotation)
    if plaintext.find(annotation.claim) == -1:
        print(
            f"For url {annotation.url}: Claim not found in plaintext. Plaintext has to be manually added to fulltext"
            f"table."
        )
        plaintext = ""

    _save_extraction_data(annotation, plaintext)
    if annotation.for_law_matching and annotation.date:
        _save_matching_data(annotation)
    connection.commit()
