import csv
from random import randint

import torch
from transformers import (
    TrainingArguments,
    IntervalStrategy,
)

from preprocessing.datasets_ import LawMatchingDatasets
from train_law_matching_model import train_law_matching_model
from train_law_matching_model import (
    indices_of_wrong_classifications as bert_wrong_indices,
)

from baseline_law_matching import train_baseline
from baseline_law_matching import (
    indices_of_wrong_classifications as baseline_wrong_indices,
)

model_checkpoint = "deepset/gbert-large"

args = TrainingArguments(
    f"/data/experiments/dehio/models/test-law-matching-{randint(0, 100000)}",
    evaluation_strategy=IntervalStrategy.EPOCH,
    learning_rate=0.00001,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    per_gpu_train_batch_size=1,
    per_gpu_eval_batch_size=1,
    num_train_epochs=3,
    weight_decay=0.01,
    eval_accumulation_steps=10,
)


def evaluate():
    datasets = LawMatchingDatasets.load_from_csv("law_matching.csv")
    wrong_predictions = []

    for i, (train_set, test_set) in enumerate(datasets.folds):
        trainer, _ = train_law_matching_model(train_set, test_set, args)
        classifier = train_baseline(train_set)

        baseline_indices = baseline_wrong_indices(test_set, classifier)
        with torch.no_grad():
            torch.cuda.empty_cache()
            bert_indices = bert_wrong_indices(test_set, trainer)

        for i in range(len(test_set)):
            if i in baseline_indices or i in bert_indices:
                wrong_predictions.append(
                    (test_set[i], bool(i in baseline_indices), bool(i in bert_indices))
                )

    with open(
        "/data/experiments/dehio/bachelor_thesis/inspection.csv", "w+", newline=""
    ) as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["Claim", "Subsection", "Label", "Baseline", "Bert"])
        for sample in wrong_predictions:
            writer.writerow(sample)