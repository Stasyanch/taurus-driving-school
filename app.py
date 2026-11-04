import os
import secrets
import sqlite3
from contextlib import contextmanager
from functools import wraps
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

ROOT = Path(__file__).resolve().parent
DATABASE = ROOT / 'database.sqlite'
app = Flask(__name__, static_folder=str(ROOT), static_url_path='')
ADMIN_USER = os.getenv('TAURUS_ADMIN_USER', 'admin')
ADMIN_PASSWORD = os.getenv('TAURUS_ADMIN_PASSWORD', 'change-me')


@contextmanager
def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def init_db():
    with get_db() as connection:
        connection.executescript((ROOT / 'schema.sql').read_text(encoding='utf-8'))


def valid_message(data):
    name = str(data.get('name', '')).strip()
    email = str(data.get('email', '')).strip()
    message = str(data.get('message', '')).strip()
    if len(name) < 2 or '@' not in email or '.' not in email.split('@')[-1] or not message:
        return None
    return name, email, message


def requires_auth(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        auth = request.authorization
        if not auth or not secrets.compare_digest(auth.username, ADMIN_USER) or not secrets.compare_digest(auth.password, ADMIN_PASSWORD):
            return jsonify({'error': 'Потрібна автентифікація.'}), 401, {'WWW-Authenticate': 'Basic realm="Taurus admin"'}
        return view(*args, **kwargs)
    return wrapped


@app.get('/')
def index():
    return send_from_directory(ROOT, 'index.html')


@app.post('/api/messages')
def create_message():
    values = valid_message(request.get_json(silent=True) or {})
    if values is None:
        return jsonify({'error': 'Введіть коректні ім’я, email і повідомлення.'}), 400
    with get_db() as connection:
        connection.execute('INSERT INTO messages (name, email, message) VALUES (?, ?, ?)', values)
    return jsonify({'success': 'Дякуємо! Заявку збережено. Ми скоро з вами зв’яжемося.'}), 201


@app.get('/api/messages')
@requires_auth
def list_messages():
    with get_db() as connection:
        rows = connection.execute('SELECT id, name, email, message, created_at FROM messages ORDER BY created_at DESC').fetchall()
    return jsonify([dict(row) for row in rows])


@app.delete('/api/messages/<int:message_id>')
@requires_auth
def delete_message(message_id):
    with get_db() as connection:
        connection.execute('DELETE FROM messages WHERE id = ?', (message_id,))
    return jsonify({'success': 'Повідомлення видалено.'})


@app.get('/messages')
@requires_auth
def messages_page():
    return send_from_directory(ROOT, 'messages.html')


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
