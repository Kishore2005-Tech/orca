import uuid
from sqlalchemy import Column, String, Float, Boolean, JSON, DateTime, ForeignKey, Text, Integer, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB, TSTZRANGE
from geoalchemy2 import Geometry
from pgvector.sqlalchemy import Vector
from sqlalchemy.sql import func
from backend.database.db import Base

class DataSource(Base):
    __tablename__ = "data_sources"
    source_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_name = Column(Text, nullable=False)
    dataset_name = Column(Text, nullable=False)
    access_method = Column(Text, nullable=False)
    spatial_resolution = Column(Text)
    spatial_tolerance_m = Column(Float)
    temporal_resolution = Column(Text)
    coverage_region = Column(Geometry(geometry_type='POLYGON', srid=4326))
    known_limitations = Column(Text)
    license = Column(Text)
    reliability_tier = Column(Integer, nullable=False, default=2)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

class Location(Base):
    __tablename__ = "locations"
    location_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    raw_query_text = Column(Text)
    geom = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    region_name = Column(Text)
    resolution_method = Column(Text, nullable=False)
    resolution_confidence = Column(Float)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        CheckConstraint('resolution_confidence >= 0 AND resolution_confidence <= 1', name='check_res_conf'),
    )

class Observation(Base):
    __tablename__ = "observations"
    observation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("data_sources.source_id"), nullable=False)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.location_id"), nullable=False)
    geom = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    variable_type = Column(Text, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(Text, nullable=False)
    data_type = Column(Text, nullable=False)
    observed_at = Column(DateTime(timezone=True), nullable=False)
    valid_until = Column(DateTime(timezone=True))
    retrieved_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    quality_flag = Column(Text)
    raw_payload = Column(JSONB)

class PfzAdvisory(Base):
    __tablename__ = "pfz_advisories"
    advisory_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("data_sources.source_id"), nullable=False)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.location_id"), nullable=False)
    zone_geom = Column(Geometry(geometry_type='POLYGON', srid=4326), nullable=False)
    issued_at = Column(DateTime(timezone=True), nullable=False)
    valid_until = Column(DateTime(timezone=True), nullable=False)
    advisory_reference = Column(Text, nullable=False)
    contributing_variables = Column(JSONB)
    retrieved_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        CheckConstraint('valid_until > issued_at', name='check_validity_pfz'),
    )

class HazardAlert(Base):
    __tablename__ = "hazard_alerts"
    alert_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("data_sources.source_id"), nullable=False)
    alert_type = Column(Text, nullable=False)
    affected_area = Column(Geometry(geometry_type='POLYGON', srid=4326), nullable=False)
    severity_as_stated = Column(Text)
    issued_at = Column(DateTime(timezone=True), nullable=False)
    valid_until = Column(DateTime(timezone=True), nullable=False)
    source_reference = Column(Text, nullable=False)
    retrieved_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        CheckConstraint('valid_until >= issued_at', name='check_validity_hazard'),
    )

class ConversationSession(Base):
    __tablename__ = "conversation_sessions"
    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    last_location_id = Column(UUID(as_uuid=True), ForeignKey("locations.location_id"))
    last_time_window = Column(TSTZRANGE)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_active_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)

class Query(Base):
    __tablename__ = "queries"
    query_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("conversation_sessions.session_id"), nullable=False)
    raw_text = Column(Text, nullable=False)
    language = Column(Text, nullable=False, default='en')
    intent_type = Column(Text)
    resolved_location_id = Column(UUID(as_uuid=True), ForeignKey("locations.location_id"))
    resolved_time_window = Column(TSTZRANGE)
    submitted_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

class AgentRun(Base):
    __tablename__ = "agent_runs"
    run_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_id = Column(UUID(as_uuid=True), ForeignKey("queries.query_id"), nullable=False)
    agent_name = Column(Text, nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    status = Column(Text, nullable=False, default='running')
    execution_mode = Column(Text)
    depends_on_run_id = Column(UUID(as_uuid=True), ForeignKey("agent_runs.run_id"))

class AgentOutput(Base):
    __tablename__ = "agent_outputs"
    output_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id = Column(UUID(as_uuid=True), ForeignKey("agent_runs.run_id"), nullable=False)
    claim_text = Column(Text, nullable=False)
    confidence_label = Column(Text)
    spatial_scope_id = Column(UUID(as_uuid=True), ForeignKey("locations.location_id"))
    temporal_scope = Column(TSTZRANGE)
    validation_status = Column(Text, nullable=False, default='pending')
    validation_failure_reason = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

class Evidence(Base):
    __tablename__ = "evidence"
    evidence_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    output_id = Column(UUID(as_uuid=True), ForeignKey("agent_outputs.output_id"), nullable=False)
    observation_id = Column(UUID(as_uuid=True), ForeignKey("observations.observation_id"))
    advisory_id = Column(UUID(as_uuid=True), ForeignKey("pfz_advisories.advisory_id"))
    alert_id = Column(UUID(as_uuid=True), ForeignKey("hazard_alerts.alert_id"))
    chunk_id = Column(UUID(as_uuid=True)) # no chunk_id fk setup yet
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

class Recommendation(Base):
    __tablename__ = "recommendations"
    recommendation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_id = Column(UUID(as_uuid=True), ForeignKey("queries.query_id"), nullable=False, unique=True)
    observations_section = Column(Text, nullable=False)
    analysis_section = Column(Text, nullable=False)
    evidence_summary = Column(Text, nullable=False)
    confidence_label = Column(Text, nullable=False)
    uncertainty_section = Column(Text, nullable=False)
    implications_section = Column(Text)
    recommended_next_step = Column(Text)
    generated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
