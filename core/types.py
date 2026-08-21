from typing import TypeVar, List, Tuple, Callable

T = TypeVar('T', covariant=True)

FitnessFunction = Callable[[T], float | int]

Initializer = Callable[[], T]

SelectionOperator = Callable[[List[T], List[float | int], 'GAConfig'], List[T]]
CrossoverOperator = Callable[[List[T], 'GAConfig'], List[T]]
MutationOperator = Callable[[List[T], 'GAConfig'], List[T]]

ReplacementOperator = Callable[[List[T], List[T], List[float | int], List[float | int], 'GAConfig'], Tuple[List[T], List[float | int]]]