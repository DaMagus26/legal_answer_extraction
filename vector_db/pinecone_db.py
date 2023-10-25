import pinecone
from .abc.abstract_vector_db import AbstractVectorDB
from typing import List, Tuple, Any
from tqdm.auto import trange


class PineconeDB(AbstractVectorDB):
    def __init__(
            self,
            api_key: str,
            environment: str,
            index_name: str) -> None:

        # self._init_pinecone(api_key, environment)
        self.index = pinecone.Index(index_name)

    @staticmethod
    def _init_pinecone(api_key: str, environment: str):
        pinecone.init(api_key=api_key, environment=environment)

    def insert(
            self,
            vectors: Tuple['str', Any] | List[Tuple['str', Any]],
            batch_size: int = 50,
            progress_bar: bool = False
            ) -> None:
        rng = trange(0, len(vectors), batch_size) if progress_bar else \
            range(0, len(vectors), batch_size)

        for i in rng:
            i_end = i + 50
            if i_end > len(vectors):
                i_end = len(vectors)
            self.index.upsert(vectors=vectors[i:i_end])

    def find(self, vector: List[float], top_k=1) -> List:
        return self.index.query(vector, top_k=top_k)['matches']
