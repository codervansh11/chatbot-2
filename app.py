from flask import Flask, render_template, request, jsonify
from chat import get_response  # Ensure this function is implemented correctly

app = Flask(__name__)

@app.get("/")
def index_get():
    return render_template("base.html")

@app.post("/predict")
def predict():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "No input provided"}), 400

    user_text = data["message"]
    bot_response = get_response(user_text)

    if not bot_response:
        return jsonify({"error": "No response generated"}), 500

    return jsonify({"answer": bot_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)  # Set host for deployment
