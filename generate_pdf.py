"""
Portugal Visa PDF - Two Line Layout
Label on top line, value on the line below it. No overlapping.
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from datetime import datetime
import io

W, H = A4

def fmt_date(d):
    if not d: return ""
    try:
        p = str(d).split("-")
        if len(p) == 3: return f"{p[2]}-{p[1]}-{p[0]}"
    except: pass
    return str(d)

def generate_visa_pdf_bytes(data: dict) -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    c.setTitle("Portugal National Visa Application")

    LBL = "Helvetica-Bold"
    VAL = "Helvetica"
    LS  = 6.5   # label font size
    VS  = 9     # value font size

    def lbl(t, x, y, sz=LS):
        """Draw label text"""
        c.setFont(LBL, sz)
        c.setFillColorRGB(0.25, 0.25, 0.25)
        c.drawString(x, y, t)

    def val(t, x, y, sz=VS):
        """Draw value text ON the line (line is at y, text sits just above)"""
        c.setFont(VAL, sz)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(x, y + 2, str(t) if t else "")

    def field(label_text, value_text, x, y, line_width, label_size=LS, value_size=VS):
        """
        Two-line field layout:
        Line 1 (y):      Label text
        Line 2 (y-13):   Underline + value text on it
        Returns y-13 (the line position)
        """
        lbl(label_text, x, y, label_size)
        hl(x, y - 13, line_width)
        val(value_text, x + 2, y - 13, value_size)
        return y - 13

    def hl(x, y, w):
        c.setStrokeColorRGB(0.45, 0.45, 0.45)
        c.setLineWidth(0.4)
        c.line(x, y, x + w, y)

    def box(x, y, w, h, title=None):
        c.setStrokeColorRGB(0.35, 0.35, 0.35)
        c.setLineWidth(0.5)
        c.rect(x, y, w, h, fill=0)
        if title:
            c.setFont(LBL, 6)
            c.setFillColorRGB(0.2, 0.2, 0.2)
            c.drawString(x + 3, y + h - 8, title)

    def chk(x, y, checked=False):
        c.setStrokeColorRGB(0.3, 0.3, 0.3)
        c.setLineWidth(0.4)
        c.rect(x, y, 7, 7, fill=0)
        if checked:
            c.setFont(LBL, 7)
            c.setFillColorRGB(0, 0, 0)
            c.drawString(x + 1, y + 0.5, "X")

    GAP = 28  # gap between fields

    # ══════════════════════════════════════════════
    # PAGE 1
    # ══════════════════════════════════════════════

    # Header
    c.setFillColorRGB(0, 0.5, 0)
    c.rect(18, H - 33, 13, 17, fill=1, stroke=0)
    c.setFillColorRGB(1, 0, 0)
    c.rect(31, H - 33, 17, 17, fill=1, stroke=0)
    c.setFont(LBL, 13)
    c.setFillColorRGB(0.05, 0.05, 0.45)
    c.drawCentredString(W / 2, H - 19, "PORTUGAL")
    c.setFont(LBL, 9)
    c.drawCentredString(W / 2, H - 30, "APPLICATION FOR NATIONAL VISA")
    c.setFont(VAL, 6.5)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawCentredString(W / 2, H - 39, "(Residence and Temporary Stay)  —  This application form is free")
    hl(18, H - 43, W - 36)

    # Official use box
    box(W - 158, H - 110, 140, 65, "FOR OFFICIAL USE ONLY")
    lbl("Date of application:", W - 155, H - 66, 5.5)
    lbl("Application number:", W - 155, H - 77, 5.5)
    lbl("File handled by:", W - 155, H - 88, 5.5)
    lbl("Application lodged at:", W - 155, H - 99, 5.5)

    # Photo box
    box(W - 158, H - 200, 60, 80)
    lbl("PHOTO", W - 141, H - 162, 6)
    lbl("35x45mm", W - 143, H - 173, 5.5)

    # ── Fields 1-3: Full width names ──────────────────────
    y = H - 57

    # Field 1
    lbl("1. Surname (Family name):", 18, y)
    y -= 13
    hl(18, y, 370)
    val(data.get("surname", ""), 20, y)

    y -= GAP
    # Field 2
    lbl("2. Surname at birth (Former family name(s)):", 18, y)
    y -= 13
    hl(18, y, 370)
    val(data.get("surname_at_birth", ""), 20, y)

    y -= GAP
    # Field 3
    lbl("3. First name(s) (Given name(s)):", 18, y)
    y -= 13
    hl(18, y, 370)
    val(data.get("first_name", ""), 20, y)

    # ── Field 4: Date of birth (own row) ─────────────────
    y -= GAP
    lbl("4. Date of birth (DD-MM-YYYY):", 18, y)
    y -= 13
    hl(18, y, 130)
    val(fmt_date(data.get("date_of_birth", "")), 20, y)

    # ── Field 5: Place of birth (own row) ────────────────
    y -= GAP
    lbl("5. Place of birth:", 18, y)
    y -= 13
    hl(18, y, 170)
    val(data.get("place_of_birth", ""), 20, y)

    # ── Field 6: Country of birth (own row) ──────────────
    y -= GAP
    lbl("6. Country of birth:", 18, y)
    y -= 13
    hl(18, y, 170)
    val(data.get("country_of_birth", ""), 20, y)

    # Application lodged at box (right side)
    box(W - 158, H - 365, 140, 90, "APPLICATION LODGED AT:")
    chk(W - 155, H - 300); lbl("Embassy/Consulate", W - 144, H - 299, 5.5)
    chk(W - 155, H - 315); lbl("Service provider", W - 144, H - 314, 5.5)
    chk(W - 155, H - 330); lbl("Commercial intermediary", W - 144, H - 329, 5.5)
    chk(W - 155, H - 345); lbl("Other:", W - 144, H - 344, 5.5)

    # ── Field 7a: Current nationality ────────────────────
    y -= GAP
    lbl("7. Current nationality:", 18, y)
    y -= 13
    hl(18, y, 170)
    val(data.get("nationality", ""), 20, y)

    # ── Field 7b: Nationality at birth ───────────────────
    y -= GAP
    lbl("   Nationality at birth, if different:", 18, y)
    y -= 13
    hl(18, y, 170)
    val(data.get("nationality_at_birth", ""), 20, y)

    # ── Field 7c: Other nationalities ────────────────────
    y -= GAP
    lbl("   Other nationalities:", 18, y)
    y -= 13
    hl(18, y, 170)
    val(data.get("other_nationalities", ""), 20, y)

    # ── Field 8: Sex ──────────────────────────────────────
    y -= GAP
    lbl("8. Sex:", 18, y)
    sex = data.get("sex", "").strip().lower()
    chk(48, y - 5, sex == "male");   lbl("Male",   58, y - 4, 7)
    chk(88, y - 5, sex == "female"); lbl("Female", 98, y - 4, 7)

    # ── Field 9: Civil status ─────────────────────────────
    lbl("9. Civil status:", 150, y)
    civil = data.get("civil_status", "").strip().lower()
    civil_opts = [
        ("Single", 210), ("Married", 252), ("Reg.Part.", 295),
        ("Separated", 345), ("Divorced", 395), ("Widow(er)", 440)
    ]
    for c_lbl, cx in civil_opts:
        chk(cx, y - 5, civil in c_lbl.lower())
        lbl(c_lbl, cx + 9, y - 4, 5.5)

    # ── Field 10: Parental authority ─────────────────────
    y -= GAP
    lbl("10. Parental authority / legal guardian (if minor):", 18, y)
    y -= 13
    hl(18, y, W - 36)
    val(data.get("parental_authority", "N/A"), 20, y)

    # ── Field 11: National ID ─────────────────────────────
    y -= GAP
    lbl("11. National identity number (where applicable):", 18, y)
    y -= 13
    hl(18, y, 210)
    val(data.get("national_id_number", ""), 20, y)

    # Supporting docs box
    box(W - 158, H - 510, 140, 110, "Supporting documents:")
    for i, d in enumerate(["Travel document", "Means of subsistence", "Invitation", "TMI", "Means of transport", "Other:"]):
        chk(W - 155, H - 435 - i * 14)
        lbl(d, W - 144, H - 434 - i * 14, 5.5)

    # Visa decision box
    box(W - 158, H - 635, 140, 115, "Visa decision:")
    chk(W - 155, H - 548); lbl("Refused", W - 144, H - 547, 5.5)
    chk(W - 155, H - 563); lbl("Issued:  E   D", W - 144, H - 562, 5.5)
    lbl("Valid From:", W - 155, H - 580, 5.5); hl(W - 122, H - 582, 104)
    lbl("Until:", W - 155, H - 597, 5.5); hl(W - 138, H - 599, 120)

    # ── Field 12: Passport type ───────────────────────────
    y -= GAP
    lbl("12. Type of travel document:", 18, y)
    ptype = data.get("passport_type", "Ordinary Passport").strip().lower()
    chk(148, y - 5, "ordinary" in ptype); lbl("Ordinary passport", 158, y - 4, 6.5)
    chk(255, y - 5, "ordinary" not in ptype); lbl("Other (specify):", 265, y - 4, 6.5)
    if "ordinary" not in ptype and ptype:
        val(data.get("passport_type", ""), 340, y - 5, 7)

    # ── Field 13: Passport number ────────────────────────
    y -= GAP
    lbl("13. Number of travel document:", 18, y)
    y -= 13
    hl(18, y, 130)
    val(data.get("passport_number", ""), 20, y)

    # ── Field 14: Date of issue ───────────────────────────
    y -= GAP
    lbl("14. Date of issue (DD-MM-YYYY):", 18, y)
    y -= 13
    hl(18, y, 130)
    val(fmt_date(data.get("passport_issue_date", "")), 20, y)

    # ── Field 15: Valid until ─────────────────────────────
    y -= GAP
    lbl("15. Valid until (DD-MM-YYYY):", 18, y)
    y -= 13
    hl(18, y, 130)
    val(fmt_date(data.get("passport_expiry", "")), 20, y)

    # ── Field 16: Issued by ───────────────────────────────
    y -= GAP
    lbl("16. Issued by (country):", 18, y)
    y -= 13
    hl(18, y, 170)
    val(data.get("passport_issued_by", ""), 20, y)

    # ── Fields 17-18: N/A ────────────────────────────────
    y -= GAP - 4
    lbl("17. Personal data of EU/EEA/CH family member: NOT APPLICABLE", 18, y, 6)
    y -= 13
    lbl("18. Family relationship with EU/EEA/CH citizen: NOT APPLICABLE", 18, y, 6)

    # ── Field 19: Address ─────────────────────────────────
    y -= GAP
    lbl("19. Applicant's home address:", 18, y)
    y -= 13
    hl(18, y, W - 36)
    val(data.get("home_address", ""), 20, y)

    y -= GAP
    lbl("E-mail:", 18, y)
    y -= 13
    hl(18, y, 200)
    val(data.get("email", ""), 20, y)

    y -= GAP
    lbl("Telephone:", 18, y)
    y -= 13
    hl(18, y, 150)
    val(data.get("phone", ""), 20, y)

    # ══════════════════════════════════════════════
    # PAGE 2
    # ══════════════════════════════════════════════
    c.showPage()
    c.setFont(LBL, 9)
    c.setFillColorRGB(0.05, 0.05, 0.45)
    c.drawCentredString(W / 2, H - 18, "PORTUGAL — APPLICATION FOR NATIONAL VISA (Page 2)")
    hl(18, H - 22, W - 36)

    y = H - 45

    # ── Field 20: Residence ───────────────────────────────
    lbl("20. Residence in a country other than country of current nationality:", 18, y)
    chk(248, y - 5); lbl("No", 258, y - 4, 6.5)
    chk(278, y - 5); lbl("Yes — Permit No.:", 288, y - 4, 6.5)
    hl(355, y - 5, 80)
    lbl("Valid until:", 442, y - 4, 6); hl(475, y - 5, 78)

    # ── Field 21: Occupation ──────────────────────────────
    y -= GAP
    lbl("*21. Current occupation:", 18, y)
    y -= 13
    hl(18, y, 260)
    val(data.get("current_occupation", ""), 20, y)

    # ── Field 22: Employer name ───────────────────────────
    y -= GAP
    lbl("*22. Employer name:", 18, y)
    y -= 13
    hl(18, y, W - 36)
    val(data.get("employer_name", ""), 20, y)

    y -= GAP
    lbl("    Employer address:", 18, y)
    y -= 13
    hl(18, y, W - 36)
    val(data.get("employer_address", ""), 20, y)

    # ── Field 23: Purpose ─────────────────────────────────
    y -= GAP
    lbl("23. Purpose(s) of the journey:", 18, y)
    y -= 16
    purpose_val = data.get("purpose_of_journey", "").lower()
    purposes = [
        ("Study", "study"), ("Training", "training"), ("Work / Remote", "work"),
        ("Familiar Regrouping", "familiar"), ("Youth mobility", "youth"),
        ("Medical reason", "medical"), ("Retired/Religious", "retired"),
        ("Internship/Volunteering", "internship"), ("Other (Digital Nomad)", "nomad"),
    ]
    px = 18
    for p_lbl2, p_key in purposes:
        is_chk = (p_key in purpose_val or
                  ("remote" in purpose_val and p_key == "work") or
                  ("nomad" in purpose_val and p_key == "nomad") or
                  ("digital" in purpose_val and p_key == "nomad"))
        chk(px, y - 5, is_chk)
        lbl(p_lbl2, px + 10, y - 4, 6)
        px += len(p_lbl2) * 4 + 22
        if px > W - 100: px = 18; y -= 14

    # ── Field 24: Additional info ─────────────────────────
    y -= GAP - 4
    lbl("24. Additional information on purpose of stay:", 18, y)
    y -= 13
    hl(18, y, W - 36)
    val(data.get("purpose_of_journey", "Digital Nomad / Remote Work"), 20, y)

    # ── Fields 25-26 ──────────────────────────────────────
    y -= GAP
    lbl("25. Member State of main destination:", 18, y)
    val("PORTUGAL", 178, y - 2)
    lbl("26. Member State of first entry:", 290, y)
    val("Portugal", 412, y - 2)

    # ── Field 27: Entries ─────────────────────────────────
    y -= GAP
    lbl("27. Number of entries requested:", 18, y)
    chk(158, y - 5); lbl("Two entries (residency)", 169, y - 4, 6.5)
    chk(275, y - 5, True); lbl("Multiple entries (temporary stay)", 286, y - 4, 6.5)

    y -= GAP
    lbl("Intended date of arrival in Portugal:", 18, y)
    y -= 13
    hl(18, y, 110)
    val(fmt_date(data.get("arrival_date", "")), 20, y)

    y -= GAP
    lbl("Intended date of departure from Portugal:", 18, y)
    y -= 13
    hl(18, y, 110)
    val(fmt_date(data.get("departure_date", "")), 20, y)

    # ── Fields 28-29: N/A ────────────────────────────────
    y -= GAP - 4
    lbl("28. Fingerprints collected previously for Schengen visa: NOT APPLICABLE", 18, y, 6)
    y -= 12
    lbl("29. Entry permit for the final country of destination: NOT APPLICABLE", 18, y, 6)

    # ── Field 30: Inviting person ─────────────────────────
    y -= GAP
    lbl("*30. Surname and first name of inviting person(s) / hotel(s):", 18, y)
    y -= 13
    hl(18, y, 260)
    val(data.get("inviting_person", ""), 20, y)

    y -= GAP
    lbl("    Address of inviting person / hotel:", 18, y)
    y -= 13
    hl(18, y, W - 36)
    val(data.get("inviting_address", ""), 20, y)

    y -= GAP
    lbl("    Telephone:", 18, y); hl(65, y - 13, 110)
    lbl("    E-mail:", 190, y); hl(222, y - 13, 130)

    # ── Field 31: Company ─────────────────────────────────
    y -= GAP
    lbl("*31. Name and address of inviting company / organisation:", 18, y)
    y -= 13
    hl(18, y, W - 36)

    y -= GAP
    lbl("    Contact person (surname, first name, address, telephone, e-mail):", 18, y)
    y -= 13
    hl(18, y, W - 36)

    # ── Field 32: Costs ───────────────────────────────────
    y -= GAP
    lbl("*32. Cost of travelling and living during the applicant's stay is covered:", 18, y)
    y -= 16
    costs = data.get("costs_covered_by", "applicant").lower()
    chk(18, y - 5, "applicant" in costs)
    lbl("by the applicant himself/herself", 28, y - 4, 6.5)
    chk(188, y - 5, "sponsor" in costs)
    lbl("by a sponsor (host, company, organisation):", 198, y - 4, 6.5)

    y -= 18
    lbl("Means of support:", 18, y)
    mx = 90
    for m in ["Cash", "Traveller's cheques", "Credit card", "Pre-paid accommodation", "Pre-paid transport", "Other"]:
        chk(mx, y - 5); lbl(m, mx + 10, y - 4, 6)
        mx += len(m) * 4.2 + 20
        if mx > W - 60: mx = 18; y -= 13

    # ── Health insurance ──────────────────────────────────
    y -= GAP
    lbl("Health / Travel Medical Insurance:", 18, y)
    hi = data.get("health_insurance", "").strip().lower()
    has_yes = "yes" in hi or (bool(hi) and not hi.startswith("no"))
    chk(172, y - 5, has_yes);     lbl("Yes", 182, y - 4, 6.5)
    chk(205, y - 5, not has_yes); lbl("No",  215, y - 4, 6.5)

    # ── Declaration ───────────────────────────────────────
    y -= 22
    hl(18, y, W - 36)
    y -= 10
    decl = (
        "I am aware that the visa fee is not refunded if the visa is refused. I declare that to the best of my knowledge "
        "all particulars supplied by me are correct and complete. I am aware that any false statements will lead to my "
        "application being rejected or to the annulment of a visa already granted and may also render me liable to "
        "prosecution under the Portuguese law. I undertake to leave Portugal before the expiry of the visa, if granted. "
        "I have been informed that possession of a visa is only one of the prerequisites for entry into Portugal. "
        "The mere fact that a visa has been granted to me does not mean that I will be entitled to compensation if "
        "I fail to comply with the national legislation applicable."
    )
    c.setFont(VAL, 5.5)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    for line in simpleSplit(decl, VAL, 5.5, W - 36):
        c.drawString(18, y, line); y -= 7.5

    # ── Signature ─────────────────────────────────────────
    y -= 18
    hl(18, y, W - 36)
    y -= 15
    lbl("Place and date:", 18, y); hl(85, y - 13, 150)
    lbl("Signature:", 255, y);     hl(292, y - 13, 200)

    # ── Footer ────────────────────────────────────────────
    c.setFont(VAL, 5.5)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawCentredString(W / 2, 16, f"Generated by Global Access — globalaccess.com — {datetime.now().strftime('%B %d, %Y')}")

    c.save()
    buf.seek(0)
    return buf.read()
