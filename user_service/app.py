from flask import Flask, jsonify, request, render_template

app = Flask(__name__, template_folder="static")

# In-memory user database
users = {
    1: {"name": "User 1", "email": "user1@example.com", "payment": 0},
    2: {"name": "User 2", "email": "user2@example.com", "payment": 0},
}

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    return jsonify(users[user_id])

@app.route("/users/<int:user_id>/update-payment", methods=["POST"])
def update_payment(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    payment = data.get("payment", 0)

    # Update the user's payment
    users[user_id]["payment"] = payment

    return jsonify({"message": "Payment updated", "user": users[user_id]}), 200

@app.route("/", methods=["GET"])
def index():
    return render_template("web.html", users=users)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "User Service is healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
