from typing import Dict, Any, List, Tuple
import math

class GeospatialAgent:
    def __init__(self):
        self.agent_id = "geospatial_agent"
        self.agent_name = "Geospatial & Spatial Intelligence Agent"
        
        # Knowledge base of key Indian coastal locations & fishing zones
        self.location_db = {
            "chennai": {
                "name": "Chennai Coast (Bay of Bengal)",
                "center": (13.0827, 80.2707),
                "zones": {
                    "ennore": {
                        "name": "Ennore Offshore (North Chennai)",
                        "lat": 13.2350,
                        "lon": 80.3650,
                        "distance_km": 18.5,
                        "distance_nm": 10.0,
                        "depth_m": 32.0,
                        "harbor": "Ennore Port / Kasimedu",
                        "bounds": [[80.32, 13.20], [80.41, 13.20], [80.41, 13.27], [80.32, 13.27], [80.32, 13.20]]
                    },
                    "mahabalipuram": {
                        "name": "Mahabalipuram Offshore (South Chennai)",
                        "lat": 12.6150,
                        "lon": 80.2450,
                        "distance_km": 24.0,
                        "distance_nm": 13.0,
                        "depth_m": 48.0,
                        "harbor": "Covelong / Muttukadu",
                        "bounds": [[80.20, 12.57], [80.29, 12.57], [80.29, 12.66], [80.20, 12.66], [80.20, 12.57]]
                    },
                    "kasimedu": {
                        "name": "Kasimedu Central",
                        "lat": 13.1250,
                        "lon": 80.3350,
                        "distance_km": 8.0,
                        "distance_nm": 4.3,
                        "depth_m": 22.0,
                        "harbor": "Kasimedu Fishing Harbor",
                        "bounds": [[80.30, 13.09], [80.37, 13.09], [80.37, 13.16], [80.30, 13.16], [80.30, 13.09]]
                    }
                }
            },
            "visakhapatnam": {
                "name": "Visakhapatnam Coast (Andhra Pradesh)",
                "center": (17.6868, 83.2185),
                "zones": {
                    "vizag_north": {
                        "name": "Bheemunipatnam Offshore",
                        "lat": 17.8900,
                        "lon": 83.4800,
                        "distance_km": 15.0,
                        "distance_nm": 8.1,
                        "depth_m": 45.0,
                        "harbor": "Visakhapatnam Fishing Harbour",
                        "bounds": [[83.42, 17.84], [83.54, 17.84], [83.54, 17.94], [83.42, 17.94], [83.42, 17.84]]
                    },
                    "vizag_south": {
                        "name": "Gangavaram Offshore",
                        "lat": 17.6100,
                        "lon": 83.3200,
                        "distance_km": 12.0,
                        "distance_nm": 6.5,
                        "depth_m": 38.0,
                        "harbor": "Gangavaram",
                        "bounds": [[83.26, 17.55], [83.38, 17.55], [83.38, 17.67], [83.26, 17.67], [83.26, 17.55]]
                    }
                }
            },
            "kochi": {
                "name": "Kochi Coast (Arabian Sea)",
                "center": (9.9312, 76.2673),
                "zones": {
                    "kochi_offshore": {
                        "name": "Kochi Offshore Upwelling Zone",
                        "lat": 9.9200,
                        "lon": 75.9800,
                        "distance_km": 32.0,
                        "distance_nm": 17.3,
                        "depth_m": 65.0,
                        "harbor": "Thoppumpady / Munambam",
                        "bounds": [[75.90, 9.85], [76.06, 9.85], [76.06, 9.99], [75.90, 9.99], [75.90, 9.85]]
                    }
                }
            },
            "paradip": {
                "name": "Paradip Coast (Odisha)",
                "center": (20.3160, 86.6110),
                "zones": {
                    "paradip_offshore": {
                        "name": "Mahanadi Estuary Offshore",
                        "lat": 20.2500,
                        "lon": 86.7500,
                        "distance_km": 20.0,
                        "distance_nm": 10.8,
                        "depth_m": 28.0,
                        "harbor": "Paradip Fishing Harbour",
                        "bounds": [[86.68, 20.18], [86.82, 20.18], [86.82, 20.32], [86.68, 20.32], [86.68, 20.18]]
                    }
                }
            },
            "goa": {
                "name": "Goa Coast (Arabian Sea)",
                "center": (15.2993, 73.9840),
                "zones": {
                    "mormugao_offshore": {
                        "name": "Mormugao Deep Reef Zone",
                        "lat": 15.3800,
                        "lon": 73.6500,
                        "distance_km": 28.0,
                        "distance_nm": 15.1,
                        "depth_m": 55.0,
                        "harbor": "Malim / Betul",
                        "bounds": [[73.55, 15.30], [73.75, 15.30], [73.75, 15.46], [73.55, 15.46], [73.55, 15.30]]
                    }
                }
            }
        }

    def resolve_location(self, query: str) -> Dict[str, Any]:
        query_lower = query.lower()
        
        # Check specific locations
        matched_loc_key = "chennai" # default
        for key in self.location_db:
            if key in query_lower:
                matched_loc_key = key
                break
        
        loc_data = self.location_db[matched_loc_key]
        
        # Check if query asks for comparative zones (e.g. Ennore vs Mahabalipuram)
        is_comparative = ("ennore" in query_lower and "mahabalipuram" in query_lower) or ("compare" in query_lower) or ("which area" in query_lower)
        
        return {
            "location_key": matched_loc_key,
            "location_name": loc_data["name"],
            "center": loc_data["center"],
            "zones": loc_data["zones"],
            "is_comparative": is_comparative
        }

    def haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> Tuple[float, float]:
        R = 6371.0 # km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        km = R * c
        nm = km * 0.539957
        return round(km, 2), round(nm, 2)

    def generate_geojson(self, location_key: str, zones_data: Dict[str, Any]) -> Dict[str, Any]:
        features = []
        
        # Add zone polygons and points
        for z_key, z_val in zones_data.items():
            if "bounds" in z_val:
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [z_val["bounds"]]
                    },
                    "properties": {
                        "id": f"zone-{z_key}",
                        "name": z_val["name"],
                        "type": "PFZ_ADVISORY_ZONE",
                        "depth_m": z_val.get("depth_m", 30),
                        "distance_km": z_val.get("distance_km", 15),
                        "harbor": z_val.get("harbor", "Regional Harbor")
                    }
                })
            
            # Point Marker
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [z_val["lon"], z_val["lat"]]
                },
                "properties": {
                    "id": f"point-{z_key}",
                    "name": z_val["name"],
                    "type": "FISHING_HOTSPOT",
                    "latitude": z_val["lat"],
                    "longitude": z_val["lon"]
                }
            })
            
        return {
            "type": "FeatureCollection",
            "features": features
        }
