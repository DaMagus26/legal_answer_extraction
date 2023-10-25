from abc import ABC, abstractmethod
from typing import List


class AbstractSentenceEncoder(ABC):
    @abstractmethod
    def encode(self, sentences: str | List[str]) -> List:
        raise NotImplementedError()
