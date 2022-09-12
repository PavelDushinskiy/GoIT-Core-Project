from collections import UserDict
from typing import Any, List
from datetime import date
import re
import pickle
from bot_feature import BotFeature


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

    def __init__(self, name: str, text: str, *args) -> None:
        self.name = Name(name)
        self.text = NoteText(text)
        self.created = date.today()
        self.tags = []

    def __repr__(self) -> str:
        return f'{self.name.value.title()} # {self.text.value} # {", ".join([p for p in self.tags])} # {self.created}'

    def add_tag(self, tag: NoteTag) -> None:
        self.tags.append(tag)

    def remove_tag(self, tag: str):
        self.tags.remove(tag)


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
        for note in self.data.values():
            print(note)

    def remove_record(self, name):
        if name in self:
            self.pop(name)
            print(f"Note {name} was deleted successfully!")
        else:
            print(f"Note {name} was not found! Please try again.")

    def change_name(self, name, new_name):
        if name in self.data:
            for value in self.data.values():
                if value.name.value == name:
                    value.name.value = new_name
                    print(f'Note {name} was changed to {new_name}')
        else:
            print(f'Note {name} not found!')

    def change_text(self, name, new_text):
        if name in self.data:
            for value in self.data.values():
                if value.name.value == name:
                    value.text.value = new_text
                    print(f'Note {name} was changed to {new_text}')
        else:
            print(f'Note {name} not found!')

    def change_tag(self, name, old_value, new_value):
        if name in self.data:
            for value in self.data.values():
                if value.name.value == name:
                    value.remove_tag(old_value)
                    value.add_tag(new_value)
                    print(f'Note {name} was changed to {new_value}')
        else:
            print(f'Note {name} not found!')

    def add_tag(self, name, tag):
        for note in self.data.values():
            if note.name.value == name:
                note.add_tag(tag)
                print(f'Note {name} was added tag {tag}')



class NoteParser(BotFeature):

    def __init__(self, notebook: Notebook) -> None:
        self.notebook = notebook
        self.commands = {
            'make': self.make,
            'change': self.change,
            'search': self.search,
            'show': self.show,
            'remove': self.remove,
            'add tag': self.add_tag
        }

    def handle(self, command: str) -> str:
        handler = self.commands.get(command)
        if handler:
            return handler()
        raise ValueError(f'Unknown command: {command}. Try again')

    def parse(self, user_input: str) -> None:
        if user_input == 'exit':
            raise SystemExit("Good bye!")
        if user_input == 'make':
            return self.make()
        if user_input == 'show':
            return self.show()
        if user_input == 'remove':
            return self.remove()
        if user_input == 'search':
            return self.search()
        if user_input == 'change':
            return self.change()
        if user_input == 'add tag':
            return self.add_tag()
        raise ValueError(f'Unknown command: {user_input}. Try again')

    def make(self):
        try:
            print(f"{'=' * 10} Make note please: {'=' * 10}")
            name = input('Enter name: ').strip()
            if name in self.notebook.data:
                print(f"Note {name} already exist! Try another name")
                name = input('Enter name: ').strip()
            text = input('Enter text: ')
            tags = input('Enter tags: ').strip().split()
            note = NoteRecord(name, text, tags)
            tags_list = tags
            for tag in tags_list:
                note.add_tag(tag)
            self.notebook.add_record(note)
            print(f"Note {name} was created successfully!")
            self.notebook.save_data()
        except ValueError as e:
            print(f"Sorry, {e}. Please try again!")

    def show(self):
        print(f"{'=' * 10} Show all notes: {'=' * 10}")
        self.notebook.show_all_notes()
        self.notebook.save_data()

    def remove(self):
        print(f"{'=' * 10} Remove note: {'=' * 10}")
        name = input('Enter name: ').strip()
        self.notebook.remove_record(name)

    def search(self):
        print(f"{'=' * 5} Find a note by tag, name or text {'=' * 5}")
        value = input('Enter value: ').strip()
        result_str = []
        for k, v in self.notebook.data.items():
            if value in k:
                result_str += [v]
            for tag in v.tags:
                if value in tag.value:
                    result_str += [v]
            if value in v.text.value:
                result_str += [v]
        if result_str:
            for i in result_str:
                print(i)
        else:
            raise ValueError(f"Note with {value} not found!")

    def change(self):
        print(f"{'=' * 5} Change anything in the note: {'=' * 5}")
        while True:
            value = input('Enter name, tag or part of the text: ')
            for note in self.notebook.data.values():
                if value in note.name.value:
                    print(f"Found note:\n"
                          f"{note}\n"
                          f"Do you want to change name note?")
                    answer = input('Enter yes or no: ').casefold()
                    if answer == 'yes':
                        self.notebook.change_name(note.name.value, input('Enter new name: '))
                        notebook.save_data()
                    elif answer == 'no':
                        print('Ok, try again')
                        continue
                    else:
                        raise ValueError(f"Sorry, {answer} is not correct. Try again!")
                elif value in note.tags:
                    print(f"Found note:\n"
                          f"{note}\n"
                          f"Do you want to change tag note?")
                    answer = input('Enter yes or no: ').casefold()
                    if answer == 'yes':
                        self.notebook.change_tag(note.name.value, value, input('Enter new tag: '))
                        notebook.save_data()
                    elif answer == 'no':
                        print('Ok, try again')
                        continue
                    else:
                        raise ValueError(f"Sorry, {answer} is not correct. Try again!")
                elif value in note.text.value:
                    print(f"Found note:\n"
                          f"{note}\n"
                          f"Do you want to change text note?")
                    answer = input('Enter yes or no: ').casefold()
                    if answer == 'yes':
                        self.notebook.change_text(note.name.value, input('Enter new text: '))
                        notebook.save_data()
                    elif answer == 'no':
                        print('Ok, try again')
                        break
                    else:
                        raise ValueError(f"Sorry, {answer} is not correct. Try again!")
            break

    def add_tag(self):
        print(f"{'=' * 5} Add tag to the note: {'=' * 5}")
        name = input('Enter name: ').strip()
        tag = input('Enter new tag: ').strip()
        self.notebook.add_tag(name, tag)
        self.notebook.save_data()