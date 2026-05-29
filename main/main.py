from launch_site.application.launch_site_service import select_launch_site
from orbital_target.application import orbital_target_service
from payload.application import payload_service
from rocket.application import rocket_service
from shared.bootstrap import init_simulator_data
import sys

def main() -> int:
    launch_sites, orbital_targets, payloads, rockets = init_simulator_data()
    
    rocket = rocket_service.select_rocket(rockets)
    orbital_target = orbital_target_service.select_orbital_target(rocket, orbital_targets)
    launch_site = select_launch_site(rocket, orbital_target, launch_sites)
    payload = payload_service.add_payloads_to_rocket(rocket, payloads)
    #delta_v     → compute_delta_v(launch_site, target) ← physique réelle
    #fuel_kg     → compute_fuel(rocket, payloads, delta_v) ← Tsiolkovsky
    
    return 0


if __name__ == "__main__":
    main()
