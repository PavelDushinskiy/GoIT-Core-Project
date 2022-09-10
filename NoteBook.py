from collections import UserDict
from typing import Any, List
from datetime import date
import re
import pickle

NAME_REGEX = re.compile(r'^[a-zA-Zа-яА-Я0-9,. ]{2,30}$')


class Field:
    def __init__(self, value) -> None:
        self._value = None
        self.value = value

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value) -> None:
        self._value = value


class Name(Field):
    @Field.value.setter
    def value(self, name: str):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if not re.match(NAME_REGEX, name):
            raise ValueError('Name must be between 2 and 30 characters')
        self._value = name


class NoteText(Field):
    pass


class NoteTag(Field):
    pass


class NoteRecord:

    def __init__(self, name: str, text: str, tags: List[str]) -> None:
        self.name = Name(name)
        self.text = NoteText(text)
        self.tags = [NoteTag(tag) for tag in tags]
        self.created = date.today()

    def __repr__(self) -> str:
        return f'{self.name.value.title()} # {self.text.value} # {", ".join([p.value for p in self.tags])} # {self.created}'

    def add_teg(self, tag: str) -> None:
        self.tags.append(NoteTag(tag))

    def remove_tag(self, tag: str):
        for i, tg in enumerate(self.tags):
            if tg.value == tag:
                return self.tags.pop(i)


class Notebook(UserDict):

    def __init__(self, save_file, *args):
        super().__init__(*args)
        self.save_file = save_file
        self.load_data()

    def add_record(self, record: NoteRecord) -> NoteRecord | None:
        if not self.data.get(record.name.value):
            self.data[record.name.value] = record
            self.save_data()
            return record

    def save_data(self):
        with open(self.save_file, 'wb') as f:
            pickle.dump(self.data, f)

    def load_data(self):
        try:
            with open(self.save_file, 'rb') as f:
                try:
                    data = pickle.load(f)
                    self.data = data
                except EOFError:
                    return 'File data is empty'
        except FileNotFoundError:
            return 'File data is empty'

    def show_all_notes(self) -> None:
        for k, v in self.data.items():
            print(v)

    def remove_record(self, name):
        if name in self:
            del self.data[name]
            return print(f"Note {name} was deleted successfully!")
        return print(f"Note {name} not found!")

    def change_name(self, name, new_name):
        for value in self.data.values():
            if value.name.value == name:
                value.name.value = new_name
                return print(f'Note {name} was changed to {new_name}')
        return print(f'Note {name} not found!')

    def change_text(self, name, new_text):
        for value in self.data.values():
            if value.name.value == name:
                value.text.value = new_text
                return print(f'Note {name} was changed to {new_text}')
        return print(f'Note {name} not found!')

    def change_tag(self, name, new_tag):
        for value in self.data.values():
            if value.name.value == name:
                value.tags[0].value = new_tag
                return print(f'Note {name} was changed to {new_tag}')


notebook = Notebook('note_data.bin')
handler_commands = ['make', 'show', 'remove', 'find', 'change', 'exit']
change_commands = ['name', 'text', 'tag', 'back']
all_commands = handler_commands + change_commands


# ________________________Notes Handler________________________
def notes_handler(command):
    if command == "make":
        try:
            print(f"{'=' * 10} Make note please: {'=' * 10}")
            name = input('Enter name: ').strip()
            if name in notebook:
                print(f"Note {name} already exist! Try another name")
                name = input('Enter name: ').strip()
            text = input('Enter text: ').strip()
            tags = input('Enter tags: ').strip().split()
            note = NoteRecord(name, text, tags)
            tags_list = tags
            for tag in tags_list:
                if tag not in tags_list:
                    note.add_teg(tag)
            notebook.add_record(note)
            print(f"Note {name} was added successfully!")
            notebook.save_data()
        except ValueError as e:
            print(f"Sorry, {e}. Please try again!")
            return True

    elif command == "show":
        notebook.show_all_notes()
        return True

    elif command == "remove":
        name = input('Enter name: ').title().strip()
        notebook.remove_record(name)
        notebook.save_data()
        return True

    elif command == "find":
        print("Find a note by tag, name or text")
        value = input('Enter value: ').strip()
        result_str = ''
        for k, v in notebook.data.items():
            if value in k:
                result_str += f'{v}\n'
            for tag in v.tags:
                if value in tag.value:
                    result_str += f'{v}\n'
            if value in v.text.value:
                result_str += f'{v}\n'
        print(result_str if result_str else 'Not found!')
        return True

    elif command == "change":
        return change_handler(command)


# ________________________Change Handler________________________
def change_handler(command):
    if command == "name":
        name = input('Enter name: ').title().strip()
        new_name = input('Enter new name: ').title().strip()
        notebook.change_name(name, new_name)
        notebook.save_data()
        return True

    elif command == "text":
        title = input("Enter title: ").title().strip()
        new_text = input("Enter new text: ").strip()
        notebook.change_text(title, new_text)
        notebook.save_data()
        return True

    elif command == "tag":
        name = input('Enter name: ').title().strip()
        new_tag = input('Enter new tag: ').title().strip()
        notebook.change_tag(name, new_tag)
        notebook.save_data()
        return True
    elif command == "back":
        notes_handler(command)
        return True


if __name__ == "__main__":
    while True:
        notebook.load_data()
        print(f"{'=' * 15} Notes {'=' * 15}")
        print(f'make - will create a new note\n'
              f'show - will display a list of notes\n'
              f'remove - will delete the required note\n'
              f'find - will find the note you need3\n'
              f'change - will change the note name, text or tag\n'
              f'exit - will exit the program\n')
        command = input("Enter command ==>: ").casefold().strip()
        if command == "change":
            print(f"{'=' * 6} What should be changed? {'=' * 6}")
            print(f'name - change the name of the note\n'
                  f'text - change the note text\n'
                  f'tag - change tag for note\n'
                  f'back - return to the main menu')
            command = input("Enter command ==>: ").casefold().strip()
            change_handler(command)
        if command == "exit":
            print("Goodbye!")
            notebook.save_data()
            break
        if command not in all_commands:
            print("Sorry, command not found! Please try again!")
            continue
        notes_handler(command)
