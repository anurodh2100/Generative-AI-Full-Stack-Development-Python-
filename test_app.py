import json
from todo_app.app import app

# Use Flask test client
def run_tests():
    client = app.test_client()
    # Ensure DB is fresh by resetting (delete file if exists)
    import os, pathlib
    db_path = pathlib.Path('todo_app') / 'todos.db'
    if db_path.exists():
        db_path.unlink()
    # Initialize DB by calling init_db via app context
    with app.app_context():
        from todo_app.app import init_db
        init_db()
    # Create a todo
    resp = client.post('/api/todos', json={'title': 'Test Todo'})
    assert resp.status_code == 201, f'Create failed {resp.status_code}'
    data = resp.get_json()
    todo_id = data['id']
    # Get list
    resp = client.get('/api/todos')
    todos = resp.get_json()
    assert any(t['id'] == todo_id for t in todos), 'Todo not in list'
    # Update
    resp = client.put(f'/api/todos/{todo_id}', json={'completed': True})
    assert resp.status_code == 200, 'Update failed'
    # Delete
    resp = client.delete(f'/api/todos/{todo_id}')
    assert resp.status_code == 204, 'Delete failed'
    # Verify deletion
    resp = client.get(f'/api/todos/{todo_id}')
    assert resp.status_code == 404, 'Todo still exists after delete'
    print('All CRUD tests passed')

if __name__ == '__main__':
    run_tests()
