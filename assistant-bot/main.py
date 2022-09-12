from typing import Tuple
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from bot import AssistantBot


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
        command_completer = WordCompleter(bot.autocomplete())

        try:
            while True:
                feature, args = self.parse_command(prompt("What do you want to do? ", completer=command_completer))
                if feature in ["goodbye", "close", "exit"]:
                    print("Goodbye!")
                    break
                else:
                    result = bot.handle(feature, args)
                    if result:
                        print(result)
        except Exception as err:
            print(err)

    @staticmethod
    def parse_command(user_input: str) -> Tuple[str, list[str]]:
        """
        Parses the input into a feature, command, and zero or more arguments.

        :param user_input: a string that user provides
        :return: tuple(command, *args)
        """
        if len(user_input) == 0:
            raise ValueError("No command is given.")
        user_input = user_input.split()
        command = user_input[0].lower()
        args = user_input[1:]
        return command, args


if __name__ == "__main__":
    App().run()