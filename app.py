"""
Global Access — Portugal Visa PDF API
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import io
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_pdf import generate_visa_pdf_bytes

app = Flask(__name__)

# CORS — allow all origins (handles Railway network-level preflight)
CORS(app, 
     resources={r"/*": {"origins": "*"}},
     allow_headers=["Content-Type", "Accept"],
     methods=["GET", "POST", "OPTIONS"],
     supports_credentials=False
)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Accept"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Max-Age"] = "86400"
    return response

@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "✅ Global Access PDF API is running",
        "endpoint": "POST /generate-pdf",
        "version": "1.0.0"
    })

@app.route("/generate-pdf", methods=["GET", "POST", "OPTIONS"])
def generate_pdf():
    # Handle CORS preflight explicitly
    if request.method == "OPTIONS":
        response = jsonify({})
        response.status_code = 200
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Accept"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Max-Age"] = "86400"
        return response

    try:
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        pdf_bytes = generate_visa_pdf_bytes(data)

        if not pdf_bytes or len(pdf_bytes) < 100:
            return jsonify({"error": "PDF generation failed — output too small"}), 500

        filename = f"portugal_visa_{data.get('surname', 'application')}.pdf".replace(" ", "_").lower()

        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

flask-cors==4.0.0
