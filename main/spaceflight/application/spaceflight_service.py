from datetime import datetime
import uuid

from launch_site.domain.launch_site import LaunchSite
from spaceflight.domain.spaceflight_status import SpaceflightStatus
from orbital_target.domain.orbital_target import OrbitalTarget
from payload.domain.payload import Payload
from rocket.domain.rocket import Rocket
from spaceflight.domain.spaceflight import Spaceflight


def create_spaceflight(rocket: Rocket, on_board_payloads: list[Payload], launch_site: LaunchSite, orbital_target: OrbitalTarget, fuel_kg: int) -> Spaceflight:
    return Spaceflight(id=uuid.uuid4(), 
                       spaceflight_code=_init_spaceflight_code(rocket, launch_site, orbital_target),
                       spaceflight_status=SpaceflightStatus.INITIALIZING,
                       spaceship_id=rocket.id,
                       on_board_payloads=on_board_payloads,
                       orbital_target_id=orbital_target.id,
                       departure_lauch_site_id=launch_site.id,
                       altitude_km=0,
                       fuel_kg=fuel_kg,
                       fuel_burn_rate_kg_per_s=0,
                       estimated_arrival_time=None,
                       estimated_departure_time=None,
                       arrival_time=None,
                       departure_time=None,
                       created_at=datetime.now(),
                       updated_at=datetime.now())


def _init_spaceflight_code(rocket: Rocket, launch_site: LaunchSite, orbital_target: OrbitalTarget) -> str:
    site = launch_site.code
    target = orbital_target.code.replace("-", "")
    rocket_part = rocket.code.replace("-", "")
    
    return f"{site}-{target}-{rocket_part}"