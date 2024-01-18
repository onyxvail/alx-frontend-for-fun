#!/usr/bin/python3
"""
    Script to convert Markdown to HTML.
"""

from sys import argv, stderr
from os.path import exists
from hashlib import md5
import re


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

    with open(input_file, "r") as f:
        markdown = f.readlines()

    html = []

    # Iterate over lines of the read file.
    index = 0
    while index < len(markdown):
        line = clean_line(markdown[index])

        # If Heading.
        if line[0] == "#":
            html.append(h(line))

        # If ordered or unordered list.
        elif line[0] == "-" or line[0] == "*":
            list_type = {"-": "ul", "*": "ol"}
            current_index = index
            ul_string = "<{}>\n".format(list_type[line[0]])
            while (current_index < len(markdown) and
                   markdown[current_index][0] in ["-", "*"]):
                ul_string += li(markdown[current_index], [])
                current_index += 1
            index = current_index - 1
            ul_string += "</{}>\n".format(list_type[line[0]])
            html.append(ul_string)

        # If only a newline.
        elif line[0] == "\n":
            line = ""

        # Else there are no special characters at the beginning of the line.
        else:
            paragraph = "<p>\n"
            new_index = index

            while new_index < len(markdown):
                line = clean_line(markdown[new_index])
                if ((new_index + 1) < len(markdown)
                        and markdown[new_index + 1] is not None):
                    next_line = markdown[new_index + 1]
                else:
                    next_line = "\n"
                paragraph += line.strip() + "\n"
                if next_line[0] in ["*", "#", "-", "\n"]:
                    index = new_index
                    break

                # If next line has no special characters.
                if next_line[0] not in ["#", "-", "\n"]:
                    br = r"<br/>"
                    br += "\n"
                    paragraph += br

                new_index += 1

            paragraph += "</p>\n"

            html.append(paragraph)

        index += 1

    # Create html text string with corresponding newlines.
    text = ""
    for line in html:
        if "\n" not in line:
            line += "\n"
        text += line

    # Write into <output_file> file.
    with open(output_file, "w") as f:
        f.write(text)

    print(f"Converted {input_file} to {output_file}")
    exit(0)


def perror(message):
    """
    Print error message to STDERR.
    """
    print(message, file=stderr)


def h(line):
    # Create heading html element
    line = line.replace("\n", "")
    line = line.strip()
    parse_space = line.split(" ")

    level = parse_space[0].count("#")

    if (level > 6):
        return (line)

    # Remove closing symbols at end of line.
    if len(parse_space[-1]) == parse_space[-1].count("#"):
        parse_space = parse_space[0:-1]

    # Concatenates the content string.
    content = ""
    for word in parse_space[1:]:
        content += word + " "
    content = content[0:-1]

    return ("<h{}>{}</h{}>".format(level, content, level))


def li(line, flags):
    # Create a list item html element.
    line = line.replace("\n", "")
    line = line.strip()
    parse_space = line.split(" ")

    # Concatenate the content string.
    content = ""
    for word in parse_space[1:]:
        content += word + " "
    content = content[0:-1]
    content = "<li>{}</li>\n".format(content)

    return (content)


def clean_line(line):
    # Styling tags with the use of Regular expressions.
    # Replace ** for <b> tags
    line = re.sub(r"\*\*(\S+)", r"<b>\1", line)
    line = re.sub(r"(\S+)\*\*", r"\1</b>", line)

    # Replace __ for <em> tags
    line = re.sub(r"\_\_(\S+)", r"<em>\1", line)
    line = re.sub(r"(\S+)\_\_", r"\1</em>", line)

    # Replace [[<content>]] for md5 hash of content.
    line = re.sub(r"\[\[(.*)\]\]", md5(r"\1".encode()).hexdigest(), line)

    # Replace ((<content>)) for no C characters on content.
    result = re.search(r"(\(\((.*)\)\))", line)
    if result is not None:
        content = result.group(2)
        content = re.sub("[cC]", "", content)
        line = re.sub(r"\(\((.*)\)\)", content, line)

    return (line)


if __name__ == "__main__":
    main()
