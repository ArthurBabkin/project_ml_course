import sys
import os
import streamlit as st
import asyncio

# Добавляем корневую директорию проекта в sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

from ml_model.ml_test import CourseRecommender
from llm_model.llm_model_main import *

# Инициализация модели рекомендаций
recommender = CourseRecommender()

# Список задач
tasks = PRODUCTION_TASKS

# Заголовок приложения
st.title("🎓 Реши задачи и получи рекомендации по курсам")

# Вкладки
tab1, tab2 = st.tabs(["📘 Решение задач", "📊 Результаты"])

# Для хранения информации об ошибках
mistake_messages = {}

with tab1:
    input_ml_model = [len(PRODUCTION_TASKS), 0, 0, 0, 0, 0]

    # Поля для ввода решений
    user_solutions = []
    task_containers = []  # Список контейнеров для каждой задачи
    for task in tasks:
        container = st.container()  # Создаем контейнер для каждой задачи
        with container:
            st.subheader(f"Условие задачи №{task['task_number']}")
            st.write(task["task_description"])
            solution = st.text_input(f"Ваше решение для задачи №{task['task_number']}", key=task["task_number"])
        user_solutions.append(solution)
        task_containers.append(container)  # Добавляем контейнер в список

    if st.button("🎯 Отослать задачи"):
        # Запускаем асинхронные вызовы для проверок решений пользователя
        ai = ChatWithAI()
        for i in range(len(user_solutions)):
            mistakes_in_number, input_ml_model = asyncio.run(ai.check_solution(i, user_solutions[i], input_ml_model))

            # Отображаем ошибки в контейнере соответствующей задачи
            with task_containers[i]:
                if mistakes_in_number is None:
                    st.write("✅ Ты не допустил ошибок в этой задаче.")
                elif mistakes_in_number:
                    st.write("❌ Ты допустил ошибки:")
                    for mistake in mistakes_in_number:
                        st.write(f"- {mistake}")

        # Получаем рекомендации от модели
        recommended_courses = recommender.recommend_courses(input_ml_model)

        st.subheader("Результаты")

        st.write(f"Ты решил правильно {input_ml_model[1]} из {input_ml_model[0]} задач.")
        if recommended_courses:
            recommended_courses_list = list(recommended_courses)  # Преобразуем set в список
            st.write("📚 Рекомендованные курсы:")
            for course in recommended_courses_list:
                st.write(f"- {course}")
        else:
            st.write("Нет рекомендаций.")

with tab2:
    # Отображение статистики
    st.metric(label="Количество задач", value=input_ml_model[0])
    st.metric(label="Ваш прогресс", value=f"{input_ml_model[1]} из {input_ml_model[0]}")
    st.write("Данные будут обновлены после отправки задач.")
