from abc import ABC, abstractmethod

# Define an abstract base class (ABC) named Action
class Action(ABC):
    def __init__(self):
        self.toString = []  # Initialize an empty list to store string representations of actions

    # Abstract method to define the action's task, must be implemented in subclasses
    @abstractmethod
    def toDo(self) -> bool:
        pass  # Placeholder method that will be overridden by subclasses

    # Abstract method to provide information about the action's execution status, must be implemented in subclasse
    @abstractmethod
    def info(self, ok: bool):
        pass  # Placeholder method that will be overridden by subclasses


