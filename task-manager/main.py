import datetime
import json
from win10toast import ToastNotifier  # Importez la bibliothèque win10toast pour les notifications

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
    
    # Envoyer une notification de succès
    toaster = ToastNotifier()
    toaster.show_toast("Tâche ajoutée", f"{name} a été ajouté avec succès", duration=5)

    print("Tâche ajoutée avec succès.")

# Fonction pour afficher les tâches
def display_tasks(tasks):
    if not tasks:
        print("Aucune tâche enregistrée.")
    else:
        print("Tâches en cours :")
        for index, task in enumerate(tasks, start=1):
            if not task.completed:
                remaining_time = task.time_remaining()
                print(f"{index}. {task} - Temps restant: {remaining_time.days} jours")
        print("\nTâches terminées :")
        for index, task in enumerate(tasks, start=1):
            if task.completed:
                print(f"{index}. {task}")

# Fonction pour sauvegarder les tâches dans un fichier JSON
def save_tasks(tasks):
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

# Fonction pour afficher la tâche la plus récente avec le temps restant dans le menu
def print_recent_task(tasks):
    if tasks:
        recent_task = max(tasks, key=lambda x: x.deadline)
        remaining_time = recent_task.time_remaining()
        print(f"(!) {recent_task.name}: {remaining_time.days} jours")
    else:
        print("(!) Aucune tâche enregistrée.")
        
# Fonction pour marquer une tâche comme terminée
def mark_task_completed(tasks):
    display_tasks(tasks)
    task_index = int(input("Entrez le numéro de la tâche terminée : ")) - 1
    if 0 <= task_index < len(tasks):
        tasks[task_index].mark_as_completed()  # Appeler la méthode pour marquer la tâche comme terminée
        
        # Envoyer une notification de succès
        toaster = ToastNotifier()
        toaster.show_toast("Tâche terminée", "La tâche a été marquée comme terminée", duration=5)

        print("Tâche marquée comme terminée.")
        save_tasks(tasks)
    else:
        print("Numéro de tâche invalide.")

# Fonction pour supprimer une tâche
def delete_task(tasks):
    display_tasks(tasks)
    task_index = int(input("Entrez le numéro de la tâche à supprimer : ")) - 1
    if 0 <= task_index < len(tasks):
        del tasks[task_index]
        
        # Envoyer une notification de succès
        toaster = ToastNotifier()
        toaster.show_toast("Tâche supprimée", "La tâche a été supprimée avec succès", duration=5)

        print("Tâche supprimée avec succès.")
        save_tasks(tasks)
    else:
        print("Numéro de tâche invalide.")

# Fonction principale
def main():
    # Charger les tâches depuis le fichier JSON s'il existe
    try:
        with open("tasks.json", "r") as file:
            tasks_data = json.load(file)
            tasks = [Task(task_data['name'], task_data['priority'], datetime.datetime.strptime(task_data['deadline'], "%Y-%m-%d").date()) for task_data in tasks_data]
            for task, task_data in zip(tasks, tasks_data):
                task.completed = task_data.get('completed', False)  # Assurez-vous de mettre à jour la propriété `completed`
    except FileNotFoundError:
        tasks = []

    while True:
        print("\n----- Menu: -----")
        print("| 1. Ajouter une tâche")
        print("| 2. Afficher les tâches")
        print("| 3. Marquer une tâche comme terminée")
        print("| 4. Supprimer une tâche")
        print("| 5. Quitter")
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
            mark_task_completed(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez entrer un choix valide.")

if __name__ == "__main__":
    main()
