"""Pygments lexer for the MDMA template format.

Grammar reference: docs/grammar.md in https://github.com/Dastfox/mdma
"""

from pygments.lexer import RegexLexer, bygroups, default, include, words
from pygments.token import (
    Comment,
    Generic,
    Keyword,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Text,
    Whitespace,
)

__all__ = ["MdmaLexer"]
__version__ = "0.1.0"

JINJA_KEYWORDS = ("if", "elif", "else", "endif", "for", "endfor", "in", "and", "or", "not")


class MdmaLexer(RegexLexer):
    """Lexer for `.mdma` files: a typed `@inputs` header followed by named
    Jinja-flavored Markdown blocks (see docs/grammar.md)."""

    name = "MDMA"
    aliases = ["mdma"]
    filenames = ["*.mdma"]

    tokens = {
        "root": [
            (r"^(@inputs)\b", Keyword.Declaration, "inputs"),
            (r"(?=^<)", Text, "header"),
            # Docs often excerpt a bare template fragment with no @inputs
            # header or enclosing block tag -- treat that as block body too.
            default("body"),
        ],
        "inputs": [
            (r"(?=^<)", Text, "#pop"),
            (
                r"([A-Za-z_]\w*)(\s*)(:)(\s*)(string|number|boolean|object)(\[\])?",
                bygroups(
                    Name.Variable,
                    Whitespace,
                    Punctuation,
                    Whitespace,
                    Keyword.Type,
                    Keyword.Type,
                ),
            ),
            (r"(\s*)(=)(\s*)", bygroups(Whitespace, Operator, Whitespace)),
            (r'""', String),
            (r'"[^"\n]*"', String),
            (r"\[\]", Punctuation),
            (r"\btrue\b|\bfalse\b", Keyword.Constant),
            (r"-?\d+(?:\.\d+)?", Number),
            (r"\n", Whitespace),
            (r"[ \t]+", Whitespace),
        ],
        "header": [
            (r">", Punctuation, ("#pop", "body")),
            (r"^<", Punctuation),
            (r"\bmultiple\b(?=\s*:)", Keyword),
            (r"\bname\b(?=\s*:)", Keyword),
            (r"\bin\b", Keyword),
            (r"[A-Za-z0-9_][\w.-]*", Name.Variable),
            (r"[:.]", Punctuation),
            (r"\s+", Whitespace),
        ],
        "body": [
            (r"(?=^<)", Text, ("#pop", "header")),
            (r"^#{1,6}(?=[ \t])", Generic.Heading),
            (r"^[ \t]*>(?=[ \t])", Generic.Emph),
            (r"^[ \t]*[-*](?=[ \t])", Generic.Strong),
            (r"\*\*[^*\n]+\*\*", Generic.Strong),
            (r"\{\{-?", String.Interpol, "jinja-expr"),
            (r"\{%-?\s*", String.Interpol, "jinja-tag"),
            (r"\{#", Comment.Multiline, "jinja-comment"),
            (r"\n", Text),
            (r".", Text),
        ],
        "jinja-comment": [
            (r"#\}", Comment.Multiline, "#pop"),
            (r"[^#]+|#", Comment.Multiline),
        ],
        "jinja-expr": [
            (r"-?\}\}", String.Interpol, "#pop"),
            include("jinja-inner"),
        ],
        "jinja-tag": [
            (r"-?%\}", String.Interpol, "#pop"),
            include("jinja-inner"),
        ],
        "jinja-inner": [
            (r"\s+", Whitespace),
            (words(JINJA_KEYWORDS, suffix=r"\b"), Keyword),
            (r"\btrue\b|\bfalse\b", Keyword.Constant),
            (r"==|!=|>=|<=|>|<", Operator),
            (r"(\|)(\s*)([A-Za-z_]\w*)", bygroups(Operator, Whitespace, Name.Function)),
            (r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*", Name.Variable),
            (r'"[^"\n]*"', String),
            (r"-?\d+(?:\.\d+)?", Number),
            (r"[(),]", Punctuation),
        ],
    }
