"""Get static files for running the app offline."""

# flake8: noqa

import sys
from pathlib import Path
from urllib import request

static = Path('bethel/static')

paths = (
    (
        'https://cdn.jsdelivr.net/npm/bulma@0.8.0/css/bulma.min.css',
        static / 'css' / 'bulma.css'
    ),
    (
        'https://use.fontawesome.com/releases/v5.3.1/js/all.js',
        static / 'js' / 'fontawesome.js'
    ),
    (
        'https://fonts.gstatic.com/s/manjari/v2/k3kQo8UPMOBO2w1UfcHoLmvDIaK18A.woff2',
        static / 'font' / 'malayalam.woff2'
    ),
    (
        'https://fonts.gstatic.com/s/manjari/v2/k3kQo8UPMOBO2w1UfdnoLmvDIaI.woff2',
        static / 'font' / 'latin.woff2'
    ),
    (
        'https://cdn.jsdelivr.net/npm/vue',
        static / 'js' / 'vue.js'
    ),
    (
        'https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.2.0/socket.io.js',
        static / 'js' / 'socket.js'
    )
)

def load() -> None:
    """Entry point for setup module."""
    for url, path in paths:
        if not path.exists():
            print(
                f'[?] {path.stem}{path.suffix} not found, downloading... ',
                file=sys.stderr,
                end=''
            )
            request.urlretrieve(url, path)
            print('Done', file=sys.stderr)
