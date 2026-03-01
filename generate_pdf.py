"""
Portugal Visa PDF Generation API - Fixed Version
Values appear ON the lines, not below them.
Sex checkbox fixed (male vs female exclusive).
All date fields properly mapped.
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from datetime import datetime
import io

W, H = A4  # 595 x 842 points

def generate_visa_pdf_bytes(data: dict) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setTitle("Portugal National Visa Application")
    c.setAuthor("Global Access")
    c.setSubject("D8 Digital Nomad Visa Application")

    LABEL = "Helvetica-Bold"
    VALUE = "Helvetica"
    SZ_LABEL = 7
    SZ_VALUE = 8
    SZ_SMALL = 6

    def lbl(text, x, y, size=SZ_LABEL):
        c.setFont(LABEL, size)
        c.setFillColorRGB(0.25, 0.25, 0.25)
        c.drawString(x, y, text)

    def val(text, x, y, size=SZ_VALUE):
        """Draw value ON the line - y is the line position, text sits just above it"""
        c.setFont(VALUE, size)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(x, y + 2, str(text) if text else "")

    def field(label_text, lx, ly, vx, vy, line_x, line_y, line_w, value_text, lsize=SZ_LABEL, vsize=SZ_VALUE):
        """Draw a complete field: label + line + value ON the line"""
        lbl(label_text, lx, ly, lsize)
        hline(line_x, line_y, line_w)
        val(value_text, vx, vy, vsize)

    def hline(x, y, w):
        c.setStrokeColorRGB(0.4, 0.4, 0.4)
        c.setLineWidth(0.5)
        c.line(x, y, x + w, y)

    def sbox(x, y, w, h, title=None):
        c.setStrokeColorRGB(0.3, 0.3, 0.3)
        c.setLineWidth(0.5)
        c.rect(x, y, w, h, fill=0)
        if title:
            c.setFont(LABEL, SZ_SMALL)
            c.setFillColorRGB(0.2, 0.2, 0.2)
            c.drawString(x + 3, y + h - 8, title)

    def chk(x, y, checked=False):
        c.setStrokeColorRGB(0.3, 0.3, 0.3)
        c.setLineWidth(0.5)
        c.rect(x, y, 7, 7, fill=0)
        if checked:
            c.setFont(LABEL, 7)
            c.setFillColorRGB(0, 0, 0)
            c.drawString(x + 1, y + 0.5, "X")

    # ════════════════════════════════════════════════════════
    # PAGE 1
    # ════════════════════════════════════════════════════════

    # Header
    c.setFillColorRGB(0.0, 0.5, 0.0)
    c.rect(18, H - 34, 14, 18, fill=1, stroke=0)
    c.setFillColorRGB(1.0, 0.0, 0.0)
    c.rect(32, H - 34, 18, 18, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 13)
    c.setFillColorRGB(0.05, 0.05, 0.45)
    c.drawCentredString(W / 2, H - 20, "PORTUGAL")
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(W / 2, H - 31, "APPLICATION FOR NATIONAL VISA")
    c.setFont(VALUE, 6.5)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawCentredString(W / 2, H - 40, "(Residence and Temporary Stay)   —   This application form is free")
    hline(18, H - 44, W - 36)

    # Official use box (top right)
    sbox(W - 168, H - 105, 150, 58, "FOR OFFICIAL USE ONLY")
    lbl("Date of application:", W - 165, H - 65, SZ_SMALL)
    lbl("Application number:", W - 165, H - 76, SZ_SMALL)
    lbl("File handled by:", W - 165, H - 87, SZ_SMALL)
    lbl("Application lodged at:", W - 165, H - 98, SZ_SMALL)

    # Photo box
    sbox(W - 168, H - 192, 62, 78)
    lbl("PHOTO", W - 150, H - 156, SZ_SMALL)
    lbl("35x45mm", W - 152, H - 165, SZ_SMALL)

    # ── Fields 1-3: Names ────────────────────────────────────
    ROW = 26  # row height
    y = H - 58

    # Field 1 - Surname
    lbl("1. Surname (Family name):", 18, y)
    hline(18, y - 3, 355)
    val(data.get("surname", ""), 20, y - 3)

    y -= ROW
    # Field 2 - Surname at birth
    lbl("2. Surname at birth (Former family name(s)):", 18, y)
    hline(18, y - 3, 355)
    val(data.get("surname_at_birth", ""), 20, y - 3)

    y -= ROW
    # Field 3 - First name
    lbl("3. First name(s) (Given name(s)):", 18, y)
    hline(18, y - 3, 355)
    val(data.get("first_name", ""), 20, y - 3)

    # ── Fields 4-6: DOB, Place, Country ──────────────────────
    y -= ROW
    # Field 4
    lbl("4. Date of birth:", 18, y)
    hline(18, y - 3, 115)
    val(data.get("date_of_birth", ""), 20, y - 3)
    # Field 5
    lbl("5. Place of birth:", 148, y)
    hline(148, y - 3, 100)
    val(data.get("place_of_birth", ""), 150, y - 3)
    # Field 6
    lbl("6. Country of birth:", 262, y)
    hline(262, y - 3, 110)
    val(data.get("country_of_birth", ""), 264, y - 3)

    # ── Field 7: Nationality ──────────────────────────────────
    y -= ROW
    lbl("7. Current nationality:", 18, y)
    hline(18, y - 3, 130)
    val(data.get("nationality", ""), 20, y - 3)

    lbl("Nat. at birth (if diff.):", 162, y)
    hline(162, y - 3, 100)
    val(data.get("nationality_at_birth", ""), 164, y - 3)

    lbl("Other nationalities:", 276, y)
    hline(276, y - 3, 96)
    val(data.get("other_nationalities", ""), 278, y - 3)

    # ── Fields 8-9: Sex, Civil Status ────────────────────────
    y -= ROW
    lbl("8. Sex:", 18, y)
    sex = data.get("sex", "").strip().lower()
    is_male = sex == "male"
    is_female = sex == "female"
    chk(45, y - 5, is_male);   lbl("Male", 54, y - 4, SZ_SMALL)
    chk(78, y - 5, is_female); lbl("Female", 87, y - 4, SZ_SMALL)

    lbl("9. Civil status:", 130, y)
    civil = data.get("civil_status", "").strip().lower()
    civil_opts = [
        ("Single", 185), ("Married", 218), ("Reg.Partnership", 255),
        ("Separated", 315), ("Divorced", 358), ("Widow(er)", 400)
    ]
    for label_text, cx in civil_opts:
        chk(cx, y - 5, civil == label_text.lower())
        lbl(label_text, cx + 9, y - 4, 5.5)

    # ── Field 10: Parental authority ──────────────────────────
    y -= ROW
    lbl("10. Parental authority / legal guardian (if minor):", 18, y)
    hline(18, y - 3, W - 200)
    val(data.get("parental_authority", "N/A"), 20, y - 3)

    # ── Field 11: National ID ──────────────────────────────────
    y -= ROW
    lbl("11. National identity number (where applicable):", 18, y)
    hline(18, y - 3, 200)
    val(data.get("national_id_number", ""), 20, y - 3)

    # Supporting docs box (right side)
    sbox(W - 168, H - 355, 150, 100, "Supporting documents:")
    doc_items = ["Travel document", "Means of subsistence", "Invitation", "TMI", "Means of transport", "Other:"]
    for i, d in enumerate(doc_items):
        chk(W - 165, H - 320 - i * 13)
        lbl(d, W - 155, H - 319 - i * 13, SZ_SMALL)

    # Visa decision box
    sbox(W - 168, H - 465, 150, 100, "Visa decision:")
    chk(W - 165, H - 395); lbl("Refused", W - 155, H - 394, SZ_SMALL)
    chk(W - 165, H - 410); lbl("Issued:  ☐ E   ☐ D", W - 155, H - 409, SZ_SMALL)
    lbl("Valid From:", W - 165, H - 425, SZ_SMALL)
    hline(W - 130, H - 427, 112)
    lbl("Until:", W - 165, H - 440, SZ_SMALL)
    hline(W - 147, H - 442, 129)

    # ── Fields 12-16: Passport ────────────────────────────────
    y -= ROW
    lbl("12. Type of travel document:", 18, y)
    ptype = data.get("passport_type", "ordinary passport").strip().lower()
    chk(130, y - 5, "ordinary" in ptype); lbl("Ordinary passport", 139, y - 4, SZ_SMALL)
    chk(220, y - 5, "ordinary" not in ptype); lbl("Other (specify):", 229, y - 4, SZ_SMALL)
    if "ordinary" not in ptype and ptype:
        val(ptype, 295, y - 5, 7)

    y -= ROW
    lbl("13. Number of travel document:", 18, y)
    hline(18, y - 3, 110)
    val(data.get("passport_number", ""), 20, y - 3)

    lbl("14. Date of issue:", 142, y)
    hline(142, y - 3, 85)
    val(str(data.get("passport_issue_date", "")), 144, y - 3)

    lbl("15. Valid until:", 240, y)
    hline(240, y - 3, 85)
    val(str(data.get("passport_expiry", "")), 242, y - 3)

    lbl("16. Issued by (country):", 338, y)
    hline(338, y - 3, 34)
    val(data.get("passport_issued_by", ""), 340, y - 3)

    # ── Fields 17-18: EU N/A ──────────────────────────────────
    y -= ROW - 4
    lbl("17. Personal data of EU/EEA/CH family member: NOT APPLICABLE", 18, y, SZ_SMALL)
    y -= 11
    lbl("18. Family relationship with EU/EEA/CH citizen: NOT APPLICABLE", 18, y, SZ_SMALL)

    # ── Field 19: Address ─────────────────────────────────────
    y -= 18
    lbl("19. Applicant's home address:", 18, y)
    hline(18, y - 3, W - 36)
    val(data.get("home_address", ""), 20, y - 3)

    y -= ROW - 4
    lbl("E-mail:", 18, y)
    hline(40, y - 3, 165)
    val(data.get("email", ""), 42, y - 3)

    lbl("Telephone:", 220, y)
    hline(252, y - 3, 120)
    val(data.get("phone", ""), 254, y - 3)

    # ════════════════════════════════════════════════════════
    # PAGE 2
    # ════════════════════════════════════════════════════════
    c.showPage()

    c.setFont("Helvetica-Bold", 9)
    c.setFillColorRGB(0.05, 0.05, 0.45)
    c.drawCentredString(W / 2, H - 18, "PORTUGAL — APPLICATION FOR NATIONAL VISA (Page 2)")
    hline(18, H - 22, W - 36)

    y = H - 42

    # ── Field 20: Residence ───────────────────────────────────
    lbl("20. Residence in a country other than country of current nationality:", 18, y)
    chk(230, y - 5); lbl("No", 239, y - 4, SZ_SMALL)
    chk(255, y - 5); lbl("Yes. Residence permit No.:", 264, y - 4, SZ_SMALL)
    hline(340, y - 3, 80)
    lbl("Valid until:", 428, y - 4, SZ_SMALL)
    hline(462, y - 3, 80)

    # ── Field 21: Occupation ──────────────────────────────────
    y -= ROW
    lbl("*21. Current occupation:", 18, y)
    hline(18, y - 3, 240)
    val(data.get("current_occupation", ""), 20, y - 3)

    # ── Field 22: Employer ────────────────────────────────────
    y -= ROW
    lbl("*22. Employer and employer's address and telephone number:", 18, y)
    hline(18, y - 3, W - 36)
    employer = f"{data.get('employer_name', '')}   {data.get('employer_address', '')}"
    val(employer.strip(), 20, y - 3)

    # ── Field 23: Purpose ─────────────────────────────────────
    y -= ROW
    lbl("23. Purpose(s) of the journey:", 18, y)
    y -= 14
    purpose_val = data.get("purpose_of_journey", "").lower()
    purposes = [
        ("Study", "study"), ("Training", "training"), ("Work / Remote", "work"),
        ("Familiar Regrouping", "familiar"), ("Youth mobility", "youth"),
        ("Medical reason", "medical"), ("Retired/Religious", "retired"),
        ("Internship/Volunteering", "internship"),
        ("Other (Digital Nomad)", "nomad")
    ]
    px = 18
    for p_label, p_key in purposes:
        is_checked = p_key in purpose_val or ("remote" in purpose_val and p_key == "work") or ("nomad" in purpose_val and p_key == "nomad")
        chk(px, y - 5, is_checked)
        lbl(p_label, px + 9, y - 4, 5.5)
        px += len(p_label) * 4.2 + 20
        if px > W - 90:
            px = 18
            y -= 13

    # ── Field 24: Additional info ─────────────────────────────
    y -= 18
    lbl("24. Additional information on purpose of stay:", 18, y)
    hline(18, y - 3, W - 36)
    val(data.get("purpose_of_journey", "Digital Nomad / Remote Work — D8 Visa"), 20, y - 3)

    # ── Fields 25-27: Destination ────────────────────────────
    y -= ROW
    lbl("25. Member State of main destination:", 18, y)
    val("PORTUGAL", 160, y - 3)
    lbl("26. Member State of first entry:", 280, y)
    val("Portugal", 400, y - 3)

    y -= ROW - 4
    lbl("27. Number of entries requested:", 18, y)
    chk(140, y - 5); lbl("Two entries (residency)", 149, y - 4, SZ_SMALL)
    chk(250, y - 5, True); lbl("Multiple entries (temporary stay)", 259, y - 4, SZ_SMALL)

    y -= ROW - 4
    lbl("Intended date of arrival in Portugal:", 18, y)
    hline(165, y - 3, 95)
    val(str(data.get("arrival_date", "")), 167, y - 3)
    lbl("Intended date of departure:", 275, y)
    hline(375, y - 3, 95)
    val(str(data.get("departure_date", "")), 377, y - 3)

    # ── Fields 28-29: N/A ────────────────────────────────────
    y -= ROW - 4
    lbl("28. Fingerprints collected previously for Schengen visa: NOT APPLICABLE", 18, y, SZ_SMALL)
    y -= 11
    lbl("29. Entry permit for the final country of destination: NOT APPLICABLE", 18, y, SZ_SMALL)

    # ── Fields 30-31: Inviting person ────────────────────────
    y -= 18
    lbl("*30. Surname and first name of inviting person(s) / hotel(s) in Portugal:", 18, y)
    hline(18, y - 3, 210)
    val(data.get("inviting_person", ""), 20, y - 3)
    lbl("Address:", 238, y)
    hline(262, y - 3, 175)
    val(data.get("inviting_address", ""), 264, y - 3)

    y -= ROW
    lbl("Telephone:", 18, y)
    hline(55, y - 3, 100)
    lbl("E-mail:", 168, y)
    hline(192, y - 3, 120)

    y -= ROW - 4
    lbl("*31. Name and address of inviting company / organisation:", 18, y)
    hline(18, y - 3, W - 36)

    y -= ROW - 4
    lbl("Contact person — surname, first name, address, telephone:", 18, y)
    hline(18, y - 3, W - 36)

    # ── Field 32: Costs ───────────────────────────────────────
    y -= ROW
    lbl("*32. Cost of travelling and living during the applicant's stay is covered:", 18, y)
    y -= 14
    costs = data.get("costs_covered_by", "applicant").lower()
    chk(18, y - 5, "applicant" in costs)
    lbl("by the applicant himself/herself", 27, y - 4, SZ_SMALL)
    chk(180, y - 5, "sponsor" in costs)
    lbl("by a sponsor (host, company, organisation):", 189, y - 4, SZ_SMALL)

    y -= 14
    lbl("Means of support:", 18, y)
    means = ["Cash", "Traveller's cheques", "Credit card", "Pre-paid accommodation", "Pre-paid transport", "Other"]
    mx = 85
    for m in means:
        chk(mx, y - 5); lbl(m, mx + 9, y - 4, 5.5)
        mx += len(m) * 4.5 + 18
        if mx > W - 60:
            mx = 18; y -= 12

    # ── Health insurance ──────────────────────────────────────
    y -= 18
    lbl("Health / Travel Medical Insurance:", 18, y)
    hi = data.get("health_insurance", "").strip().lower()
    has_insurance = "yes" in hi or (bool(hi) and "no" not in hi)
    chk(165, y - 5, has_insurance); lbl("Yes", 174, y - 4, SZ_SMALL)
    chk(195, y - 5, not has_insurance); lbl("No", 204, y - 4, SZ_SMALL)
    if hi and "yes" in hi:
        val(data.get("health_insurance", ""), 220, y - 3, 7)

    # ── Declaration ───────────────────────────────────────────
    y -= 20
    hline(18, y, W - 36)
    y -= 10
    declaration = (
        "I am aware that the visa fee is not refunded if the visa is refused. I declare that to the best "
        "of my knowledge all particulars supplied by me are correct and complete. I am aware that any false "
        "statements will lead to my application being rejected or to the annulment of a visa already granted "
        "and may also render me liable to prosecution under the Portuguese law. I undertake to leave Portugal "
        "before the expiry of the visa, if granted. I have been informed that possession of a visa is only one "
        "of the prerequisites for entry into Portugal. The mere fact that a visa has been granted to me does "
        "not mean that I will be entitled to compensation if I fail to comply with the national legislation."
    )
    c.setFont(VALUE, 5.5)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    for line in simpleSplit(declaration, VALUE, 5.5, W - 36):
        c.drawString(18, y, line)
        y -= 7.5

    # ── Signature ─────────────────────────────────────────────
    y -= 16
    hline(18, y, W - 36)
    y -= 14
    lbl("Place and date:", 18, y)
    hline(85, y - 3, 150)
    lbl("Signature:", 255, y)
    hline(290, y - 3, 200)

    # ── Footer ────────────────────────────────────────────────
    c.setFont(VALUE, 5.5)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawCentredString(W / 2, 16, f"Generated by Global Access — globalaccess.com — {datetime.now().strftime('%B %d, %Y')}")

    c.save()
    buffer.seek(0)
    return buffer.read()
