from flask import Blueprint, request
from werkzeug.utils import secure_filename
from pypdf import PdfReader
from docx import Document

import os

from database.connection import get_db_connection
from utils.response import success_response, error_response
from nlp.skill_extractor import extract_skills

resume_bp = Blueprint("resume_bp", __name__)

ALLOWED_EXTENSIONS = {"pdf", "docx"}

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "uploads"
)


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


def extract_pdf_text(file_path):

    text = ""

    reader = PdfReader(file_path)

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text.strip()


def extract_docx_text(file_path):

    document = Document(file_path)

    text = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():
            text.append(paragraph.text.strip())

    return "\n".join(text)


@resume_bp.route("/upload", methods=["POST"])
def upload_resume():

    try:

        # -----------------------------------------
        # CHECK USER ID
        # -----------------------------------------

        user_id = request.form.get("user_id")

        if not user_id:

            return error_response(
                "user_id is required",
                400
            )

        # -----------------------------------------
        # CHECK FILE
        # -----------------------------------------

        if "resume" not in request.files:

            return error_response(
                "Resume file is required",
                400
            )

        file = request.files["resume"]

        if file.filename == "":

            return error_response(
                "No file selected",
                400
            )

        # -----------------------------------------
        # CHECK FILE TYPE
        # -----------------------------------------

        if not allowed_file(file.filename):

            return error_response(
                "Only PDF and DOCX files are allowed",
                400
            )

        # -----------------------------------------
        # SECURE FILE NAME
        # -----------------------------------------

        filename = secure_filename(file.filename)

        # -----------------------------------------
        # CREATE UNIQUE FILE NAME
        # -----------------------------------------

        import uuid

        unique_filename = (
            str(uuid.uuid4()) + "_" + filename
        )

        file_path = os.path.join(
            UPLOAD_FOLDER,
            unique_filename
        )

        # -----------------------------------------
        # SAVE FILE
        # -----------------------------------------

        file.save(file_path)

        # -----------------------------------------
        # EXTRACT TEXT
        # -----------------------------------------

        extension = filename.rsplit(".", 1)[1].lower()

        if extension == "pdf":

            extracted_text = extract_pdf_text(file_path)

        else:

            extracted_text = extract_docx_text(file_path)

        # -----------------------------------------
        # CHECK EXTRACTED TEXT
        # -----------------------------------------

        if not extracted_text:

            return error_response(
                "Could not extract text from resume",
                400
            )

        # -----------------------------------------
        # SAVE RESUME IN DATABASE
        # -----------------------------------------

        connection = get_db_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO resumes
            (user_id, file_name, file_path, extracted_text)
            VALUES (%s, %s, %s, %s)
            """,
            (
                user_id,
                filename,
                file_path,
                extracted_text
            )
        )

        connection.commit()

        resume_id = cursor.lastrowid

        cursor.close()
        connection.close()

        # -----------------------------------------
        # RESPONSE
        # -----------------------------------------

        return success_response(
            "Resume uploaded successfully",
            {
                "resume_id": resume_id,
                "user_id": int(user_id),
                "file_name": filename,
                "extracted_text": extracted_text
            },
            201
        )

    except Exception as e:

        return error_response(
            "Resume upload failed: " + str(e),
            500
        )
# ---------------------------------------------------
# GET ALL RESUMES OF A USER
# ---------------------------------------------------

@resume_bp.route("/user/<int:user_id>", methods=["GET"])
def get_user_resumes(user_id):

    try:

        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                resume_id,
                user_id,
                file_name,
                file_path,
                uploaded_at
            FROM resumes
            WHERE user_id = %s
            ORDER BY uploaded_at DESC
            """,
            (user_id,)
        )

        resumes = cursor.fetchall()

        cursor.close()
        connection.close()

        return success_response(
            "Resumes retrieved successfully",
            resumes
        )

    except Exception as e:

        return error_response(
            "Failed to retrieve resumes: " + str(e),
            500
        )


# ---------------------------------------------------
# GET SINGLE RESUME
# ---------------------------------------------------

@resume_bp.route("/<int:resume_id>", methods=["GET"])
def get_resume(resume_id):

    try:

        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                resume_id,
                user_id,
                file_name,
                file_path,
                extracted_text,
                uploaded_at
            FROM resumes
            WHERE resume_id = %s
            """,
            (resume_id,)
        )

        resume = cursor.fetchone()

        cursor.close()
        connection.close()

        if not resume:

            return error_response(
                "Resume not found",
                404
            )

        return success_response(
            "Resume retrieved successfully",
            resume
        )

    except Exception as e:

        return error_response(
            "Failed to retrieve resume: " + str(e),
            500
        )

@resume_bp.route("/<int:resume_id>/extract-skills", methods=["POST"])
def extract_resume_skills(resume_id):

    try:

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Get resume text
        cursor.execute(
            """
            SELECT resume_id, extracted_text
            FROM resumes
            WHERE resume_id = %s
            """,
            (resume_id,)
        )

        resume = cursor.fetchone()

        if not resume:

            cursor.close()
            connection.close()

            return error_response(
                "Resume not found",
                404
            )

        extracted_text = resume["extracted_text"]

        if not extracted_text:

            cursor.close()
            connection.close()

            return error_response(
                "No extracted text available for this resume",
                400
            )

        # Extract skills using NLP
        skills = extract_skills(extracted_text)

        if not skills:

            cursor.close()
            connection.close()

            return success_response(
                "No skills found in resume",
                {
                    "resume_id": resume_id,
                    "skills": []
                }
            )

        # Remove previously extracted skills
        cursor.execute(
            """
            DELETE FROM skills
            WHERE resume_id = %s
            """,
            (resume_id,)
        )

        # Insert new skills
        for skill in skills:

            cursor.execute(
                """
                INSERT INTO skills
                (resume_id, skill_name)
                VALUES (%s, %s)
                """,
                (
                    resume_id,
                    skill
                )
            )

        connection.commit()

        cursor.close()
        connection.close()

        return success_response(
            "Skills extracted successfully",
            {
                "resume_id": resume_id,
                "skills": skills
            }
        )

    except Exception as e:

        return error_response(
            "Skill extraction failed: " + str(e),
            500
        )
@resume_bp.route("/<int:resume_id>/skills", methods=["GET"])
def get_resume_skills(resume_id):

    try:

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Check whether resume exists
        cursor.execute(
            """
            SELECT resume_id
            FROM resumes
            WHERE resume_id = %s
            """,
            (resume_id,)
        )

        resume = cursor.fetchone()

        if not resume:

            cursor.close()
            connection.close()

            return error_response(
                "Resume not found",
                404
            )

        # Get skills
        cursor.execute(
            """
            SELECT
                skill_id,
                resume_id,
                skill_name
            FROM skills
            WHERE resume_id = %s
            ORDER BY skill_name
            """,
            (resume_id,)
        )

        skills = cursor.fetchall()

        cursor.close()
        connection.close()

        return success_response(
            "Skills retrieved successfully",
            {
                "resume_id": resume_id,
                "skills": skills
            }
        )

    except Exception as e:

        return error_response(
            "Failed to retrieve skills: " + str(e),
            500
        )