import json

class Task:
    def __init__(self, name, priority='Normal'):
        self.name = name
        self.completed = False
        self.priority = priority

    def mark_completed(self):
        self.completed = True

    def to_dict(self):
        return {
            'name': self.name,
            'completed': self.completed,
            'priority': self.priority
        }

    @staticmethod
    def from_dict(data):
        task = Task(data['name'], data['priority'])
        task.completed = data['completed']
        return task

    def __str__(self):
        status = "✓" if self.completed else "✗"
        return f"{status} [{self.priority}] {self.name}"


class TaskManager:
    def __init__(self, filename='tasks.json'):
        self.tasks = []
        self.filename = filename
        self.load_tasks()

    def add_task(self, task_name, priority):
        task = Task(task_name, priority)
        self.tasks.append(task)
        self.save_tasks()
        print(f"Task '{task_name}' added with priority '{priority}'.")

    def complete_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].mark_completed()
            self.save_tasks()
            print(f"Task '{self.tasks[task_index].name}' completed.")
        else:
            print("Invalid task index.")

    def show_tasks(self):
        if not self.tasks:
            print("No tasks available.")
            return
        for index, task in enumerate(self.tasks):
            print(f"{index}: {task}")

    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f)

    def load_tasks(self):
        try:
            with open(self.filename, 'r') as f:
                self.tasks = [Task.from_dict(data) for data in json.load(f)]
        except FileNotFoundError:
            self.tasks = []


def main():
    task_manager = TaskManager()

    while True:
        print("\nTask Manager")
        print("1. Add Task")
        print("2. Complete Task")
        print("3. Show Tasks")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            task_name = input("Enter task name: ")
            priority = input("Enter priority (High, Normal, Low): ")
            task_manager.add_task(task_name, priority)
        elif choice == "2":
            task_manager.show_tasks()
            task_index = int(input("Enter task index to complete: "))
            task_manager.complete_task(task_index)
        elif choice == "3":
            task_manager.show_tasks()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
