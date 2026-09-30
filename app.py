from flask import Flask, jsonify, request

app = Flask(__name__)
tasks = []


@app.get("/health")
def health():
    return jsonify(status="healthy"), 200


@app.get("/tasks")
def list_tasks():
    return jsonify(tasks), 200


@app.post("/tasks")
def create_task():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(error="Send a JSON object"), 400

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify(error="A task title is required"), 400

    task = {
        "id": len(tasks) + 1,
        "title": title.strip(),
        "completed": False,
    }
    tasks.append(task)

    return jsonify(task), 201

