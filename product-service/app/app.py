from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# URL du User Service (définie via variable d’environnement ou par défaut)
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:5201")


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "service": "product-service"}), 200


@app.route("/product/<int:product_id>", methods=["GET"])
def get_product(product_id):
    dummy_products = {
        1: {"id": 1, "name": "Laptop", "price": 1200},
        2: {"id": 2, "name": "Headphones", "price": 200},
    }
    product = dummy_products.get(product_id)
    if product:
        return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404


@app.route("/product/<int:product_id>/user", methods=["GET"])
def get_product_with_user(product_id):
    """Appelle le user-service pour récupérer le propriétaire d’un produit"""
    dummy_products = {
        1: {"id": 1, "name": "Laptop", "price": 1200, "owner_id": 1},
        2: {"id": 2, "name": "Headphones", "price": 200, "owner_id": 2},
    }
    product = dummy_products.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    try:
        user_id = product["owner_id"]
        user_url = f"{USER_SERVICE_URL}/user/{user_id}"
        user_response = requests.get(user_url, timeout=3)

        if user_response.status_code == 200:
            return (
                jsonify(
                    {
                        "product": product,
                        "owner": user_response.json(),
                    }
                ),
                200,
            )

        return (
            jsonify(
                {
                    "product": product,
                    "owner_error": "User not found",
                }
            ),
            404,
        )

    except requests.exceptions.RequestException as e:
        return (
            jsonify(
                {
                    "error": "Failed to contact user-service",
                    "details": str(e),
                }
            ),
            500,
        )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5202)),
        debug=True,
    )
