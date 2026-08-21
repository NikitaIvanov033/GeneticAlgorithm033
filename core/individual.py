from typing import Protocol, TypeVar, Tuple

T = TypeVar('T', bound='Individual', covariant=True)


class Individual(Protocol):

    def copy(self: T) -> T:
        ...

    def mutate(self, rate: float) -> None:
        ...

    def crossover(self: T, other: T) -> Tuple[T, T]:
        ...

    def __len__(self) -> int:
        ...