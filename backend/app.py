from flask import Flask
from flask_cors import CORS

from routes.user_routes import user_bp
from database.connection import get_db_connection
from routes.resume_routes import resume_bp
from routes.interview_routes import interview_bp
app = Flask(__name__)

# Enable CORS
CORS(app)


# Register routes
app.register_blueprint(
    user_bp,
    url_prefix="/api/users"
)
app.register_blueprint(
    resume_bp,
    url_prefix="/api/resumes"
)
app.register_blueprint(
    interview_bp,
    url_prefix="/api/interviews"
)
@app.route("/")
def home():

    return {
        "success": True,
        "message": "AI Interview Coach API is running"
    }


@app.route("/api/health")
def health():

    return {
        "success": True,
        "message": "Backend is healthy"
    }
@app.route("/api/db-test")
def db_test():

    try:
        connection = get_db_connection()

        if connection.is_connected():
            connection.close()

            return {
                "success": True,
                "message": "MySQL connection successful"
            }

    except Exception as e:

        return {
            "success": False,
            "message": "MySQL connection failed",
            "error": str(e)
        }, 500
@app.route("/api/db/tables")
def get_tables():

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SHOW TABLES")

        tables = [row[0] for row in cursor.fetchall()]

        cursor.close()
        connection.close()

        return {
            "success": True,
            "tables": tables
        }

    except Exception as e:

        return {
            "success": False,
            "message": "Failed to read database",
            "error": str(e)
        }, 500
if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )