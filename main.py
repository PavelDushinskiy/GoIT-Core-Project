from typing import Tuple, Callable, List, Any
from re import match
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import sorter


class App:
    """
    Communicates with the user.

    Takes input from the user, parses it and sends it to the assistant bot. Responds with the result
    from the bot. Terminates the app when the user inputs one of the stop words. Before terminating, saves the contacts
    into a file and restores them from the file when run again.
    """

    def run(self):
        """
        Waits for the user input in an infinite loop. Terminates when one of the stop words is given.

        :return: result of running the command by the bot
        """
        bot = AssistantBot()
        command_completer = WordCompleter([
            "add contact", "add phone", "add email", "add birthday", "add address", "change phone", "change email",
            "change address", "remove contact", "show contact", "search contact", "change note", "remove note",
            "show note", "search note", "birthdays", "sort"
        ])

        try:
            while True:
                command, args = self.parse_command(prompt("What do you want to do? ", completer=command_completer))
                if command in ["goodbye", "close", "exit"]:
                    print("Goodbye!")
                    break
                else:
                    result = bot.handle(command, args)
                    if result:
                        print(result)
        except Exception as err:
            print(err)

    @staticmethod
    def parse_command(user_input: str) -> Tuple[str, list[str]]:
        """
        Parses the input into a command and zero or more arguments.

        :param user_input: a string that user provides
        :return: tuple(command, *args)
        """
        if len(user_input) == 0:
            raise ValueError("No command is given.")
        user_input = user_input.split()
        command = user_input[0].lower()
        args = user_input[1:]
        return command, args


def phone_is_valid(phone_number: str) -> bool:
    """
    Checks if the phone is in the right format.

    :param phone_number: phone number
    :return: True if matches the format False otherwise
    """
    if match(r"(\+?\d{12}|\d{10})", phone_number):
        return True
    return False


def email_is_valid(email: str) -> bool:
    """
    Checks if the email is in the right format.

    :param email: email
    :return: True if matches the format False otherwise
    """
    if match(r"[a-zA-Z][a-zA-Z_.0-9]+@[a-zA-Z_]+?\.[a-zA-Z]{2,}", email):
        return True
    return False


def birthday_is_valid(date: str) -> bool:
    """
    Checks if the birthdate is in the right format.

    :param date: birthdate
    :return: True if matches the format False otherwise
    """
    if match(r"\d{2}\.\d{2}\.\d{4}", date):
        return True
    return False


class AssistantBot:
    """
    Assists a user with managing their address book (adding, deleting, changing, displaying entries).
    """
    def __init__(self):
        self.commands = {
            "add": self.add_contact_info,
            "change": self.change,
            "remove": self.remove,
            "show": self.show,
            "birthdays": self.check_birthdays,
            "search": self.search,
            "note": self.make_note,
            "sort": self.sort_folder,
            "help": self.help
        }
        self.addressbook = AddressBook()
        self.notebook = Notebook()

    @staticmethod
    def input_error(func: Callable) -> Callable[[tuple[Any, ...]], str | Any]:
        """
        A decorator that catches the domain-level exceptions and returns human-readable error message.
        """
        def exception_handler(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except TypeError as err:
                return f"Invalid input, some info is missing: {err}"
            except KeyError as err:
                return f"Sorry, no such command: {err}"
            except ValueError as err:
                return f"ValueError: {err}"
            else:
                return result

        return exception_handler

    @input_error
    def handle(self, command: str, args: List[str]) -> str:
        """
        Calls the command and returns a result of it.

        :param command: command given by the user
        :param args: arguments to call the command with
        :return: result of execution of the command
        """
        handler = self.commands[command]
        return handler(*args)

    @input_error
    def add_contact_info(self, mode: str, name: str, *args: str) -> None:
        """
        Calls and returns functions that add the given information about a person to the addressbook.

        :param mode: what to add
        :param name: name of a person
        """
        if name in self.addressbook:
            record = self.addressbook[name]
        else:
            record = Record(name)

        match mode:
            case "contact":
                return self.addressbook.add_record(record)
            case "phone":
                if phone_is_valid(args[0]):
                    return record.add_phone(args[0])
                else:
                    raise ValueError("Phone doesn't match the format +123456789011 or 1234567890.")
            case "email":
                if email_is_valid(args[0]):
                    return record.add_email(args[0])
                else:
                    raise ValueError("Email doesn't seem to be valid.")
            case "birthday":
                if birthday_is_valid(args[0]):
                    return record.add_birthday(args[0])
                else:
                    raise ValueError("Enter the date in format dd.mm.yyyy.")
            case "address":
                return record.add_address(args)
            case _:
                raise ValueError("Unknown command (type 'contact', 'phone', 'email', 'birthday', 'address').")

    @input_error
    def change(self, mode: str, *args: str) -> None:
        """
        Calls and returns functions that change the given information.

        :param mode: what to change
        """
        match mode:
            case "phone":
                record = self.addressbook[args[0]]
                old_phone = args[1]
                new_phone = args[2]
                return record.change_phone(old_phone, new_phone)
            case "email":
                record = self.addressbook[args[0]]
                return record.change_email(args[1])
            case "address":
                record = self.addressbook[args[0]]
                return record.change_address(args[1:])
            case "note":
                return self.notebook.change_note(args)
            case _:
                raise ValueError("Unknown command (type 'phone', 'email', 'address', 'note').")

    @input_error
    def show(self, mode: str, *args: str) -> str:
        """
        Returns the record of the given person as a human-readable message or a note by its title.

        :param mode: what to show
        """
        match mode:
            case "contact":
                return self.addressbook.show_record(args)
            case "note":
                return self.notebook.show_note(args)
            case _:
                raise ValueError("Unknown command (type 'contact', 'note').")

    def remove(self, mode: str, *args: str) -> None:
        """
        Calls and returns a function that deletes the given record from the addressbook or the given note from the
        notebook.

        :param mode: what to remove
        """
        match mode:
            case "contact":
                record = self.addressbook[args[0]]
                return self.addressbook.remove_record(record)
            case "note":
                return self.notebook.remove_note(args)
            case _:
                raise ValueError("Unknown command (type 'contact', 'note').")

    def check_birthdays(self, num_of_days: str) -> List[str]:
        """
        Returns a list of people who have birthdays in the given range of days.

        :param num_of_days: range of days
        :return: a list of people with birthdays in the given range
        """
        if num_of_days.isdigit():
            return self.addressbook.with_birthday_in_range(num_of_days)
        else:
            raise ValueError("Enter a number of days.")

    def search(self, mode: str, *args: str) -> str:
        """
        Calls and returns a function that searches contacts or notes that have coincidences with the user query.

        :param mode: where to search
        :return: contacts or notes that contain given letters or digits
        """

        match mode:
            case "record":
                return self.addressbook.search(args)
            case "note":
                return self.notebook.search(args)
            case _:
                raise ValueError("Unknown command (type 'contact', 'note').")

    def make_note(self, args: str):
        return self.notebook.make_note(args)

    def sort_folder(self, path: str):
        return sorter.sort_folder(path)

    @staticmethod
    def help():
        return """
        To work with contacts type:
        - add contact name
        - add phone name phone (in format +123456789011 or 1234567890)
        - add email name email
        - add birthday name birthdate (in format dd.mm.yyyy)
        - add address name address
        - change phone name old_phone new_phone
        - change email name new_email
        - change address name new_address
        - remove contact name
        - show contact all/name
        - search contact name/phone
        
        To work with notes type:
        - change note title
        - remove note title
        - show note all/title
        - search note tag/title
        
        To check a list of people who have birthdays in the given interval type:
        - birthdays num_of_days
        
        To sort the given folder type:
        - sort path
        """


if __name__ == "__main__":
    App().run()
