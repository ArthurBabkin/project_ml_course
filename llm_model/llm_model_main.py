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
                 "content": f'Условие задачи: {task_description}\n Правильное решение: {correct_solution}\n Моё решение: {message}'}
            ]

            response = await self.model.chat.completions.create(
                model=MODEL,
                messages=messages,
                stream=False,
                temperature=CHAT_TEMPERATURE,
            )

            print('chlen')
            print(response.choices[0].message.content)

            if response.choices[0].message.content == 'None' or response.choices[0].message.content == None or response.choices[0].message.content == 'none':
                input_ml_model[1] += 1
                return input_ml_model
            else:
                mistakes = response.choices[0].message.content.split(' ')
                for i in mistakes:
                    if int(i) <= 4 and int(i) >= 1:
                        input_ml_model[int(i)+1] += 1
                return input_ml_model
        else:
            return input_ml_model

# async def main():
#     """
#     Главная функция для ДЕМОНСТРАЦИИ взаимодействия с классом ChatWithAI.
#     Симулирует простой разговор с AI.
#     """
#     ai = ChatWithAI()
#
#     print(PRODUCTION_TASKS[0])
#
#     response = await ai.check_solution(0, "Сложим два уравнения: \( (x + y) + (x - y) = 10 + 2 \), \( 2x = 12 \), \( x = 6 \). Подставим \( x = 6 \) в первое уравнение: \( 6 + y = 10 \), \( y = -4 \). Итог: \( x = 6, y = -4 \).", [len(PRODUCTION_TASKS), 0, 0, 0, 0, 0])
#     print(response)
#
# if __name__ == "__main__":
#     asyncio.run(main())