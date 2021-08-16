import numpy as np
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
    compute_metrics,
    report_one_pass_results,
    num_of_examples_without_claims,
)

model_checkpoint = "deepset/gbert-large"
model_name = model_checkpoint.split("/")[-1]


def inspect_sample(sample, model, tokenizer):
    output = model(
        input_ids=sample["input_ids"].unsqueeze(0).cuda(),
        attention_mask=sample["attention_mask"].unsqueeze(0).cuda(),
    )
    pred = np.argmax(output.logits.cpu().detach().numpy(), axis=2)
    original_text_raw = sample["input_ids"].detach().numpy().copy()
    text_raw = original_text_raw.copy()
    original_text_raw[np.array(sample["labels"]) == 0] = 0
    text_raw[pred[0] == 0] = 0
    print("Target text:\n")
    print(tokenizer.decode(original_text_raw))
    print("Inferred text:")
    print(tokenizer.decode(text_raw))
    print("Predictions:")
    print(pred)


def train_claim_extraction(
    epochs: int = 3,
    cross_validation: bool = True,
    inspect: bool = False,
    learning_rate: float = 2e-5,
    filter_examples_without_claims: bool = False,
):
    args = TrainingArguments(
        f"/data/experiments/dehio/models/test-claim-extraction",
        evaluation_strategy=IntervalStrategy.EPOCH,
        learning_rate=learning_rate,
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

        print(
            "Examples with no claims in train dataset:",
            num_of_examples_without_claims(train_dataset),
        )
        print(
            "Examples with no claims in test dataset:",
            num_of_examples_without_claims(test_dataset),
        )
        if filter_examples_without_claims:
            train_dataset = np.array(
                [
                    e
                    for e in train_dataset
                    if sum(filter(lambda x: x >= 0, e["labels"])) > 0
                ]
            )
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
        parameter = {"epochs": epochs, "learning_rate": learning_rate}
        report_one_pass_results(datasets, result, parameter)

        print(f"Results: {result}")
