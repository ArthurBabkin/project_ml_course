MODEL = "gpt-4o"
CHAT_TEMPERATURE = 1.1
CHECK_SOLUTION_PROMPT = (
    "You will be provided with a "
    "mathematical problem, correct solution of this problem, "
    "and my solution. Please check if my solution is correct "
    "by comparing it to the correct one. Please note that "
    "my solution might be different from the correct one "
    "but it does not mean that my solution is incorrect. "
    "Your role is to classify the mistakes of 'user' in their solution as given type of mistakes. "
    "Type of mistakes: [{'1': 'Algebra'}, {'2': 'Trigonometry'}, {'3': 'Reading conditions'}, {'4': 'Working with formulas'}]. "
    "If the mistakes from 'user' perfectly match with one of the descriptions, respond with that number (without apostrophes or any other symbols). "
    "If the mistakes from 'user' perfectly match with a few of the descriptions, respond with those numbers with one space between each two numbers (without apostrophes or any other symbols). "
    "If the dialogue does not perfectly match any of the descriptions (even if it is really close, but not exact), respond with 'none' (without apostrophes). "
    "If the solutions at all are not about the task or 'user' wrote something not relevant, so it is ALL Cases together, so you should write '1 2 3 4'. "
    "If 'user' say that he does not know how to solve and wrote almost NOTHING, so it is ALL cases together, so you should write '1 2 3 4'. "
    "Remember that you answer 'none' ONLY if you are sure that the solution is fully correct, revise the solution of user step by step. "
    "Do not confuse mistakes in reading conditions and algebra, if the user did not understand the condition correctly or rewrote it not correctly, then this is an mistake in reading the conditions, and if he did not calculate correctly during the solution process, then this is an algebraic error."
    "Remember that solutions from 'user' come from responses from 'user'."
    "Remember that user can provide short solutions without explanations, in such cases you look at the semantic of solution and final answer."

    "\n\nExamples:"
    "\n\nExample 1:"
    "\nProblem: Solve the equation x + y = 10, x - y = 2."
    "\nCorrect solution: Add the two equations: (x + y) + (x - y) = 10 + 2. This simplifies to 2x = 12, so x = 6. Substitute x = 6 into the first equation: 6 + y = 10, so y = 4. Final answer: x = 6, y = 4."
    "\nUser solution: x = 7, y = 3. Final answer: x = 7, y = 3."
    "\nClassification: 1"

    "\n\nExample 2:"
    "\nProblem: Find sin(2α) if cos(α) = 0.6 and π < α < 2π."
    "\nCorrect solution: Use the formula sin²(α) + cos²(α) = 1 to find sin(α). sin²(α) = 1 - cos²(α) = 1 - 0.36 = 0.64, so sin(α) = -√0.64 = -0.8 (since π < α < 2π, sin(α) is negative). Then use sin(2α) = 2sin(α)cos(α): sin(2α) = 2(-0.8)(0.6) = -0.96. Final answer: sin(2α) = -0.96."
    "\nUser solution: I don't know how to solve this."
    "\nClassification: 1 2 3 4"

    "\n\nExample 3:"
    "\nProblem: A farmer has 100 kg of grain. He used 20% for seeding, sold 30% of the remaining grain, and gave the rest to animals. How much grain did he give to the animals?"
    "\nCorrect solution: First, find how much grain was used for seeding: 20% of 100 kg = 20 kg. Remaining grain: 100 - 20 = 80 kg. Then calculate 30% of the remaining grain: 30% of 80 = 24 kg. Grain left after selling: 80 - 24 = 56 kg. Final answer: 56 kg."
    "\nUser solution: The farmer gave 60 kg to the animals."
    "\nClassification: 3"

    "\n\nExample 4:"
    "\nProblem: Решите систему уравнений: x + y = 10, x - y = 2."
    "\nCorrect solution: Add the two equations: (x + y) + (x - y) = 10 + 2. This simplifies to 2x = 12, so x = 6. Substitute x = 6 into the first equation: 6 + y = 10, so y = 4. Final answer: x = 6, y = 4."
    "\nUser solution: 321."
    "\nClassification: 1 2 3 4"
)

# Словарь для типов ошибок
MISTAKES_CATEGORIES = {
    1: "Алгебра",
    2: "Геометрия/тригонометрия",
    3: "Внимательность/чтение условий",
    4: "Работа с математическими формулами"
}

# Словарь с задачами на сайте/проде
# Словарь с задачами
PRODUCTION_TASKS = [
    {
        "task_number": 1,
        "task_description": r"Сколько будет 2 + 2?",
        "correct_solution": r"Ответ прост: \( 2 + 2 = 4 \).",
    },
    {
        "task_number": 2,
        "task_description": r"Если у Вас есть 3 яблока и Вы купили ещё 5, сколько яблок у Вас теперь?",
        "correct_solution": r"Ответ: \( 3 + 5 = 8 \). У Вас 8 яблок.",
    },
    {
        "task_number": 3,
        "task_description": r"Решите систему уравнений: x + y = 10, x - y = 2",
        "correct_solution": (
            r"1 способ) Сложим два уравнения: \( (x + y) + (x - y) = 10 + 2 \), "
            r"\( 2x = 12 \), \( x = 6 \). Подставим \( x = 6 \) в первое уравнение: "
            r"\( 6 + y = 10 \), \( y = 4 \). Итог: \( x = 6, y = 4 \)."
            "2 способ) x = 2+y => 2*y = 8, y = 4 и x = 6"
        ),
    },
    {
        "task_number": 4,
        "task_description": r"Найдите значение sin(2α), если дано что cos(α) = 0.6 и π < α < 2π.",
        "correct_solution": (
            r"Используем формулы: \( \sin^2 \alpha + \cos^2 \alpha = 1 \), чтобы найти \( \sin \alpha \). "
            r"\( \sin \alpha = -\sqrt{1 - (0,6)^2} = -0,8 \) (так как угол в интервале \( \pi < \alpha < 2\pi \), "
            r"синус отрицателен). Затем по формуле \( \sin 2\alpha = 2 \sin \alpha \cos \alpha \): "
            r"\( \sin 2\alpha = 2 \cdot (-0,8) \cdot 0,6 = -0,96 \). Итог: \( \sin 2\alpha = -0,96 \)."
        ),
    },
    {
        "task_number": 5,
        "task_description": (
            r"У фермера было 100 кг зерна. 20% он использовал для посева, 30% от остатка продал, "
            r"а оставшуюся часть раздал на корм животным. Сколько килограммов зерна он отдал на корм животным?"
        ),
        "correct_solution": (
            r"Сначала найдём, сколько зерна фермер использовал для посева: \( 20\% \) от 100 кг = "
            r"\( 100 \times 0,2 = 20 \) кг. Остаётся \( 100 - 20 = 80 \) кг. Далее он продал \( 30\% \) от оставшихся "
            r"80 кг: \( 80 \times 0,3 = 24 \) кг. После продажи осталось \( 80 - 24 = 56 \) кг. Всё, что осталось, "
            r"фермер отдал на корм животным. Итог: 56 кг."
        ),
    },
]
