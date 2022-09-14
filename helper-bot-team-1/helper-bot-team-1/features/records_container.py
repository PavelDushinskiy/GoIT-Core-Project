import pickle
from collections import UserDict


class RecordsContainer(UserDict):
    """
    A class that holds records.
    """

    def __init__(self, save_file):
        super().__init__()
        self.data = RecordsContainer.load_data(save_file) or {}

    @classmethod
    def load_data(cls, filepath: str) -> None | str:
        """
        Loads records from a file.

        :param filepath: a backup file
        """

        with open(filepath, 'rb') as f:
            try:
                loaded_data = pickle.load(f)
                return loaded_data
            except EOFError:
                pass

    @staticmethod
    def backup_data(handler) -> None:
        """
        Saves records to a file.

        :param handler: whose dara to save
        """

        with open(handler.save_file, 'wb') as f:
            pickle.dump(handler.data, f)

    def add_record(self, record) -> None:
        """
        Adds a new record.

        :param record:
        :return:
        """
        self.data[record.name] = record

    def remove_record(self, *args: str) -> str:
        """
        Removes a given record. Throws exception if the record does not exist.

        :param record_name: a record to remove
        :return: success message
        """

        record_name = " ".join(args)
        if self.record_exists(record_name):
            del self.data[record_name]
            return f"{record_name} was deleted successfully!"
        else:
            raise KeyError(f"{record_name} was not found!")

    def record_exists(self, record_name: str) -> bool:
        """
        Checks if record exists.

        :param record_name: a name of a record
        :return: True is exists False otherwise
        """

        return record_name in self.data

    def show_all(self) -> str:
        """
        Shows all existing records.

        :return: all records as a string
        """

        if self.data:
            result = ""
            for record in self.data.values():
                result += "\n" + str(record) + "\n"
            return result
        else:
            return "You don't have any data yet."

    def search_record(self, needle: str) -> str:
        """
        Searches and returns a record that contains a needle.

        :param needle: what to search
        :return: a result string
        """
        result = list(filter(lambda record: needle in str(record).lower(), self.data.values()))
        if result:
            return "\n".join(["\n" + str(r) for r in result])
        else:
            return "Sorry, couldn't find any records that match the query."
