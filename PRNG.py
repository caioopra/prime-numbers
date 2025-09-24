from abc import ABC, abstractmethod


class PRNG(ABC):
    """Abstract base class for Pseudo-Random Number Generators (PRNGs)."""

    @abstractmethod
    def next(self) -> int:
        """Generate the next pseudo-random number."""
        pass

    @abstractmethod
    def randbits(self, k: int) -> int:
        """Generate an integer with k random bits."""
        pass
