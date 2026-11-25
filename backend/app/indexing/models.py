from dataclasses import dataclass


@dataclass
class CodeChunk:
    chunk_id: str
    file_path: str
    symbol_name: str
    chunk_type: str
    start_line: int
    end_line: int
    code: str
    content_hash: str