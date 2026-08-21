from typing import Protocol, TypeVar, Tuple
from abc import abstractmethod

T = TypeVar('T', bound='Individual', covariant=True)


class Individual(Protocol):

    @abstractmethod
    def copy(self: T) -> T:
        ...

    @abstractmethod
    def mutate(self, rate: float) -> None:
        ...

    @abstractmethod
    def crossover(self: T, other: T) -> Tuple[T, T]:
        ...

    @abstractmethod
    def __len__(self) -> int:
        ...