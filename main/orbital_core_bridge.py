import orbital_core

def _to_orbit_type(value: str):
    return orbital_core.OrbitType.__members__[value]

def _to_launch_site_status(value: str):
    return orbital_core.LaunchSiteStatus.__members__[value]

def _to_payload_category(value: str):
    return orbital_core.PayloadCategory.__members__[value]

def _to_spaceflight_status(value: str):
    return orbital_core.SpaceflightStatus.__members__[value]


def to_cpp_launch_site(ls):
    cpp = orbital_core.LaunchSite()
    cpp.id        = ls.id
    cpp.code      = ls.code
    cpp.lat       = ls.lat
    cpp.lon       = ls.lon
    cpp.name      = ls.name
    cpp.country   = ls.country
    cpp.operator_  = ls.operator
    cpp.status    = _to_launch_site_status(ls.status)
    return cpp

def to_cpp_orbital_target(ot):
    cpp = orbital_core.OrbitalTarget()
    cpp.id                  = ot.id
    cpp.code                = ot.code
    cpp.name                = ot.name
    cpp.altitude_perigee_km = ot.altitude_perigee_km
    cpp.altitude_apogee_km  = ot.altitude_apogee_km
    cpp.inclination_deg     = ot.inclination_deg
    cpp.orbit_type          = _to_orbit_type(ot.orbit_type)
    return cpp

def to_cpp_payload(p):
    cpp = orbital_core.Payload()
    cpp.id       = p.id
    cpp.code     = p.code
    cpp.name     = p.name
    cpp.mass_kg  = p.mass_kg
    cpp.category = _to_payload_category(p.category)
    cpp.compatible_orbit_types = [_to_orbit_type(o) for o in p.compatible_orbit_types]
    return cpp

def to_cpp_payloads(payloads):
    return [to_cpp_payload(p) for p in payloads]

def to_cpp_rocket(r):
    cpp = orbital_core.Rocket()
    cpp.id                      = r.id
    cpp.code                    = r.code
    cpp.name                    = r.name
    cpp.manufacturer            = r.manufacturer
    cpp.nb_stages               = r.nb_stages
    cpp.max_payload_leo_kg      = r.max_payload_leo_kg
    cpp.max_payload_geo_kg      = r.max_payload_geo_kg
    cpp.max_fuel_kg             = r.max_fuel_kg
    cpp.fuel_burn_rate_kg_per_s = r.fuel_burn_rate_kg_per_s
    cpp.max_thrust_kn           = r.max_thrust_kn
    cpp.max_speed_m_s           = r.max_speed_m_s
    cpp.fairing_diameter_m      = r.fairing_diameter_m
    cpp.compatible_orbit_types  = [_to_orbit_type(o) for o in r.compatible_orbit_types]
    return cpp