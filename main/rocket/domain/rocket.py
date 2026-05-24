from dataclasses import dataclass, field
from datetime import datetime

from orbital_target.domain.orbit_type import OrbitType

@dataclass
class Rocket:
    id: str
    name: str
    manufacturer: str
    nb_stages: int
    max_payload_leo_kg: int 
    max_payload_geo_kg: int
    max_fuel_kg: int
    fuel_burn_rate_kg_per_s: int
    max_thrust_kn: int
    max_speed_m_s: int
    fairing_diameter_m: float
    compatible_orbit_types: list[OrbitType]
    description: str

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
