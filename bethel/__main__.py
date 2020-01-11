"""Web interface for viewing and displaying bible verses."""

from bethel import app, socketio


socketio.run(app, host='0.0.0.0', port=8000, debug=True)
