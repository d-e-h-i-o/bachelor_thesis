import os
from datetime import datetime

import numpy as np
from datasets import load_metric


def eval_k_fold(results):
    # TODO: Is this correct? Is there a better way to do this?
    num_results = len(results)
    keys = list(results[0])
    overall = {}
    for key in keys:
        overall[key] = 0.0

    for result in results:
        for key in keys:
            overall[key] += result[key]

    for key in keys:
        overall[key] /= num_results

    return overall


def compute_metrics_claim_extraction(p):
    metric = load_metric("seqeval", "IOB2")
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


def compute_metrics_law_matching(eval_pred):
    metric = load_metric("glue", "mrpc")
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return metric.compute(predictions=predictions, references=labels)


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
