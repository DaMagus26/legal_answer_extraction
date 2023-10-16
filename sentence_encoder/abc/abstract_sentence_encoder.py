from abc import ABC
from typing import List


class AbstractSentenceEncoder(ABC):
    def encode(self, sentences: str | List[str]) -> List:
        raise NotImplementedError()
