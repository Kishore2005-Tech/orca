"""
FastAPI dependencies for ORCA.

This module provides shared application services such as
configuration and the CoordinatorAgent.
"""

from functools import lru_cache

from backend.agents.coordinator import CoordinatorAgent
from backend.api.config import Settings, get_settings


@lru_cache
def get_coordinator() -> CoordinatorAgent:
    """
    Create and cache one CoordinatorAgent instance.

    The Coordinator owns the ORCA agent orchestration layer,
    including:

        Geospatial
        Ocean
        Fishery
        Safety
        Verification
    """
    return CoordinatorAgent()


def get_app_settings() -> Settings:
    """
    FastAPI dependency for application settings.
    """
    return get_settings()
