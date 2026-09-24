import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# 1. GENERAL UTILITIES
# ============================================================

def clean_question(question):
    """Clean and normalize generated questions."""

    if not question:
        return ""

    question = re.sub(r"\s+", " ", question)
    question = question.strip()

    if not question.endswith("?"):
        question += "?"

    return question


def normalize_text(text):
    """Normalize text for keyword matching."""

    if not text:
        return ""

    text = text.lower()

    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def contains_keyword(text, keyword):
    """Check whether a keyword exists in text."""

    text = normalize_text(text)
    keyword = normalize_text(keyword)

    return keyword in text


# ============================================================
# 2. JOB ROLE ANALYSIS
# ============================================================

ROLE_KEYWORDS = {

    "java developer": [
        "java",
        "oops",
        "object oriented programming",
        "collections",
        "exception handling",
        "multithreading",
        "jdbc",
        "spring",
        "spring boot",
        "hibernate"
    ],

    "python developer": [
        "python",
        "flask",
        "django",
        "fastapi",
        "oop",
        "rest api",
        "sql"
    ],

    "machine learning": [
        "python",
        "machine learning",
        "pandas",
        "numpy",
        "scikit-learn",
        "statistics",
        "data preprocessing",
        "model evaluation"
    ],

    "machine learning engineer": [
        "python",
        "machine learning",
        "pandas",
        "numpy",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "model deployment"
    ],

    "data scientist": [
        "python",
        "pandas",
        "numpy",
        "statistics",
        "machine learning",
        "sql",
        "data visualization"
    ],

    "frontend developer": [
        "html",
        "css",
        "javascript",
        "react",
        "typescript",
        "responsive design"
    ],

    "backend developer": [
        "python",
        "java",
        "node.js",
        "flask",
        "django",
        "express",
        "sql",
        "rest api",
        "database"
    ]
}


def detect_role_family(job_role):
    """Identify the closest known role family."""

    role = normalize_text(job_role)

    for role_name in ROLE_KEYWORDS:

        if role_name in role:
            return role_name

    if "java" in role:
        return "java developer"

    if "python" in role:
        return "python developer"

    if "machine learning" in role:
        return "machine learning"

    if "data" in role and "scientist" in role:
        return "data scientist"

    if "frontend" in role or "front end" in role:
        return "frontend developer"

    if "backend" in role or "back end" in role:
        return "backend developer"

    return "general"


# ============================================================
# 3. ROLE-BASED QUESTIONS
# ============================================================

def generate_role_questions(job_role, difficulty, skills):

    role = detect_role_family(job_role)

    resume_skills = [
        normalize_text(skill)
        for skill in skills
    ]

    questions = []

    # --------------------------------------------------------
    # JAVA DEVELOPER
    # --------------------------------------------------------

    if role == "java developer":

        questions.append(
            "What are the main object-oriented programming principles in Java?"
        )

        questions.append(
            "How would you choose between an interface and an abstract class in Java?"
        )

        if difficulty in ["Medium", "Hard"]:

            questions.append(
                "How does exception handling improve the reliability of a Java application?"
            )

            questions.append(
                "How would you select an appropriate Java collection for a given application requirement?"
            )

        if difficulty == "Hard":

            questions.append(
                "How would you design a Java application using object-oriented principles to keep the code maintainable?"
            )

        # Ask resume-related Java question only if Java exists
        # in the user's resume.

        if "java" in resume_skills:

            questions.append(
                "How have you applied Java concepts in your academic or project work?"
            )

    # --------------------------------------------------------
    # PYTHON DEVELOPER
    # --------------------------------------------------------

    elif role == "python developer":

        questions.append(
            "What Python features help you write maintainable application code?"
        )

        questions.append(
            "How would you structure a Python application into reusable modules?"
        )

        if difficulty in ["Medium", "Hard"]:

            questions.append(
                "How would you handle exceptions and validation in a Python backend application?"
            )

        if difficulty == "Hard":

            questions.append(
                "How would you improve the performance of a Python application when processing a large amount of data?"
            )

    # --------------------------------------------------------
    # MACHINE LEARNING
    # --------------------------------------------------------

    elif role in ["machine learning", "machine learning engineer"]:

        questions.append(
            "What steps would you follow to prepare a dataset before training a machine learning model?"
        )

        questions.append(
            "How would you decide which machine learning algorithm is suitable for a particular problem?"
        )

        if difficulty in ["Medium", "Hard"]:

            questions.append(
                "How would you identify and handle overfitting in a machine learning model?"
            )

        if difficulty == "Hard":

            questions.append(
                "How would you design a machine learning pipeline from data preprocessing to model evaluation?"
            )

    # --------------------------------------------------------
    # DATA SCIENTIST
    # --------------------------------------------------------

    elif role == "data scientist":

        questions.append(
            "How would you explore and understand a new dataset before building a model?"
        )

        questions.append(
            "How do you decide which features should be used in a data science model?"
        )

        if difficulty in ["Medium", "Hard"]:

            questions.append(
                "How would you handle missing values and outliers in a real-world dataset?"
            )

    # --------------------------------------------------------
    # FRONTEND
    # --------------------------------------------------------

    elif role == "frontend developer":

        questions.append(
            "How do HTML, CSS, and JavaScript work together in a web application?"
        )

        questions.append(
            "How would you design a responsive user interface for different screen sizes?"
        )

        if difficulty in ["Medium", "Hard"]:

            questions.append(
                "How does React component-based architecture help organize a frontend application?"
            )

    # --------------------------------------------------------
    # BACKEND
    # --------------------------------------------------------

    elif role == "backend developer":

        questions.append(
            "What are the main responsibilities of a backend application?"
        )

        questions.append(
            "How would you design a REST API for a web application?"
        )

        if difficulty in ["Medium", "Hard"]:

            questions.append(
                "How would you validate user input and handle errors in a backend API?"
            )

    # --------------------------------------------------------
    # GENERAL ROLE
    # --------------------------------------------------------

    else:

        questions.append(
            f"What technical skills are important for a {job_role}?"
        )

        questions.append(
            f"What responsibilities do you expect in a {job_role} role?"
        )

        if difficulty in ["Medium", "Hard"]:

            questions.append(
                f"How would you approach solving a technical problem as a {job_role}?"
            )

    return questions


# ============================================================
# 4. PROJECT-BASED QUESTIONS
# ============================================================

def generate_project_questions(context, job_role, difficulty):

    projects = context.get("projects", "")
    project_names = context.get("project_names", [])

    questions = []

    if not projects:
        return questions

    # Pick the first meaningful project name.
    project_name = None

    if project_names:
        project_name = project_names[0]

    if project_name:

        questions.append(
            f"Can you explain the main objective of your {project_name} project?"
        )

        questions.append(
            f"What was your specific contribution to the {project_name} project?"
        )

        if difficulty in ["Medium", "Hard"]:

            questions.append(
                f"What technical challenge did you face while developing {project_name}, and how did you solve it?"
            )

        if difficulty == "Hard":

            questions.append(
                f"If you had more time, how would you improve the {project_name} project?"
            )

    else:

        questions.append(
            "Can you explain one of the important projects mentioned in your resume?"
        )

        questions.append(
            "What was your contribution to that project?"
        )

    return questions


# ============================================================
# 5. SKILL-BASED QUESTIONS
# ============================================================

def generate_skill_questions(skills, job_role, difficulty):

    if not skills:
        return []

    role = detect_role_family(job_role)

    normalized_skills = []

    for skill in skills:

        skill_clean = skill.strip()

        if skill_clean and skill_clean not in normalized_skills:
            normalized_skills.append(skill_clean)

    # --------------------------------------------------------
    # Prioritize skills relevant to selected role
    # --------------------------------------------------------

    role_keywords = ROLE_KEYWORDS.get(role, [])

    prioritized = []
    remaining = []

    for skill in normalized_skills:

        skill_lower = normalize_text(skill)

        matched = False

        for keyword in role_keywords:

            if keyword in skill_lower or skill_lower in keyword:
                matched = True
                break

        if matched:
            prioritized.append(skill)
        else:
            remaining.append(skill)

    selected_skills = prioritized + remaining

    selected_skills = selected_skills[:5]

    questions = []

    for skill in selected_skills:

        if difficulty == "Easy":

            questions.append(
                f"What is the purpose of {skill}, and where is it commonly used?"
            )

        elif difficulty == "Medium":

            questions.append(
                f"How would you use {skill} to solve a practical software development problem?"
            )

        else:

            questions.append(
                f"What challenges can arise when using {skill}, and how would you handle them?"
            )

    return questions


# ============================================================
# 6. RESUME-BASED QUESTIONS
# ============================================================

def generate_resume_questions(context, job_role):

    questions = []

    summary = context.get("summary", "")
    education = context.get("education", "")
    certifications = context.get("certifications", "")
    experience = context.get("experience", "")

    if summary:

        questions.append(
            "Can you walk me through the key points of your professional profile?"
        )

    if education:

        questions.append(
            "How has your academic background prepared you for this role?"
        )

    if certifications:

        questions.append(
            "Which certification mentioned in your resume has been most useful to you, and why?"
        )

    if experience:

        questions.append(
            "What important technical experience did you gain from your previous work or internship?"
        )

    questions.append(
        f"Why are you interested in starting your career as a {job_role}?"
    )

    return questions


# ============================================================
# 7. HR / GENERAL QUESTIONS
# ============================================================

def generate_hr_questions(job_role):

    return [

        "Tell me about yourself.",

        f"Why are you interested in the {job_role} role?",

        "What are your strongest technical skills?",

        "What is one area you are currently working to improve?",

        "Why should a company consider you for this role?",

        "What are your career goals for the next few years?"
    ]


# ============================================================
# 8. SITUATIONAL QUESTIONS
# ============================================================

def generate_situational_questions(job_role):

    role = detect_role_family(job_role)

    questions = []

    if role == "java developer":

        questions.append(
            "Suppose your Java application suddenly becomes slow in production. How would you investigate the problem?"
        )

        questions.append(
            "Suppose you find a bug in code written by another developer. How would you approach fixing it?"
        )

    elif role in ["machine learning", "machine learning engineer"]:

        questions.append(
            "Suppose your machine learning model performs well on training data but poorly on new data. How would you investigate the problem?"
        )

        questions.append(
            "Suppose your dataset contains many missing values. How would you decide how to handle them?"
        )

    elif role == "python developer":

        questions.append(
            "Suppose your Python API starts receiving invalid input from users. How would you handle the situation?"
        )

    elif role == "frontend developer":

        questions.append(
            "Suppose your web page works on your laptop but looks incorrect on mobile devices. How would you debug it?"
        )

    else:

        questions.append(
            f"Suppose you are given a difficult technical problem as a {job_role}. How would you approach solving it?"
        )

    return questions


# ============================================================
# 9. SEMANTIC DUPLICATE REMOVAL
# ============================================================

def remove_similar_questions(question_objects, threshold=0.72):

    if len(question_objects) <= 1:
        return question_objects

    texts = [
        item["text"]
        for item in question_objects
    ]

    try:

        vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        matrix = vectorizer.fit_transform(texts)

        similarity_matrix = cosine_similarity(matrix)

    except Exception:

        return question_objects

    selected = []

    for i, question in enumerate(question_objects):

        duplicate = False

        for selected_index in selected:

            similarity = similarity_matrix[
                i,
                selected_index
            ]

            if similarity >= threshold:

                duplicate = True
                break

        if not duplicate:

            selected.append(i)

    return [
        question_objects[i]
        for i in selected
    ]


# ============================================================
# 10. CONTROLLED QUESTION MIXING
# ============================================================

def add_from_category(pool, category, result, used_texts):

    if not pool:
        return False

    for question in pool:

        cleaned = clean_question(question)

        normalized = normalize_text(cleaned)

        if normalized not in used_texts:

            result.append({
                "text": cleaned,
                "category": category
            })

            used_texts.add(normalized)

            return True

    return False


def build_mixed_questions(
    role_questions,
    project_questions,
    skill_questions,
    resume_questions,
    hr_questions,
    situational_questions,
    interview_type
):

    pools = {

        "role": role_questions,

        "project": project_questions,

        "skill": skill_questions,

        "resume": resume_questions,

        "hr": hr_questions,

        "situational": situational_questions
    }

    # --------------------------------------------------------
    # Controlled patterns
    # --------------------------------------------------------

    if interview_type == "Technical":

        pattern = [
            "role",
            "project",
            "skill",
            "hr",
            "role",
            "project",
            "resume",
            "role",
            "skill",
            "situational"
        ]

    elif interview_type == "HR":

        pattern = [
            "hr",
            "resume",
            "project",
            "hr",
            "role",
            "project",
            "resume",
            "hr",
            "situational",
            "hr"
        ]

    else:

        pattern = [
            "role",
            "project",
            "hr",
            "skill",
            "resume",
            "role",
            "project",
            "situational",
            "skill",
            "hr"
        ]

    result = []

    used_texts = set()

    # --------------------------------------------------------
    # First pass: follow controlled pattern
    # --------------------------------------------------------

    for category in pattern:

        if len(result) >= 10:
            break

        add_from_category(
            pools[category],
            category,
            result,
            used_texts
        )

    # --------------------------------------------------------
    # Second pass:
    # Fill missing positions from any available category
    # --------------------------------------------------------

    if len(result) < 10:

        for category in [
            "role",
            "project",
            "skill",
            "resume",
            "hr",
            "situational"
        ]:

            if len(result) >= 10:
                break

            while pools[category]:

                if not add_from_category(
                    pools[category],
                    category,
                    result,
                    used_texts
                ):
                    break

                if len(result) >= 10:
                    break

    return result[:10]


# ============================================================
# 11. MAIN QUESTION GENERATOR
# ============================================================

def generate_questions(
    resume_text,
    skills,
    job_role,
    difficulty,
    interview_type="Mixed"
):

    from nlp.resume_analyzer import build_resume_context

    # --------------------------------------------------------
    # Build structured resume context
    # --------------------------------------------------------

    context = build_resume_context(
        resume_text,
        skills
    )

    # --------------------------------------------------------
    # Generate category-wise question pools
    # --------------------------------------------------------

    role_questions = generate_role_questions(
        job_role,
        difficulty,
        skills
    )

    project_questions = generate_project_questions(
        context,
        job_role,
        difficulty
    )

    skill_questions = generate_skill_questions(
        skills,
        job_role,
        difficulty
    )

    resume_questions = generate_resume_questions(
        context,
        job_role
    )

    hr_questions = generate_hr_questions(
        job_role
    )

    situational_questions = generate_situational_questions(
        job_role
    )

    # --------------------------------------------------------
    # Combine everything for semantic duplicate detection
    # --------------------------------------------------------

    all_questions = []

    for category, questions in [

        ("role", role_questions),
        ("project", project_questions),
        ("skill", skill_questions),
        ("resume", resume_questions),
        ("hr", hr_questions),
        ("situational", situational_questions)

    ]:

        for question in questions:

            all_questions.append({
                "text": clean_question(question),
                "category": category
            })

    # --------------------------------------------------------
    # Remove semantically similar questions
    # --------------------------------------------------------

    unique_questions = remove_similar_questions(
        all_questions
    )

    # --------------------------------------------------------
    # Rebuild category pools after duplicate removal
    # --------------------------------------------------------

    filtered_pools = {

        "role": [],
        "project": [],
        "skill": [],
        "resume": [],
        "hr": [],
        "situational": []
    }

    for question in unique_questions:

        filtered_pools[
            question["category"]
        ].append(
            question["text"]
        )

    # --------------------------------------------------------
    # Controlled mixing
    # --------------------------------------------------------

    final_questions = build_mixed_questions(

        filtered_pools["role"],

        filtered_pools["project"],

        filtered_pools["skill"],

        filtered_pools["resume"],

        filtered_pools["hr"],

        filtered_pools["situational"],

        interview_type
    )

    # --------------------------------------------------------
    # Return only question text because the existing
    # interview_routes.py expects strings.
    # --------------------------------------------------------

    return [
        question["text"]
        for question in final_questions
    ]