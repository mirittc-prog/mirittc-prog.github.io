#!/usr/bin/env python3
"""
Weekly AI Art Opportunities Digest Generator
מייצר עמוד HTML שבועי עם הזדמנויות לאמנות AI — ישראל ובינלאומי
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
    """מספר גיליון מחושב לפי שבוע בשנה"""
    now = datetime.now()
    return (now.year - 2026) * 52 + now.isocalendar()[1]


def generate_digest():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY not set")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    date_str = hebrew_date()
    issue = issue_number()

    print(f"📅 Generating digest for {date_str} (Issue #{issue})...")

    # ---- שלב 1: חיפוש הזדמנויות ----
    print("🔍 Searching for opportunities...")

    search_prompt = f"""חפש ברשת הזדמנויות עדכניות לאמנות AI. חפש את הנושאים הבאים:

1. "AI film festival open call 2026"
2. "AI art competition open call 2026"
3. "AI video art exhibition 2026 submissions"
4. "AI art residency fellowship 2026"
5. "AI for Good film festival 2026"
6. "Runway AI festival 2026"
7. "קול קורא אמנות בינה מלאכותית ישראל 2026"
8. "AI art Israel exhibition 2026"

עבור כל הזדמנות שמצאת, ספק:
- שם ההזדמנות
- תיאור קצר (2-3 משפטים)
- תאריך דדליין (אם ידוע)
- מיקום / פלטפורמה
- קישור (URL)
- האם זו הזדמנות ישראלית (כן/לא)

החזר את התוצאות כרשימה מובנית."""

    try:
        search_response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4000,
            tools=[{"type": "web_search_20250305", "name": "web_search"}],
            messages=[{"role": "user", "content": search_prompt}]
        )

        opportunities_data = ""
        for block in search_response.content:
            if hasattr(block, "text") and block.text:
                opportunities_data += block.text

        print(f"✅ Found opportunities data ({len(opportunities_data)} chars)")

    except Exception as e:
        print(f"⚠️ Web search unavailable ({e}), using model knowledge...")
        opportunities_data = "השתמש בידע שלך על הזדמנויות אמנות AI עדכניות לשנת 2026."

    # ---- שלב 2: יצירת HTML ----
    print("🎨 Generating HTML page...")

    html_prompt = f"""בהתבסס על ההזדמנויות הבאות שנמצאו:

{opportunities_data}

צור עמוד HTML מלא ומושלם — תקציר הזדמנויות שבועי לאמנות AI.

דרישות מדויקות:

METADATA:
- תאריך: {date_str}
- גיליון מספר: {issue}
- שפה: עברית מלאה (RTL)

עיצוב:
- רקע כהה: #0d0d14
- כרטיסים: #1e1e2e עם גבול #2a2a3e
- אקסנט בינלאומי: #e94560
- אקסנט ישראל: #4a9eff
- טיפוגרפיה: Arial / sans-serif
- מגיב למובייל (responsive)
- כל CSS ו-JS מוטמעים בקובץ אחד

מבנה העמוד:
1. navbar עם לוגו "🤖 הזדמנויות AI" + תאריך (sticky)
2. hero section עם כותרת, תת-כותרת, ומספרים (כמה הזדמנויות בכל קטגוריה)
3. טאבים: הכל / פסטיבלי סרטים / אמנות / שהיות / 🇮🇱 ישראל
4. סקציות:
   - 🎬 פסטיבלי סרטים ותחרויות (בינלאומי)
   - 🖼️ קולות קוראים לאמנות (בינלאומי)
   - 🏛️ שהיות ומלגות (בינלאומי)
   - מפריד כחול "🇮🇱 הזדמנויות בישראל"
   - 🎨 תערוכות ואירועים בישראל
   - 🏠 שהיות אמנים בישראל
   - 💰 מענקים ותמיכה כספית
5. footer עם: "נוצר אוטומטית על ידי Claude · {date_str}"

כרטיס הזדמנות (card):
- כותרת
- תגיות: דדליין (אדום/כחול), מיקום (אפור), "חינם" (ירוק) אם רלוונטי
- תגית "⚠️ דחוף!" מהבהבת אם הדדליין בשבועיים הקרובים
- תיאור 2-3 משפטים בעברית
- כפתור קישור

JavaScript:
- פונקציית showTab() לפילטור לפי קטגוריה
- כרטיסי ישראל מוצגים גם בטאב "הכל" וגם בטאב "ישראל"

החזר אך ורק את קוד ה-HTML המלא — מ-<!DOCTYPE html> ועד </html> — ללא שום טקסט נוסף לפני או אחרי."""

    html_response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=16000,
        messages=[{"role": "user", "content": html_prompt}]
    )

    html = ""
    for block in html_response.content:
        if hasattr(block, "text") and block.text:
            html = block.text
            break

    # ניקוי — שלוף רק את ה-HTML אם יש טקסט מסביב
    if "<!DOCTYPE" in html:
        start = html.find("<!DOCTYPE")
        end = html.rfind("</html>") + 7
        if end > start:
            html = html[start:end]

    if "<!DOCTYPE" not in html or "</html>" not in html:
        print("❌ Error: Generated content is not valid HTML")
        print(f"Preview: {html[:300]}")
        sys.exit(1)

    # שמירה
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ index.html saved successfully! ({len(html):,} chars)")


if __name__ == "__main__":
    generate_digest()
