from .fetch_annotations import fetch_annotations


def run_pipeline():
    annotations = fetch_annotations()


if __name__ == '__main__':
    run_pipeline()
