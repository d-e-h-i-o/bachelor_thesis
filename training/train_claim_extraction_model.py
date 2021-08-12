import typer
from transformers import (
    AutoModelForTokenClassification,
    TrainingArguments,
    Trainer,
    AutoTokenizer,
    IntervalStrategy,
)
from preprocessing import Preprocessor
from preprocessing.datasets_ import ClaimExtractionDatasets

from utils import eval_k_fold, compute_metrics

model_checkpoint = "deepset/gbert-large"
model_name = model_checkpoint.split("/")[-1]


def main(epochs: int = 3, cross_validation: bool = True, inspect: bool = False):
    args = TrainingArguments(
        f"/data/experiments/dehio/models/test-claim-extraction",
        evaluation_strategy=IntervalStrategy.EPOCH,
        learning_rate=2e-5,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        per_gpu_train_batch_size=1,
        num_train_epochs=epochs,
        weight_decay=0.01,
    )

    datasets = ClaimExtractionDatasets.load_from_database()
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
    preprocessor = Preprocessor(tokenizer, "claim_extraction")
    results = []

    if cross_validation:
        for i, (train_set, test_set) in enumerate(datasets.folds):
            model = AutoModelForTokenClassification.from_pretrained(
                model_checkpoint, num_labels=3
            )
            train_dataset = preprocessor(train_set)
            test_dataset = preprocessor(test_set)
            trainer = Trainer(
                model,
                args,
                train_dataset=train_dataset,
                eval_dataset=test_dataset,
                tokenizer=tokenizer,
                compute_metrics=compute_metrics,
            )
            trainer.train()
            result = trainer.evaluate()
            results.append(result)

            print(f"Results for fold {i}: {result}")

        print(f"Overall results: {eval_k_fold(results)}")
    else:
        model = AutoModelForTokenClassification.from_pretrained(
            model_checkpoint, num_labels=3
        )
        train_dataset = preprocessor(datasets.train)
        test_dataset = preprocessor(datasets.test)
        trainer = Trainer(
            model,
            args,
            train_dataset=train_dataset,
            eval_dataset=test_dataset,
            tokenizer=tokenizer,
            compute_metrics=compute_metrics,
        )
        trainer.train()
        if inspect:
            breakpoint()
        result = trainer.evaluate()
        results.append(result)

        print(f"Results: {result}")


if __name__ == "__main__":
    typer.run(main)
