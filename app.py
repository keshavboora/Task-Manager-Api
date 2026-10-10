from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = []
next_id = 1


@app.route("/tasks", methods=["GET"])
def list_tasks():
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def create_task():
    global next_id
    data = request.get_json()
    task = {"id": next_id, "title": data["title"], "done": False}
    tasks.append(task)
    next_id += 1
    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return jsonify(task)
    return jsonify({"error": "not found"}), 404

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    for i in range(len(tasks)):
        if tasks[i]["id"] == task_id:
            tasks.pop(i)
            return jsonify({"message": "deleted"})
    return jsonify({"error": "not found"}), 404


@app.route("/tasks/search", methods=["GET"])
def search_tasks():
    q = request.args.get("q")
    return jsonify([t for t in tasks if q in t["title"]])
    
if __name__ == "__main__":
    app.run(debug=True)
