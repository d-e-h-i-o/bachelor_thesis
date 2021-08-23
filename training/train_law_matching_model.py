from typing import Optional
from random import randint

import numpy as np
import torch
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
    from_file: Optional[str] = None,
):
    args = TrainingArguments(
        f"/data/experiments/dehio/models/test-law-matching-{randint(0, 100000)}",
        evaluation_strategy=IntervalStrategy.EPOCH,
        learning_rate=learning_rate,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        per_gpu_train_batch_size=1,
        num_train_epochs=epochs,
        weight_decay=0.01,
    )

    if from_file:
        datasets = LawMatchingDatasets.load_from_csv(from_file)
    else:
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

            def inspect_sample(nr: int):
                texts = tokenizer.decode(test_dataset[nr]["input_ids"]).split(" [SEP] ")
                output = model(
                    input_ids=torch.from_numpy(np.array(test_dataset[nr]["input_ids"]))
                    .unsqueeze(0)
                    .cuda(),
                    attention_mask=torch.from_numpy(
                        np.array(test_dataset[nr]["attention_mask"])
                    )
                    .unsqueeze(0)
                    .cuda(),
                )
                print(f"Claim: {texts[0][6:]}\n")
                print(f"Law: {texts[1][:][:-6]}\n")
                print(f"Label: {bool(test_dataset[nr]['labels'])}\n")
                logits = output.logits.cpu().detach().numpy()
                predictions = np.argmax(logits, axis=1)
                print(f"Prediction: {bool(predictions)}")

            breakpoint()
        result = trainer.evaluate()
        print(result)
