import typer

from train_claim_extraction_model import train_claim_extraction

app = typer.Typer()


@app.command()
def claim_extraction(
    epochs: int = 3,
    cross_validation: bool = True,
    inspect: bool = False,
    learning_rate: float = 2e-5,
):
    train_claim_extraction(epochs, cross_validation, inspect, learning_rate)


@app.command()
def law_matching():
    pass


if __name__ == "__main__":
    app()
