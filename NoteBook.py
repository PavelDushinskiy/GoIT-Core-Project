from collections import UserDict
from typing import List
from datetime import date
import pickle
from prettytable import PrettyTable

notes = PrettyTable()


class Field:
    def __init__(self, value) -> None:
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class NoteName(Field):
    @Field.value.setter
    def value(self, name: str):
        if not isinstance(name, str):
            raise TypeError('The name must be a string!')
        # if not re.match(r"^[a-zA-Z]{1,25}$", name):
        #     raise ValueError('The name must contain only letters up to 25 characters long!')
        self._value = name


class NoteTag(Field):
    pass
    # @Field.value.setter
    # def value(self, tag: str):
    #     if not isinstance(tag, str):
    #         raise TypeError('The phone must be a string!')
    #     self._value = tag


class NoteText(Field):
    pass
    # @Field.value.setter
    # def value(self, note_text: str):
    #     if not isinstance(note_text, str):
    #         raise TypeError('The email must be a string!')
    #     self._value = note_text


class NoteRecord:
    def __init__(self, note_name: NoteName, note_text: NoteText, tag: List[NoteTag] = []) -> None:
        self.note_name = note_name
        self.note_text = note_text
        self.note_tags = tag
        self.created = date.today()
        self.modified = date.today()

    def __repr__(self):
        return f'{self.note_name.value} {self.note_text.value} {", ".join([p.value for p in self.note_tags])} {self.created} {self.modified} '

    def add_tag(self, tag: NoteTag):
        if tag.value not in [p.value for p in self.note_tags]:
            self.note_tags.append(tag)
            self.modified = date.today()
            return tag

    def remove_tag(self, tag: NoteTag):
        if tag.value in [p.value for p in self.note_tags]:
            self.note_tags.remove(tag)
            self.modified = date.today()
            return tag

    def change_name(self, name: NoteName):
        self.note_name = name
        self.modified = date.today()
        return name


class NoteBook(UserDict):
    def add_note(self, record: NoteRecord) -> NoteRecord | None:
        if not self.data.get(record.note_name.value):
            self.data[record.note_name.value] = record
            return record

    def del_note(self, key: str):
        note_del = self.data.get(key)
        if note_del:
            self.data.pop(key)
            return note_del

    def find_note(self, note_name: NoteName):
        return self.data.get(note_name.value)

    def save_file(self):
        with open('my_NoteBook', 'wb') as f:
            pickle.dump(self, f)

    def load_file(self):
        try:
            with open('my_NoteBook', "rb") as f:
                self.data = pickle.load(f)
        except FileNotFoundError:
            return 'File not found!'

    def iterator(self, n=20):
        step = 0
        result = '*' * 20 + '\n'
        for k, v in self.data.items():
            result += f'{k} {v}\n'
            step += 1
            if step >= n:
                yield result
                result = '_' * 20 + '\n'
                step = 0
        yield result


notebook = NoteBook()


def add_note():
    name = NoteName(input('Enter note name: '))
    text = NoteText(input('Enter text: '))
    tag = NoteTag(input('Enter tag: '))
    notebook.add_note(NoteRecord(name, text, [tag]))
    return f"Note {name.value} added!"


def show_notes():
    notes.field_names = ["Title", "Text", "Teg", "Created", "Modified"]
    for k, v in notebook.data.items():
        notes.add_row(
            [v.note_name.value, v.note_text.value, ", ".join([p.value for p in v.note_tags]), v.created, v.modified])
    return notes
    # if not notebook:
    #     return 'NoteBook are empty'
    # result = "My NoteBook:\n"
    # print_result = notebook.iterator()
    # for line in print_result:
    #     result += line
    # return result


def to_exit():
    return 'Good bye!'


def change_note_name():
    name = NoteName(input('Enter note name: '))
    new_name = NoteName(input('Enter new name: '))
    note = notebook.find_note(name)
    if note:
        note.change_name(new_name)
        return f"Note {name.value} changed to {new_name.value}!"
    return f"Note {name.value} not found!"


def change_note_text():
    name = NoteName(input('Enter note name: '))
    new_text = NoteText(input('Enter new text: '))
    note = notebook.find_note(name)
    if note:
        note.note_text = new_text
        return f"Note {name.value} changed!"
    return f"Note {name.value} not found!"


def add_tag():
    name = NoteName(input('Enter note name: '))
    tag = NoteTag(input('Enter tag: '))
    note = notebook.find_note(name)
    if note:
        note.add_tag(tag)
        return f"Tag {tag.value} added to {name.value}!"
    return f"Note {name.value} not found!"


def remove_tag():
    name = NoteName(input('Enter note name: '))
    tag = NoteTag(input('Enter tag: '))
    note = notebook.find_note(name)
    if note:
        note.remove_tag(tag)
        return f"Tag {tag.value} removed from {name.value}!"
    return f"Note {name.value} not found!"


def del_note():
    name = NoteName(input('Enter note name: '))
    note = notebook.del_note(name.value)
    if note:
        return f"Note {name.value} deleted!"
    return f"Note {name.value} not found!"


def find_note():
    name = NoteName(input('Enter note name: '))
    note = notebook.find_note(name)
    if note:
        return f"{note}"
    return f"Note {name.value} not found!"


def unknown_command():
    return 'Unknown command!'


def help():
    helper = PrettyTable()
    helper.field_names = ["Command", "Description"]
    comm = [["add", "new"], ["change", "replace"], ["change text", "text"], ["show all", "show"],
            ["good bye", "exit", "bye", "stop"], ["add tag", "tag"], ["remove tag", "remove tag"],
            ["del", "delete", "remove"], ["find", "search"]]
    description = ["Add new note", "Change note name", "Change note text", "Show all notes", "Exit from notebook",
                   "Add tag to note", "Remove tag from note", "Delete note", "Find note"]
    for i, j in enumerate(comm):
        helper.add_row([j, description[i]])
    print(helper)


commands = {
    add_note: ["add", "new"],
    change_note_name: ["change", "replace"],
    change_note_text: ["change text", "text"],
    show_notes: ["show all", "show"],
    to_exit: ["good bye", "close", "exit", ".", "bye", "stop"],
    add_tag: ["add tag", "tag"],
    remove_tag: ["remove tag", "remove tag"],
    del_note: ["del", "delete", "remove"],
    find_note: ["find", "search"],
    help: ["help"]
}


def input_parser(user_input):
    for key, values in commands.items():
        for i in values:
            if user_input.lower().startswith(i.lower()):
                return key, user_input[len(i):].strip().split()
    return unknown_command, []


def main():
    notebook.load_file()
    help()
    while True:
        user_input = input('Waiting your command:>>> ')
        command, parser_data = input_parser(user_input)
        print(command(*parser_data))
        if command is to_exit:
            notebook.save_file()
            break


if __name__ == "__main__":
    main()
