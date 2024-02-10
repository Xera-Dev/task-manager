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

    def time_remaining(self):
        current_date = datetime.date.today()
        deadline_date = datetime.datetime.strptime(self.deadline, "%Y-%m-%d").date()  # Convertir la chaîne en date
        remaining_time = deadline_date - current_date
        return remaining_time

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
            remaining_time = task.time_remaining()
            print(f"{index}. {task} - Temps restant: {remaining_time.days} jours")

# Fonction pour sauvegarder les tâches dans un fichier JSON
def save_tasks(tasks):
    tasks_data = []
    for task in tasks:
        task_data = {
            'name': task.name,
            'priority': task.priority,
            'deadline': task.deadline.strftime("%Y-%m-%d")  # Convertir la date en chaîne de caractères
        }
        tasks_data.append(task_data)

    with open("tasks.json", "w") as file:
        json.dump(tasks_data, file)

# Fonction pour afficher la tâche la plus récente avec le temps restant dans le menu
def print_recent_task(tasks):
    if tasks:
        recent_task = max(tasks, key=lambda x: x.deadline)
        remaining_time = recent_task.time_remaining()
        print(f"(!) {recent_task.name}: {remaining_time.days} jours")
    else:
        print("(!) Aucune tâche enregistrée.")

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
        print("\n----- Menu: -----")
        print("| 1. Ajouter une tâche")
        print("| 2. Afficher les tâches")
        print("| 3. Quitter")
        print("-------------------")
        print_recent_task(tasks)
        print("-------------------")

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

