from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .schemas import (
    EvidenceItem,
    KnowledgeDocument,
    KnowledgeSource,
)


@dataclass(frozen=True)
class SearchResult:
    document: KnowledgeDocument
    score: float


def normalize_query(query: str) -> str:
    """
    Normalize a knowledge-search query without changing its meaning.
    """

    if not isinstance(query, str):
        raise ValueError("Knowledge query must be a string.")

    normalized = " ".join(query.strip().split())

    if not normalized:
        raise ValueError("Knowledge query cannot be empty.")

    return normalized


def tokenize(text: str) -> set[str]:
    """
    Lightweight tokenization used by the local fallback search.

    Real deployments can replace this with vector/semantic retrieval.
    """

    return {
        token.lower().strip(".,!?;:\"'()[]{}")
        for token in text.split()
        if token.strip()
    }


def lexical_relevance(query: str, document: KnowledgeDocument) -> float:
    """
    Calculate a simple lexical relevance score.

    This is only a fallback retrieval mechanism. It must not be
    interpreted as scientific confidence.
    """

    query_tokens = tokenize(query)

    if not query_tokens:
        return 0.0

    searchable_text = " ".join(
        [
            document.title,
            document.content,
            document.source.title,
            document.source.publisher,
        ]
    )

    document_tokens = tokenize(searchable_text)

    if not document_tokens:
        return 0.0

    overlap = query_tokens.intersection(document_tokens)

    return min(
        1.0,
        len(overlap) / len(query_tokens),
    )


def search_documents(
    query: str,
    documents: Iterable[KnowledgeDocument],
    *,
    min_score: float = 0.0,
    limit: int = 10,
) -> list[SearchResult]:
    """
    Search a supplied knowledge collection.

    The function only ranks documents; it does not generate facts.
    """

    normalized_query = normalize_query(query)

    if limit <= 0:
        raise ValueError("limit must be greater than zero.")

    results: list[SearchResult] = []

    for document in documents:
        score = lexical_relevance(
            normalized_query,
            document,
        )

        if score >= min_score:
            results.append(
                SearchResult(
                    document=document,
                    score=score,
                )
            )

    results.sort(
        key=lambda result: result.score,
        reverse=True,
    )

    return results[:limit]


def deduplicate_documents(
    documents: Iterable[KnowledgeDocument],
) -> list[KnowledgeDocument]:
    """
    Remove duplicate documents by document_id.
    """

    seen: set[str] = set()
    unique: list[KnowledgeDocument] = []

    for document in documents:
        if document.document_id in seen:
            continue

        seen.add(document.document_id)
        unique.append(document)

    return unique


def collect_sources(
    documents: Iterable[KnowledgeDocument],
) -> list[KnowledgeSource]:
    """
    Extract unique source records from retrieved documents.
    """

    seen: set[str] = set()
    sources: list[KnowledgeSource] = []

    for document in documents:
        source = document.source

        if source.source_id in seen:
            continue

        seen.add(source.source_id)
        sources.append(source)

    return sources


def collect_evidence(
    evidence: Iterable[EvidenceItem],
) -> list[EvidenceItem]:
    """
    Remove duplicate evidence records while preserving order.
    """

    seen: set[tuple[str, str, str | None]] = set()
    unique: list[EvidenceItem] = []

    for item in evidence:
        key = (
            item.source_id,
            item.statement,
            item.source_section,
        )

        if key in seen:
            continue

        seen.add(key)
        unique.append(item)

    return unique


def build_evidence_from_document(
    document: KnowledgeDocument,
    statement: str,
    *,
    evidence_type: str = "established_relationship",
    confidence: str = "medium",
) -> EvidenceItem:
    """
    Build an evidence item tied directly to a retrieved source.

    The caller remains responsible for selecting the correct
    evidence classification.
    """

    return EvidenceItem(
        statement=statement,
        evidence_type=evidence_type,
        source_id=document.source.source_id,
        source_section=document.source.section,
        confidence=confidence,
        supports_claim=True,
    )
