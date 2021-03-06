import re
import tokenize
from io import StringIO


class CodeTrimmer:
    def __init__(self, code):
        self.code = code

    def trim(self):
        self.remove_comments_and_docstrings()
        self.remove_white_spaces()
        return self.code

    def trim_comment(self):
        self.remove_comments_and_docstrings()
        return self.code

    def remove_comments_and_docstrings(self):
        out = ""
        prev_toktype = tokenize.INDENT
        last_lineno = -1
        last_col = 0
        for tok in tokenize.generate_tokens(StringIO(self.code).readline):
            token_type = tok[0]
            token_string = tok[1]
            start_line, start_col = tok[2]
            end_line, end_col = tok[3]
            if start_line > last_lineno:
                last_col = 0
            if start_col > last_col:
                out += (" " * (start_col - last_col))
            if token_type == tokenize.COMMENT:
                pass
            elif token_type == tokenize.STRING:
                if prev_toktype != tokenize.INDENT:
                    if prev_toktype != tokenize.NEWLINE:
                        if start_col > 0:
                            out += token_string
            else:
                out += token_string
            prev_toktype = token_type
            last_col = end_col
            last_lineno = end_line
        out = '\n'.join(l for l in out.splitlines() if l.strip())
        return out

    def remove_white_spaces(self):
        self.code = re.sub(r"\s+", "", self.code)
        return self.code
