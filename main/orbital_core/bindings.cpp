#pragma once

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "models.h"
#include "orbital_core.h"

namespace py = pybind11;

inline void bind_enums(py::module_& m) {

    py::enum_<OrbitType>(m, "OrbitType")
        .value("LOW_EARTH_ORBIT",        OrbitType::LOW_EARTH_ORBIT)
        .value("MEDIUM_EARTH_ORBIT",     OrbitType::MEDIUM_EARTH_ORBIT)
        .value("GEOSTATIONARY_ORBIT",    OrbitType::GEOSTATIONARY_ORBIT)
        .value("GEOSYNCHRONOUS_ORBIT",   OrbitType::GEOSYNCHRONOUS_ORBIT)
        .value("SUN_SYNCHRONOUS_ORBIT",  OrbitType::SUN_SYNCHRONOUS_ORBIT)
        .value("HIGHLY_ELLIPTICAL_ORBIT",OrbitType::HIGHLY_ELLIPTICAL_ORBIT)
        .value("TRANS_LUNAR_INJECTION",  OrbitType::TRANS_LUNAR_INJECTION)
        .value("LUNAR_ORBIT",            OrbitType::LUNAR_ORBIT)
        .export_values();

    py::enum_<LaunchSiteStatus>(m, "LaunchSiteStatus")
        .value("ACTIVE",             LaunchSiteStatus::ACTIVE)
        .value("INACTIVE",           LaunchSiteStatus::INACTIVE)
        .value("UNDER_CONSTRUCTION", LaunchSiteStatus::UNDER_CONSTRUCTION)
        .export_values();

    py::enum_<PayloadCategory>(m, "PayloadCategory")
        .value("NANOSATELLITE",    PayloadCategory::NANOSATELLITE)
        .value("EARTH_OBSERVATION",PayloadCategory::EARTH_OBSERVATION)
        .value("METEOROLOGY",      PayloadCategory::METEOROLOGY)
        .value("TELECOMMUNICATIONS",PayloadCategory::TELECOMMUNICATIONS)
        .value("NAVIGATION",       PayloadCategory::NAVIGATION)
        .value("INTELLIGENCE",     PayloadCategory::INTELLIGENCE)
        .value("CARGO",            PayloadCategory::CARGO)
        .value("SCIENTIFIC",       PayloadCategory::SCIENTIFIC)
        .value("EXPLORATION",      PayloadCategory::EXPLORATION)
        .value("CREWED",           PayloadCategory::CREWED)
        .export_values();

    py::enum_<SpaceflightStatus>(m, "SpaceflightStatus")
        .value("INITIALIZING", SpaceflightStatus::INITIALIZING)
        .value("LAUNCHING",    SpaceflightStatus::LAUNCHING)
        .value("IN_ORBIT",     SpaceflightStatus::IN_ORBIT)
        .value("COMPLETED",    SpaceflightStatus::COMPLETED)
        .value("FAILED",       SpaceflightStatus::FAILED)
        .export_values();
}

inline void bind_models(py::module_& m) {

    py::class_<LaunchSite>(m, "LaunchSite")
        .def(py::init<>())
        .def_readwrite("id",       &LaunchSite::id)
        .def_readwrite("code",     &LaunchSite::code)
        .def_readwrite("status",   &LaunchSite::status)
        .def_readwrite("lat",      &LaunchSite::lat)
        .def_readwrite("lon",      &LaunchSite::lon)
        .def_readwrite("name",     &LaunchSite::name)
        .def_readwrite("country",  &LaunchSite::country)
        .def_readwrite("operator_",&LaunchSite::operator_);

    py::class_<OrbitalTarget>(m, "OrbitalTarget")
        .def(py::init<>())
        .def_readwrite("id",                  &OrbitalTarget::id)
        .def_readwrite("code",                &OrbitalTarget::code)
        .def_readwrite("name",                &OrbitalTarget::name)
        .def_readwrite("orbit_type",          &OrbitalTarget::orbit_type)
        .def_readwrite("altitude_perigee_km", &OrbitalTarget::altitude_perigee_km)
        .def_readwrite("altitude_apogee_km",  &OrbitalTarget::altitude_apogee_km)
        .def_readwrite("inclination_deg",     &OrbitalTarget::inclination_deg)
        .def_readwrite("description",         &OrbitalTarget::description);

    py::class_<Payload>(m, "Payload")
        .def(py::init<>())
        .def_readwrite("id",                    &Payload::id)
        .def_readwrite("code",                  &Payload::code)
        .def_readwrite("name",                  &Payload::name)
        .def_readwrite("mass_kg",               &Payload::mass_kg)
        .def_readwrite("category",              &Payload::category)
        .def_readwrite("compatible_orbit_types",&Payload::compatible_orbit_types)
        .def_readwrite("description",           &Payload::description);

    py::class_<Stage>(m, "Stage")
        .def(py::init<>())
        .def_readwrite("stage_number",   &Stage::stage_number)
        .def_readwrite("thrust_kn",      &Stage::thrust_kn)
        .def_readwrite("isp_vac_s",      &Stage::isp_vac_s)
        .def_readwrite("isp_sl_s",       &Stage::isp_sl_s)
        .def_readwrite("fuel_mass_kg",   &Stage::fuel_mass_kg)
        .def_readwrite("dry_mass_kg",    &Stage::dry_mass_kg)
        .def_readwrite("t_burn_s",       &Stage::t_burn_s)
        .def_readwrite("h_mean_m",       &Stage::h_mean_m)
        .def_readwrite("gamma_mean_deg", &Stage::gamma_mean_deg);
        .def_readwrite("cd",             &Stage::cd);
        .def_readwrite("v_maxq_m_s",     &Stage::v_maxq_m_s);

    py::class_<Rocket>(m, "Rocket")
        .def(py::init<>())
        .def_readwrite("id",                      &Rocket::id)
        .def_readwrite("code",                    &Rocket::code)
        .def_readwrite("name",                    &Rocket::name)
        .def_readwrite("manufacturer",            &Rocket::manufacturer)
        .def_readwrite("nb_stages",               &Rocket::nb_stages)
        .def_readwrite("max_payload_leo_kg",      &Rocket::max_payload_leo_kg)
        .def_readwrite("max_payload_geo_kg",      &Rocket::max_payload_geo_kg)
        .def_readwrite("max_fuel_kg",             &Rocket::max_fuel_kg)
        .def_readwrite("fuel_burn_rate_kg_per_s", &Rocket::fuel_burn_rate_kg_per_s)
        .def_readwrite("max_thrust_kn",           &Rocket::max_thrust_kn)
        .def_readwrite("max_speed_m_s",           &Rocket::max_speed_m_s)
        .def_readwrite("fairing_diameter_m",      &Rocket::fairing_diameter_m)
        .def_readwrite("compatible_orbit_types",  &Rocket::compatible_orbit_types)
        .def_readwrite("stages",                  &Rocket::stages)
        .def_readwrite("description",             &Rocket::description);

    py::class_<Spaceflight>(m, "Spaceflight")
        .def(py::init<>())
        .def_readwrite("id",                       &Spaceflight::id)
        .def_readwrite("spaceflight_code",         &Spaceflight::spaceflight_code)
        .def_readwrite("spaceflight_status",       &Spaceflight::spaceflight_status)
        .def_readwrite("spaceship_id",             &Spaceflight::spaceship_id)
        .def_readwrite("on_board_payloads",        &Spaceflight::on_board_payloads)
        .def_readwrite("orbital_target_id",        &Spaceflight::orbital_target_id)
        .def_readwrite("departure_launch_site_id", &Spaceflight::departure_launch_site_id)
        .def_readwrite("altitude_km",              &Spaceflight::altitude_km)
        .def_readwrite("fuel_kg",                  &Spaceflight::fuel_kg)
        .def_readwrite("fuel_burn_rate_kg_per_s",  &Spaceflight::fuel_burn_rate_kg_per_s);
}

inline void bind_functions(py::module_& m) {

    m.def("compute_delta_v", &compute_delta_v,
        py::arg("launch_site"),
        py::arg("target"),
        py::arg("rocket"),
        py::arg("payloads"),
        "Compute the delta-v (m/s) required to reach the orbital target from the given launch site.");

    m.def("compute_fuel", &compute_fuel,
        py::arg("rocket"),
        py::arg("payloads"),
        py::arg("delta_v"),
        "Compute the fuel mass (kg) required for the mission using the Tsiolkovsky rocket equation.");
}

PYBIND11_MODULE(orbital_core, m) {
    m.doc() = "orbital_core — C++ physics engine for the Orbital Flight Simulator";
    bind_enums(m);
    bind_models(m);
    bind_functions(m);
}
