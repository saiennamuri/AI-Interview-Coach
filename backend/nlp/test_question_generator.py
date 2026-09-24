from question_generator import generate_questions


skills = [
    "python",
    "sql",
    "flask",
    "machine learning"
]

job_role = "Python Developer"

difficulty = "Medium"


questions = generate_questions(
    skills,
    job_role,
    difficulty
)


print("Generated Interview Questions:")
print("--------------------------------")

for i, question in enumerate(questions, start=1):

    print(f"{i}. {question}")