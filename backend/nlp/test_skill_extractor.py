from skill_extractor import extract_skills


resume_text = """
Purna Sanny Sai is a B.Tech student with skills in Python,
Java, SQL, Machine Learning, NLP, Flask, React, MySQL,
Pandas, NumPy, Git and GitHub.
"""


skills = extract_skills(resume_text)


print("Extracted Skills:")
print("------------------")

for skill in skills:

    print(skill)
