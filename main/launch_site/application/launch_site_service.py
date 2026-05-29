import sys
import os
import math

from launch_site.domain.launch_site import LaunchSite
from launch_site.domain.launch_site_status import LaunchSiteStatus
from orbital_target.domain.orbital_target import OrbitalTarget
from rocket.domain.rocket import Rocket

CYAN  = "\033[1;36m"
GREEN = "\033[1;32m"
YELLOW= "\033[1;33m"
RED   = "\033[1;31m"
GRAY  = "\033[90m"
BOLD  = "\033[1m"
RESET = "\033[0m"

MANUFACTURER_OPERATOR_TOKENS: dict[str, list[str]] = {
    "SpaceX":       ["SpaceX"],
    "Rocket Lab":   ["Rocket Lab"],
    "Arianespace":  ["Arianespace", "ESA"],
    "Roscosmos":    ["Roscosmos"],
    "CASC":         ["CASC"],
    "JAXA":         ["JAXA"],
    "ISRO":         ["ISRO"],
    "NASA":         ["NASA", "SpaceX"],
    "Blue Origin":  ["NASA", "USSF", "SpaceX"],
    "ULA":          ["NASA", "USSF", "SpaceX"],
}

INCLINATION_BY_ORBIT: dict[str, float] = {
    "LOW_EARTH_ORBIT":          51.6,
    "SUN_SYNCHRONOUS_ORBIT":    97.8,
    "MEDIUM_EARTH_ORBIT":       55.0,
    "GEOSTATIONARY_ORBIT":       0.0,
    "HIGHLY_ELLIPTICAL_ORBIT":  63.4,
    "TRANS_LUNAR_INJECTION":    28.5,
    "LUNAR_ORBIT":              28.5,
}
INCLINATION_MARGIN_DEG = 2.0


def _operator_matches(site: LaunchSite, manufacturer: str) -> bool:
    tokens = MANUFACTURER_OPERATOR_TOKENS.get(manufacturer)
    if tokens is None:
        return True
    return any(tok.lower() in site.operator.lower() for tok in tokens)


def _inclination_compatible(site: LaunchSite, target: OrbitalTarget) -> bool:
    required = INCLINATION_BY_ORBIT.get(str(target.orbit_type), target.inclination_deg)
    if required >= 90:
        return abs(site.lat) >= (90 - INCLINATION_MARGIN_DEG)
    return abs(site.lat) <= required + INCLINATION_MARGIN_DEG


def _equatorial_bonus_m_s(lat_deg: float) -> float:
    """Bonus de vitesse dû à la rotation terrestre selon la latitude du site."""
    EARTH_EQUATORIAL_SPEED_M_S = 465.1
    return EARTH_EQUATORIAL_SPEED_M_S * math.cos(math.radians(lat_deg))


def _compatibility_label(site: LaunchSite, target: OrbitalTarget) -> tuple[str, str]:
    """Retourne (couleur, label court) décrivant la compatibilité d'inclinaison."""
    required = INCLINATION_BY_ORBIT.get(str(target.orbit_type), target.inclination_deg)
    diff = abs(abs(site.lat) - required)
    if diff <= INCLINATION_MARGIN_DEG:
        return GREEN, "optimal"
    elif diff <= 10:
        return YELLOW, f"Δ{diff:.0f}° Δv penalty"
    else:
        return RED, f"Δ{diff:.0f}° high penalty"


def clear():
    os.system('cls' if sys.platform == "win32" else 'clear')


def select_launch_site(
    rocket: Rocket,
    orbital_target: OrbitalTarget,
    launch_sites: dict[str, LaunchSite],
) -> LaunchSite:
    manufacturer_ok = [
        s for s in launch_sites.values()
        if s.status == LaunchSiteStatus.ACTIVE
        and _operator_matches(s, rocket.manufacturer)
    ]
    compatible = [s for s in manufacturer_ok if _inclination_compatible(s, orbital_target)]
    suboptimal = [s for s in manufacturer_ok if not _inclination_compatible(s, orbital_target)]

    display_list: list[tuple[LaunchSite, bool]] = (
        [(s, True) for s in compatible] + [(s, False) for s in suboptimal]
    )

    if not display_list:
        raise ValueError(
            f"No launch site available for rocket '{rocket.name}' "
            f"(manufacturer: {rocket.manufacturer})."
        )

    selected_index = 0

    def print_menu():
        clear()
        print(f"{BOLD}┌─ Launch Site Selection ──────────────────────────────────────────┐{RESET}")
        print(f"{BOLD}│{RESET}  Rocket      : {CYAN}{rocket.name}{RESET}")
        print(f"{BOLD}│{RESET}  Manufacturer: {CYAN}{rocket.manufacturer}{RESET}")
        print(f"{BOLD}│{RESET}  Target orbit: {CYAN}{target_orbit_label}{RESET}  "
              f"({GRAY}incl. {required_inc:.1f}°{RESET})")
        print(f"{BOLD}└──────────────────────────────────────────────────────────────────┘{RESET}\n")

        print(f"{GRAY}? Choose a launch site  "
              f"[{GREEN}{len(compatible)} compatible{RESET}{GRAY}  /  "
              f"{YELLOW}{len(suboptimal)} suboptimal{RESET}{GRAY}]{RESET}\n")

        for i, (site, is_compat) in enumerate(display_list):
            color, compat_label = _compatibility_label(site, orbital_target)
            bonus = _equatorial_bonus_m_s(site.lat)

            if i == selected_index:
                prefix = f"{CYAN}❯"
                name_c = CYAN
            else:
                prefix = f"{GRAY} "
                name_c = GRAY if not is_compat else RESET

            status_dot = f"{GREEN}●{RESET}" if is_compat else f"{color}●{RESET}"

            print(f"  {prefix} {status_dot} {name_c}{site.name}{RESET}  "
                  f"{GRAY}[{site.launch_site_code}] {site.country}{RESET}")

            if i == selected_index:
                print(f"       {GRAY}Operator : {site.operator}{RESET}")
                print(f"       {GRAY}Position : {site.lat:+.2f}° lat  {site.lon:+.2f}° lon{RESET}")
                print(f"       {color}Inclination compatibility : {compat_label}{RESET}")
                print(f"       {CYAN}Equatorial speed bonus   : +{bonus:.0f} m/s{RESET}")

        print(f"\n{GRAY}  ↑↓ navigate · Enter confirm{RESET}")

    target_orbit_label = str(orbital_target.orbit_type).replace("_", " ")
    required_inc = INCLINATION_BY_ORBIT.get(
        str(orbital_target.orbit_type), orbital_target.inclination_deg
    )

    def read_key_unix():
        import tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
            if key == '\x1b':
                key += sys.stdin.read(2)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return key

    def read_key_win():
        import msvcrt
        key = msvcrt.getch()
        if key == b'\xe0':
            key += msvcrt.getch()
        return key

    while True:
        print_menu()

        if sys.platform == "win32":
            key = read_key_win()
            up    = key == b'\xe0H'
            down  = key == b'\xe0P'
            enter = key == b'\r'
        else:
            key = read_key_unix()
            up    = key == '\x1b[A'
            down  = key == '\x1b[B'
            enter = key == '\r'

        if up and selected_index > 0:
            selected_index -= 1
        elif down and selected_index < len(display_list) - 1:
            selected_index += 1
        elif enter:
            break

    chosen_site, _ = display_list[selected_index]
    clear()
    print(
        f"{GRAY}? Choose a launch site "
        f"{CYAN}❯ {chosen_site.name} [{chosen_site.launch_site_code}]{RESET}\n"
    )
    return chosen_site