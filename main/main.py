import orbital_core

from launch_site.application.launch_site_service import select_launch_site
from spaceflight.application.spaceflight_service import create_spaceflight
from orbital_target.application import orbital_target_service
from payload.application import payload_service
from rocket.application import rocket_service
from shared.bootstrap import init_simulator_data

def main() -> int:
    launch_sites, orbital_targets, payloads, rockets = init_simulator_data()
    
    rocket = rocket_service.select_rocket(rockets)
    orbital_target = orbital_target_service.select_orbital_target(rocket, orbital_targets)
    launch_site = select_launch_site(rocket, orbital_target, launch_sites)
    on_board_payloads = payload_service.add_payloads_to_rocket(rocket, payloads)

    delta_v = orbital_core.compute_delta_v(launch_site, orbital_target)
    fuel_kg = orbital_core.compute_fuel(rocket, payloads, delta_v)

    spaceflight = create_spaceflight(rocket, on_board_payloads, launch_site, orbital_target, fuel_kg)
    
    return 0


if __name__ == "__main__":
    main()
