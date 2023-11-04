"""
This module contains examples of Python code.
"""

import discordbot


def main() -> None:
    """Main function."""
    print(discordbot.ollama.get_answer('Say hi'))

if __name__ == "__main__":
    main()
