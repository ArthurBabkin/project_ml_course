import joblib
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from ml_model.ml_model_constants import * # Импортируем из ml_model_constants.py

class CourseRecommender:
    def __init__(self):
        """
        Инициализация класса для рекомендаций курсов.
        """
        self.model = joblib.load(MODEL_PATH)  # Загрузка модели
        self.scaler = joblib.load(SCALER_PATH)  # Загрузка StandardScaler

        # Инициализация MultiLabelBinarizer
        self.mlb = MultiLabelBinarizer()
        self.mlb.fit([LABELS])

    def recommend_courses(self, input_data):
        """
        Рекомендует курсы на основе введённых данных.

        :param input_data: Список с входными данными.
        :return: Список рекомендованных курсов.
        """
        # Преобразование данных в numpy array и масштабирование
        scaled_input = self.scaler.transform(np.array(input_data).reshape(1, -1))

        # Предсказание
        prediction = self.model.predict(scaled_input)

        # Преобразование результата в метки
        recommended_courses = self.mlb.inverse_transform(prediction)

        return set(recommended_courses[0])

# # Инициализация
# recommender = CourseRecommender()
#
# # Ввод данных
# manual_input = [30, 29, 1, 1, 0, 0]
#
# # Получение рекомендаций
# recommended_courses = recommender.recommend_courses(manual_input)
# print("Рекомендованные курсы:", recommended_courses)