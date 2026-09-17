from __future__ import annotations

from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


class KnowledgeQueryType(str, Enum):
    SEARCH = "search"
    LOOKUP = "lookup"
    VERIFY = "verify"


class EvidenceType(str, Enum):
    OBSERVATION = "observation"
    DERIVED_INDICATOR = "derived_indicator"
    ESTABLISHED_RELATIONSHIP = "established_relationship"
    STATISTICAL_RELATIONSHIP = "statistical_relationship"
    OPERATIONAL_HEURISTIC = "operational_heuristic"
    MODEL_PREDICTION = "model_prediction"
    ASSUMPTION = "assumption"


class SourceType(str, Enum):
    OFFICIAL = "official"
    SCIENTIFIC = "scientific"
    DATASET = "dataset"
    OPERATIONAL = "operational"
    INTERNAL = "internal"


class KnowledgeQuery(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: UUID = Field(default_factory=uuid4)
    query_type: KnowledgeQueryType
    question: str
    domain: str | None = None
    location: str | None = None
    requested_date: str | None = None
    required_sources: list[str] = Field(default_factory=list)

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Knowledge question cannot be empty.")

        return value


class KnowledgeSource(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_id: str
    title: str
    publisher: str
    source_type: SourceType

    url: str | None = None
    publication_date: str | None = None
    effective_from: str | None = None
    effective_to: str | None = None

    section: str | None = None
    accessed_at: str | None = None


class EvidenceItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    statement: str
    evidence_type: EvidenceType

    source_id: str
    source_section: str | None = None

    confidence: Literal["high", "medium", "low"] = "medium"

    supports_claim: bool = True


class KnowledgeDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    document_id: str
    title: str
    content: str

    source: KnowledgeSource

    relevance_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )


class KnowledgeResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["success", "error"]

    request_id: UUID
    query_type: KnowledgeQueryType

    answer: str | None = None

    documents: list[KnowledgeDocument] = Field(default_factory=list)
    evidence: list[EvidenceItem] = Field(default_factory=list)

    sources: list[KnowledgeSource] = Field(default_factory=list)

    uncertainty: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)

    is_informational_only: Literal[True] = True
