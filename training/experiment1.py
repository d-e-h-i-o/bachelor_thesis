from random import randint

from transformers import (
    AutoModelForTokenClassification,
    TrainingArguments,
    Trainer,
    AutoTokenizer,
    IntervalStrategy,
)
from preprocessing import Preprocessor
from preprocessing.datasets_ import ClaimExtractionDatasets

from utils import (
    eval_k_fold,
    compute_metrics_claim_extraction,
    report_results,
)


def run_experiment1(
    epochs: int = 30,
    learning_rate: float = 2e-5,
):

    datasets = ClaimExtractionDatasets.load_from_database()

    for model_checkpoint in [
        "deepset/gbert-large",
        "deepset/gbert-base",
        "deepset/gelectra-large",
        "deepset/gelectra-base",
        "/data/experiments/dehio/germeval2021/experiments/models/d5d3bd2c2ec20360d4e3827411fdfe6e81a7aaf46dcd285c1a8892b4b8b42d63_gbert-large_fact",
    ]:
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
        except EnvironmentError:
            tokenizer = AutoTokenizer.from_pretrained(
                "deepset/gbert-large"
            )  # in case only model weights were saved

        preprocessor = Preprocessor(tokenizer, "claim_extraction")
        results = []
        for run in range(5):
            for i, (train_set, test_set) in enumerate(datasets.folds):
                model = AutoModelForTokenClassification.from_pretrained(
                    model_checkpoint, num_labels=3, ignore_mismatched_sizes=True
                )
                args = TrainingArguments(
                    f"/data/experiments/dehio/models/test-claim-extraction-{randint(0, 100000)}",
                    evaluation_strategy=IntervalStrategy.EPOCH,
                    learning_rate=learning_rate,
                    per_device_train_batch_size=4,
                    per_device_eval_batch_size=4,
                    per_gpu_train_batch_size=1,
                    num_train_epochs=epochs,
                    weight_decay=0.01,
                    seed=run * 100,
                )
                train_dataset = preprocessor(train_set)
                test_dataset = preprocessor(test_set)
                trainer = Trainer(
                    model,
                    args,
                    train_dataset=train_dataset,
                    eval_dataset=test_dataset,
                    tokenizer=tokenizer,
                    compute_metrics=compute_metrics_claim_extraction,
                )
                trainer.train()
                result = trainer.evaluate()
                results.append(result)

                print(f"Results for fold {i}: {result}")

            print(f"Overall results: {eval_k_fold(results)}")
            report_results(
                "experiment1-claim_extraction",
                eval_k_fold(results),
                datasets,
                parameters={
                    "epochs": epochs,
                    "learning_rate": learning_rate,
                    "model": model_checkpoint,
                },
            )
