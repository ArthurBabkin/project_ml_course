import pandas as pd
import random
from synthetic_dataset_generation.dataset_constants import *

# Функция для рекомендации курсов с использованием относительных порогов и случайности
def recommend_courses(total_questions, total_correct, algebra_mistakes, geometry_mistakes, attention_mistakes,
                      formula_mistakes):
    recommendations = []
    total_mistakes = total_questions - total_correct  # Общее количество ошибок
    ratio_mistakes = total_mistakes / total_questions  # Отношение ошибок ко всем вопросам

    # Если пользователь решил 90% и более задач правильно
    if total_correct / total_questions >= ACCURACY_THRESHOLD:
        random_integer = random.randint(0, 1)
        if random_integer == 1:  # Иногда предлагаем продвинутые курсы
            random_integer = random.randint(0, 5)
            if random_integer == 1:
                recommendations.append(COURSES["advanced_algebra"])
            elif random_integer == 2:
                recommendations.append(COURSES["advanced_geometry"])
            elif random_integer == 3:
                recommendations.append(COURSES["advanced_geometry"])
                recommendations.append(COURSES["advanced_algebra"])
        return recommendations

    # Если есть ошибки, анализируем их распределение
    elif total_mistakes > 0:
        algebra_ratio = algebra_mistakes / total_mistakes  # Доля ошибок в алгебре
        geometry_ratio = geometry_mistakes / total_mistakes  # Доля ошибок в геометрии
        attention_ratio = attention_mistakes / total_mistakes  # Доля ошибок во внимательности
        formulas_ratio = formula_mistakes / total_mistakes  # Доля ошибок в формулах

        # Рекомендации для алгебры
        if algebra_ratio > RELATIVE_ALGEBRA_RATIO and ratio_mistakes > ALGORITHMIC_THRESHOLD:
            recommendations.append(COURSES["algebra"])
        elif 0.05 < algebra_ratio <= RELATIVE_ALGEBRA_RATIO and ratio_mistakes <= ALGORITHMIC_THRESHOLD:
            if random.randint(0, 1) == 1:  # Иногда добавляем продвинутый курс
                recommendations.append(COURSES["advanced_algebra"])

        # Рекомендации для геометрии
        if geometry_ratio > RELATIVE_GEOMETRY_RATIO:
            recommendations.append(COURSES["geometry"])
        elif 0.05 < geometry_ratio <= RELATIVE_GEOMETRY_RATIO:
            if random.randint(0, 1) == 1:
                recommendations.append(COURSES["advanced_geometry"])

        # Рекомендации для внимательности
        if attention_ratio > ATTENTION_RATIO_THRESHOLD:
            recommendations.append(COURSES["attention"])

        # Рекомендации для работы с формулами
        if formulas_ratio > FORMULAS_RATIO_THRESHOLD:
            recommendations.append(COURSES["general_math"])

    # Удаление дубликатов и возврат списка рекомендаций
    return list(set(recommendations))


# Генерация данных
data = []

for user_id in range(1, NUM_USERS + 1):  # Генерация данных для NUM_USERS пользователей
    # Генерация случайного числа вопросов
    total_questions = random.randint(*QUESTIONS_RANGE)

    # Генерация случайного количества правильных решений
    total_correct_solutions = random.randint(0, total_questions)

    # Генерация общего количества ошибок с некоторой вариацией
    random_float = random.uniform(*RANDOM_FLOAT_RANGE)
    total_mistakes = int(random_float * (total_questions - total_correct_solutions))

    # Темы для распределения ошибок
    themes = ["algebra", "geometry", "attention", "formulas"]
    random.shuffle(themes)  # Перемешиваем темы для случайного распределения

    # Распределяем ошибки по темам
    mistakes = {theme: 0 for theme in themes}
    remaining_mistakes = total_mistakes
    for theme in themes[:-1]:  # Распределяем ошибки по всем темам, кроме последней
        mistakes[theme] = random.randint(0, remaining_mistakes)
        remaining_mistakes -= mistakes[theme]
    mistakes[themes[-1]] = remaining_mistakes  # Остаток ошибок уходит в последнюю тему

    # Проверка корректности распределения ошибок
    assert sum(mistakes.values()) >= total_mistakes, "Сумма ошибок меньше общего количества ошибок!"

    # Генерация рекомендаций курсов
    course_recommend = recommend_courses(
        total_questions, total_correct_solutions,
        mistakes["algebra"], mistakes["geometry"],
        mistakes["attention"], mistakes["formulas"]
    )

    # Добавление данных пользователя в список
    data.append({
        "user_id": user_id,
        "total_questions": total_questions,
        "total_correct_solutions": total_correct_solutions,
        "number_algebra_mistakes": mistakes["algebra"],
        "number_trigonometry_mistakes": mistakes["geometry"],
        "number_reading_mistakes": mistakes["attention"],
        "number_working_with_formulas_mistakes": mistakes["formulas"],
        "course_recommend": ", ".join(course_recommend) if course_recommend else "Sleep and recover more. You are best!"
    })

# Создание DataFrame
df = pd.DataFrame(data)

# Сохранение данных в CSV
df.to_csv("synthetic_users_data.csv", index=False, encoding="utf-8")

print("Синтетический датасет успешно создан и сохранён в 'synthetic_users_data.csv'")
