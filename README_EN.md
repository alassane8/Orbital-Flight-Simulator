# Orbital Flight Simulator

An orbital flight simulator I'm building to apply as much realism as possible to every stage of the flight — from liftoff to orbital insertion, and beyond.

This project comes from a conviction: the best way to truly understand orbital mechanics and GNC is to implement it yourself, equation by equation.

---

## What the simulator covers

The complete flight of a launch vehicle, from the launch pad to lunar orbit:

- **Atmospheric phase** — ISA model, aerodynamic drag, gravity turn, propellant consumption (Tsiolkovsky)
- **Orbital insertion** — RK4 integrator, transition to Keplerian elements
- **Orbital mechanics** — Keplerian propagator, J2 perturbation (Earth oblateness), impulsive Δv maneuvers
- **Earth–Moon transfer** — Hohmann maneuver, Δv budget calculation
- **Attitude dynamics (in progress)** — quaternion representation, Euler equations, PD controller

The simulation advances in fixed time steps. Physics is numerically integrated every tick, with a real-time pygame visualization.

---

## Architecture

```
orbital-flight-simulator/
├── main/
│   ├── config/           — simulation parameters
│   ├── launch_site/      — launch sites
│   ├── orbital_core/     — computation core (RK4, Kepler, J2, Hohmann)
│   ├── orbital_target/   — target orbits
│   ├── payload/          — payload
│   ├── rocket/           — launch vehicle model
│   ├── shared/           — shared utilities
│   ├── spaceflight/      — flight sequence and mission integration
│   └── main.py
└── requirements.txt
```

**Stack:** Python for mission logic and visualization · C++ (pybind11 + Eigen) for the numerical computation core · Simulink for cross-validation of control laws

The Python/C++ boundary is intentional: force assembly stays in Python for flexibility, while pure computation (RK4, Kepler, J2) runs in C++ for performance.

---

## What the project will include

- ISA atmospheric model (troposphere → 80 km)
- 3-DOF launch dynamics with gravity turn and propellant consumption
- RK4 integrator in C++ (pybind11 + Eigen)
- Keplerian propagator with J2 perturbation
- Impulsive Δv maneuvers and Earth–Moon Hohmann transfer
- 6-DOF attitude dynamics — quaternions, Euler equations, PD controller
- Real-time pygame visualization (3D trajectory, HUD)
- Python / Simulink cross-validation of control laws

---

## Why this project

I wanted to understand how a real launch vehicle goes from 0 m/s on a pad to a precise orbit. Not by reading formulas, but by running them and watching whether the trajectory converges.

Each module was an opportunity to dig into something real: why RK4 and not Euler, how the gravity turn minimizes structural loads, what J2 actually does to an orbit over a few revolutions, why quaternions and not Euler angles for attitude.

The end goal is a simulator that gets as close as possible to industry practices — the 3-DOF/6-DOF separation, the Python→Simulink→embedded C workflow, and reference models (ISA, WGS84, EGM2008).