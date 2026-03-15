#!/usr/bin/env python3
"""
Weekly AI Art Opportunities Digest Generator
מייצר עמוד HTML שבועי עם הזדמנויות לאמנות AI — ישראל ובינלאומי
גרסה 2: קריאה אחת לAPI (חיפוש + יצירת HTML ביחד)
"""

import anthropic
import os
import sys
from datetime import datetime

HEBREW_MONTHS = [
    "ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני",
    "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"
]

def hebrew_date():
    now = datetime.now()
    return f"{now.day} ב{HEBREW_MONTHS[now.month - 1]} {now.year}"

def issue_number():
    now = datetime.now()
    base = datetime(2026, 3, 15)
    weeks = max(1, int((now - base).days / 7) + 1)
    return weeks


def generate_digest():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY not set")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    date_str = hebrew_date()
    issue = issue_number()

    print(f"📅 Generating digest for {date_str} (Issue #{issue})...")
    print("🔍 Searching and generating HTML in one pass...")

    prompt = f"""חפש ברשת הזדמנויות עדכניות לאמנות AI לשנת 2026. חפש את:
1. "AI film festival open call 2026"
2. "AI art competition open call 2026"
3. "AI video art exhibition 2026"
4. "AI art residency fellowship 2026"
5. "קול קורא אמנות AI ישראל 2026"

אחרי החיפוש, צור עמוד HTML מלא ומושלם בעברית.

דרישות עיצוב:
- כיוון RTL, שפה עברית
- רקע כהה: background #0d0d14
- כרטיסים: #1e1e2e עם גבול #2a2a3e
- אקסנט בינלאומי: #e94560 | אקסנט ישראל: #4a9eff
- כל CSS ו-JS מוטמעים בקובץ אחד
- מגיב למובייל

מבנה העמוד:
1. navbar עם "🤖 הזדמנויות AI" + תאריך {date_str} (sticky)
2. hero: כותרת "הזדמנויות שבועיות לאמנות AI", גיליון #{issue}, סטטיסטיקות
3. טאבים: הכל / פסטיבלי סרטים / אמנות / שהיות / 🇮🇱 ישראל
4. סקציות עם כרטיסים:
   - 🎬 פסטיבלי סרטים (בינלאומי)
   - 🖼️ קולות קוראים לאמנות (בינלאומי)
   - 🏛️ שהיות ומלגות (בינלאומי)
   - מפריד כחול "🇮🇱 הזדמנויות בישראל"
   - תערוכות / שהיות / מענקים ישראליים
5. footer: "נוצר אוטומטית על ידי Claude · {date_str}"

כל כרטיס מכיל: כותרת, תגיות (דדליין, מיקום, חינם), תיאור 2-3 משפטים בעברית, כפתור קישור.
תגית "⚠️ דחוף!" מהבהבת אם הדדליין בשבועיים הקרובים.

JavaScript: פונקציית showTab() לפילטור לפי קטגוריה.

החזר אך ורק את קוד ה-HTML המלא מ-<!DOCTYPE html> ועד </html>, ללא שום טקסט לפני או אחרי."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=16000,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": prompt}]
    )

    # חילוץ ה-HTML מהתשובה
    html = ""
    for block in response.content:
        if hasattr(block, "text") and block.text:
            html += block.text

    # ניקוי — שלוף רק את ה-HTML
    if "<!DOCTYPE" in html:
        start = html.find("<!DOCTYPE")
        end = html.rfind("</html>") + 7
        if end > start:
            html = html[start:end]

    if "<!DOCTYPE" not in html or "</html>" not in html:
        print(f"❌ Error: No valid HTML in response")
        print(f"Response preview: {html[:500]}")
        sys.exit(1)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ index.html saved! ({len(html):,} chars)")


if __name__ == "__main__":
    generate_digest()
