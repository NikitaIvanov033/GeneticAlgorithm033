"""
Replacement strategies.

Available:
- elitist_replacement: mu+lambda (parents + offspring)
- generational_replacement: mu,lambda (offspring only)
"""

from .elitist import elitist_replacement
from .generational import generational_replacement

__all__ = [
    'elitist_replacement',
    'generational_replacement',
]