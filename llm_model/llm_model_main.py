import os
import dotenv
import asyncio
from openai import AsyncAzureOpenAI

from llm_model.llm_constants import *

class ChatWithAI:
    def __init__(self):
        # Загружаем переменные окружения из файла .env
        dotenv.load_dotenv()

        self.model = AsyncAzureOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_version=os.environ["AZURE_OPENAI_API_VERSION"],
            azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"]
        )

    async def check_solution(self, task_number: 0, message: str, input_ml_model: []):
        """
        Функция для чата с моделью gpt 4-o mini.
        Получает список объектов сообщений в модель ИИ и возвращает содержимое ответа ИИ.

        :param messages: Историю переписки в виде списка объектов dict, где каждый объект содержит 'role' и 'content'
        :return: Содержимое ответа модели в виде строки
        """
        if 0 <= task_number < len(PRODUCTION_TASKS):
            task_description = PRODUCTION_TASKS[task_number]['task_description']
            correct_solution = PRODUCTION_TASKS[task_number]['correct_solution']
            messages = [
                {"role": "system", "content": CHECK_SOLUTION_PROMPT},
                {"role": "user",
                 "content": f'Task description: {task_description}\n Correct solution: {correct_solution}\n My solution (YOU need to check my solution): {message}'}
            ]

            response = await self.model.chat.completions.create(
                model=MODEL,
                messages=messages,
                stream=False,
                temperature=CHAT_TEMPERATURE,
            )

            if response.choices[0].message.content == 'None' or response.choices[0].message.content == None or response.choices[0].message.content == 'none':
                input_ml_model[1] += 1
                return None, input_ml_model
            else:
                mistakes = response.choices[0].message.content.split(' ')
                mistakes_description = []
                for i in mistakes:
                    if int(i) <= 4 and int(i) >= 1:
                        input_ml_model[int(i)+1] += 1
                        mistakes_description.append(MISTAKES_CATEGORIES[int(i)])
                return mistakes_description, input_ml_model
        else:
            return None, input_ml_model
