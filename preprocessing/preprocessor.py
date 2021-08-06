from typing import List, Tuple, TypedDict

import numpy as np
from numpy.typing import NDArray

Offset = Tuple[int, int]


class Input(TypedDict):
    input_ids: List[int]
    offset_mapping: List[Offset]
    labels: NDArray[int]


class Preprocessor:
    """
    Usage:
        dataset = ClaimExtractionDataset.from_database()
        preprocessor = Preprocessor(task='claim_extraction', tokenizer=AutoTokenizer.from_pretrained(checkpoint))
        input = preprocessor(dataset)
        output = model(**input)
    """

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def preprocess_claim_extraction(self, X) -> List[Input]:
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

        for i in range(len(tokenized_inputs)):
            input_ids = tokenized_inputs[i]["input_ids"]
            offset_mapping = tokenized_inputs[i]["offset_mappings"]
            claim_offsets = sample_offsets[i]
            tokenized_inputs[i]["labels"] = self.align_claim_labels(
                input_ids, offset_mapping, claim_offsets
            )
        return tokenized_inputs

    def chunk_fulltext(
        self, fulltext: str, claims: List[Offset]
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
                    chunk_claims.append((claim_start, claim_end))

            offset = next_offset or 0
            chunks.append((chunk, chunk_claims))

        return chunks

    def align_claim_labels(
        self,
        input_ids: List[int],
        offset_mappings: List[Offset],
        claim_offsets: List[Offset],
    ) -> NDArray[int]:
        """Takes a list of input ids, offset mapping from the tokenizer, and (claim_start, claim_end) tuples,
        that mark the offset for the original text. Returns a list with labels in BIO schema for the tokenized text."""
        labels = np.zeros(len(input_ids))

        def get_offset(original_position: int) -> int:
            for index, (offset_start, offset_end) in enumerate(offset_mappings):
                if offset_end == 0:
                    # special token
                    continue
                if offset_start <= original_position < offset_end:
                    return index

        for claim_start, claim_end in claim_offsets:
            start = get_offset(claim_start)
            end = get_offset(claim_end - 1)
            labels[start] = 1
            labels[range(start + 1, end + 1)] = 2

        return labels

    def __call__(self, dataset):
        if dataset.TASK == "claim_extraction":
            return self.preprocess_claim_extraction(dataset)
        if dataset.TASK == "law_matching":
            raise NotImplementedError
