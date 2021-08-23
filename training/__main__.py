import typer

from train_claim_extraction_model import train_claim_extraction
from train_law_matching_model import train_law_matching

app = typer.Typer()


@app.command()
def claim_extraction(
    epochs: int = 3,
    cross_validation: bool = True,
    inspect: bool = False,
    learning_rate: float = 2e-5,
    filter_examples_without_claims: bool = False,
):
    train_claim_extraction(
        epochs, cross_validation, inspect, learning_rate, filter_examples_without_claims
    )


@app.command()
def law_matching(
    epochs: int = 3,
    cross_validation: bool = True,
    inspect: bool = False,
    learning_rate: float = 2e-5,
    from_file: str = typer.Option(
        None, help="Load dataset from csv file with this path."
    ),
):
    train_law_matching(epochs, cross_validation, inspect, learning_rate, from_file)


if __name__ == "__main__":
    app()
