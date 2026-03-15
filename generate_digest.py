#!/usr/bin/env python3
"""
Weekly AI Art Opportunities Digest Generator
מייצר עמוד HTML שבועי עם הזדמנויות לאמנות AI — ישראל ובינלאומי
"""

import anthropic
import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

HEBREW_MONTHS = [
    "ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני",
    "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"
]

RECIPIENT_EMAIL = "miritronicohen@gmail.com"
SENDER_EMAIL    = "miritronicohen@gmail.com"
SITE_URL        = "https://mirittc-prog.github.io"


def hebrew_date():
    now = datetime.now()
    return f"{now.day} ב{HEBREW_MONTHS[now.month - 1]} {now.year}"

def issue_number():
    now = datetime.now()
    base = datetime(2026, 3, 15)
    return max(1, int((now - base).days / 7) + 1)


def generate_html(client, date_str, issue):
    print("🔍 Searching and generating HTML...")

    prompt = f"""חפש ברשת הזדמנויות עדכניות לאמנות AI לשנת 2026. חפש את:
1. "AI film festival open call 2026"
2. "AI art competition open call 2026"
3. "AI video art exhibition 2026"
4. "AI art residency fellowship 2026"
5. "קול קורא אמנות AI ישראל 2026"

אחרי החיפוש, צור עמוד HTML מלא ומושלם בעברית.

דרישות עיצוב:
- כיוון RTL, שפה עברית
- רקע כהה: #0d0d14 | כרטיסים: #1e1e2e עם גבול #2a2a3e
- אקסנט בינלאומי: #e94560 | אקסנט ישראל: #4a9eff
- כל CSS ו-JS מוטמעים בקובץ אחד | מגיב למובייל

מבנה:
1. navbar: "🤖 הזדמנויות AI" + {date_str} (sticky)
2. hero: כותרת, גיליון #{issue}, סטטיסטיקות לפי קטגוריה
3. טאבים: הכל / פסטיבלי סרטים / אמנות / שהיות / 🇮🇱 ישראל
4. סקציות: 🎬 פסטיבלים · 🖼️ קולות קוראים · 🏛️ שהיות · מפריד ישראל · 🇮🇱 ישראל
5. footer: "נוצר אוטומטית על ידי Claude · {date_str}"

כרטיס: כותרת, תגיות (דדליין/מיקום/חינם), תיאור 2-3 משפטים, כפתור קישור.
תגית "⚠️ דחוף!" מהבהבת אם הדדליין בשבועיים הקרובים.
JS: showTab() לפילטור לפי קטגוריה.

החזר אך ורק HTML מלא מ-<!DOCTYPE html> עד </html>, ללא שום טקסט אחר."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=16000,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": prompt}]
    )

    html = ""
    for block in response.content:
        if hasattr(block, "text") and block.text:
            html += block.text

    if "<!DOCTYPE" in html:
        start = html.find("<!DOCTYPE")
        end = html.rfind("</html>") + 7
        if end > start:
            html = html[start:end]

    if "<!DOCTYPE" not in html or "</html>" not in html:
        print(f"❌ No valid HTML generated\nPreview: {html[:300]}")
        sys.exit(1)

    return html


def send_notification_email(date_str, issue, app_password):
    print("📧 Sending notification email...")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🤖 גיליון #{issue} עודכן — הזדמנויות AI חדשות מחכות לך!"
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = RECIPIENT_EMAIL

    html_body = f"""<!DOCTYPE html>
<html dir="rtl" lang="he">
<head><meta charset="UTF-8"></head>
<body style="font-family:Arial,sans-serif;background:#f5f5f5;margin:0;padding:20px;direction:rtl;">
  <div style="max-width:520px;margin:0 auto;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.1);">

    <div style="background:linear-gradient(135deg,#1a1a2e,#0f3460);padding:32px;text-align:center;">
      <div style="font-size:36px;margin-bottom:8px;">🤖</div>
      <h1 style="color:#e94560;margin:0;font-size:20px;">הזדמנויות AI — גיליון #{issue}</h1>
      <p style="color:#aaa;margin:6px 0 0;font-size:13px;">{date_str}</p>
    </div>

    <div style="padding:28px 32px;">
      <p style="font-size:16px;color:#333;line-height:1.6;">היי מירית! 👋</p>
      <p style="font-size:15px;color:#555;line-height:1.7;">
        הגיליון השבועי שלך עודכן ומוכן לצפייה —<br>
        תחרויות, קולות קוראים, שהיות ומענקים לאמנות AI.
      </p>

      <div style="text-align:center;margin:28px 0;">
        <a href="{SITE_URL}" style="background:#e94560;color:white;text-decoration:none;padding:14px 36px;border-radius:8px;font-size:16px;font-weight:bold;display:inline-block;">
          לצפייה בגיליון ←
        </a>
      </div>

      <p style="font-size:13px;color:#999;border-top:1px solid #eee;padding-top:16px;margin-top:8px;">
        נשלח אוטומטית על ידי Claude · {date_str}<br>
        <a href="{SITE_URL}" style="color:#7c6af5;">{SITE_URL}</a>
      </p>
    </div>

  </div>
</body>
</html>"""

    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER_EMAIL, app_password)
        server.send_message(msg)

    print(f"✅ Email sent to {RECIPIENT_EMAIL}")


def main():
    # בדיקת משתני סביבה
    api_key      = os.environ.get("ANTHROPIC_API_KEY")
    app_password = os.environ.get("GMAIL_APP_PASSWORD", "").replace('\xa0', '').replace(' ', '').strip()
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not set")
        sys.exit(1)
    if not app_password:
        print("❌ GMAIL_APP_PASSWORD not set")
        sys.exit(1)

    client    = anthropic.Anthropic(api_key=api_key)
    date_str  = hebrew_date()
    issue     = issue_number()

    print(f"📅 Generating digest — {date_str} (Issue #{issue})")

    # 1. יצירת HTML
    html = generate_html(client, date_str, issue)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ index.html saved ({len(html):,} chars)")

    # 2. שליחת מייל
    send_notification_email(date_str, issue, app_password)


if __name__ == "__main__":
    main()
