import os
from flask import Flask, request, jsonify, render_template, send_from_directory
import sqlite3
from pathlib import Path

app = Flask(__name__, static_folder='static', template_folder='templates')

DB_PATH = Path(__file__).parent / 'todos.db'

def get_db_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not DB_PATH.exists():
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed BOOLEAN NOT NULL CHECK (completed IN (0,1))
            )
        ''')
        conn.commit()
        conn.close()

@app.route('/')
def index():
    return render_template('index.html')

# API endpoints
@app.route('/api/todos', methods=['GET'])
def get_todos():
    conn = get_db_connection()
    todos = conn.execute('SELECT * FROM todos').fetchall()
    conn.close()
    return jsonify([dict(todo) for todo in todos])

@app.route('/api/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    conn = get_db_connection()
    todo = conn.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()
    conn.close()
    if todo is None:
        return jsonify({'error': 'Todo not found'}), 404
    return jsonify(dict(todo))

@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    title = data.get('title')
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    conn = get_db_connection()
    cur = conn.execute('INSERT INTO todos (title, completed) VALUES (?, ?)', (title, False))
    conn.commit()
    todo_id = cur.lastrowid
    conn.close()
    return jsonify({'id': todo_id, 'title': title, 'completed': False}), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    title = data.get('title')
    completed = data.get('completed')
    conn = get_db_connection()
    todo = conn.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()
    if todo is None:
        conn.close()
        return jsonify({'error': 'Todo not found'}), 404
    # Update fields if provided
    new_title = title if title is not None else todo['title']
    new_completed = completed if completed is not None else todo['completed']
    conn.execute('UPDATE todos SET title = ?, completed = ? WHERE id = ?', (new_title, int(bool(new_completed)), todo_id))
    conn.commit()
    conn.close()
    return jsonify({'id': todo_id, 'title': new_title, 'completed': bool(new_completed)})

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    conn = get_db_connection()
    todo = conn.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()
    if todo is None:
        conn.close()
        return jsonify({'error': 'Todo not found'}), 404
    conn.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    return '', 204

# Serve static files (if needed)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    init_db()
    # Use port 5000 by default
    app.run(debug=True)
