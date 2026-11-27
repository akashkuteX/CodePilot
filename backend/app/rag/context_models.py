from dataclasses import dataclass


@dataclass
class Source:
    source_id: int
    file_path: str
    symbol_name: str
    start_line: int
    end_line: int


@dataclass
class BuiltContext:
    text: str
    sources: list[Source]