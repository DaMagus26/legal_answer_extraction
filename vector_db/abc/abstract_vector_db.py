from abc import ABC
from typing import List, Tuple, Any


class AbstractVectorDB(ABC):
    def insert(self,
               vectors: Tuple['str', Any] | List[Tuple['str', Any]]
               ) -> None:
        raise NotImplementedError()

    def find(self, vector: List[float]) -> List:
        raise NotImplementedError()
