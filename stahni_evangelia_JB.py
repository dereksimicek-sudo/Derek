#!/usr/bin/env python3
"""
Stáhne čtyři evangelia Jeruzalémské Bible z obohu.cz a uloží je jako PDF.

Požadavky:
    pip install requests beautifulsoup4 reportlab lxml

Spuštění:
    python stahni_evangelia_JB.py
"""

import os
import time
import sys
import requests
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER


def _get_unicode_font_name() -> str:
    """Registruje a vrátí font s podporou Unicode pro české znaky."""
    candidates = [
        r"C:\Windows\Fonts\Arial.ttf",
        r"C:\Windows\Fonts\Calibri.ttf",
        r"C:\Windows\Fonts\Times.ttf",
        r"/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        r"/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                font_name = "PDFUnicode"
                pdfmetrics.registerFont(TTFont(font_name, path))
                return font_name
            except Exception:
                continue
    return "Helvetica"

# ── Evangelia: zkratka obohu.cz, název, počet kapitol ──────────────────────
EVANGELIA = [
    ("Mt", "Evangelium podle Matouše",  28),
    ("Mk", "Evangelium podle Marka",    16),
    ("Lk", "Evangelium podle Lukáše",   24),
    ("J",  "Evangelium podle Jana",     21),
]

BASE_URL = "https://www.obohu.cz/bible/index.php"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "cs,en;q=0.8",
    "Referer": "https://www.obohu.cz/",
}
DELAY = 1.2   # vteřiny mezi požadavky – buď slušný k serveru


# ── Stahování ───────────────────────────────────────────────────────────────

def fetch_chapter(zkratka: str, kap: int) -> list[tuple[str, str]]:
    """
    Vrátí seznam (číslo_verše, text) pro danou kapitolu.
    Pokud se stažení nepodaří, vrátí prázdný seznam.
    """
    params = {"lang": "cz", "styl": "JB", "k": zkratka, "kap": kap}
    try:
        r = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=20)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"  ✗ Chyba stahování {zkratka} {kap}: {e}", file=sys.stderr)
        return []

    soup = BeautifulSoup(r.text, "lxml")

    verses = []

    # Na obohu.cz jsou verše v bloku #blok_versu jako <span class="cv">,
    # čísla veršů jsou v <span class="cisloversen">.
    for block in soup.select("#blok_versu span.cv"):
        num_tag = block.select_one("span.cisloversen")
        if not num_tag:
            continue

        num = num_tag.get_text(strip=True)
        raw = block.get_text(" ", strip=True)
        text = raw[len(num):].strip(" .:–-")
        if text:
            verses.append((num, text))

    if verses:
        return verses

    # Záložní přístup: hledej div s id="textbox" nebo třídou obsahující "bible"
    for sel in ["div#textbox", "div.bibletext", "td.bibletext", "div.text"]:
        box = soup.select_one(sel)
        if box:
            raw_text = box.get_text("\n", strip=True)
            verses = _parse_plain_text(raw_text)
            if verses:
                return verses

    # Poslední záchrana: vezmi celý <body> a zkus najít číslované verše
    body_text = soup.get_text("\n", strip=True)
    verses = _parse_plain_text(body_text)
    return verses


def _parse_plain_text(text: str) -> list[tuple[str, str]]:
    """Pokusí se z prostého textu extrahovat verše začínající číslem."""
    import re
    verses = []
    # Verše bývají ve formátu "1Text verše 2Další verš..." nebo "1 Text verše"
    pattern = re.compile(r"(?<!\w)(\d{1,3})\s+(.+?)(?=(?<!\w)\d{1,3}\s|\Z)", re.DOTALL)
    for m in pattern.finditer(text):
        num, content = m.group(1), m.group(2).replace("\n", " ").strip()
        if 3 < len(content) < 2000:
            verses.append((num, content))
    return verses


# ── Tvorba PDF ──────────────────────────────────────────────────────────────

def build_pdf(all_data: dict, output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=2.5 * cm,
        rightMargin=2.5 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm,
        title="Jeruzalémská Bible – Čtyři evangelia",
        author="obohu.cz (překlad: Dagmar a František X. Halasovi)",
    )

    base = getSampleStyleSheet()
    font_name = _get_unicode_font_name()

    title_style = ParagraphStyle(
        "BookTitle",
        parent=base["Title"],
        fontName=font_name,
        fontSize=22,
        leading=28,
        spaceAfter=6,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#2C1810"),
    )
    chapter_style = ParagraphStyle(
        "ChapterHead",
        parent=base["Heading2"],
        fontName=font_name,
        fontSize=13,
        leading=18,
        spaceBefore=18,
        spaceAfter=6,
        textColor=colors.HexColor("#5A3010"),
    )
    verse_style = ParagraphStyle(
        "Verse",
        parent=base["Normal"],
        fontName=font_name,
        fontSize=10.5,
        leading=15,
        alignment=TA_JUSTIFY,
        spaceAfter=2,
    )
    num_style = ParagraphStyle(
        "VerseNum",
        parent=verse_style,
        fontName=font_name,
        textColor=colors.HexColor("#888888"),
        fontSize=8,
    )

    story = []

    # Titulní strana
    story.append(Spacer(1, 4 * cm))
    story.append(Paragraph("Jeruzalémská Bible", title_style))
    story.append(Paragraph("Čtyři evangelia", ParagraphStyle(
        "Sub", parent=title_style, fontSize=15, textColor=colors.HexColor("#666666")
    )))
    story.append(Spacer(1, 1 * cm))
    story.append(HRFlowable(width="60%", color=colors.HexColor("#CCAA88")))
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(
        "Překlad: Dagmar a František X. Halasovi<br/>Zdroj: obohu.cz",
        ParagraphStyle("Info", parent=base["Normal"], fontName=font_name,
                       fontSize=9, alignment=TA_CENTER, textColor=colors.grey)
    ))
    story.append(PageBreak())

    for zkratka, nazev, _ in EVANGELIA:
        chapters = all_data.get(zkratka, {})
        if not chapters:
            continue

        # Nadpis knihy
        story.append(Paragraph(nazev, title_style))
        story.append(HRFlowable(width="100%", color=colors.HexColor("#CCAA88"),
                                spaceAfter=8))

        for kap_num in sorted(chapters.keys()):
            verses = chapters[kap_num]
            story.append(Paragraph(f"Kapitola {kap_num}", chapter_style))

            for v_num, v_text in verses:
                # Číslo verše jako horní index + text
                combined = (
                    f'<font size="8" color="#999999"><super>{v_num}</super></font> '
                    f'{v_text}'
                )
                story.append(Paragraph(combined, verse_style))

        story.append(PageBreak())

    doc.build(story)


# ── Hlavní program ──────────────────────────────────────────────────────────

def main():
    output = "evangelia_JB.pdf"
    all_data: dict[str, dict[int, list]] = {}
    total_chapters = sum(n for _, _, n in EVANGELIA)
    done = 0

    print("=" * 55)
    print("  Stahování evangelií Jeruzalémské Bible z obohu.cz")
    print("=" * 55)

    for zkratka, nazev, pocet_kap in EVANGELIA:
        print(f"\n► {nazev}")
        all_data[zkratka] = {}

        for kap in range(1, pocet_kap + 1):
            sys.stdout.write(f"  Kapitola {kap:2d}/{pocet_kap}... ")
            sys.stdout.flush()

            verses = fetch_chapter(zkratka, kap)
            all_data[zkratka][kap] = verses

            done += 1
            pct = done / total_chapters * 100
            status = f"{len(verses)} veršů  [{pct:.0f}%]"
            print(status)

            time.sleep(DELAY)

    print(f"\n✔ Stahování dokončeno. Tvořím PDF: {output}")
    build_pdf(all_data, output)
    print(f"✔ Hotovo! Soubor uložen jako: {output}")
    print(f"  (velikost: {__import__('os').path.getsize(output) // 1024} KB)")


if __name__ == "__main__":
    main()
