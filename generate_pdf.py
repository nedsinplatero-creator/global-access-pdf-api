"""
Portugal Visa PDF Generation API
Deploy this to Vercel, Railway, or Render as a Python serverless function.
It receives applicant data as JSON and returns a filled PDF binary.
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from datetime import datetime
import io

W, H = A4

def generate_visa_pdf_bytes(data: dict) -> bytes:
    """Generate filled Portugal visa PDF and return as bytes."""
    
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setTitle("Portugal National Visa Application")
    c.setAuthor("Global Access")
    c.setSubject("D8 Digital Nomad Visa Application")

    LABEL  = "Helvetica-Bold"
    VALUE  = "Helvetica"
    S, N   = 7, 9

    def lbl(text, x, y, size=S):
        c.setFont(LABEL, size)
        c.setFillColorRGB(0.2, 0.2, 0.2)
        c.drawString(x, y, text)

    def val(text, x, y, size=N):
        c.setFont(VALUE, size)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(x, y, str(text) if text else "")

    def hline(x, y, w):
        c.setStrokeColorRGB(0.5, 0.5, 0.5)
        c.setLineWidth(0.5)
        c.line(x, y, x + w, y)

    def sbox(x, y, w, h, title=None):
        c.setStrokeColorRGB(0.3, 0.3, 0.3)
        c.setLineWidth(0.5)
        c.setFillColorRGB(1, 1, 1)
        c.rect(x, y, w, h, fill=0)
        if title:
            c.setFont(LABEL, S)
            c.setFillColorRGB(0.2, 0.2, 0.2)
            c.drawString(x + 3, y + h - 9, title)

    def chk(x, y, checked=False):
        c.setStrokeColorRGB(0.3, 0.3, 0.3)
        c.setLineWidth(0.5)
        c.rect(x, y, 8, 8, fill=0)
        if checked:
            c.setFont(LABEL, 8)
            c.setFillColorRGB(0, 0, 0)
            c.drawString(x + 1, y + 1, "X")

    # ── PAGE 1 ──────────────────────────────────────────────────────────────

    # Header
    c.setFillColorRGB(0.0, 0.5, 0.0)
    c.rect(20, H-35, 15, 20, fill=1, stroke=0)
    c.setFillColorRGB(1.0, 0.0, 0.0)
    c.rect(35, H-35, 20, 20, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 14)
    c.setFillColorRGB(0.1, 0.1, 0.5)
    c.drawCentredString(W/2, H-22, "PORTUGAL")
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(W/2, H-34, "APPLICATION FOR NATIONAL VISA")
    c.setFont(VALUE, 7)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawCentredString(W/2, H-43, "(Residence and Temporary Stay)   —   This application form is free")
    hline(20, H-47, W-40)

    # Official use box
    sbox(W-175, H-110, 155, 60, "FOR OFFICIAL USE ONLY")
    lbl("Date of application:", W-172, H-68)
    lbl("Application number:", W-172, H-80)
    lbl("File handled by:", W-172, H-92)

    # Photo box
    sbox(W-175, H-200, 65, 80)
    lbl("PHOTO", W-158, H-162)

    # Fields 1-3
    y = H-65
    lbl("1. Surname (Family name):", 20, y)
    hline(20, y-3, 360); val(data.get("surname",""), 22, y-14)

    y -= 30
    lbl("2. Surname at birth:", 20, y)
    hline(20, y-3, 360); val(data.get("surname_at_birth",""), 22, y-14)

    y -= 30
    lbl("3. First name(s):", 20, y)
    hline(20, y-3, 360); val(data.get("first_name",""), 22, y-14)

    # Fields 4-6
    y -= 30
    lbl("4. Date of birth:", 20, y)
    hline(20, y-3, 120); val(data.get("date_of_birth",""), 22, y-14)
    lbl("5. Place of birth:", 155, y)
    hline(155, y-3, 100); val(data.get("place_of_birth",""), 157, y-14)
    lbl("6. Country of birth:", 268, y)
    hline(268, y-3, 110); val(data.get("country_of_birth",""), 270, y-14)

    # Field 7
    y -= 30
    lbl("7. Current nationality:", 20, y)
    hline(20, y-3, 140); val(data.get("nationality",""), 22, y-14)
    lbl("Nationality at birth:", 175, y)
    hline(175, y-3, 110); val(data.get("nationality_at_birth",""), 177, y-14)
    lbl("Other nationalities:", 300, y)
    hline(300, y-3, 100); val(data.get("other_nationalities",""), 302, y-14)

    # Application lodged at box
    sbox(W-175, H-285, 155, 80, "APPLICATION LODGED AT:")
    chk(W-172, H-248); lbl("Embassy/Consulate", W-160, H-247, 6)
    chk(W-172, H-262); lbl("Service provider", W-160, H-261, 6)
    chk(W-172, H-276); lbl("Commercial intermediary", W-160, H-275, 6)

    # Fields 8-9
    y -= 35
    lbl("8. Sex:", 20, y)
    sex = data.get("sex","").lower()
    chk(48, y-2, "male" in sex); lbl("Male", 59, y-1)
    chk(88, y-2, "female" in sex); lbl("Female", 99, y-1)

    lbl("9. Civil status:", 155, y)
    civil = data.get("civil_status","").lower()
    statuses = [("Single",210),("Married",255),("Sep.",305),("Div.",340),("Widow(er)",375)]
    for s, sx in statuses:
        chk(sx, y-2, civil == s.lower())
        lbl(s, sx+11, y-1, 6)

    # Field 10
    y -= 25
    lbl("10. Parental authority / legal guardian (if minor):", 20, y)
    hline(20, y-3, W-215); val(data.get("parental_authority","N/A"), 22, y-14)

    # Supporting docs box
    sbox(W-175, H-390, 155, 95, "Supporting documents:")
    docs = ["Travel document","Means of subsistence","Invitation","TMI","Means of transport","Other:"]
    for i, d in enumerate(docs):
        chk(W-172, H-355-i*14)
        lbl(d, W-161, H-354-i*14, 6)

    # Visa decision box
    sbox(W-175, H-490, 155, 90, "Visa decision:")
    chk(W-172, H-420); lbl("Refused", W-161, H-419, 6)
    chk(W-172, H-434); lbl("Issued: ☐ E  ☐ D", W-161, H-433, 6)
    lbl("Valid From:", W-172, H-450, 6); hline(W-130, H-452, 115)
    lbl("Until:", W-172, H-464, 6); hline(W-148, H-466, 133)

    # Field 11
    y -= 30
    lbl("11. National identity number:", 20, y)
    hline(20, y-3, 180); val(data.get("national_id_number",""), 22, y-14)

    # Fields 12-16
    y -= 30
    lbl("12. Type of travel document:", 20, y)
    ptype = data.get("passport_type","ordinary").lower()
    chk(135, y-2, "ordinary" in ptype); lbl("Ordinary passport", 146, y-1, 7)
    chk(245, y-2); lbl("Other (specify):", 256, y-1, 7)

    y -= 22
    lbl("13. Passport number:", 20, y)
    hline(20, y-3, 110); val(data.get("passport_number",""), 22, y-14)
    lbl("14. Date of issue:", 145, y)
    hline(145, y-3, 90); val(str(data.get("passport_issue_date","")), 147, y-14)
    lbl("15. Valid until:", 250, y)
    hline(250, y-3, 90); val(str(data.get("passport_expiry","")), 252, y-14)
    lbl("16. Issued by:", 355, y)
    hline(355, y-3, 90); val(data.get("passport_issued_by",""), 357, y-14)

    # Fields 17-18 N/A
    y -= 28
    lbl("17-18. EU/EEA family member data: NOT APPLICABLE", 20, y, S)

    # Field 19
    y -= 18
    lbl("19. Home address and e-mail:", 20, y)
    hline(20, y-3, W-42); val(data.get("home_address",""), 22, y-14)
    y -= 18
    lbl("Email:", 20, y); hline(45, y-3, 180); val(data.get("email",""), 47, y-14)
    lbl("Tel:", 240, y); hline(255, y-3, 120); val(data.get("phone",""), 257, y-14)

    # ── PAGE 2 ──────────────────────────────────────────────────────────────
    c.showPage()

    c.setFont("Helvetica-Bold", 9)
    c.setFillColorRGB(0.1, 0.1, 0.5)
    c.drawCentredString(W/2, H-20, "PORTUGAL — NATIONAL VISA APPLICATION (Page 2)")
    hline(20, H-25, W-40)

    y = H-50

    # Field 20
    lbl("20. Residence in country other than nationality:", 20, y)
    chk(220, y-2); lbl("No", 231, y-1)
    chk(250, y-2); lbl("Yes — Permit No.:", 261, y-1)
    hline(330, y-3, 80); lbl("Valid until:", 420, y-1); hline(460, y-3, 80)

    # Fields 21-22
    y -= 25
    lbl("*21. Current occupation:", 20, y)
    hline(20, y-3, 250); val(data.get("current_occupation",""), 22, y-14)

    y -= 28
    lbl("*22. Employer name, address and telephone:", 20, y)
    hline(20, y-3, W-42)
    employer_text = f"{data.get('employer_name','')}   {data.get('employer_address','')}   {data.get('phone','')}"
    val(employer_text, 22, y-14)

    # Field 23
    y -= 30
    lbl("23. Purpose(s) of the journey:", 20, y)
    y -= 16
    purposes = ["Study","Training","Work","Familiar Regrouping","Medical","Retired/Religious","Other"]
    purpose_val = data.get("purpose_of_journey","Remote Work").lower()
    px2 = 20
    for p in purposes:
        is_checked = (p.lower() in purpose_val) or ("nomad" in purpose_val and p == "Other") or ("remote" in purpose_val and p == "Work")
        chk(px2, y-2, is_checked); lbl(p, px2+11, y-1, 7)
        px2 += len(p)*5 + 25
        if px2 > W-80: px2 = 20; y -= 14

    # Field 24
    y -= 22
    lbl("24. Additional information on purpose of stay:", 20, y)
    hline(20, y-3, W-42); val(data.get("purpose_of_journey","Digital Nomad / Remote Work — D8 Visa"), 22, y-14)

    # Fields 25-27
    y -= 30
    lbl("25. Main destination: PORTUGAL", 20, y)
    lbl("26. First entry: Portugal", 250, y)

    y -= 20
    lbl("27. Entries requested:", 20, y)
    chk(120, y-2); lbl("Two entries", 131, y-1, 7)
    chk(200, y-2, True); lbl("Multiple entries (temporary stay)", 211, y-1, 7)

    y -= 18
    lbl("Intended arrival in Portugal:", 20, y)
    hline(160, y-3, 100); val(str(data.get("arrival_date","")), 162, y-14)
    lbl("Intended departure:", 275, y)
    hline(360, y-3, 100); val(str(data.get("departure_date","")), 362, y-14)

    # Fields 28-29 N/A
    y -= 28
    lbl("28. Fingerprints collected previously: NOT APPLICABLE", 20, y, S)
    y -= 12
    lbl("29. Entry permit for final country: NOT APPLICABLE", 20, y, S)

    # Fields 30-31
    y -= 20
    lbl("*30. Inviting person / Hotel:", 20, y)
    hline(20, y-3, 200); val(data.get("inviting_person",""), 22, y-14)
    lbl("Address:", 235, y); hline(265, y-3, 170); val(data.get("inviting_address",""), 267, y-14)

    y -= 28
    lbl("*31. Inviting company / organisation:", 20, y)
    hline(20, y-3, W-42)

    # Field 32
    y -= 28
    lbl("*32. Cost of stay covered:", 20, y)
    costs = data.get("costs_covered_by","applicant").lower()
    chk(135, y-2, "applicant" in costs); lbl("By the applicant himself/herself", 146, y-1, 7)
    chk(310, y-2); lbl("By a sponsor", 321, y-1, 7)
    y -= 16
    lbl("Means of support:", 20, y)
    for i, m in enumerate(["Cash","Credit card","Pre-paid accommodation","Pre-paid transport"]):
        chk(90 + i*110, y-2); lbl(m, 101 + i*110, y-1, 6)

    # Health insurance
    y -= 20
    lbl("Health Insurance:", 20, y)
    hi = data.get("health_insurance","").lower()
    chk(100, y-2, "yes" in hi or bool(hi)); lbl("Yes", 111, y-1)
    chk(135, y-2, "no" in hi and len(hi) < 5); lbl("No", 146, y-1)
    val(data.get("health_insurance",""), 165, y)

    # Declaration
    y -= 20
    hline(20, y, W-40)
    y -= 12
    declaration = (
        "I am aware that the visa fee is not refunded if the visa is refused. I declare that to the best of "
        "my knowledge all particulars supplied by me are correct and complete. I am aware that any false "
        "statements will lead to my application being rejected or to the annulment of a visa already granted "
        "and may also render me liable to prosecution under Portuguese law. I undertake to leave Portugal "
        "before the expiry of the visa, if granted. I have been informed that possession of a visa is only "
        "one of the prerequisites for entry into Portugal."
    )
    c.setFont(VALUE, 6)
    c.setFillColorRGB(0.25, 0.25, 0.25)
    for line in simpleSplit(declaration, VALUE, 6, W-42):
        c.drawString(20, y, line); y -= 8

    # Signature
    y -= 18
    hline(20, y, W-40)
    y -= 16
    lbl("Place and date:", 20, y); hline(90, y-3, 150)
    lbl("Signature:", 260, y); hline(305, y-3, 215)

    # Footer
    c.setFont(VALUE, 6)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawCentredString(W/2, 18, f"Generated by Global Access — {datetime.now().strftime('%B %d, %Y')}")

    c.save()
    buffer.seek(0)
    return buffer.read()
