import pandas as pd
from .abc.abstract_article_db import AbstractArticleDB
from typing import Dict


class PandasArticleDB(AbstractArticleDB):
    def __init__(self, contents: Dict['str', pd.DataFrame]):
        self.tables = contents

    def get_table(self, table_name: str) -> pd.DataFrame:
        return self.tables[table_name]
