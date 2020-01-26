var app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  methods: {
    verseClick: function(event) {
      app.verse = event.target.textContent.split(" ")[0] - 1
      loadVerse.call()
    },
    dropdownClick: function(event) {
      event.preventDefault();
      searchBar.value = event.target.text.trim() + ' '
    },
    recentClick: function(event) {
      [app.book, app.chapter, app.verse] = getVerseFromString(event.target.text)
      app.hidden = false;
      loadVerse.call()
    },
    hideClick: function(event) {
      event.preventDefault();
      if (app.hidden) {
        loadVerse.call();
        app.socket.emit('update', JSON.stringify(app.presentable))
        app.hidden = false;
      } else {
        app.presentable = [];
        app.socket.emit('update', '[]');
        app.hidden = true;
      }
    }
  },
  data: {
    book: 0,
    verse: 0,
    chapter: 1,
    verses: [],
    recents: [],
    results: [],
    mode: "Verses",
    panel: "Recent",
    presentable: [],
    hidden: false,
    socket: io.connect('http://' + document.domain + ':' + location.port + '/socket')
  }
})

var icon = document.getElementById('hide-icon')
var searchBar = document.getElementById('search')
var dropdown = document.getElementById('dropdown')
var button = document.getElementById('hide-button')
var dropdownContainer = document.getElementById('dropdown-menu')
var searchContainer = document.getElementById('search-container')

books = [
  "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
  "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
  "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel",
  "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi",
  "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
  "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon",
  "Hebrews", "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation"
]

searchBar.onfocus = function() {
  dropdownContainer.classList.remove('is-hidden')
  searchContainer.classList.add('is-loading')
}

searchBar.onblur = function() {
  dropdownContainer.classList.add('is-hidden')
  searchContainer.classList.remove('is-loading')
}

function getBookIndex(target) {
  var index = 0;
  for (const book of books) {
    if (book.toLowerCase().startsWith(target.toLowerCase())) {
      return index
    }
    index++
  }
  return 0
}

function getVerseFromString(string) {
  string = string.trim();
  [_, book, chapter, verse] = /\s*^(\d? ?[a-zA-Z]+)*? ?(\d+)?:? ?(\d+)?\s*$/gm.exec(string)
  return [getBookIndex(book), chapter, verse - 1]
}

searchBar.onkeydown = function(event) {
  if (event.keyCode === 13) {
    event.preventDefault();
    [book, chapter, verse] = getVerseFromString(searchBar.value)
    if (book == undefined) {
      book = 0
    }
    if (chapter == undefined) {
      chapter = 1
    }
    if (verse == undefined | isNaN(verse)) {
      verse = 1
    }
    searchBar.value = "";
    searchBar.blur();
    app.book = book
    app.chapter = chapter
    app.verse = parseInt(verse)
    loadVerse.call()
    loadChapter()
  }
}

function removeBookEntry(book) {
  var book = book.toLowerCase()
  var length = app.results.length
  app.results.slice().reverse().forEach(function(result, index) {
    if (result.text.toLowerCase() === book) {
      app.results.splice(length - index - 1, 1)
    }
  })
}

function bookEntryExists(book) {
  var book = book.toLowerCase()
  for (const result of app.results) {
    if (result.text.toLowerCase() === book) {
      return true
    }
  }
  return false
}

searchBar.onkeyup = function() {
  if (app.mode == 'Verses') {
    var input = searchBar.value.toLowerCase()
    books.forEach(function(book, index) {
      if (book.toLowerCase().startsWith(input) && app.results.length <= 5 && input.length > 0) {
        if (!bookEntryExists(book)) {
          app.results.push({text: book})
        }
      } else {
        while (bookEntryExists(book)) {
          removeBookEntry(book)
        }
      }
    })
  } else if (app.mode == 'Lyrics') {
    var cyrillic = to_cyrillic(searchBar.value);
    var result = post.call(1, '/api/search', {term: cyrillic})
    console.log(result)
  }
}

async function post(url = '', data = {}) {
  const response = await fetch(url, {
    method: 'POST',
    mode: 'cors',
    cache: 'force-cache',
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json'
    },
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
    body: JSON.stringify(data)
  });
  console.log(response);
  return await response.json();
}

async function loadChapter() {
  app.verses = []
  verses = await post('/api/verses', {book: app.book, chapter: app.chapter})
  for (const verse of verses) {
    app.verses.push({
      number: verse[0],
      english: verse[1][0], 
      malayalam: verse[2][0]
    })
  }
}

function trimRecents() {
  if (app.recents.length > 10) {
    app.recents = app.recents.slice(1, 11)
  }
}

function addToRecents(entry) {
  for (const recent of app.recents) {
    if (recent.text == entry.text) {
      return
    }
  }
  app.recents.push(entry)
}

async function loadVerse() {
  app.hidden = false;
  app.presentable = await post('/api/verse', {
    book: app.book,
    chapter: app.chapter,
    verse: 1 + parseInt(app.verse)
  })
  app.socket.emit('update', JSON.stringify(app.presentable))
  addToRecents({
    icon: {'fa-bible': true},
    text: books[app.book] + ' ' + app.chapter + ': ' + (1 + parseInt(app.verse))
  })
  trimRecents()
}

loadChapter.call()

function advanceVerseBy(amount) {
  var newVerse = app.verse + amount
  if (newVerse < app.verses.length && newVerse >= 0) {
    app.verse = newVerse;
    loadVerse.call()
  }
}

document.onkeydown = function(event) {
  if (event.key == 'ArrowLeft') {
    advanceVerseBy(-1);
  } else if (event.key == 'ArrowRight') {
    advanceVerseBy(1);
  }
}
