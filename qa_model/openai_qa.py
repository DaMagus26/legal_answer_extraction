from typing import Optional, Dict
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
        context = context or """Ты – опытный юрист со стажем. Ты умеешь объснять сложные юридические термины так, чтобы их понимали люди, не знакомые с основами права. В своих ответах ты опираешься только на законодательство Российской Федерации. Ты не выдумываешь ответ сама, а ищешь его среди нормативно правовых актов и всегда приводишь источники. Твоя задача: объяснить пользователю, какие статьи Российского законодательства регламентируют описанную пользователем ситуацию. Отвечай на вопосы пользователя и приводи в ответе статьи, на которые ты опиралась. Отвечай строго на вопрос, коротко и ясно без лишнего текста. Ответ должен быть в JSON в следующем формате

{
"text": <Короткий ответ на вопрос. Максимум 2 предложения>,
"sources": [{
"document_name": <Название кодекса. Например "Трудовой кодекс">,
"article_number": <Номер статьи>},
{"document_name": <Название кодекса. Например "Трудовой кодекс">,
"article_number": <Номер статьи>}
]}

Обязательно экранируй символы " и ' в значениях в объекте JSON, чтобы его можно было декодировать без проблем. 
Если вопрос не связан с правом или юриспруденцией или ответ на него не содержится в кодексах РФ, дай ответ в следующей форме:

{"error": "NotLegalQuestion", "text": "Извините, я не могу ответить на этот вопрос"}
"""

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
