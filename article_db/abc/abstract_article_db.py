import abc
from abc import ABC
import pandas as pd


class AbstractArticleDB(ABC):
    @abc.abstractmethod
    def get_table(self, table_name: str) -> pd.DataFrame:
        raise NotImplementedError()