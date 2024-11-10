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
    "If 'user' is saying that he does not know how to do, so it is ALL Cases together, so you should write '1 2 3 4'. "
    "REMEMBER that you answer 'none' ONLY if you are sure that the solution is fully correct, revise the solution of user step by step. "
    "Remember that solutions from 'user' come from responses from 'user'."

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

PRODUCTION_TASKS = [
    {
        "task_number": 1,
        "task_description": (
            "Решите систему уравнений: x + y = 10, x - y = 2"
        ),
        "correct_solution": (
            "Сложим два уравнения: \( (x + y) + (x - y) = 10 + 2 \), "
            "\( 2x = 12 \), \( x = 6 \). Подставим \( x = 6 \) в первое уравнение: "
            "\( 6 + y = 10 \), \( y = 4 \). Итог: \( x = 6, y = 4 \)."
        ),
    },
    {
        "task_number": 2,
        "task_description": (
            "Найдите значение sin(2α), если дано что cos(α) = 0.6 и π < α < 2π."
        ),
        "correct_solution": (
            "Используем формулы: \( \sin^2 \alpha + \cos^2 \alpha = 1 \), чтобы найти \( \sin \alpha \). "
            "\( \sin \alpha = -\sqrt{1 - (0,6)^2} = -0,8 \) (так как угол в интервале \( \pi < \alpha < 2\pi \), "
            "синус отрицателен). Затем по формуле \( \sin 2\alpha = 2 \sin \alpha \cos \alpha \): "
            "\( \sin 2\alpha = 2 \cdot (-0,8) \cdot 0,6 = -0,96 \). Итог: \( \sin 2\alpha = -0,96 \)."
        ),
    },
    {
        "task_number": 3,
        "task_description": (
            "У фермера было 100 кг зерна. 20% он использовал для посева, 30% от остатка продал, "
            "а оставшуюся часть раздал на корм животным. Сколько килограммов зерна он отдал на корм животным?"
        ),
        "correct_solution": (
            "Сначала найдём, сколько зерна фермер использовал для посева: \( 20\% \) от 100 кг = "
            "\( 100 \times 0,2 = 20 \) кг. Остаётся \( 100 - 20 = 80 \) кг. Далее он продал \( 30\% \) от оставшихся "
            "80 кг: \( 80 \times 0,3 = 24 \) кг. После продажи осталось \( 80 - 24 = 56 \) кг. Всё, что осталось, "
            "фермер отдал на корм животным. Итог: 56 кг."
        ),
    },
]
