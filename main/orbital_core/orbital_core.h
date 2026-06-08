#pragma once

#include <vector>
#include "models.h"

/**
 * Computes the delta-v (m/s) required to reach the orbital target from the given launch site.
 * Takes into account the launch site latitude, the target orbit altitude, inclination,
 * and the Earth's rotation contribution.
 *
 * @param launch_site  The launch site from which the rocket departs
 * @param target       The orbital target (altitude, inclination, orbit type)
 * @param rocket       The rocket
 * @return             The required delta-v in m/s
 */
double compute_delta_v(const LaunchSite& launch_site, const OrbitalTarget& target, const Rocket& rocket);

/**
 * Computes the total fuel mass (kg) required for the mission using the Tsiolkovsky rocket equation.
 * Accounts for the rocket's specific impulse, its dry mass, and the total payload mass.
 *
 * @param rocket    The rocket performing the mission
 * @param payloads  The list of payloads on board
 * @param delta_v   The required delta-v in m/s, as returned by compute_delta_v
 * @return          The required fuel mass in kg
 */
double compute_fuel(const Rocket& rocket, const std::vector<Payload>& payloads, double delta_v);
// Fonctions internes (déclarées ici pour être visibles dans tout le .cpp)
double compute_delta_v_orbital(const LaunchSite& launch_site, const OrbitalTarget& target);
double compute_delta_v_gravity_drag(const Rocket& rocket);
double compute_delta_v_aero_drag();
double compute_delta_v_steering();
double compute_delta_v_plan_change();
 