from dataclasses import dataclass, field
from datetime import datetime

from payload.domain.payload import Payload
from spaceflight.domain.spaceflight_status import SpaceflightStatus

@dataclass
class Spaceflight: 
    id: str
    spaceflight_code: str
    spaceflight_status: SpaceflightStatus
    spaceship_id: str    
    on_board_payloads: list[Payload]
    orbital_target_id: str
    departure_lauch_site_id: str
    altitude_km: float
    fuel_kg: float
    fuel_burn_rate_kg_per_s: float

    estimated_arrival_time: datetime = field(default_factory=datetime.now)
    estimated_departure_time: datetime = field(default_factory=datetime.now)

    arrival_time: datetime = field(default_factory=datetime.now)
    departure_time: datetime = field(default_factory=datetime.now)

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)