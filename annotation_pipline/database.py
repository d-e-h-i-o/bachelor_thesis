import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()


def not_yet_processed(annotation) -> bool:
    """Returns false if the annotations is already in the database."""
    cursor.execute("SELECT * FROM extraction_data WHERE id = ?", (annotation["id"],))
    return not bool(cursor.fetchone())


def _save_extraction_data(_id, plaintext, claim_starts, claim_ends) -> None:
    cursor.execute(
        "INSERT INTO extraction_data VALUES(?, ?, ?, ?)",
        (_id, plaintext, claim_starts, claim_ends),
    )


def _save_matching_data(_id, claim, reference, date) -> None:
    cursor.execute(
        "INSERT INTO matching_data VALUES(?, ?, ?, ?)",
        (_id, claim, reference, date),
    )


def save_to_database(annotation, plaintext) -> None:
    claim = annotation["target"][0]["selector"][2]["exact"]
    claim_starts = plaintext.find(claim)
    if claim_starts == -1:
        print(
            f"Could not process annotation with id {annotation['id']}: Claim not found in plaintext."
        )
        return
    claim_ends = claim_starts + len(claim)

    _save_extraction_data(annotation["id"], plaintext, claim_starts, claim_ends)
    _save_matching_data(
        annotation["id"], claim, annotation["text"], annotation["tags"][0]
    )
    connection.commit()
