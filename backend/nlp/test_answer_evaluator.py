from answer_evaluator import evaluate_answer


question = (
    "What is Python and how is it used "
    "in machine learning?"
)


answer = (
    "Python is a high-level programming language "
    "widely used in machine learning. "
    "Libraries such as NumPy, Pandas and "
    "scikit-learn are commonly used for "
    "data processing and machine learning."
)


result = evaluate_answer(
    question,
    answer
)


print("Answer Evaluation")
print("------------------")

print(
    "Relevance Score:",
    result["relevance_score"]
)

print(
    "Keyword Score:",
    result["keyword_score"]
)

print(
    "Semantic Score:",
    result["semantic_score"]
)

print(
    "Clarity Score:",
    result["clarity_score"]
)

print(
    "Overall Score:",
    result["overall_score"]
)

print(
    "Feedback:",
    result["feedback"]
)