from typing import List, Callable
import pickle


class BotFeature:
    """
    A base class that handles commands for the features.
    """

    def __init__(self, command_handlers: dict[str, Callable]):
        self.command_handlers = command_handlers
        self.data = {}

    @classmethod
    def load_data(cls, filepath):
        with open(filepath, 'rb') as f:
            try:
                loaded_data = pickle.load(f)
                return loaded_data
            except Exception:
                print("Can't load data from file")
                return None

    def name(self):
        pass

    def handle_command(self, command: str, *args: List[str]):
        handler = self.command_handlers.get(command, None)
        if handler:
            return handler(*args)
        else:
            raise ValueError("Unexpected command")

    @staticmethod
    def backup_data(handler):
        with open(handler.save_file, 'wb') as f:
            pickle.dump(handler.data, f)

    def add_record(self, record):
        self.data[record.name] = record

    def remove_record(self, record_name):
        if self.record_exists(record_name):
            del self.data[record_name]
            return f"{record_name} was deleted successfully!"
        else:
            return f"{record_name} was not found!"

    def record_exists(self, record_name):
        return record_name in self.data

    def show_all(self):
        if self.data:
            result = ""
            for record in self.data.values():
                result += str(record) + "\n"
            return result
        else:
            return "You don't have any data yet."

    def search_record(self, needle: str) -> str:
        result = list(filter(lambda record: needle in str(record), self.data.values()))
        if result:
            return "\n".join([str(r) for r in result])
        else:
            return "Sorry, couldn't find any records that match the query."
