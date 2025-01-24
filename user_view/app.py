from flask import Flask, render_template
import mysql.connector
import os

app = Flask(__name__, template_folder="templates")

# Database configuration (same as the original service)
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'password'),
    'database': os.getenv('DB_NAME', 'user_service_db'),
}

# Database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route("/", methods=["GET"])
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users")
    users = {row["id"]: row for row in cursor.fetchall()}

    cursor.close()
    conn.close()

    return render_template("index.html", users=users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)  # You can choose a different port if needed
