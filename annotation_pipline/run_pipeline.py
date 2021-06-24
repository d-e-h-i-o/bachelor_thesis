from fetch_annotations import fetch_annotations
from save_to_wayback_machine import save_to_wayback_machine
from get_plaintext import fetch_plaintext
from database import not_yet_processed, save_to_database


def run_pipeline():
    annotations = fetch_annotations()
    new_annotations = filter(not_yet_processed, annotations)

    for annotation in new_annotations:
        save_to_wayback_machine(annotation["uri"])
        plaintext = fetch_plaintext(annotation["uri"])
        save_to_database(annotation, plaintext)
        print(f"Processed annotation with id {annotation['id']}")


if __name__ == "__main__":
    run_pipeline()