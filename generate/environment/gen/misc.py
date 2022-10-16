import enum as _enum
import re as _re
import sys as _sys
import typing as _typing
import unicodedata as _unicodedata

from . import text_code as _text_code

_punctuations: _typing.Collection[str] = tuple(chr(char) for char in range(_sys.maxunicode)
                                               if _unicodedata.category(chr(char)).startswith('P'))


@_enum.unique
class Tag(_enum.Enum):
    COMMON = ''
    TEXT = 'text'
    MEMORIZE = 'mem'
    SEMANTICS = 'sem'


def affix_lines(text: str, /, *, prefix: str = '', suffix: str = '') -> str:
    def ret_gen() -> _typing.Iterator[str]:
        newline: str = ''
        for line in text.splitlines():
            yield newline
            yield prefix
            yield line
            yield suffix
            newline = '\n'
    return ''.join(ret_gen())


def split_by_punctuations(text: str) -> _typing.Sequence[str]:
    delims: str = '|'.join(map(_re.escape, _punctuations))
    return tuple(chunk for chunk in _re.split(f'(?<={delims})(?!{delims})', text) if chunk)


def code_to_strs(code: _text_code.TextCode, /, *,
                 tag: Tag | str = Tag.COMMON) -> _typing.Iterator[str]:
    tag_name: str = tag.value if isinstance(tag, Tag) else tag
    return (block.text for block in code.blocks if block.common or block.tag == tag_name)


def code_to_str(code: _text_code.TextCode, /, *,
                tag: Tag | str = Tag.COMMON) -> str:
    return ''.join(code_to_strs(code, tag=tag))