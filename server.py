import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from google import genai

API_KEY = "AIzaSyCuWTW8hvY2TogrpV8DNA_8TnaETHaIKdI"  # Replace with your Gemini API key

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

client = genai.Client(api_key=API_KEY)
conversation_state = {}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files.get('file')
    if not uploaded_file or uploaded_file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    filename = secure_filename(uploaded_file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    uploaded_file.save(file_path)

    try:
        api_file = client.files.upload(
            file=open(file_path, "rb"),
            config={"mime_type": "application/pdf"}
        )
    except Exception as e:
        return jsonify({"error": f"Failed uploading to Gemini API: {str(e)}"}), 500

    user_id = request.remote_addr
    conversation = [
        {
            "role": "user",
            "parts": [
                {"file_data": {"file_uri": api_file.uri, "mime_type": api_file.mime_type}},
                {"text": "This is the document for our chat."}
            ]
        }
    ]
    conversation_state[user_id] = conversation

    return jsonify({"success": True})

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').strip()
    user_id = request.remote_addr
    print(f"Received message from user {user_id}: {user_message}")


    if user_id not in conversation_state:
        return jsonify({"error": "No uploaded file. Please upload a PDF first."}), 400

    if not user_message:
        return jsonify({"error": "Empty message received."}), 400

    conversation = conversation_state[user_id]
    conversation.append({"role": "user", "parts": [{"text": user_message}]})

    try:
        gemini_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conversation
    )
        response_text = gemini_response.text
        cleaned_response = response_text.replace("*", "")
        print(f"Gemini response: {response_text}")  # Debug print Gemini's reply
    except Exception as e:
        cleaned_response = f"Error calling Gemini API: {e}"
        print(response_text)  # Print error to Flask console


    return jsonify({"reply": cleaned_response})

if __name__ == "__main__":
    app.run(debug=True)
