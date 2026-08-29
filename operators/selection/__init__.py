"""
Selection operators.

Available:
- tournament_selection: tournament selection (created via create_tournament_selection)
- rank_selection: rank-based selection
"""

from .rank import rank_selection
from .tournament import create_tournament_selection

__all__ = [
    'rank_selection',
    'create_tournament_selection',
]