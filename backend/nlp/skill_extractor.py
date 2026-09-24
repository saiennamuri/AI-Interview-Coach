import spacy


# Load spaCy English model
nlp = spacy.load("en_core_web_sm")


# Technical skills
SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "c#",
    "javascript",
    "typescript",

    "html",
    "css",
    "react",
    "react.js",
    "node.js",
    "express",
    "flask",
    "django",

    "mysql",
    "sql",
    "mongodb",
    "postgresql",
    "oracle",

    "machine learning",
    "deep learning",
    "artificial intelligence",
    "nlp",
    "natural language processing",
    "computer vision",

    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",

    "git",
    "github",
    "docker",
    "linux",

    "aws",
    "azure",
    "google cloud"
]


def extract_skills(text):

    if not text:
        return []

    # Process text using spaCy
    doc = nlp(text.lower())

    # Get processed text
    processed_text = doc.text

    found_skills = []

    for skill in SKILLS:

        if skill.lower() in processed_text:

            if skill.lower() not in found_skills:

                found_skills.append(skill.lower())

    return found_skills
