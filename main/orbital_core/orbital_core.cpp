#include "orbital_core.h"
#include "constants.h"
#include <cmath>
#include <math.h>

double compute_delta_v(const LaunchSite& launch_site, const OrbitalTarget& target, const Rocket& rocket){
    double v_orbital = compute_delta_v_orbital(launch_site, target);
    double v_gravity_drag = compute_delta_v_gravity_drag(rocket);
    double v_aero_drag = compute_delta_v_aero_drag();
    double v_steering = compute_delta_v_steering();
    double v_plan_change = compute_delta_v_plan_change();

    return v_orbital + v_gravity_drag + v_aero_drag + v_steering + v_plan_change;
}

double compute_fuel(const Rocket& rocket, const std::vector<Payload>& payloads, double delta_v){
    return 0.0; // TODO: implémenter
}

double compute_delta_v_orbital(const LaunchSite& launch_site, const OrbitalTarget& target){
    orbital_target_inclinaison = target.inclination_deg * M_PI / 180.0;
    latitude_launch_site = launch_site.lat * M_PI / 180.0;
    orbital_target_altitude = target.altitude_perigee_km * 1000.0;

    const double v_orbital  = std::sqrt(CONSTANTS::MU / (CONSTANTS::R_EARTH + orbital_target_altitude));
    const double v_rotation = CONSTANTS::OMEGA_EARTH
                            * CONSTANTS::R_EARTH
                            * std::cos(latitude_launch_site)
                            * std::cos(orbital_target_inclinaison);

    return v_orbital - v_rotation;
}

double compute_delta_v_gravity_drag(const Rocket& rocket) {
    double dv_gravity_drag = 0.0;

    for (int i = 0; i < rocket.stages.size(); i++) {
        Stage stage = rocket.stages[i];
        double g_mean   = Constants::MU / std::pow(Constants::R_EARTH + stage.h_mean_m, 2);
        double gamma_rad = stage.gamma_mean_deg * M_PI / 180.0;
        dv_gravity_drag += g_mean * std::sin(gamma_rad) * stage.t_burn_s;
    }

    return dv_gravity_drag;
}

double compute_delta_v_aero_drag(){

}
double compute_delta_v_steering(){

}
double compute_delta_v_plan_change(){

}