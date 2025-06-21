from typing import Callable, Generator, Literal, TextIO
from dataclasses import dataclass

from src.text.processors import Segment, Position, TextWithPosition
from src.common.abc import IGraphVizible
from src.common.pretty import wrap


@dataclass(frozen=True)
class Keyword(Segment, IGraphVizible):
    value: Literal[
        "fn",
        "main",
        "{",
        "}",
        "if",
        "else",
        "return",
        "int",
        "for",
        "(",
        ")",
        "-",
        "+",
        "=",
        ";",
        "<",
        "<=",
        ">",
        ">=",
        "==",
        "!=",
    ]

    def to_graphviz(self) -> str:
        return '\t{} [label="{}"]\n'.format(
            self.node_name, wrap(str(self)).replace('"', "'")
        )


@dataclass(frozen=True)
class EOF(Segment, IGraphVizible):
    def to_graphviz(self) -> str:
        return '\t{} [label="{}"]\n'.format(
            self.node_name, wrap(str(self)).replace('"', "'")
        )


@dataclass(frozen=True)
class Ident(Segment, IGraphVizible):
    value: str

    def to_graphviz(self) -> str:
        return '\t{} [label="{}"]\n'.format(
            self.node_name, wrap(str(self)).replace('"', "'")
        )


@dataclass(frozen=True)
class Number(Segment, IGraphVizible):
    value: int

    def to_graphviz(self) -> str:
        return '\t{} [label="{}"]\n'.format(
            self.node_name, wrap(str(self)).replace('"', "'")
        )


@dataclass(frozen=True)
class ScanError:
    message: str
    pos: Position


Token = Number | Ident | Keyword | EOF

KEYWORD_VALUES: set[str] = {
    "fn",
    "main",
    "{",
    "}",
    "if",
    "else",
    "return",
    "int",
    "for",
    "(",
    ")",
    "-",
    "+",
    "=",
    ";",
    "<",
    "<=",
    ">",
    ">=",
    "==",
    "!=",
}


class Scanner:
    def __init__(self, f: TextIO):
        self._text = TextWithPosition(f)

    def __iter__(self) -> Generator[Token | ScanError, None, None]:
        while True:
            ch: str | None = self._skip_whitespace()
            pos: Position = self._text.position()

            if ch is None:
                yield EOF(start=pos, end=pos)
                break

            # Identifiers or keywords: [a-zA-Z_][a-zA-Z0-9_]*
            if ch.isalpha() or ch == "_":
                ident: str = self._consume_while(lambda c: c.isalnum() or c == "_")
                end: Position = self._text.position()
                if ident in KEYWORD_VALUES:
                    yield Keyword(value=ident, start=pos, end=end)
                else:
                    yield Ident(value=ident, start=pos, end=end)
                continue

            # Numbers: [0-9]+
            if ch.isdigit():
                num_str: str = self._consume_while(str.isdigit)
                end: Position = self._text.position()
                try:
                    value: int = int(num_str)
                    yield Number(value=value, start=pos, end=end)
                except ValueError:
                    yield ScanError(message=f"Invalid number: {num_str}", pos=pos)
                continue

            # Multi-char operators
            two_char_ops: set[str] = {">=", "<=", "==", "!="}
            op: str = ch
            self._text.advance()
            next_ch: str | None = self._text.peek()
            if next_ch and (op + next_ch) in two_char_ops:
                op += next_ch
                self._text.advance()
            if op in KEYWORD_VALUES:
                end: Position = self._text.position()
                yield Keyword(value=op, start=pos, end=end)
                continue

            # Single-char keywords
            if ch in KEYWORD_VALUES:
                end: Position = self._text.position()
                yield Keyword(value=ch, start=pos, end=end)
                continue

            # Unknown character
            self._text.advance()
            yield ScanError(message=f"Unexpected character: {ch}", pos=pos)

    def _skip_whitespace(self) -> str | None:
        while True:
            ch: str | None = self._text.peek()
            if ch is None or not ch.isspace():
                return ch
            self._text.advance()

    def _consume_while(self, cond: Callable[[str], bool]) -> str:
        result: str = ""
        while True:
            ch: str | None = self._text.peek()
            if ch is None or not cond(ch):
                break
            result += ch
            self._text.advance()
        return result
