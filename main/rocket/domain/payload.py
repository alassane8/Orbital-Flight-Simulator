    
from dataclasses import dataclass, field
import datetime

from main.orbital_target.domain.orbit_type import OrbitType
from main.rocket.domain.payload_category import PayloadCategory


@dataclass
class Payload:
    id: str
    name: str
    mass_kg: str
    category: PayloadCategory
    compatible_orbit_types: list[OrbitType]
    description: str

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

