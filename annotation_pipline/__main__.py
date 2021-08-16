import re

import typer

from annotation import Annotation
from fetch_annotations import fetch_annotations
from save_to_wayback_machine import save_to_wayback_machine
from get_plaintext import fetch_plaintext
from database import (
    not_yet_processed,
    save_to_database,
    fetch_all_claims,
    fetch_all_fulltext,
    update_claim,
    update_fulltext,
    fetch_for_healthcheck,
)

app = typer.Typer()


def clean_string(string: str) -> str:
    string = (
        re.sub(r"\n\s*", " ", string).replace("\n", " ").replace("\xa0", " ").strip()
    )
    return string


def clean_data(annotation, plaintext):
    annotation.claim = clean_string(annotation.claim)
    plaintext = clean_string(plaintext)
    return annotation, plaintext


@app.command()
def run():
    annotations = fetch_annotations()
    new_annotations = filter(not_yet_processed, annotations)

    for annotation in new_annotations:
        save_to_wayback_machine(annotation["uri"])
        plaintext = fetch_plaintext(annotation["uri"])
        annotation = Annotation(annotation)
        annotation, plaintext = clean_data(annotation, plaintext)
        save_to_database(annotation, plaintext)
        print(f"Processed annotation with id {annotation['id']}")


@app.command()
def clean():
    for annotation_id, claim, _ in fetch_all_claims():
        claim = clean_string(claim)
        update_claim(claim, annotation_id)

    for annotation_id, plaintext, _ in fetch_all_fulltext():
        plaintext = clean_string(plaintext)
        update_fulltext(plaintext, annotation_id)


@app.command()
def healthcheck(verbose: bool = False):
    count = 0
    for annotation_id, claim, plaintext in fetch_for_healthcheck():
        if claim not in plaintext:
            count += 1
            if verbose:
                print(annotation_id)
                print(claim)
                print(plaintext)
    print(f"Claims not in plaintext: {count}")


if __name__ == "__main__":
    app()
