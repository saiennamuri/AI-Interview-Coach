import re


def clean_text(text):
    """
    Clean resume text by removing
    unnecessary spaces and blank lines.
    """

    if not text:
        return ""

    text = text.replace("\r", "\n")

    # Remove multiple spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n+", "\n", text)

    return text.strip()


def extract_section(text, section_names):
    """
    Extract content belonging to a resume section.
    """

    if not text:
        return ""

    lines = text.split("\n")

    start_index = -1

    # Find section heading
    for i, line in enumerate(lines):

        cleaned_line = line.strip().lower()

        for section in section_names:

            if cleaned_line == section.lower():
                start_index = i + 1
                break

        if start_index != -1:
            break

    if start_index == -1:
        return ""

    section_content = []

    # Common resume section headings
    all_sections = [
        "skills",
        "technical skills",
        "projects",
        "project",
        "experience",
        "work experience",
        "education",
        "certifications",
        "certificates",
        "achievements",
        "internship",
        "internships",
        "summary",
        "profile",
        "objective"
    ]

    for line in lines[start_index:]:

        cleaned_line = line.strip().lower()

        is_next_section = False

        for section in all_sections:

            if cleaned_line == section.lower():
                is_next_section = True
                break

        if is_next_section:
            break

        if line.strip():
            section_content.append(line.strip())

    return "\n".join(section_content).strip()


def extract_projects(text):
    """
    Extract project-related information from resume.
    """

    return extract_section(
        text,
        [
            "projects",
            "project",
            "academic projects",
            "personal projects"
        ]
    )


def extract_experience(text):
    """
    Extract work experience or internship information.
    """

    return extract_section(
        text,
        [
            "experience",
            "work experience",
            "professional experience",
            "internship",
            "internships"
        ]
    )


def extract_education(text):
    """
    Extract education information.
    """

    return extract_section(
        text,
        [
            "education",
            "academic background",
            "qualification",
            "qualifications"
        ]
    )


def extract_certifications(text):
    """
    Extract certification information.
    """

    return extract_section(
        text,
        [
            "certifications",
            "certificates",
            "certification"
        ]
    )


def extract_summary(text):
    """
    Extract resume summary/objective.
    """

    return extract_section(
        text,
        [
            "summary",
            "profile",
            "objective",
            "career objective"
        ]
    )


def extract_project_names(project_text):
    """
    Try to identify project names from project section.
    """

    if not project_text:
        return []

    lines = project_text.split("\n")

    project_names = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Ignore very long description lines
        if len(line) > 100:
            continue

        # Ignore common technology/description lines
        lower_line = line.lower()

        if any(
            keyword in lower_line
            for keyword in [
                "technology",
                "technologies",
                "tools",
                "description",
                "developed",
                "implemented",
                "using",
                "responsibilities"
            ]
        ):
            continue

        # Remove bullet characters
        line = re.sub(
            r"^[•\-*▪]+",
            "",
            line
        ).strip()

        if line:
            project_names.append(line)

    return project_names


def build_resume_context(text, skills=None):
    """
    Build structured information from a resume.
    """

    text = clean_text(text)

    if skills is None:
        skills = []

    projects = extract_projects(text)
    experience = extract_experience(text)
    education = extract_education(text)
    certifications = extract_certifications(text)
    summary = extract_summary(text)

    project_names = extract_project_names(projects)

    context = {
        "full_text": text,
        "summary": summary,
        "skills": skills,
        "projects": projects,
        "project_names": project_names,
        "experience": experience,
        "education": education,
        "certifications": certifications
    }

    return context