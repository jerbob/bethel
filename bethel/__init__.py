"""Web interface for viewing and displaying bible verses."""

from functools import lru_cache

from bethel import setup
from bethel.database import Bible, Songs

from flask import Flask, jsonify, render_template, request

from flask_socketio import SocketIO, emit


app = Flask(__name__)
socketio = SocketIO(app)

# Load static files, bibles and songs
setup.load()

songs = Songs()
english = Bible('english')
malayalam = Bible('malayalam')


@lru_cache
def get_chapter(book: int, chapter: int):
    """Get a full chapter."""
    count = 1
    verses = []
    for english_verse, malayalam_verse in zip(
        english.get_chapter(book, chapter),
        malayalam.get_chapter(book, chapter)
    ):
        verses.append([count, english_verse, malayalam_verse])
        count += 1
    return verses


@lru_cache
def get_verse(book: int, chapter: int, verse: int):
    """Get a particular verse."""
    return [
        *english.get_verse(book, chapter, verse),
        *malayalam.get_verse(book, chapter, verse)
    ]


@app.route('/')
def index():
    """Route for the controller application."""
    return render_template(
        'index.html'
    )


@app.route('/presentation')
def presentation():
    """Route for the current presentation."""
    return render_template(
        'presentation.html'
    )


@app.route('/api/verses', methods=['POST'])
def verses():
    """Return verses of a book as JSON."""
    book = request.json.get('book', 0)
    chapter = request.json.get('chapter', 1)
    return jsonify(get_chapter(book, chapter))


@app.route('/api/verse', methods=['POST'])
def verse():
    """Return a particular verse."""
    book = request.json.get('book', 0)
    chapter = request.json.get('chapter', 1)
    verse = request.json.get('verse', 1)
    return jsonify(get_verse(book, chapter, verse))


@app.route('/api/search', methods=['POST'])
def search():
    """Search the song database for specified lyrics."""
    term = request.json.get('term', '')
    return jsonify(songs.search(term))


@socketio.on('update', namespace='/socket')
def message(message):
    """Broadcast a verse update to all clients."""
    emit('update', message, broadcast=True)
