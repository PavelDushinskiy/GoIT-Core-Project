from typing import List, Callable
from abc import ABC, abstractmethod


class BotFeature(ABC):
    """
    A base class that handles commands for the features.
    """

    @abstractmethod
    def __init__(self, command_handlers: dict[str, Callable]):
        self.command_handlers = command_handlers

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def handle_command(self, command: str, *args: List[str]):
        handler = self.command_handlers.get(command, None)
        if handler:
            return handler(*args)
        else:
            raise ValueError("Unexpected command")
