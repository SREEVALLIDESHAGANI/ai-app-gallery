from flask import Flask, render_template, request, jsonify
import os
import openai
from PIL import Image
from waitress import serve

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Set your OpenAI API Key (replace with your key)
openai.api_key = "YOUR_OPENAI_API_KEY"

# Function to generate descriptions using OpenAI's GPT-4 Vision
def generate_description(image_path):
    with open(image_path, "rb") as img:
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[{"role": "user", "content": [{"type": "image", "image": img}]}]
        )
    return response["choices"][0]["message"]["content"]

# Route for homepage
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        file = request.files["image"]
        if file:
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)
            description = generate_description(file_path)
            return jsonify({"description": description})
    return render_template("index.html")

if __name__ == "__main__":
    # For local development, use Flask's built-in server (for debugging)
    # app.run(debug=True)

    # For production, use Waitress to serve the app
    serve(app, host='0.0.0.0', port=5000)
