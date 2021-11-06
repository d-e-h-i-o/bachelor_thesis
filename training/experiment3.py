import json
import os
from datetime import datetime
from typing import Optional
from random import randint

import numpy as np
import torch
from datasets import load_metric
from transformers import (
    TrainingArguments,
    Trainer,
    AutoTokenizer,
    IntervalStrategy,
    AutoModelForSequenceClassification,
)

from preprocessing import Preprocessor
from preprocessing.datasets_ import LawMatchingDatasets

from utils import eval_k_fold, compute_metrics_law_matching, report_results


def train_law_matching_model(
    train_set, test_set, args, model_checkpoint, preprocessor, tokenizer
):
    model = AutoModelForSequenceClassification.from_pretrained(
        model_checkpoint, num_labels=2
    )
    model.config.gradient_checkpointing = True
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
    return trainer, model


def indices_of_wrong_classifications(test_dataset, trainer, preprocessor):
    metric = load_metric("glue", "mrpc")
    test_dataset = preprocessor(test_dataset)
    logits, labels, _ = trainer.predict(test_dataset)
    predictions = np.argmax(logits, axis=1)
    wrong_predictions = []

    for i in range(len(predictions)):
        if predictions[i] != labels[i]:
            wrong_predictions.append(i)

    result = metric.compute(predictions=predictions, references=labels)
    print(
        "Results for BERT model:",
        result,
        f"{(len(labels) - len(wrong_predictions)) /len(labels)}",
    )
    return wrong_predictions


def run_experiment3(
    epochs: int = 3,
    learning_rate: float = 0.00001,
):

    datasets = LawMatchingDatasets.load_from_csv(
        "results/law_matching_09.09.21_1/dataset.csv"
    )

    results = {
        "deepset/gbert-large": {},
        "deepset/gbert-base": {},
        "deepset/gelectra-large": {},
        "deepset/gelectra-base": {},
    }

    for i, (train_set, test_set) in enumerate(datasets.folds):
        for model_checkpoint in results.keys():
            tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
            preprocessor = Preprocessor(tokenizer, "law_matching")
            for run in range(5):
                args = TrainingArguments(
                    f"/data/experiments/dehio/models/test-law-matching-{randint(0, 100000)}",
                    evaluation_strategy=IntervalStrategy.EPOCH,
                    learning_rate=learning_rate,
                    per_device_train_batch_size=4,
                    per_device_eval_batch_size=4,
                    per_gpu_train_batch_size=1,
                    num_train_epochs=epochs,
                    weight_decay=0.01,
                    seed=run * 100,
                )
                trainer, model = train_law_matching_model(
                    train_set, test_set, args, model_checkpoint, preprocessor, tokenizer
                )
                result = trainer.evaluate()
                if run in results[model_checkpoint]:
                    results[model_checkpoint][run].append(result.copy())
                else:
                    results[model_checkpoint][run] = [result.copy()]

                torch.cuda.empty_cache()
                del trainer
                del model
                print(f"Results for fold {i}: {result}")
                del result

    path = "/data/experiments/dehio/bachelor_thesis/results"
    for model_checkpoint, result_dict in results.items():
        date = datetime.today().strftime("%d.%m.%y")
        full_path = f"{path}/experiment3_{model_checkpoint.split('/')[-1]}{date}"
        os.mkdir(full_path)
        with open(f"{full_path}/results.txt", "w+") as file:
            file.write(
                json.dumps(
                    {
                        "epochs": epochs,
                        "learning_rate": learning_rate,
                        "model": model_checkpoint,
                    },
                    indent=2,
                )
            )
            for run, run_result in result_dict.items():
                file.write(f"\nRun{run}")
                file.write(json.dumps(eval_k_fold(run_result), indent=2))
        datasets.save_to_csv(f"{full_path}/dataset.csv")
