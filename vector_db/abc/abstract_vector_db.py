from abc import ABC, abstractmethod
from typing import List, Tuple, Any


class AbstractVectorDB(ABC):
    @abstractmethod
    def insert(self,
               vectors: Tuple['str', Any] | List[Tuple['str', Any]]
               ) -> None:
        raise NotImplementedError()

    @abstractmethod
    def find(self, vector: List[float]) -> List:
        raise NotImplementedError()
