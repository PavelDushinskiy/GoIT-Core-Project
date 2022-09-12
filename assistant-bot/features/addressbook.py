from typing import List

from bot_feature import BotFeature


class AddressBook(BotFeature):
    """
    A feature that allows users to manage their contacts.
    """

    def __init__(self, file_path: str):
        super().__init__({
            "add": self.add,
            "change": self.change,
            "remove": self.remove,
            "show": self.show,
            "birthdays": self.check_birthdays,
            "search": self.search
        })
        # TODO: Implement deserialization
        print(f"Restoring the address book from {file_path}")

    def name(self):
        return "contacts"

    # TODO: Implement the methods

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
