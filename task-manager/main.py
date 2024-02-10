import datetime
import json

# Classe pour représenter une tâche
class Task:
    def __init__(self, name, priority, deadline):
        self.name = name
        self.priority = priority
        self.deadline = deadline

    def __str__(self):
        return f"{self.name} (Priorité: {self.priority}, Deadline: {self.deadline})"

# Fonction pour ajouter une tâche
def add_task(tasks):
    name = input("Nom de la tâche : ")
    priority = input("Priorité de la tâche (1 / 2 / 3): ")
    if priority == "1":
        priority = "Elevée"
        print("Prioritée définie sur élevée")
    elif priority == "2":
        priority = "Moyenne"
        print("Prioritée définie sur moyenne")
    elif priority == "3":
        priority = "Faible"
        print("Prioritée définie sur faible")
    else:
        priority = "None"
        print("Prioritée définie sur None")
    deadline = input("Date limite (format YYYY-MM-DD) : ")
    deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d").date()
    task = Task(name, priority, deadline)
    tasks.append(task)
    print("Tâche ajoutée avec succès.")

# Fonction pour afficher les tâches
def display_tasks(tasks):
    if not tasks:
        print("Aucune tâche enregistrée.")
    else:
        print("Tâches en cours :")
        for index, task in enumerate(tasks, start=1):
            print(f"{index}. {task}")

# Fonction pour sauvegarder les tâches dans un fichier JSON
def save_tasks(tasks):
    tasks_data = []
    for task in tasks:
        task_data = {
            'name': task.name,
            'priority': task.priority,
            'deadline': task.deadline  # Utiliser directement la date limite telle quelle
        }
        tasks_data.append(task_data)

    with open("tasks.json", "w") as file:
        json.dump(tasks_data, file, default=str)  # Utiliser default=str pour gérer la sérialisation de la date

# Fonction principale
def main():
    # Charger les tâches depuis le fichier JSON s'il existe
    try:
        with open("tasks.json", "r") as file:
            tasks_data = json.load(file)
            tasks = [Task(**task_data) for task_data in tasks_data]
    except FileNotFoundError:
        tasks = []

    while True:
        print("\nMenu:")
        print("1. Ajouter une tâche")
        print("2. Afficher les tâches")
        print("3. Quitter")

        choice = input("Entrez votre choix : ")

        if choice == "1":
            add_task(tasks)
            save_tasks(tasks)
        elif choice == "2":
            display_tasks(tasks)
        elif choice == "3":
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez entrer un choix valide.")

if __name__ == "__main__":
    main()
