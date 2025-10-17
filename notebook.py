import json
import os

class Note:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def to_dict(self):
        return {
            'title': self.title,
            'content': self.content
        }

    @staticmethod
    def from_dict(data):
        return Note(data['title'], data['content'])

    def __str__(self):
        return f"Title: {self.title}\nContent: {self.content}\n"


class NoteManager:
    def __init__(self, filename='notes.json'):
        self.notes = []
        self.filename = filename
        self.load_notes()

    def add_note(self, title, content):
        note = Note(title, content)
        self.notes.append(note)
        self.save_notes()
        print(f"Note '{title}' added.")

    def show_notes(self):
        if not self.notes:
            print("No notes available.")
            return
        for index, note in enumerate(self.notes):
            print(f"{index + 1}:\n{note}")

    def delete_note(self, note_index):
        if 0 <= note_index < len(self.notes):
            deleted_note = self.notes.pop(note_index)
            self.save_notes()
            print(f"Note '{deleted_note.title}' deleted.")
        else:
            print("Invalid note index.")

    def save_notes(self):
        with open(self.filename, 'w') as f:
            json.dump([note.to_dict() for note in self.notes], f)

    def load_notes(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.notes = [Note.from_dict(data) for data in json.load(f)]
        else:
            self.notes = []


def main():
    note_manager = NoteManager()

    while True:
        print("\nNote Manager")
        print("1. Add Note")
        print("2. Show Notes")
        print("3. Delete Note")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            title = input("Enter note title: ")
            content = input("Enter note content: ")
            note_manager.add_note(title, content)
        elif choice == "2":
            note_manager.show_notes()
        elif choice == "3":
            note_manager.show_notes()
            note_index = int(input("Enter note index to delete: ")) - 1
            note_manager.delete_note(note_index)
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
