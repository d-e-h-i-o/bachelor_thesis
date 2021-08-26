import typer

from train_claim_extraction_model import train_claim_extraction
from train_law_matching_model import train_law_matching
from baseline_law_matching import calculate_baseline_law_matching
from evaluate_law_matching import evaluate as _evaluate

app = typer.Typer()


@app.command()
def claim_extraction(
    epochs: int = typer.Option(3, help="Number of epochs"),
    cross_validation: bool = typer.Option(True, help="5-fold cross validation"),
    inspect: bool = typer.Option(
        False,
        help="Sets breakpoint after model was trained, to interactively inspect results.",
    ),
    learning_rate: float = 2e-5,
):
    train_claim_extraction(epochs, cross_validation, inspect, learning_rate)


@app.command()
def law_matching(
    epochs: int = typer.Option(3, help="Number of epochs"),
    cross_validation: bool = typer.Option(True, help="5-fold cross validation"),
    inspect: bool = typer.Option(
        False,
        help="Sets breakpoint after model was trained, to interactively inspect results.",
    ),
    learning_rate: float = 2e-5,
    from_file: str = typer.Option(
        None, help="Load dataset from csv file with this path."
    ),
):
    train_law_matching(epochs, cross_validation, inspect, learning_rate, from_file)


@app.command()
def baseline_law_matching(
    from_file: str = typer.Option(
        None, help="Load dataset from csv file with this path."
    )
):
    calculate_baseline_law_matching(from_file)


@app.command()
def evaluate():
    _evaluate()


if __name__ == "__main__":
    app()
