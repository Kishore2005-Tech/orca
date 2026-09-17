from __future__ import annotations

from typing import Iterable

from .prompts import KNOWLEDGE_SYSTEM_PROMPT
from .schemas import (
    EvidenceItem,
    KnowledgeDocument,
    KnowledgeQuery,
    KnowledgeQueryType,
    KnowledgeResult,
)
from .tools import (
    collect_evidence,
    collect_sources,
    deduplicate_documents,
    search_documents,
)


class KnowledgeAgent:
    """
    ORCA Knowledge Agent.

    Provides evidence-oriented retrieval and verification.

    It deliberately does not manufacture domain facts. External
    knowledge bases, scientific literature indexes, regulations,
    datasets and internal documents can be passed into the agent.
    """

    agent_id = "knowledge"
    agent_name = "Knowledge & Evidence Agent"

    system_prompt = KNOWLEDGE_SYSTEM_PROMPT

    def __init__(self) -> None:
        self.agent_id = "knowledge"
        self.agent_name = "Knowledge & Evidence Agent"

    def run(
        self,
        query: KnowledgeQuery,
        *,
        documents: Iterable[KnowledgeDocument] | None = None,
        evidence: Iterable[EvidenceItem] | None = None,
        limit: int = 5,
        min_score: float = 0.0,
    ) -> KnowledgeResult:
        """
        Execute a knowledge retrieval request.
        """

        try:
            self._validate_query(query)

            document_list = deduplicate_documents(
                documents or []
            )

            search_results = search_documents(
                query.question,
                document_list,
                min_score=min_score,
                limit=limit,
            )

            retrieved_documents = [
                result.document
                for result in search_results
            ]

            supplied_evidence = list(evidence or [])

            retrieved_evidence = self._build_retrieval_evidence(
                retrieved_documents
            )

            combined_evidence = collect_evidence(
                [
                    *supplied_evidence,
                    *retrieved_evidence,
                ]
            )

            sources = collect_sources(
                retrieved_documents
            )

            if not retrieved_documents:
                return KnowledgeResult(
                    status="error",
                    request_id=query.request_id,
                    query_type=query.query_type,
                    answer=None,
                    documents=[],
                    evidence=[],
                    sources=[],
                    uncertainty=[
                        "No supporting knowledge documents were retrieved."
                    ],
                    warnings=[
                        "The agent did not infer an answer from missing evidence."
                    ],
                    errors=[
                        "ORCA_ERR_NO_DATA: No relevant knowledge was found."
                    ],
                )

            answer = self._build_answer(
                query,
                retrieved_documents,
            )

            uncertainty = self._build_uncertainty(
                retrieved_documents
            )

            warnings = []

            if query.query_type == KnowledgeQueryType.VERIFY:
                warnings.append(
                    "Verification depends on the supplied source material "
                    "and does not establish truth beyond that evidence."
                )

            return KnowledgeResult(
                status="success",
                request_id=query.request_id,
                query_type=query.query_type,
                answer=answer,
                documents=retrieved_documents,
                evidence=combined_evidence,
                sources=sources,
                uncertainty=uncertainty,
                warnings=warnings,
                errors=[],
            )

        except ValueError as exc:
            return KnowledgeResult(
                status="error",
                request_id=query.request_id,
                query_type=query.query_type,
                errors=[
                    f"ORCA_ERR_INVALID_QUERY: {exc}"
                ],
            )

        except Exception as exc:
            return KnowledgeResult(
                status="error",
                request_id=query.request_id,
                query_type=query.query_type,
                errors=[
                    f"ORCA_ERR_SOURCE_UNAVAILABLE: {exc}"
                ],
            )

    def search(
        self,
        question: str,
        documents: Iterable[KnowledgeDocument],
        *,
        limit: int = 5,
    ) -> list[KnowledgeDocument]:
        """
        Convenience method for retrieval.
        """

        results = search_documents(
            question,
            documents,
            limit=limit,
        )

        return [
            result.document
            for result in results
        ]

    def verify_claim(
        self,
        claim: str,
        documents: Iterable[KnowledgeDocument],
    ) -> KnowledgeResult:
        """
        Verify whether retrieved documentation contains support
        for a claim.

        This method intentionally does not return a binary
        'scientifically true' judgment.
        """

        query = KnowledgeQuery(
            query_type=KnowledgeQueryType.VERIFY,
            question=claim,
        )

        return self.run(
            query,
            documents=documents,
        )

    def _validate_query(
        self,
        query: KnowledgeQuery,
    ) -> None:
        if not query.question.strip():
            raise ValueError(
                "Knowledge question cannot be empty."
            )

    def _build_retrieval_evidence(
        self,
        documents: list[KnowledgeDocument],
    ) -> list[EvidenceItem]:
        evidence: list[EvidenceItem] = []

        for document in documents:
            evidence.append(
                EvidenceItem(
                    statement=(
                        f"Retrieved from '{document.title}' "
                        f"published by {document.source.publisher}."
                    ),
                    evidence_type="observation",
                    source_id=document.source.source_id,
                    source_section=document.source.section,
                    confidence=self._source_confidence(
                        document
                    ),
                    supports_claim=True,
                )
            )

        return evidence

    def _source_confidence(
        self,
        document: KnowledgeDocument,
    ) -> str:
        """
        Retrieval relevance is deliberately kept separate from
        scientific confidence.

        This method only assigns a conservative source confidence
        based on source classification.
        """

        source_type = document.source.source_type.value

        if source_type in {
            "official",
            "scientific",
            "dataset",
        }:
            return "high"

        if source_type == "operational":
            return "medium"

        return "low"

    def _build_answer(
        self,
        query: KnowledgeQuery,
        documents: list[KnowledgeDocument],
    ) -> str:
        """
        Build a provenance-preserving answer from retrieved documents.

        The implementation intentionally summarizes available evidence
        instead of inventing a synthetic scientific conclusion.
        """

        if query.query_type == KnowledgeQueryType.VERIFY:
            return (
                "The retrieved documentation provides the evidence "
                "summarized in the returned source records. Review the "
                "linked document sections before treating the claim as "
                "established."
            )

        titles = [
            document.title
            for document in documents[:3]
        ]

        joined_titles = "; ".join(titles)

        return (
            "Relevant ORCA knowledge was retrieved from the following "
            f"documented sources: {joined_titles}. "
            "The source records and evidence classifications should be "
            "used to interpret the information without extending it "
            "beyond the documented scope."
        )

    def _build_uncertainty(
        self,
        documents: list[KnowledgeDocument],
    ) -> list[str]:
        uncertainty: list[str] = []

        if not documents:
            uncertainty.append(
                "No documents were available."
            )
            return uncertainty

        if all(
            document.relevance_score < 0.5
            for document in documents
        ):
            uncertainty.append(
                "Retrieved documents have limited relevance scores; "
                "additional retrieval may be required."
            )

        if any(
            document.source.publication_date is None
            for document in documents
        ):
            uncertainty.append(
                "At least one source does not provide a publication date."
            )

        return uncertainty
