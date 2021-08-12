from transformers import (
    AutoModelForTokenClassification,
    TrainingArguments,
    Trainer,
    AutoTokenizer,
)
from preprocessing import Preprocessor
from preprocessing.datasets_ import ClaimExtractionDatasets

from utils import eval_k_fold, compute_metrics

model_checkpoint = "deepset/gbert-large"
model_name = model_checkpoint.split("/")[-1]
args = TrainingArguments(
    f"/data/experiments/dehio/models/test-claim-extraction",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    per_gpu_train_batch_size=1,
    num_train_epochs=30,
    weight_decay=0.01,
)


def train():
    datasets = ClaimExtractionDatasets.load_from_database()
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
    preprocessor = Preprocessor(tokenizer, "claim_extraction")
    results = []

    for i, (train_split, test_split) in enumerate(datasets.folds):
        model = AutoModelForTokenClassification.from_pretrained(
            model_checkpoint, num_labels=3
        )
        train_dataset = preprocessor(datasets.X[train_split])
        test_dataset = preprocessor(datasets.X[test_split])
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


if __name__ == "__main__":
    train()
