"""
Task Manager API
A small REST API used as the target application for the automated
test suite in this repo. Run with: python app.py
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory "database" — resets every time the app restarts.
tasks = {
    1: {"id": 1, "title": "Learn pytest", "completed": False},
    2: {"id": 2, "title": "Write API tests", "completed": False},
}
next_id = 3


@app.get("/health")
def health():
    """Simple health-check endpoint."""
    return jsonify({"status": "ok"}), 200


@app.get("/tasks")
def get_tasks():
    """Return all tasks."""
    return jsonify(list(tasks.values())), 200


@app.get("/tasks/<int:task_id>")
def get_task(task_id):
    """Return a single task by id, or 404 if it doesn't exist."""
    task = tasks.get(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task), 200


@app.post("/tasks")
def create_task():
    """Create a new task. Requires a JSON body with a 'title' field."""
    global next_id
    data = request.get_json(silent=True)

    if not data or "title" not in data or not str(data["title"]).strip():
        return jsonify({"error": "'title' is required"}), 400

    task = {"id": next_id, "title": data["title"], "completed": False}
    tasks[next_id] = task
    next_id += 1
    return jsonify(task), 201


@app.put("/tasks/<int:task_id>")
def update_task(task_id):
    """Update an existing task's title and/or completed status."""
    task = tasks.get(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json(silent=True) or {}
    if "title" in data:
        task["title"] = data["title"]
    if "completed" in data:
        task["completed"] = bool(data["completed"])

    return jsonify(task), 200


@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    """Delete a task by id."""
    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404
    del tasks[task_id]
    return jsonify({"message": "Task deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
