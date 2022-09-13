from typing import Any, List
from datetime import date
import re
import pickle

from features.bot_feature import BotFeature

NAME_REGEX = re.compile(r"[a-zA-Zа-яА-Я0-9,.'\w]{2,30}")


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


class Title(Field):

    @Field.value.setter
    def value(self, title: str):
        if not re.match(NAME_REGEX, title):
            raise ValueError("Title must be between 2 and 30 characters.")
        self._value = title

    def __hash__(self):
        return self.value.__hash__()

    def __eq__(self, obj):
        return self.value == obj


class NoteRecord:

    def __init__(self, title: str, text: str, tags: List[str]) -> None:
        self.title = Title(title)
        self.text = text
        self.created = date.today()
        self.tags = tags

    def __str__(self) -> str:
        return f'{self.title.value}\n{self.text}\n{", ".join([p for p in self.tags])}\n{self.created}'

    def change_title(self, new_title: str):
        self.title = Title(new_title)

    def change_tags(self, *args: str):
        self.tags.clear()
        self.tags = list(args)

    def change_text(self, new_text: str):
        self.text = new_text

    def remove_tag(self, tag: str):
        self.tags.remove(tag)


class Notebook(BotFeature):

    def __init__(self, save_file: str):
        """
        An app feature that helps users to manage their notes.
        """
        super().__init__({
            "make": self.make,
            "change": self.change,
            "remove": self.remove_note,
            "show": self.show_all_notes,
            "search": self.search
            })
        self.save_file = save_file
        self.data = {}

    @staticmethod
    def name():
        return "notes"

    def backup_data(self):
        with open(self.save_file, 'wb') as f:
            pickle.dump(self.data, f)

    # def load_data(self):
    #     with open(self.save_file, 'rb') as f:
    #         try:
    #             loaded_data = pickle.load(f)
    #             self.data = loaded_data
    #         except Exception:
    #             self.data = {}
    #             return "Can't load data from file"

    def make(self):
        title = input('Enter the title: ').strip()

        if self.note_exists(title):
            return f"Note {title} already exists! Try another name."

        text = input('Enter the text: ')
        tags = input('Enter the tags: ').strip().split()
        note = NoteRecord(title, text, tags)
        self.add_record(note)
        return f"Note {title} was created successfully!"

    def add_record(self, record: NoteRecord) -> None:
        self.data[record.title] = record

    def change(self, *args: str):
        title = " ".join(args)
        if self.note_exists(title):
            note_to_change = self.data[title]
            while True:
                to_change = input("What do you want to change? Type title, tags or text: ")
                if to_change.lower() not in ["title", "tags", "text"]:
                    print("Unknown command")
                    continue
                elif to_change.lower() == "title":
                    new_title = input("Enter a new title: ")
                    note_to_change.change_title(new_title)
                    self.remove_note(title)
                    self.add_record(note_to_change)
                elif to_change.lower() == "tags":
                    new_tags = input("Enter new tags: ")
                    note_to_change.change_tags(new_tags)
                elif to_change.lower() == "text":
                    new_text = input("Enter new text here: ")
                    note_to_change.change_text(new_text)

                to_continue = input("Do you want to change something else in this note? Enter y or n: ")
                if to_continue.lower() not in ["y", "n"]:
                    print("Enter y or n.")
                    continue
                elif to_continue.lower() == "y":
                    continue
                else:
                    return "The note was changed successfully!"
        else:
            raise KeyError("Note with this title doesn't exist.")

    def remove_note(self, title):
        if self.note_exists(title):
            del self.data[title]
            return f"Note {title} was deleted successfully!"
        else:
            return f"Note {title} was not found! Please try again."

    def show_note(self, title) -> str:
        return str(self.data[title])

    def show_all_notes(self) -> str:
        result = ""
        for note in self.data.values():
            result += str(note) + "\n"
        return result

    def search(self, needle: str):
        result = list(filter(lambda note: needle in str(note), self.data.values()))
        if result:
            return "\n".join([str(r) for r in result])
        else:
            return "Sorry, couldn't find any notes that match the query."

    def note_exists(self, title) -> bool:
        return title in self.data
