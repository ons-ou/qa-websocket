import re


def extract_json(input_string: str):
    # Initialize variables to track curly braces
    start = None
    end = None
    open_braces = 0
    for i, char in enumerate(input_string):
        if char == '{':
            if open_braces == 0:
                start = i  # Mark the start of the JSON
            open_braces += 1
        elif char == '}':
            open_braces -= 1
            if open_braces == 0:
                end = i
                break

    if start is not None and end is not None:
        return input_string[start:end+1].replace("\n", " ")
    else:
        return None