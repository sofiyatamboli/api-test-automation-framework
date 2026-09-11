"""
Task Manager API
A small REST API used as the target application for the automated
test suite in this repo. Run with: python app.py
"""

from flask import Flask, jsonify, request
from models import db, Task

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    # Seed the same two starter tasks the in-memory version had,
    # but only if the table is empty (so restarts don't duplicate them).
    if Task.query.count() == 0:
        db.session.add(Task(title="Learn pytest", completed=False))
        db.session.add(Task(title="Write API tests", completed=False))
        db.session.commit()


@app.get("/health")
def health():
    """Simple health-check endpoint."""
    return jsonify({"status": "ok"}), 200


@app.get("/tasks")
def get_tasks():
    """Return all tasks."""
    tasks = Task.query.all()
    return jsonify([t.to_dict() for t in tasks]), 200


@app.get("/tasks/<int:task_id>")
def get_task(task_id):
    """Return a single task by id, or 404 if it doesn't exist."""
    task = db.session.get(Task, task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task.to_dict()), 200


@app.post("/tasks")
def create_task():
    """Create a new task. Requires a JSON body with a 'title' field."""
    data = request.get_json(silent=True)

    if not data or "title" not in data or not str(data["title"]).strip():
        return jsonify({"error": "'title' is required"}), 400

    task = Task(title=data["title"], completed=False)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@app.put("/tasks/<int:task_id>")
def update_task(task_id):
    """Update an existing task's title and/or completed status."""
    task = db.session.get(Task, task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json(silent=True) or {}
    if "title" in data:
        task.title = data["title"]
    if "completed" in data:
        task.completed = bool(data["completed"])

    db.session.commit()
    return jsonify(task.to_dict()), 200


@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    """Delete a task by id."""
    task = db.session.get(Task, task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)