from typing import Optional, Dict
import os
import json
import openai
from .abc.abstract_qa_model import AbstractQAModel
# https://api.proxyapi.ru/openai/v1
# sk-uJPlEJyqRg8jeYD1rSRxzV0DyXHzQtNb


class OpenAIModel(AbstractQAModel):
    def __init__(
            self,
            api_key: str,
            base_url: str,
    ) -> None:
        self.client = openai.OpenAI(
            base_url=base_url,
            api_key=api_key,
        )

    def __call__(
            self,
            query: str,
            context: Optional[str] = None
    ) -> Dict:
        with open('legal_answer_extraction/confs/config_qa.toml', 'r') as file:
            context = context or file.read()

        # Retrieve answer
        try:
            completion = self.client.chat.completions.create(
                model='gpt-4',
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": query},
                ]
            )

            response = completion.choices[0].message.content.replace('\n', '')
        except openai.OpenAIError as err:
            raise ConnectionError(f'OpenAI error') from err

        # Convert answer to JSON
        try:
            json_dict = json.loads(response)
        except json.JSONDecodeError as err:
            # raise RuntimeError(f'Could not decode json response: {response}') from err
            return json.loads('{"error": "JSONDecoderError", "text": "Произошла ошибка. Повторите запрос."}')

        # Invalidate response, if it's structure is not as expected
        if 'text' not in json_dict or 'sources' not in json_dict:
            return json.loads('{"error": "AnswerStructureError", "text": "Произошла ошибка. Повторите запрос."}')
        if not isinstance(json_dict['text'], str):
            return json.loads('{"error": "AnswerStructureError", "text": "Произошла ошибка. Повторите запрос."}')
        if not (isinstance(json_dict['sources'], list) and len(json_dict['sources']) >= 1):
            return json.loads('{"error": "AnswerStructureError", "text": "Произошла ошибка. Повторите запрос."}')
        for source in json_dict['sources']:
            if 'document_name' not in source or 'article_number' not in source:
                return json.loads('{"error": "AnswerStructureError", "text": "Произошла ошибка. Повторите запрос."}')
            if not (isinstance(source['document_name'], str) and isinstance(source['document_name'], str)):
                return json.loads('{"error": "AnswerStructureError", "text": "Произошла ошибка. Повторите запрос."}')

        # Invalidate answer, if it's sources are not as expected
        for source in json_dict['sources']:
            if 'кодекс' not in source['document_name'].lower():
                return json.loads('{"error": "InvalidSource", "text": "Извините, я не могу ответить найти ответ на этот вопрос"}')

        return json_dict
