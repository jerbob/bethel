"""Connection methods for song and bible databases."""

import sqlite3
from typing import List
from dataclasses import dataclass


@dataclass
class Bible:
    """Connection manager for bible databases."""

    language: str

    def get_chapter(self, book: int, chapter: int):
        """Select (and cache) verses of a particular chapter."""
        with sqlite3.connect(f'{self.language}.db') as connection:
            cursor = connection.cursor()
            cursor.execute(
                'SELECT verse FROM bible WHERE book=? AND chapter=?',
                (book, chapter)
            )
            results = cursor.fetchall()
        return results

    def get_verse(self, book: int, chapter: int, verse: int):
        """Select one specified verse from the bible."""
        with sqlite3.connect(f'{self.language}.db') as connection:
            cursor = connection.cursor()
            cursor.execute(
                'SELECT verse FROM bible WHERE book=? AND chapter=?',
                (book, chapter)
            )
            for index, text in enumerate(cursor.fetchall(), 1):
                if index == verse:
                    result = text
                    break
            else:
                result = ''
            return result


class Songs:
    """Connection manager for the song database."""

    def search(self, term: str) -> List[int]:
        """Search song lyrics for a metaphonic term."""
        with sqlite3.connect('songs.db') as connection:
            cursor = connection.cursor()
            cursor.execute(
                'SELECT _rowid_ FROM songs WHERE metaphone LIKE ? '
                'ORDER BY INSTR(metaphone, ?) LIMIT 10',
                (f'%{term}%', term)
            )
            results = cursor.fetchall()
        return results
