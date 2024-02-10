from flask import Flask, render_template, request, redirect, url_for
import datetime
import json

app = Flask(__name__)

# Classe pour représenter une tâche
class Task:
    def __init__(self, name, priority, deadline):
        self.name = name
        self.priority = priority
        self.deadline = deadline
        self.completed = False  # Initialiser la tâche comme non terminée

    def __str__(self):
        return f"{self.name} (Priorité: {self.priority}, Deadline: {self.deadline})"

    def time_remaining(self):
        current_date = datetime.date.today()
        remaining_time = self.deadline - current_date
        return remaining_time

    def mark_as_completed(self):
        self.completed = True  # Marquer la tâche comme terminée

# Liste de tâches
tasks = []

# Charger les tâches depuis le fichier JSON s'il existe
try:
    with open("tasks.json", "r") as file:
        tasks_data = json.load(file)
        tasks = [Task(task_data['name'], task_data['priority'], datetime.datetime.strptime(task_data['deadline'], "%Y-%m-%d").date()) for task_data in tasks_data]
        for task, task_data in zip(tasks, tasks_data):
            task.completed = task_data.get('completed', False)  # Assurez-vous de mettre à jour la propriété `completed`
except FileNotFoundError:
    tasks = []

# Routes
@app.route("/")
def index():
    return render_template("index.html", tasks=tasks)

@app.route("/add_task", methods=["POST"])
def add_task():
    name = request.form["name"]
    priority = request.form["priority"]
    deadline = datetime.datetime.strptime(request.form["deadline"], "%Y-%m-%d").date()
    task = Task(name, priority, deadline)
    tasks.append(task)
    save_tasks()
    return redirect(url_for("index"))

@app.route("/mark_task_completed/<int:task_index>")
def mark_task_completed(task_index):
    if 0 <= task_index < len(tasks):
        tasks[task_index].mark_as_completed()
        save_tasks()
    return redirect(url_for("index"))

# Fonction pour sauvegarder les tâches dans un fichier JSON
def save_tasks():
    tasks_data = []
    for task in tasks:
        task_data = {
            'name': task.name,
            'priority': task.priority,
            'deadline': task.deadline.strftime("%Y-%m-%d"),  # Convertir en chaîne de caractères
            'completed': task.completed
        }
        tasks_data.append(task_data)

    with open("tasks.json", "w") as file:
        json.dump(tasks_data, file)

if __name__ == "__main__":
    app.run(debug=True)
