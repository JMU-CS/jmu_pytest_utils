"""Strip comments and docstrings from a file."""

# Based on: https://gist.github.com/BroHui/aca2b8e6e6bdf3cb4af4b246c9837fa3

import sys
import token
import tokenize
import io


def remove_comments(source):
    """Remove comments from the given code.

    Args:
        source (str): Original source code.

    Returns:
        str: Modified source code.
    """
    mod = io.StringIO()  # open(fname + ",strip", "w")

    prev_toktype = token.INDENT
    last_lineno = -1
    last_col = 0

    tokgen = tokenize.generate_tokens(io.StringIO(source).readline)
    for toktype, ttext, (slineno, scol), (elineno, ecol), ltext in tokgen:
        if 0:  # Change to if 1 to see the tokens fly by.
            print("%10s %-14s %-20r %r" % (
                tokenize.tok_name.get(toktype, toktype),
                "%d.%d-%d.%d" % (slineno, scol, elineno, ecol),
                ttext, ltext
            ))
        if slineno > last_lineno:
            last_col = 0
        if scol > last_col:
            mod.write(" " * (scol - last_col))
        if (toktype == token.STRING and
                (prev_toktype == token.INDENT or prev_toktype == token.NEWLINE)):
            # Docstring
            # mod.write("#--")
            pass
        elif toktype == tokenize.COMMENT:
            # Comment
            # mod.write("##\n")
            pass
        else:
            mod.write(ttext)
        prev_toktype = toktype
        last_col = ecol
        last_lineno = elineno
    return mod.getvalue()


if __name__ == '__main__':
    print(remove_comments(sys.argv[1]))
