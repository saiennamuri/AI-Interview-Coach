from flask import Blueprint, request

from database.connection import get_db_connection
from utils.response import success_response, error_response
from nlp.question_generator import generate_questions
from nlp.answer_evaluator import evaluate_answer
interview_bp = Blueprint("interview_bp", __name__)


@interview_bp.route("/test", methods=["GET"])
def test_interviews():

    return success_response(
        "Interview API is working"
    )


@interview_bp.route("/create", methods=["POST"])
def create_interview():

    try:

        data = request.get_json()

        if not data:

            return error_response(
                "Request body is required",
                400
            )

        user_id = data.get("user_id")
        job_role = data.get("job_role")
        difficulty = data.get("difficulty")
        interview_type = data.get("interview_type")

        # Validate required fields
        if not user_id:
            return error_response(
                "user_id is required",
                400
            )

        if not job_role:
            return error_response(
                "job_role is required",
                400
            )

        if not difficulty:
            return error_response(
                "difficulty is required",
                400
            )

        if not interview_type:
            return error_response(
                "interview_type is required",
                400
            )

        # Validate difficulty
        allowed_difficulties = [
            "Easy",
            "Medium",
            "Hard"
        ]

        if difficulty not in allowed_difficulties:

            return error_response(
                "Difficulty must be Easy, Medium or Hard",
                400
            )

        # Validate interview type
        allowed_types = [
            "Technical",
            "HR",
            "Mixed"
        ]

        if interview_type not in allowed_types:

            return error_response(
                "Interview type must be Technical, HR or Mixed",
                400
            )

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Check whether user exists
        cursor.execute(
            """
            SELECT user_id, name
            FROM users
            WHERE user_id = %s
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        if not user:

            cursor.close()
            connection.close()

            return error_response(
                "User not found",
                404
            )

        # Create interview
        cursor.execute(
            """
            INSERT INTO interviews
            (user_id, job_role, difficulty, interview_type)
            VALUES (%s, %s, %s, %s)
            """,
            (
                user_id,
                job_role,
                difficulty,
                interview_type
            )
        )

        connection.commit()

        interview_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return success_response(
            "Interview created successfully",
            {
                "interview_id": interview_id,
                "user_id": int(user_id),
                "job_role": job_role,
                "difficulty": difficulty,
                "interview_type": interview_type
            },
            201
        )

    except Exception as e:

        return error_response(
            "Interview creation failed: " + str(e),
            500
        )
@interview_bp.route("/user/<int:user_id>", methods=["GET"])
def get_user_interviews(user_id):

    try:

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Check whether user exists
        cursor.execute(
            """
            SELECT user_id
            FROM users
            WHERE user_id = %s
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        if not user:

            cursor.close()
            connection.close()

            return error_response(
                "User not found",
                404
            )

        # Get all interviews of the user
        cursor.execute(
            """
            SELECT
                interview_id,
                user_id,
                job_role,
                difficulty,
                interview_type,
                started_at,
                completed_at
            FROM interviews
            WHERE user_id = %s
            ORDER BY started_at DESC
            """,
            (user_id,)
        )

        interviews = cursor.fetchall()

        cursor.close()
        connection.close()

        return success_response(
            "Interviews retrieved successfully",
            {
                "user_id": user_id,
                "interviews": interviews
            }
        )

    except Exception as e:

        return error_response(
            "Failed to retrieve interviews: " + str(e),
            500
        )
@interview_bp.route("/<int:interview_id>", methods=["GET"])
def get_interview(interview_id):

    try:

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Get interview details
        cursor.execute(
            """
            SELECT
                interview_id,
                user_id,
                job_role,
                difficulty,
                interview_type,
                started_at,
                completed_at
            FROM interviews
            WHERE interview_id = %s
            """,
            (interview_id,)
        )

        interview = cursor.fetchone()

        cursor.close()
        connection.close()

        if not interview:

            return error_response(
                "Interview not found",
                404
            )

        return success_response(
            "Interview retrieved successfully",
            interview
        )

    except Exception as e:

        return error_response(
            "Failed to retrieve interview: " + str(e),
            500
        )
@interview_bp.route("/<int:interview_id>/generate-questions", methods=["POST"])
def generate_interview_questions(interview_id):

    try:

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Get interview details
        cursor.execute(
            """
            SELECT
                interview_id,
                user_id,
                job_role,
                difficulty,
                interview_type
            FROM interviews
            WHERE interview_id = %s
            """,
            (interview_id,)
        )

        interview = cursor.fetchone()

        if not interview:

            cursor.close()
            connection.close()

            return error_response(
                "Interview not found",
                404
            )

        user_id = interview["user_id"]
        job_role = interview["job_role"]
        difficulty = interview["difficulty"]

        # Get latest resume of the user
        cursor.execute(
            """
            SELECT
                resume_id,
                extracted_text
            FROM resumes
            WHERE user_id = %s
            ORDER BY uploaded_at DESC
            LIMIT 1
            """,
            (user_id,)
        )

        resume = cursor.fetchone()

        if not resume:

            cursor.close()
            connection.close()

            return error_response(
                "No resume found for this user",
                404
            )

        resume_id = resume["resume_id"]
        resume_text = resume["extracted_text"] or ""

        # Get skills from resume
        cursor.execute(
            """
            SELECT skill_name
            FROM skills
            WHERE resume_id = %s
            ORDER BY skill_name
            """,
            (resume_id,)
        )

        skill_rows = cursor.fetchall()

        skills = [
            row["skill_name"]
            for row in skill_rows
        ]

        if not skills:

            cursor.close()
            connection.close()

            return error_response(
                "No skills found for this resume. Extract skills first.",
                400
            )

        # Generate questions
        questions = generate_questions(
            resume_text,
            skills,
            job_role,
            difficulty,
            interview["interview_type"]
        )

        if not questions:

            cursor.close()
            connection.close()

            return error_response(
                "Could not generate questions",
                500
            )

        # Remove previously generated questions
        cursor.execute(
            """
            DELETE FROM questions
            WHERE interview_id = %s
            """,
            (interview_id,)
        )

        # Save questions
        saved_questions = []

        for question_text in questions:

            # Determine question type
            if question_text.startswith("What are"):

                question_type = "General"

            elif question_text.startswith("Why are"):

                question_type = "HR"

            else:

                question_type = "Technical"

            cursor.execute(
                """
                INSERT INTO questions
                (
                    interview_id,
                    question_text,
                    question_type,
                    difficulty
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    interview_id,
                    question_text,
                    question_type,
                    difficulty
                )
            )

            question_id = cursor.lastrowid

            saved_questions.append(
                {
                    "question_id": question_id,
                    "question_text": question_text,
                    "question_type": question_type,
                    "difficulty": difficulty
                }
            )

        connection.commit()

        cursor.close()
        connection.close()

        return success_response(
            "Interview questions generated successfully",
            {
                "interview_id": interview_id,
                "job_role": job_role,
                "difficulty": difficulty,
                "resume_id": resume_id,
                "skills": skills,
                "questions": saved_questions
            },
            201
        )

    except Exception as e:

        return error_response(
            "Question generation failed: " + str(e),
            500
        )
@interview_bp.route("/<int:interview_id>/questions", methods=["GET"])
def get_interview_questions(interview_id):

    try:

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Check whether interview exists
        cursor.execute(
            """
            SELECT interview_id
            FROM interviews
            WHERE interview_id = %s
            """,
            (interview_id,)
        )

        interview = cursor.fetchone()

        if not interview:

            cursor.close()
            connection.close()

            return error_response(
                "Interview not found",
                404
            )

        # Get questions
        cursor.execute(
            """
            SELECT
                question_id,
                interview_id,
                question_text,
                question_type,
                difficulty
            FROM questions
            WHERE interview_id = %s
            ORDER BY question_id
            """,
            (interview_id,)
        )

        questions = cursor.fetchall()

        cursor.close()
        connection.close()

        return success_response(
            "Interview questions retrieved successfully",
            {
                "interview_id": interview_id,
                "questions": questions
            }
        )

    except Exception as e:

        return error_response(
            "Failed to retrieve questions: " + str(e),
            500
        )
@interview_bp.route("/questions/<int:question_id>/answer", methods=["POST"])
def submit_answer(question_id):

    try:

        data = request.get_json()

        if not data:

            return error_response(
                "Request body is required",
                400
            )

        answer_text = data.get("answer_text")

        if not answer_text or not answer_text.strip():

            return error_response(
                "answer_text is required",
                400
            )

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Check whether question exists
        cursor.execute(
            """
            SELECT
                question_id,
                interview_id,
                question_text
            FROM questions
            WHERE question_id = %s
            """,
            (question_id,)
        )

        question = cursor.fetchone()

        if not question:

            cursor.close()
            connection.close()

            return error_response(
                "Question not found",
                404
            )

        # Save answer
        cursor.execute(
            """
            INSERT INTO answers
            (
                question_id,
                answer_text
            )
            VALUES (%s, %s)
            """,
            (
                question_id,
                answer_text.strip()
            )
        )

        connection.commit()

        answer_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return success_response(
            "Answer submitted successfully",
            {
                "answer_id": answer_id,
                "question_id": question_id,
                "interview_id": question["interview_id"],
                "answer_text": answer_text.strip()
            },
            201
        )

    except Exception as e:

        return error_response(
            "Answer submission failed: " + str(e),
            500
        )
@interview_bp.route("/questions/<int:question_id>/answer", methods=["GET"])
def get_question_answer(question_id):

    try:

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Check whether question exists
        cursor.execute(
            """
            SELECT
                question_id,
                interview_id,
                question_text
            FROM questions
            WHERE question_id = %s
            """,
            (question_id,)
        )

        question = cursor.fetchone()

        if not question:

            cursor.close()
            connection.close()

            return error_response(
                "Question not found",
                404
            )

        # Get submitted answer
        cursor.execute(
            """
            SELECT
                answer_id,
                question_id,
                answer_text,
                answered_at
            FROM answers
            WHERE question_id = %s
            ORDER BY answered_at DESC
            LIMIT 1
            """,
            (question_id,)
        )

        answer = cursor.fetchone()

        cursor.close()
        connection.close()

        if not answer:

            return error_response(
                "No answer submitted for this question",
                404
            )

        return success_response(
            "Answer retrieved successfully",
            {
                "question": question,
                "answer": answer
            }
        )

    except Exception as e:

        return error_response(
            "Failed to retrieve answer: " + str(e),
            500
        )
@interview_bp.route(
    "/questions/<int:question_id>/evaluate",
    methods=["POST"]
)
def evaluate_question_answer(question_id):

    try:

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Get question
        cursor.execute(
            """
            SELECT
                question_id,
                interview_id,
                question_text
            FROM questions
            WHERE question_id = %s
            """,
            (question_id,)
        )

        question = cursor.fetchone()

        if not question:

            cursor.close()
            connection.close()

            return error_response(
                "Question not found",
                404
            )

        # Get latest submitted answer
        cursor.execute(
            """
            SELECT
                answer_id,
                question_id,
                answer_text
            FROM answers
            WHERE question_id = %s
            ORDER BY answered_at DESC
            LIMIT 1
            """,
            (question_id,)
        )

        answer = cursor.fetchone()

        if not answer:

            cursor.close()
            connection.close()

            return error_response(
                "No answer submitted for this question",
                404
            )

        # NLP evaluation
        evaluation = evaluate_answer(
            question["question_text"],
            answer["answer_text"]
        )

        # Save evaluation into database
        cursor.execute(
            """
            INSERT INTO evaluations
            (
                answer_id,
                relevance_score,
                keyword_score,
                semantic_score,
                clarity_score,
                overall_score,
                feedback
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                answer["answer_id"],
                evaluation["relevance_score"],
                evaluation["keyword_score"],
                evaluation["semantic_score"],
                evaluation["clarity_score"],
                evaluation["overall_score"],
                evaluation["feedback"]
            )
        )

        connection.commit()

        evaluation_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return success_response(
            "Answer evaluated successfully",
            {
                "evaluation_id": evaluation_id,
                "question_id": question_id,
                "answer_id": answer["answer_id"],
                "scores": {
                    "relevance_score":
                        evaluation["relevance_score"],

                    "keyword_score":
                        evaluation["keyword_score"],

                    "semantic_score":
                        evaluation["semantic_score"],

                    "clarity_score":
                        evaluation["clarity_score"],

                    "overall_score":
                        evaluation["overall_score"]
                },
                "feedback":
                    evaluation["feedback"]
            },
            201
        )

    except Exception as e:

        return error_response(
            "Answer evaluation failed: " + str(e),
            500
        )
@interview_bp.route(
    "/answers/<int:answer_id>/evaluation",
    methods=["GET"]
)
def get_answer_evaluation(answer_id):

    try:

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Check whether answer exists
        cursor.execute(
            """
            SELECT
                answer_id,
                question_id,
                answer_text
            FROM answers
            WHERE answer_id = %s
            """,
            (answer_id,)
        )

        answer = cursor.fetchone()

        if not answer:

            cursor.close()
            connection.close()

            return error_response(
                "Answer not found",
                404
            )

        # Get latest evaluation
        cursor.execute(
            """
            SELECT
                evaluation_id,
                answer_id,
                relevance_score,
                keyword_score,
                semantic_score,
                clarity_score,
                overall_score,
                feedback,
                evaluated_at
            FROM evaluations
            WHERE answer_id = %s
            ORDER BY evaluated_at DESC
            LIMIT 1
            """,
            (answer_id,)
        )

        evaluation = cursor.fetchone()

        cursor.close()
        connection.close()

        if not evaluation:

            return error_response(
                "No evaluation found for this answer",
                404
            )

        return success_response(
            "Evaluation retrieved successfully",
            {
                "answer": answer,
                "evaluation": evaluation
            }
        )

    except Exception as e:

        return error_response(
            "Failed to retrieve evaluation: " + str(e),
            500
        )
@interview_bp.route(
    "/<int:interview_id>/complete",
    methods=["PUT"]
)
def complete_interview(interview_id):

    try:

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Check whether interview exists
        cursor.execute(
            """
            SELECT
                interview_id,
                user_id,
                job_role,
                difficulty,
                interview_type,
                started_at,
                completed_at
            FROM interviews
            WHERE interview_id = %s
            """,
            (interview_id,)
        )

        interview = cursor.fetchone()

        if not interview:

            cursor.close()
            connection.close()

            return error_response(
                "Interview not found",
                404
            )

        # Check whether interview is already completed
        if interview["completed_at"] is not None:

            cursor.close()
            connection.close()

            return error_response(
                "Interview is already completed",
                400
            )

        # Mark interview as completed
        cursor.execute(
            """
            UPDATE interviews
            SET completed_at = CURRENT_TIMESTAMP
            WHERE interview_id = %s
            """,
            (interview_id,)
        )

        connection.commit()

        # Get updated interview
        cursor.execute(
            """
            SELECT
                interview_id,
                user_id,
                job_role,
                difficulty,
                interview_type,
                started_at,
                completed_at
            FROM interviews
            WHERE interview_id = %s
            """,
            (interview_id,)
        )

        completed_interview = cursor.fetchone()

        cursor.close()
        connection.close()

        return success_response(
            "Interview completed successfully",
            completed_interview
        )

    except Exception as e:

        return error_response(
            "Failed to complete interview: " + str(e),
            500
        )
@interview_bp.route(
    "/<int:interview_id>/result",
    methods=["GET"]
)
def get_interview_result(interview_id):

    try:

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Check whether interview exists
        cursor.execute(
            """
            SELECT
                interview_id,
                user_id,
                job_role,
                difficulty,
                interview_type,
                started_at,
                completed_at
            FROM interviews
            WHERE interview_id = %s
            """,
            (interview_id,)
        )

        interview = cursor.fetchone()

        if not interview:

            cursor.close()
            connection.close()

            return error_response(
                "Interview not found",
                404
            )

        # Get total number of questions
        cursor.execute(
            """
            SELECT COUNT(*) AS total_questions
            FROM questions
            WHERE interview_id = %s
            """,
            (interview_id,)
        )

        total_questions = cursor.fetchone()["total_questions"]

        # Get answered questions
        cursor.execute(
            """
            SELECT COUNT(DISTINCT a.question_id) AS answered_questions
            FROM answers a
            INNER JOIN questions q
                ON a.question_id = q.question_id
            WHERE q.interview_id = %s
            """,
            (interview_id,)
        )

        answered_questions = cursor.fetchone()["answered_questions"]

        # Get evaluated questions
        cursor.execute(
            """
            SELECT COUNT(DISTINCT e.answer_id) AS evaluated_questions
            FROM evaluations e
            INNER JOIN answers a
                ON e.answer_id = a.answer_id
            INNER JOIN questions q
                ON a.question_id = q.question_id
            WHERE q.interview_id = %s
            """,
            (interview_id,)
        )

        evaluated_questions = cursor.fetchone()["evaluated_questions"]

        # Calculate average scores
        cursor.execute(
            """
            SELECT
                AVG(e.relevance_score) AS average_relevance_score,
                AVG(e.keyword_score) AS average_keyword_score,
                AVG(e.semantic_score) AS average_semantic_score,
                AVG(e.clarity_score) AS average_clarity_score,
                AVG(e.overall_score) AS overall_score
            FROM evaluations e
            INNER JOIN answers a
                ON e.answer_id = a.answer_id
            INNER JOIN questions q
                ON a.question_id = q.question_id
            WHERE q.interview_id = %s
            """,
            (interview_id,)
        )

        scores = cursor.fetchone()

        cursor.close()
        connection.close()

        # No evaluations yet
        if evaluated_questions == 0:

            return success_response(
                "No evaluated answers found",
                {
                    "interview": interview,
                    "statistics": {
                        "total_questions": total_questions,
                        "answered_questions": answered_questions,
                        "evaluated_questions": 0
                    },
                    "scores": {
                        "average_relevance_score": 0.0,
                        "average_keyword_score": 0.0,
                        "average_semantic_score": 0.0,
                        "average_clarity_score": 0.0,
                        "overall_score": 0.0
                    }
                }
            )

        # Convert database Decimal values to float
        average_relevance = float(
            scores["average_relevance_score"] or 0
        )

        average_keyword = float(
            scores["average_keyword_score"] or 0
        )

        average_semantic = float(
            scores["average_semantic_score"] or 0
        )

        average_clarity = float(
            scores["average_clarity_score"] or 0
        )

        overall_score = float(
            scores["overall_score"] or 0
        )

        # Generate overall performance feedback
        if overall_score >= 85:

            feedback = (
                "Excellent interview performance. "
                "You demonstrated strong relevance, "
                "technical understanding and clarity."
            )

        elif overall_score >= 70:

            feedback = (
                "Good interview performance. "
                "Your answers were mostly strong, "
                "but there is room for improvement."
            )

        elif overall_score >= 50:

            feedback = (
                "Average interview performance. "
                "Try to improve your technical explanations, "
                "keyword usage and answer clarity."
            )

        else:

            feedback = (
                "Interview performance needs improvement. "
                "Focus on understanding the questions and "
                "providing clear and relevant answers."
            )

        return success_response(
            "Interview result retrieved successfully",
            {
                "interview": interview,

                "statistics": {
                    "total_questions": total_questions,
                    "answered_questions": answered_questions,
                    "evaluated_questions": evaluated_questions
                },

                "scores": {
                    "average_relevance_score":
                        round(average_relevance, 2),

                    "average_keyword_score":
                        round(average_keyword, 2),

                    "average_semantic_score":
                        round(average_semantic, 2),

                    "average_clarity_score":
                        round(average_clarity, 2),

                    "overall_score":
                        round(overall_score, 2)
                },

                "feedback": feedback
            }
        )

    except Exception as e:

        return error_response(
            "Failed to retrieve interview result: " + str(e),
            500
        )