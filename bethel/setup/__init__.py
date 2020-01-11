"""Set up relevant static files and bible data."""

from bethel.setup import bibles, songs, static


def load():
    """Entry point for setup script."""
    songs.load()
    bibles.load()
    static.load()
