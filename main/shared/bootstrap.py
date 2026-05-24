import time

from shared import data_loader, init_logger, object_factory

def init_simulator_data():
    init_logger.log(">>> BOOT SEQUENCE INITIATED...")
    time.sleep(0.8)

    init_logger.phase("Loading data modules")

    init_logger.loading("Fetching launching sites data")
    launch_sites_data = data_loader.load_data("config/launch_sites.json")
    init_logger.success("Launch sites data loaded")

    init_logger.loading("Fetching orbital targets data")
    orbital_targets_data = data_loader.load_data("config/orbital_targets.json")
    init_logger.success("Orbital targets loaded")

    init_logger.loading("Fetching payloads data")
    payloads_data = data_loader.load_data("config/payloads.json")
    init_logger.success("Payloads data loaded")

    init_logger.loading("Fetching rockets data")
    rockets_data = data_loader.load_data("config/rockets.json")
    init_logger.success("Rockets data loaded")

    init_logger.phase("Building system objects")

    init_logger.loading("Initializing launch sites")
    launch_sites = object_factory.create_launch_sites(launch_sites_data)
    init_logger.success(f"{len(launch_sites)} launch sites online")

    init_logger.loading("Initializing orbital targets")
    orbital_targets = object_factory.create_orbital_targets(orbital_targets_data)
    init_logger.success(f"{len(orbital_targets)} orbital targets online")
    
    init_logger.loading("Initializing payloads")
    payloads = object_factory.create_payloads(payloads_data)
    init_logger.success(f"{len(payloads)} payloads plotted")

    init_logger.loading("Initializing rockets")
    rockets = object_factory.create_rockets(rockets_data)
    init_logger.success(f"{len(rockets)} rockets operational")
