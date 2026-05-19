#!/usr/bin/env python3
"""Bible.py

Tkinter aplikace pro čtení a vyhledávání čtyř evangelijních knih
(zatím Matouš, Marek, Lukáš, Jan). Aplikace stáhne text z obohu.cz,
uloží ho do cache a umožní procházet kapitoly a vyhledávat verše podle
klíčových slov.
"""

import json
import os
import re
import threading
import time
import requests
import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from bs4 import BeautifulSoup
import fitz

# Seznam evangelií: kód, jméno a počet kapitol.
EVANGELIA = [
    ("Mt", "Matouš", 28),
    ("Mk", "Marek", 16),
    ("Lk", "Lukáš", 24),
    ("J", "Jan", 21),
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
CACHE_FILE = Path(__file__).with_suffix(".json")
PDF_FILE = Path(__file__).resolve().parents[1] / "evangelia_JB.pdf"
DELAY_SECONDS = 0.8


def fetch_chapter(book_code: str, chapter: int) -> list[tuple[str, str]]:
    """Stáhne jednu kapitolu evangelia a vrátí seznam verzí (číslo, text)."""
    params = {"lang": "cz", "styl": "JB", "k": book_code, "kap": chapter}
    try:
        response = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=20)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Chyba při stahování {book_code} {chapter}: {exc}") from exc

    soup = BeautifulSoup(response.text, "lxml")
    verses = []

    # Na stránce obohu.cz jsou texty v bloku #blok_versu a verše v <span class="cv">.
    for item in soup.select("#blok_versu span.cv"):
        number_tag = item.select_one("span.cisloversen")
        if not number_tag:
            continue

        number = number_tag.get_text(strip=True)
        raw_text = item.get_text(" ", strip=True)
        verse_text = raw_text[len(number):].lstrip(" .:–-")
        if verse_text:
            verses.append((number, verse_text))

    if verses:
        return verses

    # Pokud se nenašlo nic, zkuste alternativní zpracování nebo vyhoďte chybu.
    raise RuntimeError(f"Nepodařilo se parsovat kapitolu {book_code} {chapter}.")


def save_cache(data: dict) -> None:
    """Uloží stažený text do JSON cache souboru."""
    with CACHE_FILE.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)


def _is_valid_data(data: object) -> bool:
    """Zkontroluje, zda data obsahují očekávanou strukturu evangelia."""
    if not isinstance(data, dict):
        return False
    expected_books = {code for code, _, _ in EVANGELIA}
    if set(data.keys()) != expected_books:
        return False
    for chapters in data.values():
        if not isinstance(chapters, dict):
            return False
        for chapter, verses in chapters.items():
            if not isinstance(chapter, str) or not isinstance(verses, list):
                return False
            for verse in verses:
                if not isinstance(verse, list) or len(verse) != 2:
                    return False
    return True


def load_cache() -> dict | None:
    """Načte cache soubor, pokud existuje a je validní."""
    if not CACHE_FILE.exists():
        return None
    with CACHE_FILE.open("r", encoding="utf-8") as handle:
        try:
            data = json.load(handle)
        except json.JSONDecodeError:
            return None
    return data if _is_valid_data(data) else None


def load_data_from_pdf() -> dict:
    """Načte evangelia z PDF souboru a vrátí strukturovaná data."""
    if not PDF_FILE.exists():
        raise FileNotFoundError(f"PDF soubor nebyl nalezen: {PDF_FILE}")

    doc = fitz.open(str(PDF_FILE))
    text_parts = []
    for page in doc:
        page_text = page.get_text()
        if page_text:
            text_parts.append(page_text)

    full_text = "\n".join(text_parts)
    data: dict[str, dict[str, list[list[str]]]] = {}
    current_book = None
    current_chapter = None
    current_verse = None
    current_text = []
    current_book_index = -1
    # pro případ, že extrakce textu z PDF poškodí diakritiku, zachováme pořadí knih
    book_codes = [code for code, _, _ in EVANGELIA]

    for raw_line in full_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        # nový blok evangelia (v PDF mohou být diakriticky poškozené názvy)
        if line.startswith("Evangelium podle"):
            current_book_index += 1
            if current_book_index < len(book_codes):
                current_book = book_codes[current_book_index]
                data.setdefault(current_book, {})
            else:
                current_book = None
            current_chapter = None
            current_verse = None
            current_text = []
            continue

        chapter_match = re.match(r"^Kapitola\s+(\d+)$", line)
        if chapter_match and current_book is not None:
            if current_verse is not None and current_chapter is not None:
                verse_text = " ".join(current_text).strip()
                if verse_text:
                    data[current_book][current_chapter].append([current_verse, verse_text])
            current_chapter = chapter_match.group(1)
            data[current_book].setdefault(current_chapter, [])
            current_verse = None
            current_text = []
            continue

        verse_match = re.match(r"^(\d{1,3})\s+(.*)$", line)
        if verse_match and current_book is not None and current_chapter is not None:
            if current_verse is not None:
                verse_text = " ".join(current_text).strip()
                if verse_text:
                    data[current_book][current_chapter].append([current_verse, verse_text])
            current_verse = verse_match.group(1)
            current_text = [verse_match.group(2).strip()]
            continue

        if current_verse is not None:
            current_text.append(line)

    if current_book is not None and current_chapter is not None and current_verse is not None:
        verse_text = " ".join(current_text).strip()
        if verse_text:
            data[current_book][current_chapter].append([current_verse, verse_text])

    return data


def build_initial_data() -> dict:
    """Načte všechna evangelia z cache, PDF nebo z webu a vrátí slovník dat."""
    cached = load_cache()
    if cached is not None:
        return cached

    if PDF_FILE.exists():
        data = load_data_from_pdf()
        if _is_valid_data(data):
            save_cache(data)
            return data

    all_books: dict[str, dict[str, list[list[str]]]] = {}
    for code, _, chapters in EVANGELIA:
        all_books[code] = {}
        for chapter in range(1, chapters + 1):
            verses = fetch_chapter(code, chapter)
            all_books[code][str(chapter)] = [[num, text] for num, text in verses]
            time.sleep(DELAY_SECONDS)

    save_cache(all_books)
    return all_books


def search_verses(data: dict, query: str) -> list[dict]:
    """Vyhledá frázi v loaded datech a vrátí seznam výsledků."""
    query = query.strip().lower()
    if not query:
        return []

    results = []
    book_names = {code: name for code, name, _ in EVANGELIA}

    for code, chapters in data.items():
        book_name = book_names.get(code, code)
        for chapter, verses in chapters.items():
            for verse_number, verse_text in verses:
                if query in verse_text.lower():
                    results.append(
                        {
                            "book_code": code,
                            "book_name": book_name,
                            "chapter": chapter,
                            "verse": verse_number,
                            "text": verse_text,
                        }
                    )
    return results


class BibleApp(tk.Tk):
    """Hlavní aplikace pro čtení evangelijních textů."""

    def __init__(self):
        super().__init__()
        self.title("Bible - evangelia")
        self.geometry("920x700")
        self.resizable(True, True)

        self.data: dict | None = None
        self.book_var = tk.StringVar(value=EVANGELIA[0][0])
        self.chapter_var = tk.StringVar(value="1")
        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Data nejsou načtena. Klikněte na 'Načíst evangelia'.")

        self._build_ui()
        self._populate_chapter_menu()
        self._load_cached_data()

    def _build_ui(self) -> None:
        """Sestaví všechny widgety uživatelského rozhraní."""
        top_frame = ttk.Frame(self, padding=10)
        top_frame.pack(fill=tk.X)

        # Výběr knihy a kapitoly
        ttk.Label(top_frame, text="Kniha:").grid(row=0, column=0, sticky=tk.W)
        book_names = [name for _, name, _ in EVANGELIA]
        book_codes = [code for code, _, _ in EVANGELIA]
        self.book_menu = ttk.OptionMenu(
            top_frame,
            self.book_var,
            book_codes[0],
            *book_codes,
            command=self._on_book_changed,
        )
        self.book_menu.grid(row=0, column=1, sticky=tk.W, padx=(4, 20))

        ttk.Label(top_frame, text="Kapitola:").grid(row=0, column=2, sticky=tk.W)
        self.chapter_menu = ttk.OptionMenu(top_frame, self.chapter_var, "1")
        self.chapter_menu.grid(row=0, column=3, sticky=tk.W, padx=(4, 20))

        self.load_button = ttk.Button(
            top_frame,
            text="Načíst evangelia",
            command=self._on_load_click,
        )
        self.load_button.grid(row=0, column=4, sticky=tk.W)

        self.show_chapter_button = ttk.Button(
            top_frame,
            text="Zobrazit kapitolu",
            command=self._display_chapter,
            state=tk.DISABLED,
        )
        self.show_chapter_button.grid(row=0, column=5, sticky=tk.W, padx=(10, 0))

        # Vyhledávání
        search_frame = ttk.Frame(self, padding=(10, 8, 10, 0))
        search_frame.pack(fill=tk.X)

        ttk.Label(search_frame, text="Hledat verše:").grid(row=0, column=0, sticky=tk.W)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.grid(row=0, column=1, sticky=tk.W, padx=(4, 4))
        search_entry.bind("<Return>", lambda _: self._display_search())

        search_button = ttk.Button(search_frame, text="Hledat", command=self._display_search)
        search_button.grid(row=0, column=2, sticky=tk.W)

        clear_button = ttk.Button(search_frame, text="Smazat hledání", command=self._clear_search)
        clear_button.grid(row=0, column=3, sticky=tk.W, padx=(10, 0))

        # Výsledný text
        self.text_widget = ScrolledText(self, wrap=tk.WORD, font=("Segoe UI", 11), undo=True)
        self.text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=(6, 0))
        self.text_widget.configure(state=tk.DISABLED)

        status_frame = ttk.Frame(self, padding=10)
        status_frame.pack(fill=tk.X)
        ttk.Label(status_frame, textvariable=self.status_var).pack(side=tk.LEFT)

    def _populate_chapter_menu(self) -> None:
        """Aktualizuje seznam kapitol podle právě vybrané knihy."""
        book_code = self.book_var.get()
        chapter_count = self._chapter_count_for_book(book_code)
        menu = self.chapter_menu["menu"]
        menu.delete(0, tk.END)

        for chapter in range(1, chapter_count + 1):
            menu.add_command(
                label=str(chapter),
                command=lambda value=str(chapter): self.chapter_var.set(value),
            )

        self.chapter_var.set("1")

    def _chapter_count_for_book(self, book_code: str) -> int:
        """Vrátí počet kapitol pro danou knihu podle definice EVANGELIA."""
        for code, _, chapters in EVANGELIA:
            if code == book_code:
                return chapters
        return 1

    def _on_book_changed(self, _=None) -> None:
        """Uživatel změnil knihu; aktualizujeme kapitoly."""
        self._populate_chapter_menu()

    def _set_status(self, message: str) -> None:
        self.status_var.set(message)

    def _set_buttons_state(self, load_enabled: bool, show_enabled: bool) -> None:
        self.load_button.configure(state=tk.NORMAL if load_enabled else tk.DISABLED)
        self.show_chapter_button.configure(state=tk.NORMAL if show_enabled else tk.DISABLED)

    def _load_cached_data(self) -> None:
        """Pokud existuje cache nebo PDF, inicializujeme tlačítka aplikace."""
        cached = load_cache()
        if cached is not None:
            self.data = cached
            self._set_status("Data načtena z cache. Vyberte knihu a kapitolu.")
            self._set_buttons_state(True, True)
            return

        if PDF_FILE.exists():
            self._set_status("Cache nenalezena. Nalezen PDF, klikněte na 'Načíst evangelia'.")
            self._set_buttons_state(True, False)
        else:
            self._set_status("Cache nenalezena. Klikněte na 'Načíst evangelia'.")
            self._set_buttons_state(True, False)

    def _on_load_click(self) -> None:
        """Spustí načítání evangelijních knih na pozadí."""
        self.load_button.configure(state=tk.DISABLED)
        self._set_status("Načítám evangelia, prosím čekejte...")
        threading.Thread(target=self._load_data_thread, daemon=True).start()

    def _load_data_thread(self) -> None:
        """Funkce běžící v pozadí, která stáhne a uloží data."""
        try:
            self.data = build_initial_data()
        except Exception as exc:
            self.after(0, lambda: self._on_load_failed(exc))
            return

        self.after(0, self._on_load_finished)

    def _on_load_finished(self) -> None:
        self._set_status("Evangelia byla úspěšně načtena a uložena do cache.")
        self._set_buttons_state(True, True)

    def _on_load_failed(self, exc: Exception) -> None:
        messagebox.showerror("Chyba při načítání", str(exc))
        self._set_status("Nepodařilo se načíst evangelia. Zkontrolujte připojení.")
        self._set_buttons_state(True, False)

    def _display_chapter(self) -> None:
        """Zobrazí zvolenou kapitolu v textové oblasti."""
        if not self.data:
            messagebox.showwarning("Chyba", "Nejsou načtena žádná data.")
            return

        book_code = self.book_var.get()
        chapter = self.chapter_var.get()
        book_name = next(name for code, name, _ in EVANGELIA if code == book_code)
        chapter_data = self.data.get(book_code, {}).get(chapter)

        if not chapter_data:
            self.text_widget.configure(state=tk.NORMAL)
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, f"Kapitola {chapter} nebyla nalezena.\n")
            self.text_widget.configure(state=tk.DISABLED)
            return

        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, f"{book_name} {chapter}\n")
        self.text_widget.insert(tk.END, "=" * 60 + "\n\n")

        for verse_number, verse_text in chapter_data:
            self.text_widget.insert(tk.END, f"{verse_number}. {verse_text}\n\n")

        self.text_widget.configure(state=tk.DISABLED)
        self._set_status(f"Zobrazuji {book_name} {chapter}.")

    def _display_search(self) -> None:
        """Vyhledá zadanou frázi a zobrazí nalezené verše."""
        if not self.data:
            messagebox.showwarning("Chyba", "Nejsou načtena žádná data.")
            return

        query = self.search_var.get().strip()
        if not query:
            self._set_status("Zadejte hledaný výraz.")
            return

        results = search_verses(self.data, query)
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)

        if not results:
            self.text_widget.insert(tk.END, f"Nebyly nalezeny žádné verše obsahující: {query}\n")
            self.text_widget.configure(state=tk.DISABLED)
            self._set_status("Vyhledávání ukončeno: bez výsledků.")
            return

        self.text_widget.insert(tk.END, f"Výsledky hledání: {query}\n")
        self.text_widget.insert(tk.END, "=" * 60 + "\n\n")

        for item in results:
            self.text_widget.insert(
                tk.END,
                f"{item['book_name']} {item['chapter']}:{item['verse']} — {item['text']}\n\n",
            )

        self.text_widget.configure(state=tk.DISABLED)
        self._set_status(f"Nalezeno {len(results)} veršů pro '{query}'.")

    def _clear_search(self) -> None:
        """Vymaže vyhledávací pole a textovou oblast."""
        self.search_var.set("")
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.configure(state=tk.DISABLED)
        self._set_status("Hledání vymazáno.")


if __name__ == "__main__":
    app = BibleApp()
    app.mainloop()
