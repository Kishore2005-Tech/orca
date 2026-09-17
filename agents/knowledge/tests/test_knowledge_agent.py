from uuid import uuid4

import pytest

from agents.knowledge.agent import KnowledgeAgent
from agents.knowledge.schemas import (
    EvidenceType,
    KnowledgeDocument,
    KnowledgeQuery,
    KnowledgeQueryType,
    KnowledgeSource,
    SourceType,
)
from agents.knowledge.tools import (
    collect_sources,
    lexical_relevance,
    normalize_query,
    search_documents,
)


@pytest.fixture
def agent() -> KnowledgeAgent:
    return KnowledgeAgent()


@pytest.fixture
def documents() -> list[KnowledgeDocument]:
    source = KnowledgeSource(
        source_id="orca-test-source-001",
        title="Marine Ecosystem Reference",
        publisher="ORCA Test Authority",
        source_type=SourceType.SCIENTIFIC,
        publication_date="2026-01-01",
        section="Marine Productivity",
    )

    second_source = KnowledgeSource(
        source_id="orca-test-source-002",
        title="Ocean Observation Reference",
        publisher="ORCA Test Dataset",
        source_type=SourceType.DATASET,
        publication_date="2026-02-01",
        section="Ocean Observations",
    )

    return [
        KnowledgeDocument(
            document_id="doc-001",
            title="Marine Productivity",
            content=(
                "Chlorophyll concentration can be used as an indicator "
                "of phytoplankton biomass and biological productivity."
            ),
            source=source,
            relevance_score=0.9,
        ),
        KnowledgeDocument(
            document_id="doc-002",
            title="Ocean Observations",
            content=(
                "Sea surface temperature provides information about "
                "thermal conditions at the ocean surface."
            ),
            source=second_source,
            relevance_score=0.8,
        ),
    ]


def test_normalize_query():
    result = normalize_query(
        "   sea   surface   temperature   "
    )

    assert result == "sea surface temperature"


def test_empty_query_is_rejected():
    with pytest.raises(ValueError):
        normalize_query("   ")


def test_lexical_relevance_returns_score(documents):
    score = lexical_relevance(
        "chlorophyll biological productivity",
        documents[0],
    )

    assert 0.0 <= score <= 1.0
    assert score > 0


def test_search_documents_returns_relevant_document(documents):
    results = search_documents(
        "chlorophyll productivity",
        documents,
        limit=1,
    )

    assert len(results) == 1
    assert results[0].document.document_id == "doc-001"


def test_collect_sources(documents):
    sources = collect_sources(documents)

    assert len(sources) == 2
    assert sources[0].source_id == "orca-test-source-001"


def test_agent_search(agent, documents):
    result = agent.search(
        "chlorophyll productivity",
        documents,
    )

    assert len(result) >= 1
    assert result[0].document_id == "doc-001"


def test_agent_run_success(agent, documents):
    query = KnowledgeQuery(
        request_id=uuid4(),
        query_type=KnowledgeQueryType.SEARCH,
        question="What does chlorophyll indicate?",
    )

    result = agent.run(
        query,
        documents=documents,
    )

    assert result.status == "success"
    assert result.answer is not None
    assert len(result.documents) > 0
    assert len(result.sources) > 0
    assert result.is_informational_only is True


def test_agent_preserves_source_provenance(agent, documents):
    query = KnowledgeQuery(
        request_id=uuid4(),
        query_type=KnowledgeQueryType.LOOKUP,
        question="sea surface temperature",
    )

    result = agent.run(
        query,
        documents=documents,
    )

    assert result.status == "success"

    source_ids = {
        source.source_id
        for source in result.sources
    }

    assert "orca-test-source-002" in source_ids


def test_agent_returns_no_data_without_documents(agent):
    query = KnowledgeQuery(
        request_id=uuid4(),
        query_type=KnowledgeQueryType.SEARCH,
        question="marine productivity",
    )

    result = agent.run(
        query,
        documents=[],
    )

    assert result.status == "error"
    assert "ORCA_ERR_NO_DATA" in result.errors[0]


def test_agent_does_not_answer_empty_question(agent, documents):
    with pytest.raises(Exception):
        KnowledgeQuery(
            query_type=KnowledgeQueryType.SEARCH,
            question="",
        )


def test_verify_claim(agent, documents):
    result = agent.verify_claim(
        "chlorophyll biological productivity",
        documents,
    )

    assert result.status == "success"
    assert result.query_type == KnowledgeQueryType.VERIFY
    assert len(result.documents) > 0


def test_evidence_type_enum():
    assert (
        EvidenceType.ESTABLISHED_RELATIONSHIP.value
        == "established_relationship"
    )


def test_is_informational_only_is_hard_coded(agent, documents):
    query = KnowledgeQuery(
        query_type=KnowledgeQueryType.SEARCH,
        question="marine productivity",
    )

    result = agent.run(
        query,
        documents=documents,
    )

    assert result.is_informational_only is True


def test_low_relevance_can_generate_uncertainty(agent):
    source = KnowledgeSource(
        source_id="weak-source",
        title="Unrelated Document",
        publisher="Test Publisher",
        source_type=SourceType.INTERNAL,
    )

    document = KnowledgeDocument(
        document_id="weak-doc",
        title="Unrelated Document",
        content="Completely unrelated information.",
        source=source,
        relevance_score=0.1,
    )

    query = KnowledgeQuery(
        query_type=KnowledgeQueryType.SEARCH,
        question="ocean ecosystem",
    )

    result = agent.run(
        query,
        documents=[document],
    )

    if result.status == "success":
        assert isinstance(result.uncertainty, list)


def test_duplicate_documents_are_not_repeated(agent, documents):
    duplicated = [
        documents[0],
        documents[0],
        documents[1],
    ]

    query = KnowledgeQuery(
        query_type=KnowledgeQueryType.SEARCH,
        question="chlorophyll productivity",
    )

    result = agent.run(
        query,
        documents=duplicated,
    )

    ids = [
        document.document_id
        for document in result.documents
    ]

    assert len(ids) == len(set(ids))
