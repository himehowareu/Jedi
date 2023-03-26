#!/usr/bin/env python3

__author__ = "Raymond Hettinger"

import builtins
import functools
import keyword
import tokenize


def is_builtin(s):
    return hasattr(builtins, s)


def combine_range(lines, start, end):
    (srow, scol), (erow, ecol) = start, end
    if srow == erow:
        return lines[srow - 1][scol:ecol], end
    rows = [lines[srow - 1][scol:]] + lines[srow : erow - 1] + [lines[erow - 1][:ecol]]
    return "".join(rows), end


def analyze_python(source):

    lines = source.splitlines(True)
    lines.append("")
    readline = functools.partial(next, iter(lines), "")
    kind = tok_str = ""
    tok_type = tokenize.COMMENT
    written = (1, 0)
    for tok in tokenize.generate_tokens(readline):
        prev_tok_type, prev_tok_str = tok_type, tok_str
        tok_type, tok_str, (srow, scol), (erow, ecol), _ = tok
        kind = ""
        if tok_type == tokenize.COMMENT:
            kind = "comment"
        elif tok_type == tokenize.OP and tok_str[:1] not in "{}[](),.:;@":
            kind = "operator"
        elif tok_type == tokenize.STRING:
            kind = "string"
            if prev_tok_type == tokenize.INDENT or scol == 0:
                kind = "docstring"
        elif tok_type == tokenize.NAME:
            if tok_str in ("def", "class", "import", "from"):
                kind = "definition"
            elif prev_tok_str in ("def", "class"):
                kind = "defname"
            elif keyword.iskeyword(tok_str):
                if tok_str in ("or", "and", "not"):
                    kind = "com"
                else:
                    kind = "keyword"
            elif is_builtin(tok_str) and prev_tok_str != ".":
                kind = "builtin"
        if kind:
            text, written = combine_range(lines, written, (srow, scol))
            yield "", text
            text, written = tok_str, (erow, ecol)
            yield kind, text
    line_upto_token, written = combine_range(lines, written, (erow, ecol))
    yield "", line_upto_token


colors = {
    "comment": ("\033[0;31m", "\033[0m"),
    "string": ("\033[0;36m", "\033[0m"),
    "docstring": ("\033[0;32m", "\033[0m"),
    "keyword": ("\033[0;33m", "\033[0m"),
    "builtin": ("\033[0;35m", "\033[0m"),
    "definition": ("\033[0;33m", "\033[0m"),
    "defname": ("\033[0;34m", "\033[0m"),
    "defname": ("\033[0;96m", "\033[0m"),
    "com": ("\033[0;91m", "\033[0m"),
    "operator": ("\033[0;95m", "\033[0m"),
}


def ansi_highlight(classified_text):
    result = []
    for kind, text in classified_text:
        opener, closer = colors.get(kind, ("", ""))
        result += [opener, text, closer]
    return "".join(result)
