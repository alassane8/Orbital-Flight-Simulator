from dataclasses import dataclass, field
from datetime import datetime

from orbital_target.domain.orbit_type import OrbitType


@dataclass
class OrbitalTarget:
    id: str
    code: str
    name: str
    orbit_type: OrbitType
    altitude_perigee_km: float
    altitude_apogee_km: float
    inclination_deg: float
    description: str

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)