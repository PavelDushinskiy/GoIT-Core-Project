from typing import List, Any, Callable

from features.addressbook import AddressBook
from features.files import Files
from features.notebook import Notebook
from features.bot_feature import BotFeature

ADDRESS_BOOK_FILE = "assistant-bot/address_book.bin"
NOTEBOOK_FILE = "assistant-bot/notebook.bin"


class AssistantBot:
    """
    Assists a user with managing the features of the application.
    """

    def __init__(self):
        self.features = [
            Files(),
            Notebook(NOTEBOOK_FILE),
            #AddressBook(ADDRESS_BOOK_FILE)
        ]

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
                return f"Sorry: {err}"
            except ValueError as err:
                return f"ValueError: {err}"
            else:
                return result

        return exception_handler

    @input_error
    def handle(self, handler_name: str, args: List[str]) -> str:
        """
        Calls the commands of the features and returns results.

        :param handler_name: command given by the user
        :param args: arguments to call the command with
        :return: result of execution of the command
        """
        if handler_name == "help":
            return self.help()

        command_handler = self._get_handler(handler_name)

        if command_handler:
            command_arguments = args[1:] if len(args) > 1 else []
            return command_handler.handle_command(args[0], *command_arguments)
        else:
            raise ValueError(f"Unexpected command: {command_handler}")

    def _get_handler(self, handler_name: str) -> Any:
        handler = next(filter(lambda x: x.name() == handler_name, self.features), None)
        return handler

    @staticmethod
    def help():
        return """
        To work with contacts type:
        - contacts add name
        - contacts add phone name phone (in format +123456789011 or 1234567890)
        - contacts add email name email
        - contacts add birthday name birthdate (in format dd.mm.yyyy)
        - contacts add address name address
        - contacts change phone name old_phone new_phone
        - contacts change email name new_email
        - contacts change address name new_address
        - contacts remove name
        - contacts show
        - contacts search name/phone

        To work with notes type:
        - notes make 
        - notes change title
        - notes remove title
        - notes show 
        - notes search tag/title/text

        To check a list of people who have birthdays in the given interval type:
        - contacts birthdays num_of_days

        To sort the given folder type:
        - files sort path
        """

    def autocomplete(self):
        result = []
        for feature in self.features:
            for command_name in feature.command_handlers.keys():
                result.append(f"{feature.name()} {command_name}")
        return result

    def backup_data(self):
        for handler in self.features:
            if isinstance(handler, BotFeature):
                handler.backup_data()
