import numpy as np
from datasets import load_metric

metric = load_metric("seqeval")


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

    results = metric.compute(predictions=predictions, references=labels)
    return {
        "precision": results["overall_precision"],
        "recall": results["overall_recall"],
        "f1": results["overall_f1"],
        "accuracy": results["overall_accuracy"],
    }
