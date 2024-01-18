#!/usr/bin/python3
"""
    Script to convert Markdown to HTML.
"""

from sys import argv, stderr
from os.path import exists


def main():
    """
    Main function to convert Markdown to HTML.
    """
    if len(argv) < 3:
        perror("Usage: ./markdown2html.py README.md README.html")
        exit(1)

    input_file = argv[1]
    output_file = argv[2]

    if not exists(input_file):
        perror(f"Missing {input_file}")
        exit(1)

    # Markdown to HTML conversion

    print(f"Converted {input_file} to {output_file}")
    exit(0)


def perror(message):
    """
    Print error message to STDERR.
    """
    print(message, file=stderr)


if __name__ == "__main__":
    main()
