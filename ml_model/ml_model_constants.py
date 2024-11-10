import os

# Базовая директория проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Относительный путь к файлу модели
MODEL_PATH = os.path.join(BASE_DIR, "ml_model", "best_model.pkl")

# Относительный путь к файлу StandardScaler
SCALER_PATH = os.path.join(BASE_DIR, "ml_model", "scaler.pkl")

# Список меток, использованных при обучении
LABELS = [
    "Курс по улучшению внимательности",
    "Курс по тригонометрии",
    "Курс по олимпиадной геометрии",
    "Курс по олимпиадной алгебре",
    "Курс по логическому мышлению и математике для начинающих",
    "Курс по алгебре",
    "Sleep and recover more. You are best!"
]
