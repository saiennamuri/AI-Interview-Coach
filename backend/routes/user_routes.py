from flask import Blueprint, request

from database.connection import get_db_connection
from utils.response import success_response, error_response

from werkzeug.security import generate_password_hash, check_password_hash


user_bp = Blueprint("user_bp", __name__)


# ---------------------------------------------------
# TEST API
# ---------------------------------------------------

@user_bp.route("/test", methods=["GET"])
def test_users():

    return success_response(
        "User API is working"
    )


# ---------------------------------------------------
# USER REGISTRATION
# ---------------------------------------------------

@user_bp.route("/register", methods=["POST"])
def register_user():

    try:

        data = request.get_json()

        if not data:
            return error_response(
                "Request body is required",
                400
            )

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return error_response(
                "Name, email and password are required",
                400
            )

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT user_id FROM users WHERE email = %s",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            cursor.close()
            connection.close()

            return error_response(
                "Email already registered",
                409
            )

        hashed_password = generate_password_hash(password)

        cursor.execute(
            """
            INSERT INTO users
            (name, email, password)
            VALUES (%s, %s, %s)
            """,
            (
                name,
                email,
                hashed_password
            )
        )

        connection.commit()

        user_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return success_response(
            "User registered successfully",
            {
                "user_id": user_id,
                "name": name,
                "email": email
            },
            201
        )

    except Exception as e:

        return error_response(
            "Registration failed: " + str(e),
            500
        )


# ---------------------------------------------------
# USER LOGIN
# ---------------------------------------------------

@user_bp.route("/login", methods=["POST"])
def login_user():

    try:

        data = request.get_json()

        if not data:
            return error_response(
                "Request body is required",
                400
            )

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return error_response(
                "Email and password are required",
                400
            )

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT user_id, name, email, password
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        # IMPORTANT:
        # If email does not exist, stop here.
        if not user:
            return error_response(
                "Invalid email or password",
                401
            )

        # Verify password against stored hash
        if not check_password_hash(
            user["password"],
            password
        ):
            return error_response(
                "Invalid email or password",
                401
            )

        return success_response(
            "Login successful",
            {
                "user_id": user["user_id"],
                "name": user["name"],
                "email": user["email"]
            }
        )

    except Exception as e:

        return error_response(
            "Login failed: " + str(e),
            500
        )