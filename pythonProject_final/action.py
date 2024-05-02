from abc import ABC, abstractmethod


class Action(ABC):
    def __init__(self):
        self.toString = []

    @abstractmethod
    def toDo(self) -> bool:
        pass

    @abstractmethod
    def info(self, ok: bool):
        pass
