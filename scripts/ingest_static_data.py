import json
from datetime import datetime
from backend.database.db import SessionLocal
from backend.database.models import DataSource, Location, Observation, PfzAdvisory, HazardAlert
from sqlalchemy.orm import Session

def load_data(db: Session):
    print("Creating tables...")
    from backend.database.db import engine
    import backend.database.models as models
    models.Base.metadata.create_all(bind=engine)
    
    print("Loading mock data...")
    # Add a mock data source
    ds = DataSource(
        provider_name="INCOIS",
        dataset_name="Mock PFZ and OSF",
        access_method="mock_script",
        reliability_tier=1,
        is_active=True
    )
    db.add(ds)
    db.commit()
    db.refresh(ds)
    print(f"Added data source: {ds.source_id}")

    # Add a mock location
    loc = Location(
        raw_query_text="Bay of Bengal Test",
        geom="POINT(88.0 15.0)",  # WKT format
        region_name="Bay of Bengal",
        resolution_method="exact_coordinates",
        resolution_confidence=1.0
    )
    db.add(loc)
    db.commit()
    db.refresh(loc)
    
    # Add a mock observation
    obs = Observation(
        source_id=ds.source_id,
        location_id=loc.location_id,
        geom="POINT(88.0 15.0)",
        variable_type="sst",
        value=28.5,
        unit="degC",
        data_type="observation",
        observed_at=datetime.utcnow(),
    )
    db.add(obs)
    db.commit()
    print("Mock data loaded successfully.")

if __name__ == "__main__":
    db = SessionLocal()
    load_data(db)
    db.close()
