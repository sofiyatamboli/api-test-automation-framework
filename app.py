"""
Task Manager API
A small REST API used as the target application for the automated
test suite in this repo. Run with: python app.py
"""

from flask import Flask, jsonify, request
from models import db, Task


def create_app(db_uri="sqlite:///tasks.db"):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()
        if Task.query.count() == 0:
            db.session.add(Task(title="Learn pytest", completed=False))
            db.session.add(Task(title="Write API tests", completed=False))
            db.session.commit()

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    @app.get("/tasks")
    def get_tasks():
        tasks = Task.query.all()
        return jsonify([t.to_dict() for t in tasks]), 200

    @app.get("/tasks/<int:task_id>")
    def get_task(task_id):
        task = db.session.get(Task, task_id)
        if task is None:
            return jsonify({"error": "Task not found"}), 404
        return jsonify(task.to_dict()), 200

    @app.post("/tasks")
    def create_task():
        data = request.get_json(silent=True)
        if not data or "title" not in data or not str(data["title"]).strip():
            return jsonify({"error": "'title' is required"}), 400
        task = Task(title=data["title"], completed=False)
        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict()), 201

    @app.put("/tasks/<int:task_id>")
    def update_task(task_id):
        task = db.session.get(Task, task_id)
        if task is None:
            return jsonify({"error": "Task not found"}), 404
        data = request.get_json(silent=True) or {}
        if "title" in data:
            if not str(data["title"]).strip():
                return jsonify({"error": "'title' cannot be empty"}), 400
            task.title = data["title"]
        if "completed" in data:
            task.completed = bool(data["completed"])
        db.session.commit()
        return jsonify(task.to_dict()), 200

    @app.delete("/tasks/<int:task_id>")
    def delete_task(task_id):
        task = db.session.get(Task, task_id)
        if task is None:
            return jsonify({"error": "Task not found"}), 404
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted"}), 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)