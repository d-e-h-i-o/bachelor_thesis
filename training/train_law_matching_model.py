from transformers import (
    TrainingArguments,
    Trainer,
    AutoTokenizer,
    IntervalStrategy,
    AutoModelForSequenceClassification,
)

from preprocessing import Preprocessor
from preprocessing.datasets_ import LawMatchingDatasets

from utils import (
    eval_k_fold,
    compute_metrics_law_matching,
)

model_checkpoint = "deepset/gbert-large"
model_name = model_checkpoint.split("/")[-1]


def train_law_matching(
    epochs: int = 3,
    cross_validation: bool = True,
    inspect: bool = False,
    learning_rate: float = 2e-5,
):
    args = TrainingArguments(
        f"/data/experiments/dehio/models/test-law-matching",
        evaluation_strategy=IntervalStrategy.EPOCH,
        learning_rate=learning_rate,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        per_gpu_train_batch_size=1,
        num_train_epochs=epochs,
        weight_decay=0.01,
    )

    datasets = LawMatchingDatasets.load_from_database()
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
    preprocessor = Preprocessor(tokenizer, "law_matching")
    results = []

    if cross_validation:
        for i, (train_set, test_set) in enumerate(datasets.folds):
            model = AutoModelForSequenceClassification.from_pretrained(
                model_checkpoint, num_labels=2
            )
            train_dataset = preprocessor(train_set)
            test_dataset = preprocessor(test_set)
            trainer = Trainer(
                model,
                args,
                train_dataset=train_dataset,
                eval_dataset=test_dataset,
                tokenizer=tokenizer,
                compute_metrics=compute_metrics_law_matching,
            )
            trainer.train()
            result = trainer.evaluate()
            results.append(result)

            print(f"Results for fold {i}: {result}")

        print(f"Overall results: {eval_k_fold(results)}")
    else:
        model = AutoModelForSequenceClassification.from_pretrained(
            model_checkpoint, num_labels=2
        )
        train_dataset = preprocessor(datasets.train)
        test_dataset = preprocessor(datasets.test)
        trainer = Trainer(
            model,
            args,
            train_dataset=train_dataset,
            eval_dataset=test_dataset,
            tokenizer=tokenizer,
            compute_metrics=compute_metrics_law_matching,
        )
        trainer.train()
        if inspect:
            breakpoint()
        result = trainer.evaluate()
        print(result)
