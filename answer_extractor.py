from vector_db.weaviate_db import WeaviateDB
from sentence_transformers import SentenceTransformer
from article_db.pandas_article_db import PandasArticleDB
from transformers import pipeline


class AnswerExtractor:
    def __init__(
            self,
            vector_db: WeaviateDB,
            article_db: PandasArticleDB,
            qa_model: SentenceTransformer,
            sequence_encoder
    ):
        self.vector_db = vector_db
        self.article_db = article_db
        self.qa_model = qa_model
        self.sequence_encoder = sequence_encoder

    def find(self, query):
        enc_query = self.sequence_encoder.encode(query).tolist()
        vdb_response = self.vector_db.find(enc_query)
        contexts = [item['article_text'] for item in vdb_response]

        contexts = [item['article_text'] for item in vdb_response]
        ids = [item['_additional']['id'] for item in vdb_response]

        article_table = self.article_db.get_table('labor_code')

        results = []
        for ctx_id, ctx in zip(ids, contexts):
            results.append((ctx_id, self.qa_model(question=query, context=ctx)))

        final_result = max(results, key=lambda x: x[1]['score'])
        response = {
            'part': article_table.loc[final_result[0], 'part'],
            'section': article_table.loc[final_result[0], 'section'],
            'chapter': article_table.loc[final_result[0], 'chapter'],
            'article': article_table.loc[final_result[0], 'article'],
            'article_text': article_table.loc[final_result[0], 'text'],
            'start': final_result[1]['start'],
            'end': final_result[1]['end'],
        }

        return response

