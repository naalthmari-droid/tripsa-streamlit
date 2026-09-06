"""TRIPSA — Export the Final Plan to a clean, shareable PDF."""
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

OLIVE = colors.HexColor("#2f5233")
GOLD = colors.HexColor("#c9a24b")
SAND = colors.HexColor("#f6f1e7")
INK = colors.HexColor("#1c2b21")
MUTED = colors.HexColor("#6b7560")


def _styles():
    ss = getSampleStyleSheet()
    return {
        "brand": ParagraphStyle("brand", parent=ss["Normal"], textColor=GOLD,
                                fontName="Helvetica-Bold", fontSize=11, spaceAfter=2),
        "title": ParagraphStyle("title", parent=ss["Title"], textColor=OLIVE,
                                fontName="Helvetica-Bold", fontSize=22, spaceAfter=4),
        "meta": ParagraphStyle("meta", parent=ss["Normal"], textColor=MUTED, fontSize=10, spaceAfter=10),
        "h2": ParagraphStyle("h2", parent=ss["Heading2"], textColor=OLIVE,
                             fontName="Helvetica-Bold", fontSize=14, spaceBefore=10, spaceAfter=4),
        "stop": ParagraphStyle("stop", parent=ss["Normal"], textColor=INK,
                               fontName="Helvetica-Bold", fontSize=12, spaceAfter=2),
        "sub": ParagraphStyle("sub", parent=ss["Normal"], textColor=MUTED, fontSize=9, spaceAfter=4),
        "act": ParagraphStyle("act", parent=ss["Normal"], textColor=INK, fontSize=9.5,
                              leftIndent=14, spaceAfter=2),
        "day": ParagraphStyle("day", parent=ss["Normal"], textColor=GOLD,
                              fontName="Helvetica-Bold", fontSize=10, spaceBefore=4, spaceAfter=2),
    }


def build_final_plan_pdf(trip, members=None):
    """Build a PDF (bytes) of the trip's final shared plan."""
    import engine, data
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=1.6 * cm, bottomMargin=1.6 * cm,
                            leftMargin=1.8 * cm, rightMargin=1.8 * cm, title="TRIPSA Final Plan")
    st = _styles()
    el = []

    # Header
    el.append(Paragraph("T R I P S A", st["brand"]))
    el.append(Paragraph(trip.get("title", "Trip"), st["title"]))
    meta = f'{trip.get("start_date", "")} → {trip.get("end_date", "")} · {trip.get("travelers", "")} travelers · Invite {trip.get("invite_code", "")}'
    el.append(Paragraph(meta, st["meta"]))
    el.append(HRFlowable(width="100%", thickness=1, color=GOLD))
    el.append(Spacer(1, 8))

    # Route summary
    route = trip.get("route", {})
    stops = route.get("stops", [])
    summary = [["Total distance", "Travel time", "Est. cost"]]
    summary.append([
        f'{route.get("total_distance_km", 0):,} km',
        f'{route.get("total_duration_min", 0) // 60}h {route.get("total_duration_min", 0) % 60}m',
        f'SAR {route.get("estimated_cost", 0):,}',
    ])
    tbl = Table(summary, colWidths=[5.4 * cm] * 3)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), OLIVE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, 1), SAND),
        ("TEXTCOLOR", (0, 1), (-1, 1), INK),
        ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#e3dcc6")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    el.append(tbl)
    el.append(Spacer(1, 12))

    # Members
    if members:
        names = ", ".join(f'#{m.get("seq", i + 1)} {m["name"]}' for i, m in enumerate(members))
        el.append(Paragraph(f"Group: {names}", st["sub"]))
        el.append(Spacer(1, 6))

    # Per-stop schedule
    el.append(Paragraph("Final itinerary", st["h2"]))
    for s in stops:
        el.append(Paragraph(f'{s["order"]}. {s["name"]}', st["stop"]))
        el.append(Paragraph(
            f'{s["nights"]} night(s) · {str(s["check_in"])[:10]} → {str(s["check_out"])[:10]}',
            st["sub"]))
        try:
            days = engine.schedule_trip_days(s["destination_id"], s["nights"],
                                             trip.get("day_start", 9), trip.get("day_end", 22),
                                             trip.get("pace", "moderate"), trip.get("cuisines", []))
            for di, acts in enumerate(days, 1):
                el.append(Paragraph(f"Day {di}", st["day"]))
                for a in acts:
                    star = f'  ★{a["rating"]}' if a.get("rating") else ""
                    el.append(Paragraph(f'{a["time"]}–{a["end"]}   {a["label"]}{star}', st["act"]))
        except Exception:
            pass
        el.append(Spacer(1, 6))

    el.append(Spacer(1, 10))
    el.append(HRFlowable(width="100%", thickness=0.6, color=GOLD))
    el.append(Paragraph("Generated by TRIPSA — Saudi Route Intelligence", st["meta"]))

    doc.build(el)
    return buf.getvalue()
