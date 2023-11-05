"""
This module contains examples of Python code.
"""

import discordbot


def main() -> None:
    """Main function."""
    print(discordbot.ollama.predict('Say hi'))

if __name__ == "__main__":
    main()
