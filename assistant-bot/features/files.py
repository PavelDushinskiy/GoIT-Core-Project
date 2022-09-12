from ..sorter import sort_folder
from bot_feature import BotFeature


class Files(BotFeature):
    """
    A feature that allows a user to sort files in a given directory according to files extensions.
    """

    def __init__(self):
        super().__init__({
            "sort": self.sort
        })

    def name(self):
        return "files"

    @staticmethod
    def sort(*args: str) -> str:
        path = args[0]
        sort_folder(path)
        return "Folder is sorted"
