"""Common interface every engine adapter must follow (filled in Phase 4)."""
from abc import ABC, abstractmethod


class BaseEngine(ABC):
    name = "base"

    @abstractmethod
    def load(self, path: str): ...

    @abstractmethod
    def filter(self, data, column: str, op: str, value): ...

    @abstractmethod
    def select(self, data, columns: list): ...

    @abstractmethod
    def sort(self, data, column: str, ascending: bool = True): ...

    @abstractmethod
    def group_agg(self, data, by: list, column: str, agg: str): ...

    @abstractmethod
    def join(self, left, right, on: str, how: str = "inner"): ...

    @abstractmethod
    def fill_missing(self, data, column: str, value): ...

    @abstractmethod
    def drop_duplicates(self, data): ...

    @abstractmethod
    def to_pandas(self, data):
        """Convert result to pandas so outputs can be compared across engines."""
