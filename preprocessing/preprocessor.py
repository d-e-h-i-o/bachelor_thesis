from typing import List, Tuple, TypedDict

import numpy as np
from numpy.typing import NDArray

from preprocessing.datasets import LawMatchingSample

Offset = Tuple[int, int]
RawClaimExtractionDataset = NDArray[Tuple[str, List[Offset]]]
RawLawMatchingDataset = NDArray[LawMatchingSample]


class Input(TypedDict):
    input_ids: List[int]
    offset_mapping: List[Offset]
    labels: NDArray[int]


from torch.utils.data import Dataset


class CustomDataset(Dataset):
    def __init__(self, X: List[Input]):
        self.X = X

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx]


class Preprocessor:
    """
    Takes raw data from a *Datasets class, tokenizes is, and returns a torch Dataset.
    Usage:
        datasets = ClaimExtractionDatasets.from_database()
        preprocessor = Preprocessor(task='claim_extraction', tokenizer=AutoTokenizer.from_pretrained(checkpoint))
        inputs = preprocessor(datasets.X)
        output = model(**inputs[0])
    """

    def __init__(self, tokenizer, task: str):
        self.tokenizer = tokenizer
        self.task = task

    def preprocess_claim_extraction(
        self, X: RawClaimExtractionDataset
    ) -> CustomDataset:
        """
        Transforms a the raw data (text string with list of claim (start, end) tuples),
        tokenizes them, aligns the claim indexes with the tokenized text, and returns
        a torch Dataset.
        """
        samples = []
        sample_offsets = []
        for sample_text, claim_offsets in X:
            chunks = self.chunk_fulltext(sample_text, claim_offsets)
            for chunked_text, chunked_offsets in chunks:
                samples.append(chunked_text)
                sample_offsets.append(chunked_offsets)

        tokenized_inputs = self.tokenizer(
            samples, return_offsets_mapping=True, truncation=True
        )

        tokenized_inputs["labels"] = []
        for i in range(len(tokenized_inputs["input_ids"])):
            input_ids = tokenized_inputs["input_ids"][i]
            offset_mapping = tokenized_inputs["offset_mapping"][i]
            claim_offsets = sample_offsets[i]
            tokenized_inputs["labels"].append(
                self.align_claim_labels(input_ids, offset_mapping, claim_offsets),
            )
        return CustomDataset(tokenized_inputs)

    @staticmethod
    def chunk_fulltext(
        fulltext: str, claims: List[Offset]
    ) -> List[Tuple[str, List[Offset]]]:
        """Split article fulltext into smaller chunks (max. 512 tokens), with the condition that
        every claim is fully contained in one chunk."""
        length = 2500  # 2500 chars are a heuristic
        offset = 0
        chunks = []

        for i in range(0, len(fulltext), length):
            chunk_last = i + length
            chunk = fulltext[i - offset : chunk_last]
            chunk_claims = []

            next_offset = None
            for claim_start, claim_end in claims:
                if claim_start <= chunk_last <= claim_end:
                    # overlapping claim
                    next_offset = chunk_last - claim_start
                    chunk_last = claim_start
                    chunk = fulltext[i - offset : chunk_last]

            for claim_start, claim_end in claims:
                # add claims that are fully contained in chunk
                if claim_start >= (i - offset) and claim_end <= chunk_last:
                    # offsets have to be newly calculated for the chunk
                    claim = fulltext[claim_start:claim_end]
                    new_start: int = chunk.find(claim)
                    new_end: int = new_start + len(claim)
                    chunk_claims.append((new_start, new_end))

            offset = next_offset or 0
            chunks.append((chunk, chunk_claims))

        return chunks

    @staticmethod
    def align_claim_labels(
        input_ids: List[int],
        offset_mapping: List[Offset],
        claim_offsets: List[Offset],
    ) -> NDArray[int]:
        """Takes a list of input ids, offset mapping from the tokenizer, and (claim_start, claim_end) tuples,
        that mark the offset for the original text. Returns a list with labels in BIO schema for the tokenized text."""
        labels = np.zeros(len(input_ids))

        def get_offset(original_position: int) -> int:
            # Does not work if the original claim started or ended with a space, since those don't have an offset
            for index, (offset_start, offset_end) in enumerate(offset_mapping):
                if offset_end == 0:
                    # special token
                    continue
                if offset_start <= original_position < offset_end:
                    return index

        for claim_start, claim_end in claim_offsets:
            start = get_offset(claim_start)
            end = get_offset(claim_end - 1)
            labels[start] = 1
            labels[slice(start + 1, end + 1)] = 2

        return labels

    def preprocess_law_matching(self, X: RawLawMatchingDataset) -> CustomDataset:
        pass

    def __call__(self, data: NDArray) -> Dataset:
        if self.task == "claim_extraction":
            return self.preprocess_claim_extraction(data)
        if self.task == "law_matching":
            raise NotImplementedError
        else:
            raise NotImplementedError
