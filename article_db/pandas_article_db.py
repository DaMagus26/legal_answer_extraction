import pandas as pd
from .abc.abstract_article_db import AbstractArticleDB
import os


class PandasArticleDB(AbstractArticleDB):
    def __init__(self, file_path: str):
        file_name = os.path.basename(file_path).split('.')[0]
        self.tables = {file_name: pd.read_csv(file_path, index_col='id')}

    def get_table(self, table_name: str) -> pd.DataFrame:
        return self.tables[table_name]
