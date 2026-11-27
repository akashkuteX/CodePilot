import re
from dataclasses import dataclass

from .context_models import Source


@dataclass
class CitationReport:
    valid_citations: list[int]
    invalid_citations: list[int]
    has_citations: bool


class CitationValidator:

    def validate(
        self,
        answer: str,
        sources: list[Source]
    ) -> CitationReport:

        # Extract cited source IDs
        cited_ids = {
            int(source_id)
            for source_id in re.findall(
                r"\[Source\s+(\d+)\]",
                answer
            )
        }

        # Collect actual source IDs
        available_ids = {
            source.source_id
            for source in sources
        }

        # Compare cited and available sources
        valid = cited_ids & available_ids
        invalid = cited_ids - available_ids

        return CitationReport(
            valid_citations=sorted(valid),
            invalid_citations=sorted(invalid),
            has_citations=bool(cited_ids)
        )