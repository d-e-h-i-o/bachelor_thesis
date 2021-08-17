import os
from datetime import datetime

import numpy as np
from datasets import load_metric

metric = load_metric("seqeval", "IOB2")


def eval_k_fold(results):
    # TODO: Is this correct? Is there a better way to do this?
    num_results = len(results)
    overall = {
        "eval_loss": 0.0,
        "eval_precision": 0.0,
        "eval_recall": 0.0,
        "eval_f1": 0.0,
        "eval_accuracy": 0.0,
    }
    for result in results:
        overall["eval_loss"] += result["eval_loss"]
        overall["eval_precision"] += result["eval_precision"]
        overall["eval_recall"] += result["eval_recall"]
        overall["eval_f1"] += result["eval_f1"]
        overall["eval_accuracy"] += result["eval_accuracy"]

    overall["eval_loss"] /= num_results
    overall["eval_precision"] /= num_results
    overall["eval_recall"] /= num_results
    overall["eval_f1"] /= num_results
    overall["eval_accuracy"] /= num_results

    return overall


def compute_metrics(p):
    predictions, labels = p
    predictions = np.argmax(predictions, axis=2)

    label_list = ["O", "B", "I"]

    true_predictions = [
        [label_list[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    true_labels = [
        [label_list[l] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]

    results = metric.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": results["overall_precision"],
        "recall": results["overall_recall"],
        "f1": results["overall_f1"],
        "accuracy": results["overall_accuracy"],
    }


def report_cross_validation_results():
    pass


def report_one_pass_results(dataset, results, parameters):
    path = "/data/experiments/dehio/results"
    if not os.path.exists(path):
        os.mkdir(path)
    name = f'Run: {datetime.today().strftime("%c")}'
    os.mkdir("name")
    dataset.save_to_disk(path + f"/{name}/dataset")

    with open(path + "results/{name}/results.txt", "w+") as file:
        file.write(str(results))
        file.write(str(parameters))


def num_of_examples_without_claims(dataset):
    return len([e for e in dataset if sum(filter(lambda x: x >= 0, e["labels"])) == 0])
