from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "service": "user-service"}), 200


@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    # Simule une base de données temporaire
    dummy_users = {
        1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
        2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
    }
    user = dummy_users.get(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5201, debug=True)
