from flask import Flask, jsonify, request
from flask_cors import CORS
from routes.chatbot_routes import chatbot_bp

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests (for React)
app.register_blueprint(chatbot_bp, url_prefix="/api/chatbot")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Cyber Crime Victim Assistance Chatbot API is running"}), 200

if __name__ == "__main__":
    app.run(debug=True)
