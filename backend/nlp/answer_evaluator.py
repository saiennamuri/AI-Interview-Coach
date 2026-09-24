import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sentence_transformers import SentenceTransformer


# Load semantic similarity model
model = SentenceTransformer("all-MiniLM-L6-v2")


def clean_text(text):

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        "",
        text
    )

    return text


def calculate_keyword_score(question, answer):

    question_words = set(
        clean_text(question).split()
    )

    answer_words = set(
        clean_text(answer).split()
    )

    if not question_words:

        return 0.0

    matched_words = (
        question_words.intersection(answer_words)
    )

    score = (
        len(matched_words)
        / len(question_words)
    ) * 100

    return round(score, 2)


def calculate_relevance_score(question, answer):

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        [
            clean_text(question),
            clean_text(answer)
        ]
    )

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(
        float(similarity * 100),
        2
    )


def calculate_semantic_score(question, answer):

    embeddings = model.encode(
        [
            question,
            answer
        ]
    )

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return round(
        float(similarity * 100),
        2
    )


def calculate_clarity_score(answer):

    words = answer.split()

    if not words:

        return 0.0

    word_count = len(words)

    sentences = re.split(
        r"[.!?]+",
        answer
    )

    sentences = [
        sentence
        for sentence in sentences
        if sentence.strip()
    ]

    sentence_count = len(sentences)

    if sentence_count == 0:

        sentence_count = 1

    average_sentence_length = (
        word_count / sentence_count
    )

    # Reasonable interview answer length
    if 8 <= average_sentence_length <= 25:

        score = 100

    elif 5 <= average_sentence_length < 8:

        score = 75

    elif 25 < average_sentence_length <= 35:

        score = 75

    elif average_sentence_length < 5:

        score = 50

    else:

        score = 50

    return float(score)


def calculate_overall_score(
    relevance_score,
    keyword_score,
    semantic_score,
    clarity_score
):

    overall_score = (
        float(relevance_score)* 0.25
        + float(keyword_score )* 0.20
        + float(semantic_score)* 0.40
        + float(clarity_score) * 0.15
    )

    return round(
        float(overall_score),
        2
    )


def generate_feedback(
    overall_score
):

    if overall_score >= 85:

        return (
            "Excellent answer. "
            "The answer is relevant, clear and "
            "shows strong understanding."
        )

    elif overall_score >= 70:

        return (
            "Good answer. "
            "The answer is mostly relevant, "
            "but there is some room for improvement."
        )

    elif overall_score >= 50:

        return (
            "Average answer. "
            "Try to provide more relevant keywords "
            "and explain the concept more clearly."
        )

    else:

        return (
            "Needs improvement. "
            "Try to directly answer the question "
            "and include important technical concepts."
        )


def evaluate_answer(question, answer):

    relevance_score = calculate_relevance_score(
        question,
        answer
    )

    keyword_score = calculate_keyword_score(
        question,
        answer
    )

    semantic_score = calculate_semantic_score(
        question,
        answer
    )

    clarity_score = calculate_clarity_score(
        answer
    )

    overall_score = calculate_overall_score(
        relevance_score,
        keyword_score,
        semantic_score,
        clarity_score
    )

    feedback = generate_feedback(
        overall_score
    )

    return {
        "relevance_score": relevance_score,
        "keyword_score": keyword_score,
        "semantic_score": semantic_score,
        "clarity_score": clarity_score,
        "overall_score": overall_score,
        "feedback": feedback
    }