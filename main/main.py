from orbital_target.application import orbital_target_service
from payload.application import payload_service
from rocket.application import rocket_service
from shared.bootstrap import init_simulator_data
import sys

def main() -> int:
    launch_sites, orbital_targets, payloads, rockets = init_simulator_data()
    
    rocket = rocket_service.select_rocket(rockets)
    orbital_target = orbital_target_service.select_orbital_target(rocket, orbital_targets)
    payload = payload_service.add_payloads_to_rocket(rocket, payloads, orbital_target)
    # choosing launch_site based on rocket manufacturer
    # coompute fuel based on launch site weigth payloads orbital targets.
    # choosing orbital target based on operating weight fuel position of target and lauch site position
    return 0


if __name__ == "__main__":
    main()
