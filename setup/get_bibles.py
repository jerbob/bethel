"""Get sqlite3 databases from godlytalias/Bible-Database."""

import sys
from pathlib import Path
from urllib import request


print('[?] Checking for bibles...', file=sys.stderr)

bible_url = 'https://github.com/godlytalias/Bible-Database/raw/master/'

bibles = {
    'english.db': bible_url + 'English/holybible.db',
    'malayalam.db': bible_url + 'Malayalam/holybible.db'
}

for bible, url in bibles.items():
    if not Path(bible).exists():
        print(
            f'[!] {bible} not found, downloading... ',
            file=sys.stderr,
            end=''
        )
        request.urlretrieve(url, bible)
        print('Done.', file=sys.stderr)
    else:
        print(f'[!] {bible} found.')
