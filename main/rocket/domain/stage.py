from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Stage:
    stage_number: int
    thrust_kn: float
    isp_vac_s: float
    isp_sl_s: float
    fuel_mass_kg: float
    dry_mass_kg: float
    t_burn_s: float
    h_mean_m: float
    gamma_mean_deg: float
    cd: float
    v_maxq_m_s: float

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)