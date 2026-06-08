#pragma once

#include <string>
#include <vector>
#include "enums.h"

struct LaunchSite {
    std::string id;
    std::string code;
    LaunchSiteStatus status;
    double lat;
    double lon;
    std::string name;
    std::string country;
    std::string operator_;
};

struct OrbitalTarget {
    std::string id;
    std::string code;
    std::string name;
    OrbitType orbit_type;
    double altitude_perigee_km;
    double altitude_apogee_km;
    double inclination_deg;
    std::string description;
};

struct Payload {
    std::string id;
    std::string code;
    std::string name;
    double mass_kg;
    PayloadCategory category;
    std::vector<OrbitType> compatible_orbit_types;
    std::string description;
};

struct Stage {
    int::stage_number;
    double thrust_kn;
    double isp_vac_s;
    double isp_sl_s;
    double fuel_mass_kg;
    double dry_mass_kg;
    double t_burn_s;
    double h_mean_m;
    double gamma_mean_deg;
};

struct Rocket {
    std::string id;
    std::string code;
    std::string name;
    std::string manufacturer;
    int nb_stages;
    int max_payload_leo_kg;
    int max_payload_geo_kg;
    int max_fuel_kg;
    int fuel_burn_rate_kg_per_s;
    int max_thrust_kn;
    int max_speed_m_s;
    double fairing_diameter_m;
    std::vector<OrbitType> compatible_orbit_types;
    std::vector<Stage> stages;
    std::string description;
};

struct Spaceflight {
    std::string id;
    std::string spaceflight_code;
    SpaceflightStatus spaceflight_status;
    std::string spaceship_id;
    std::vector<Payload> on_board_payloads;
    std::string orbital_target_id;
    std::string departure_launch_site_id;
    double altitude_km;
    double fuel_kg;
    double fuel_burn_rate_kg_per_s;
};
