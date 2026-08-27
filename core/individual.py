from typing import Protocol, TypeVar

T = TypeVar('T', bound='Individual', covariant=True)


class Individual(Protocol):

    def copy(self: T) -> T:
        ...

    def __len__(self) -> int:
        ...