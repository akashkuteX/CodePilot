import numpy as np

from .database import get_connection
from ..indexing.models import CodeChunk
from ..retrieval.models import EmbeddedChunk, SearchResult


class VectorRepository:

    def save_chunks(self, chunks: list[EmbeddedChunk]) -> int:

        if not chunks:
            return 0

        # Insert new chunks or update existing ones
        sql = """
            INSERT INTO code_chunks (
                chunk_id,
                file_path,
                symbol_name,
                chunk_type,
                start_line,
                end_line,
                code,
                content_hash,
                embedding
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (chunk_id)
            DO UPDATE SET
                file_path = EXCLUDED.file_path,
                symbol_name = EXCLUDED.symbol_name,
                chunk_type = EXCLUDED.chunk_type,
                start_line = EXCLUDED.start_line,
                end_line = EXCLUDED.end_line,
                code = EXCLUDED.code,
                content_hash = EXCLUDED.content_hash,
                embedding = EXCLUDED.embedding,
                updated_at = CURRENT_TIMESTAMP;
        """

        # Prepare database records
        records = [
            (
                item.chunk.chunk_id,
                item.chunk.file_path,
                item.chunk.symbol_name,
                item.chunk.chunk_type,
                item.chunk.start_line,
                item.chunk.end_line,
                item.chunk.code,
                item.chunk.content_hash,
                np.asarray(item.embedding, dtype=np.float32)
            )
            for item in chunks
        ]

        # Execute inserts within a transaction
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.executemany(sql, records)

        return len(records)

    def count(self) -> int:

        # Count stored code chunks
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM code_chunks")
                return cursor.fetchone()[0]

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5
    ) -> list[SearchResult]:

        if top_k <= 0:
            raise ValueError("top_k must be positive")

        # Retrieve chunks ordered by cosine distance
        sql = """
            SELECT
                chunk_id,
                file_path,
                symbol_name,
                chunk_type,
                start_line,
                end_line,
                code,
                content_hash,
                1 - (embedding <=> %s) AS score
            FROM code_chunks
            ORDER BY embedding <=> %s
            LIMIT %s;
        """

        vector = np.asarray(
            query_embedding,
            dtype=np.float32
        )

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (vector, vector, top_k))
                rows = cursor.fetchall()

        # Convert database rows into search results
        return [
            SearchResult(
                chunk=CodeChunk(
                    chunk_id=row[0],
                    file_path=row[1],
                    symbol_name=row[2],
                    chunk_type=row[3],
                    start_line=row[4],
                    end_line=row[5],
                    code=row[6],
                    content_hash=row[7]
                ),
                score=float(row[8])
            )
            for row in rows
        ]