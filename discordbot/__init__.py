"""
__init__ file.
"""

from .model_manager import predict, predict_streaming
from .bot import main
from .version import __version__

__all__ = ["predict_streaming", "predict", "__version__"]

if __name__ == "__main__":
    main()
