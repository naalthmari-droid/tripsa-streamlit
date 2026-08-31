"""TRIPSA — email notifications via SMTP (Streamlit Secrets) with a safe demo mode.

Configure in Streamlit Cloud → Settings → Secrets:
    SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, FROM_EMAIL
If not configured, emails are logged to the `notifications` table (demo mode).
"""
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

import db


def _smtp_config():
    try:
        import streamlit as st
        s = st.secrets
        return {
            "host": s.get("SMTP_HOST"),
            "port": int(s.get("SMTP_PORT", 587)),
            "user": s.get("SMTP_USER"),
            "password": s.get("SMTP_PASSWORD"),
            "from_email": s.get("FROM_EMAIL", s.get("SMTP_USER", "no-reply@tripsa.app")),
        }
    except Exception:
        return {}


def is_configured():
    c = _smtp_config()
    return bool(c.get("host") and c.get("user") and c.get("password"))


def _send(to_email, subject, html_body):
    """Send an email; returns (ok, mode). mode='smtp' or 'demo'."""
    if not to_email:
        return False, "no-recipient"
    cfg = _smtp_config()
    if is_configured():
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = cfg["from_email"]
            msg["To"] = to_email
            msg.attach(MIMEText(html_body, "html"))
            ctx = ssl.create_default_context()
            with smtplib.SMTP(cfg["host"], cfg["port"], timeout=20) as server:
                server.starttls(context=ctx)
                server.login(cfg["user"], cfg["password"])
                server.sendmail(cfg["from_email"], [to_email], msg.as_string())
            db.log_notification(to_email, subject, "sent")
            return True, "smtp"
        except Exception:
            db.log_notification(to_email, subject, "failed")
            return False, "smtp-error"
    # demo mode — log only
    db.log_notification(to_email, subject, "demo")
    return True, "demo"


def _wrap(title, body_html):
    return f"""
    <div style="font-family:Arial,sans-serif;background:#f6f1e3;padding:24px">
      <div style="max-width:560px;margin:auto;background:#fff;border-radius:16px;
                  overflow:hidden;border:1px solid #eee4c9">
        <div style="background:linear-gradient(135deg,#2f5233,#3e6b44);color:#fff;
                    padding:20px 24px;font-size:20px;font-weight:700">
          ✈️ TRIPSA — {title}
        </div>
        <div style="padding:24px;color:#1c2b21;font-size:15px;line-height:1.6">
          {body_html}
          <p style="color:#7a7361;font-size:12px;margin-top:24px">
            This is an automated message from TRIPSA. Safe travels!
          </p>
        </div>
      </div>
    </div>"""


# ----------------------------- Event notifications -----------------------------
def notify_trip_created(to_email, owner, title, invite_code, start, end):
    body = f"""
      <p>Hi <b>{owner}</b>,</p>
      <p>Your trip <b>"{title}"</b> is confirmed! 🎉</p>
      <p><b>Dates:</b> {start} → {end}<br/>
         <b>Invite code:</b> <span style="background:#f1ead6;padding:2px 8px;
         border-radius:8px;font-weight:700">{invite_code}</span></p>
      <p>Share the code so your group can join, vote and plan together.</p>"""
    return _send(to_email, f"Trip confirmed: {title}", _wrap("Trip confirmed", body))


def notify_member_joined(to_email, owner, member, title):
    body = f"""
      <p>Hi <b>{owner}</b>,</p>
      <p><b>{member}</b> just joined your trip <b>"{title}"</b>.</p>
      <p>Open the group room to see their preferences and votes.</p>"""
    return _send(to_email, f"{member} joined {title}", _wrap("New member", body))


def notify_trip_updated(to_email, name, title, change_desc):
    body = f"""
      <p>Hi <b>{name}</b>,</p>
      <p>The trip <b>"{title}"</b> was updated:</p>
      <p style="background:#f7f2e4;padding:12px;border-radius:10px">{change_desc}</p>
      <p>Open the trip to review the latest details.</p>"""
    return _send(to_email, f"Trip updated: {title}", _wrap("Trip updated", body))
