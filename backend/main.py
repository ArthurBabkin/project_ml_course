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

with tab1:
    input_ml_model = [len(PRODUCTION_TASKS), 0, 0, 0, 0, 0]

    # Поля для ввода решений
    user_solutions = []
    for task in tasks:
        st.subheader(f"Условие задачи №{task['task_number']}")
        st.write(task["task_description"])
        solution = st.text_input(f"Ваше решение для задачи №{task['task_number']}", key=task["task_number"])
        user_solutions.append(solution)

    if st.button("🎯 Отослать задачи"):
        # Обрабатываем решения пользователя
        ai = ChatWithAI()

        # Запускаем асинхронные вызовы
        for i in range(len(user_solutions)):
            input_ml_model = asyncio.run(ai.check_solution(i, user_solutions[i], input_ml_model))

        # Получаем рекомендации от модели
        recommended_courses = recommender.recommend_courses(input_ml_model)

        # Отображаем результаты
        st.subheader("Результаты")
        if recommended_courses:
            recommended_courses_list = list(recommended_courses)  # Преобразуем set в список
            st.write(f"Рекомендованные курсы:")
            for i in recommended_courses_list:
                st.write(i)
        else:
            st.write("Нет рекомендаций.")

with tab2:
    # Отображение статистики
    st.metric(label="Количество задач", value=input_ml_model[1])
    st.metric(label="Ваш прогресс", value= f'{input_ml_model[1]} из {input_ml_model[0]}')
    st.write("Данные будут обновлены после отправки задач.")
