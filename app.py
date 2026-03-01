"""
Global Access — Portugal Visa PDF API
Deploy to Railway.app or Render.com in 2 minutes.
POST /generate-pdf with JSON body of applicant data → returns PDF binary
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import io
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from api.generate_pdf import generate_visa_pdf_bytes

app = Flask(__name__)
CORS(app, origins=["*"])  # Restrict to your domain in production


@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "✅ Global Access PDF API is running",
        "endpoint": "POST /generate-pdf",
        "version": "1.0.0"
    })


@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    """
    Accepts applicant JSON data, returns a filled Portugal visa PDF.
    
    Expected JSON fields (all optional except first_name, surname, email):
    - first_name, surname, surname_at_birth
    - date_of_birth, place_of_birth, country_of_birth
    - nationality, nationality_at_birth, other_nationalities
    - sex, civil_status, national_id_number
    - passport_type, passport_number, passport_issue_date, passport_expiry, passport_issued_by
    - home_address, email, phone
    - current_occupation, employer_name, employer_address
    - purpose_of_journey, arrival_date, departure_date
    - costs_covered_by, inviting_person, inviting_address
    - health_insurance
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Generate the PDF
        pdf_bytes = generate_visa_pdf_bytes(data)

        if not pdf_bytes or len(pdf_bytes) < 100:
            return jsonify({"error": "PDF generation failed — empty output"}), 500

        # Return as downloadable PDF
        filename = f"portugal_visa_{data.get('surname','application')}_{data.get('first_name','')}.pdf"
        filename = filename.replace(" ", "_").lower()

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
