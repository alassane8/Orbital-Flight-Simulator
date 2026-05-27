
from datetime import datetime
import uuid

from launch_site.domain.launch_site import LaunchSite
from orbital_target.domain.orbital_target import OrbitalTarget
from payload.domain.payload import Payload
from rocket.domain.rocket import Rocket

def create_rockets(rockets_data: dict) -> dict[Rocket]:
    all_rockets = {}
    for rocket in rockets_data.get("rockets", []):
        obj = Rocket(
            rocket.get("id", uuid.uuid4()),
            rocket.get("name", ""),
            rocket.get("manufacturer", ""),
            rocket.get("nb_stages", 0),
            rocket.get("max_payload_leo_kg", 0),
            rocket.get("max_payload_geo_kg", 0),
            rocket.get("max_fuel_kg", 0),
            rocket.get("fuel_burn_rate_kg_per_s", 0),
            rocket.get("max_thrust_kn", 0),
            rocket.get("max_speed_m_s", 0),
            rocket.get("fairing_diameter_m", 0.0),
            rocket.get("compatible_orbit_types", []),
            rocket.get("description", ""),
            rocket.get("created_at", datetime.now()),
            rocket.get("updated_at", datetime.now()),
        )
        all_rockets[rocket.get("id")] = obj
    return all_rockets
    
def create_orbital_targets(orbital_targets_data: dict) -> dict[OrbitalTarget]:
    all_orbital_targets = {}
    for target in orbital_targets_data.get("orbital_targets", []):
        obj = OrbitalTarget(
            target.get("id", uuid.uuid4()),
            target.get("name", ""),
            target.get("orbit_type", ""),
            target.get("altitude_perigee_km", 0),
            target.get("altitude_apogee_km", 0),
            target.get("inclination_deg", 0.0),
            target.get("description", ""),
        )
        all_orbital_targets[target.get("id")] = obj
    return all_orbital_targets

def create_payloads(payloads_data: dict) -> dict[Payload]:
    all_payloads = {}
    for payload in payloads_data.get("payloads", []):
        obj = Payload(
            payload.get("id", uuid.uuid4()),
            payload.get("name", ""),
            payload.get("mass_kg", 0),
            payload.get("category", ""),
            payload.get("compatible_orbit_types", []),
            payload.get("description", ""),
        )
        all_payloads[payload.get("id")] = obj
    return all_payloads

def create_launch_sites(launch_sites_data: dict) -> dict[LaunchSite]:
    all_launch_sites = {}
    for site in launch_sites_data.get("launch_sites", []):
        obj = LaunchSite(
            site.get("id", uuid.uuid4()),
            site.get("launch_site_code", ""),
            site.get("status", ""),
            site.get("lat", 0.0),
            site.get("lon", 0.0),
            site.get("name", ""),
            site.get("country", ""),
            site.get("operator", ""),
            site.get("created_at", datetime.now()),
            site.get("updated_at", datetime.now()),
        )
        all_launch_sites[site.get("id")] = obj
    return all_launch_sites

