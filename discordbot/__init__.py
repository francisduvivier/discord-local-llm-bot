"""
__init__ file.
"""

from .ollama import get_answer
from .version import __version__
__all__ = ["get_answer", "__version__"]
