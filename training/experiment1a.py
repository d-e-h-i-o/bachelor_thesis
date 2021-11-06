import json
import os
from datetime import datetime
from random import randint

from transformers import (
    AutoModelForTokenClassification,
    TrainingArguments,
    Trainer,
    AutoTokenizer,
    IntervalStrategy,
    set_seed,
)
from preprocessing import Preprocessor
from preprocessing.datasets_ import ClaimExtractionDatasets

from utils import (
    eval_k_fold,
    compute_metrics_claim_extraction,
    report_results,
)


def run_experiment1a(
    epochs: int = 30,
    learning_rate: float = 2e-5,
):

    set_seed(0)
    datasets = ClaimExtractionDatasets.load_from_database()

    results = {
        "deepset/gbert-large": {1: [], 2: [], 3: [], 4: []},
        "deepset/gelectra-large": {1: [], 2: [], 3: [], 4: []},
        "deepset/gbert-base": {1: [], 2: [], 3: [], 4: []},
        "deepset/gelectra-base": {1: [], 2: [], 3: [], 4: []},
        "/data/experiments/dehio/germeval2021/experiments/models/d5d3bd2c2ec20360d4e3827411fdfe6e81a7aaf46dcd285c1a8892b4b8b42d63_gbert-large_fact": {
            1: [],
            2: [],
            3: [],
            4: [],
        },
        "/data/experiments/dehio/germeval2021/experiments/models/4f975e12f0255e5e185c4f41334c5284e64bea06d7da465bba3c8250da9f4c54_gelectra-large_fact": {
            1: [],
            2: [],
            3: [],
            4: [],
        },
    }
    for run in range(5):
        for i, (train_set, test_set) in enumerate(datasets.folds):
            for model_checkpoint in [
                "deepset/gbert-large",
                "deepset/gelectra-large",
                "deepset/gbert-base",
                "deepset/gelectra-base",
                "/data/experiments/dehio/germeval2021/experiments/models/d5d3bd2c2ec20360d4e3827411fdfe6e81a7aaf46dcd285c1a8892b4b8b42d63_gbert-large_fact",
                "/data/experiments/dehio/germeval2021/experiments/models/4f975e12f0255e5e185c4f41334c5284e64bea06d7da465bba3c8250da9f4c54_gelectra-large_fact",
                # 0.7668
            ]:
                try:
                    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
                except EnvironmentError:
                    # in case only model weights were saved
                    if "gbert-large" in model_checkpoint:
                        tokenizer = AutoTokenizer.from_pretrained("deepset/gbert-large")
                    else:
                        tokenizer = AutoTokenizer.from_pretrained(
                            "deepset/gelectra-large"
                        )

                preprocessor = Preprocessor(tokenizer, "claim_extraction")
                model = AutoModelForTokenClassification.from_pretrained(
                    model_checkpoint, num_labels=3, ignore_mismatched_sizes=True
                )
                model_name = model_checkpoint.split("/")[-1] + f"run-{run}"
                args = TrainingArguments(
                    f"/data/experiments/dehio/models/experiment1a-{model_name}",
                    evaluation_strategy=IntervalStrategy.EPOCH,
                    save_strategy=IntervalStrategy.EPOCH,
                    learning_rate=learning_rate,
                    per_device_train_batch_size=4,
                    per_device_eval_batch_size=4,
                    per_gpu_train_batch_size=1,
                    num_train_epochs=epochs,
                    weight_decay=0.01,
                    seed=run * 100,
                    save_total_limit=5,
                    load_best_model_at_end=True,
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
                trainer.save_model(
                    f"/data/experiments/dehio/models/experiment1a-{model_name}-best"
                )
                results[model_checkpoint][run].append(result)

    date = datetime.today().strftime("%d.%m.%y")
    path = f"/data/experiments/dehio/bachelor_thesis/results/experiment1a_{date}"
    os.mkdir(path)
    datasets.save_to_csv(f"{path}/dataset.csv")
    with open(f"{path}/results.txt", "w+") as file:
        for model_checkpoint, result_dict in results.items():
            runs = []
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
                runs.append(eval_k_fold(run_result))
                file.write(f"\nRun {run}")
                file.write(json.dumps(eval_k_fold(run_result), indent=2))
            file.write("\nResult over all runs")
            file.write(json.dumps(eval_k_fold(runs), indent=2))
