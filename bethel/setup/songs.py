"""Get song lyrics from kristheeyagaanavali.com."""

import contextlib
import re
import sqlite3
import sys
from pathlib import Path

from lxml import etree
from requests_html import HTMLSession

from .mlphone import MLphone

converter = MLphone()
session = HTMLSession()

root = "https://www.kristheeyagaanavali.com/mal/Songbook/Athmeeya_Geethangal"


def get_verses(link: str) -> str:
    """Get song verses, given an absolute URL."""
    verse, verses = [], []
    for line in session.get(link).html.find("p"):
        if "copyright" not in line.attrs.get("class", ""):
            if line.text.strip():
                verse.append(line.text)
            else:
                verses.append(verse.copy())
                verse.clear()
    verses.append(verse)
    return "\n".join(map("\t".join, verses))


def load() -> None:
    """Entry point for setup module."""
    if Path("songs.db").exists():
        return

    print("[?] songs.db not found, creating...", file=sys.stderr)
    with sqlite3.connect("songs.db") as connection:
        connection.execute("CREATE TABLE songs (lyrics, metaphone)")

    links = [link for link in session.get(root).html.absolute_links if root in link]

    total = len(links)
    for i, link in enumerate(links, 1):
        print(f"[?] Getting song [{i}/{total}]...", end="\r")
        with contextlib.suppress(etree.ParserError):
            verses = get_verses(link)
            key = converter.compute(re.sub(r"\s", "", verses))[0]
            with sqlite3.connect("songs.db") as connection:
                connection.execute("INSERT INTO songs VALUES (?, ?)", (verses, key))

    print(f"[?] songs.db populated with {total} songs.")
