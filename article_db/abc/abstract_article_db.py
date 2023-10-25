from abc import ABC, abstractmethod
import pandas as pd


class AbstractArticleDB(ABC):
    @abstractmethod
    def get_table(self, table_name: str) -> pd.DataFrame:
        raise NotImplementedError()