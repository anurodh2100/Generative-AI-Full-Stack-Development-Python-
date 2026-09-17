document.addEventListener('DOMContentLoaded', function() {
    const todoList = document.getElementById('todo-list');
    const addBtn = document.getElementById('add-btn');
    const newTitle = document.getElementById('new-title');

    function fetchTodos() {
        fetch('/api/todos')
            .then(res => res.json())
            .then(renderTodos)
            .catch(console.error);
    }

    function renderTodos(todos) {
        todoList.innerHTML = '';
        todos.forEach(todo => {
            const li = document.createElement('li');
            li.dataset.id = todo.id;
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.checked = todo.completed;
            checkbox.addEventListener('change', toggleCompleted);
            const span = document.createElement('span');
            span.textContent = todo.title;
            span.contentEditable = true;
            span.addEventListener('blur', editTitle);
            const delBtn = document.createElement('button');
            delBtn.textContent = 'Delete';
            delBtn.addEventListener('click', deleteTodo);
            li.appendChild(checkbox);
            li.appendChild(span);
            li.appendChild(delBtn);
            todoList.appendChild(li);
        });
    }

    function addTodo() {
        const title = newTitle.value.trim();
        if (!title) return;
        fetch('/api/todos', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({title})
        })
        .then(res => {
            if (!res.ok) throw new Error('Failed to create');
            return res.json();
        })
        .then(() => {
            newTitle.value = '';
            fetchTodos();
        })
        .catch(console.error);
    }

    function toggleCompleted(e) {
        const li = e.target.closest('li');
        const id = li.dataset.id;
        const completed = e.target.checked;
        fetch(`/api/todos/${id}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({completed})
        })
        .then(res => {
            if (!res.ok) throw new Error('Failed to update');
            fetchTodos();
        })
        .catch(console.error);
    }

    function editTitle(e) {
        const li = e.target.closest('li');
        const id = li.dataset.id;
        const title = e.target.textContent.trim();
        if (!title) {
            // revert to previous by refetching
            fetchTodos();
            return;
        }
        fetch(`/api/todos/${id}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({title})
        })
        .then(res => {
            if (!res.ok) throw new Error('Failed to update');
            fetchTodos();
        })
        .catch(console.error);
    }

    function deleteTodo(e) {
        const li = e.target.closest('li');
        const id = li.dataset.id;
        fetch(`/api/todos/${id}`, {method: 'DELETE'})
        .then(res => {
            if (res.status === 204) {
                fetchTodos();
            } else {
                throw new Error('Failed to delete');
            }
        })
        .catch(console.error);
    }

    addBtn.addEventListener('click', addTodo);
    fetchTodos();
});
