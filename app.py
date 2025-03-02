from flask import Flask, render_template, request, jsonify
from chat import get_response

app = Flask(__name__)

@app.get("/")
def index_get():
    return render_template("base.html")

@app.post("/predict")
def predict():
    data = request.get_json()
    print("Received data:", data)  # Debugging line
    text = data.get("messages")  # Make sure this matches the key used in JS

    if not text:  # Check if text is None or empty
        return jsonify({"error": "No input provided"}), 400

    response = get_response(text)  # Ensure this handles the input properly
    message = {"answer": response}
    return jsonify(message)


if __name__ == "__main__":
    app.run(host="0.0.0.0" , port=5000 , debug=False)
