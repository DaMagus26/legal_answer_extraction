import weaviate
from typing import List, Tuple, Any
from .abc.abstract_vector_db import AbstractVectorDB


class WeaviateDB(AbstractVectorDB):
    def __init__(self, url: str, api_key: str) -> None:
        auth_config = weaviate.AuthApiKey(api_key=api_key)
        self.__client = weaviate.Client(
            url=url,
            auth_client_secret=auth_config,
        )
        self.__class_name = 'LaborCodeCorpus'

    def find(self, vector: List[float]) -> List:
        if not self.__client.schema.exists(self.__class_name):
            raise RuntimeError(f'Class "{self.__class_name}"'
                               f' does not exist.')
        if not self.__client.is_ready():
            raise RuntimeError('Client is not ready')

        response = self.__client.query.get(self.__class_name, ['article_text'])\
            .with_near_vector({'vector': vector})\
            .with_additional(['id', 'certainty'])\
            .with_limit(5)\
            .do()

        return response['data']['Get'][self.__class_name]
        # return response

    def insert(self,
               vectors: Tuple[str, Any] | List[Tuple[str, Any]]
               ) -> None:
        pass
