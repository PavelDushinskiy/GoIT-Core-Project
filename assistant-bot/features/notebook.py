from typing import List
from collections import UserDict

from features.bot_feature import BotFeature


class Notebook(BotFeature, UserDict):
    """
    An app feature that helps users to manage their notes.
    """
    def __init__(self, file_path):
        super().__init__({
            "add": self.add,
            "change": self.change,
            "remove": self.remove,
            "show": self.show,
            "search": self.search
        })
        # TODO: Implement deserialization
        print(f"Restoring the notebook from {file_path}")

    # TODO: Implement the methods

    def name(self):
        return "notes"

    def add(self, *args: List[str]) -> str:
        print(args)
        raise NotImplementedError("This method is not implemented yet")

    def change(self, *args: List[str]) -> str:
        print(args)
        raise NotImplementedError("This method is not implemented yet")

    def remove(self, *args: List[str]) -> str:
        print(args)
        raise NotImplementedError("This method is not implemented yet")

    def show(self, *args: List[str]) -> str:
        print(args)
        raise NotImplementedError("This method is not implemented yet")

    def check_birthdays(self, *args: List[str]) -> str:
        print(args)
        raise NotImplementedError("This method is not implemented yet")

    def search(self, *args: List[str]) -> str:
        print(args)
        raise NotImplementedError("This method is not implemented yet")

    def save_data(self):
        raise NotImplementedError("This method is not implemented yet")
