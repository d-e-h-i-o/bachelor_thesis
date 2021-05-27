from .fetch_annotations import fetch_annotations
from .save_to_wayback_machine import save_to_wayback_machine


def run_pipeline():
    annotations = fetch_annotations()

    for annotation in annotations:
        save_to_wayback_machine(annotation["url"])


if __name__ == "__main__":
    run_pipeline()
