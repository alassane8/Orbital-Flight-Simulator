from dataclasses import dataclass, field
import datetime

@dataclass
class Spaceship:
    id: str
    spaceship_code: str
    maximum_speed_m_s: float
    operating_empty_weight_kg: float
    maximum_operating_empty_weight_kg: float
    max_fuel_kg: float

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)