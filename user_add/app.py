from flask import Flask, jsonify, request, render_template
import mysql.connector
import os

app = Flask(__name__, template_folder="static")

# Database configuration
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

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user)


@app.route("/users/<int:user_id>/update-payment", methods=["POST"])
def update_payment(user_id):
    data = request.get_json()
    payment = data.get("payment", 0)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET payment = %s WHERE id = %s", (payment, user_id))
    conn.commit()

    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "Payment updated", "user": user}), 200



@app.route("/", methods=["GET"])
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users")
    users = {row["id"]: row for row in cursor.fetchall()}

    cursor.close()
    conn.close()

    return render_template("web.html", users=users)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "User Service is healthy"})

@app.route("/users/add", methods=["POST"])
def add_user_from_form():
    name = request.form.get("name")
    email = request.form.get("email")
    payment = request.form.get("payment", 0)

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, email, payment) VALUES (%s, %s, %s)",
        (name, email, payment),
    )
    conn.commit()
    cursor.close()
    conn.close()

    # Redirect back to the home page to show the updated user list
    return jsonify({"message": "User Added Successfully"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
