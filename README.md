# Global Access — PDF Generation API

## What This Is
A Python Flask API that generates filled Portugal National Visa (D8) 
application PDFs from applicant form data. Deploy it once and call it 
from your Lovable frontend forever.

## Deploy in 3 Minutes (Railway.app — Free)

1. Go to https://railway.app and sign up with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Upload this folder as a GitHub repo (or use Railway's file upload)
4. Railway auto-detects Python and deploys
5. Copy the public URL Railway gives you (e.g. https://your-app.railway.app)

## Alternative: Render.com (Also Free)

1. Go to https://render.com
2. New → Web Service → Connect GitHub repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `python app.py`
5. Copy the public URL

## API Usage

### Endpoint
POST https://your-deployed-url.railway.app/generate-pdf

### Request Body (JSON)
```json
{
  "first_name": "John",
  "surname": "Smith",
  "date_of_birth": "1988-03-15",
  "place_of_birth": "New York",
  "country_of_birth": "United States",
  "nationality": "American",
  "sex": "Male",
  "civil_status": "Single",
  "national_id_number": "123-45-6789",
  "passport_type": "Ordinary Passport",
  "passport_number": "A12345678",
  "passport_issue_date": "2019-06-01",
  "passport_expiry": "2029-05-31",
  "passport_issued_by": "United States",
  "home_address": "123 Main St, New York, NY 10001",
  "email": "john@email.com",
  "phone": "+1 212 555 0100",
  "current_occupation": "Software Engineer",
  "employer_name": "Tech Company Inc.",
  "employer_address": "456 Tech Ave, San Francisco, CA",
  "purpose_of_journey": "Digital Nomad / Remote Work",
  "arrival_date": "2026-06-01",
  "departure_date": "",
  "costs_covered_by": "by the applicant himself/herself",
  "health_insurance": "Yes — International Plan"
}
```

### Response
Returns a PDF binary file with Content-Type: application/pdf

## Wire Into Lovable

After deploying, paste this prompt into Lovable:

"On the confirmation screen after form submission, replace the current PDF 
download button logic with a direct API call. When the user clicks 
'Download Your Application →', make a POST request to 
https://YOUR-RAILWAY-URL/generate-pdf with all the form data as JSON. 
When the response comes back (it will be a PDF binary), trigger an 
automatic browser download using a Blob URL. Show a loading spinner 
on the button while waiting. If the request fails, show an error message."

## Test It Locally

```bash
pip install flask flask-cors reportlab
python app.py
# Then in another terminal:
curl -X POST http://localhost:5000/generate-pdf \
  -H "Content-Type: application/json" \
  -d '{"first_name":"John","surname":"Smith","email":"john@test.com"}' \
  --output test.pdf
open test.pdf
```
