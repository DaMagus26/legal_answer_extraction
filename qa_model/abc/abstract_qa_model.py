from abc import ABC, abstractmethod
from typing import List, Dict


class AbstractQAModel(ABC):
    @abstractmethod
    def __call__(
            self,
            question: str | List[str],
            context: str | List[str]) -> Dict:
        raise NotImplementedError()