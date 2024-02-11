from flask import Flask, render_template, request, redirect, url_for, flash
import datetime
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Changez ceci pour une clé secrète sécurisée

# Classe pour représenter une tâche
class Task:
    def __init__(self, name, priority, deadline, category, completed=False):
        self.name = name
        self.priority = priority
        self.deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d").date()
        self.category = category
        self.completed = completed

    def time_remaining(self):
        current_date = datetime.date.today()
        remaining_time = self.deadline - current_date
        return remaining_time

    def mark_as_completed(self):
        self.completed = True  # Marquer la tâche comme terminée

# Fonction pour charger les tâches à partir du fichier JSON
def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            tasks_data = json.load(file)
            return [Task(name=task_data['name'], priority=task_data['priority'], deadline=task_data['deadline'], category=task_data['category'], completed=task_data['completed']) for task_data in tasks_data]
    except FileNotFoundError:
        return []

# Fonction pour sauvegarder les tâches dans un fichier JSON
def save_tasks(tasks):
    tasks_data = []
    for task in tasks:
        task_data = {
            'name': task.name,
            'priority': task.priority,
            'deadline': task.deadline.strftime("%Y-%m-%d"),
            'category': task.category,
            'completed': task.completed
        }
        tasks_data.append(task_data)

    with open("tasks.json", "w") as file:
        json.dump(tasks_data, file)

# Charger les tâches au démarrage de l'application
tasks = load_tasks()

# Route pour la page d'accueil avec possibilité de tri
@app.route('/')
def index():
    # Récupérer le paramètre de filtre de l'URL
    filter_by = request.args.get('filter')

    # Trier les tâches en fonction du paramètre de filtre
    if filter_by == 'name':
        tasks.sort(key=lambda x: x.name)
    elif filter_by == 'priority':
        tasks.sort(key=lambda x: x.priority)
    elif filter_by == 'deadline':
        tasks.sort(key=lambda x: x.deadline)

    return render_template('index.html', tasks=tasks)


# Route pour ajouter une tâche
@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form['taskName']
    task_priority = request.form['taskPriority']
    task_deadline = request.form['taskDeadline']
    task_category = request.form['taskCategory']
    task = Task(task_name, task_priority, task_deadline, task_category)
    tasks.append(task)
    save_tasks(tasks)  # Sauvegarder les tâches dans le fichier JSON
    flash('Tâche ajoutée avec succès.', 'success')
    return redirect(url_for('index'))

# Route pour marquer une tâche comme terminée
@app.route('/mark_task_completed/<int:task_index>', methods=['POST'])
def mark_task_completed(task_index):
    if 0 <= task_index < len(tasks):
        tasks[task_index].mark_as_completed()
        save_tasks(tasks)  # Sauvegarder les tâches dans le fichier JSON
        flash('Tâche marquée comme terminée.', 'success')
    else:
        flash('Numéro de tâche invalide.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
