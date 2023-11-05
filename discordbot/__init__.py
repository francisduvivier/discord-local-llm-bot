"""
__init__ file.
"""

from .model_manager import predict, stream
from .bot import main
from .version import __version__

__all__ = ["stream", "predict", "__version__"]

if __name__ == "__main__":
    main()
