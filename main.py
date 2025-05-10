from werkzeug.utils import secure_filename
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# ---------- Env ----------
os.environ['TIKA_LOG_PATH'] = os.getenv('TIKA_LOG_PATH', '.')
log_file = os.path.join(os.environ['TIKA_LOG_PATH'], 'tika.log')

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------- Import Models ----------
from models.event_parser import event_parser
from models.file_store import upload_file
# ---------- Flask Settings ----------
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# ---------- Endpoints ----------
@app.route('/upload_file', methods=['POST', 'OPTIONS'])
def upload_file_endpoint():
    if request.method == 'OPTIONS':
        # CORS session_id=None,user_text=Nonepre‑flight
        resp = app.response_class()
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return resp, 200

    file = request.files.get('file')
    if not file:
        return {"error": "No file provided"}, 400

    filename = secure_filename(os.path.basename(file.filename))
    if not filename:
        return {"error": "Invalid file name"}, 400

    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    try:
        session_id = upload_file(file_path)
        return {"session_id": session_id}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@app.route('/event_parser', methods=['POST'])
def analyze_contract_endpoint():
    data = request.get_json() or {}
    session_id = data.get('session_id', None)
    user_text = data.get('user_text', None)

    if not session_id and not user_text:
        return {"error": "Either session_id or user_text must be provided"}, 400

    model    = data.get('model', "gpt-4o")   # for better response
    try:
        result = event_parser(session_id=session_id,
                              user_text=user_text,
                              model=model)
        return jsonify(result), 200
    except Exception as e:
        return {"error": str(e)}, 500


# ---------- Run Server----------
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
