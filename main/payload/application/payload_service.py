import sys
import os

from payload.domain.payload import Payload
from rocket.domain.rocket import Rocket

CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
GRAY = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"

GEO_ORBIT_TYPES = {"GEOSTATIONARY_ORBIT"}
LEO_ORBIT_TYPES = {
    "LOW_EARTH_ORBIT",
    "SUN_SYNCHRONOUS_ORBIT",
    "MEDIUM_EARTH_ORBIT",
    "HIGHLY_ELLIPTICAL_ORBIT",
    "TRANS_LUNAR_INJECTION",
    "LUNAR_ORBIT",
}


def clear():
    os.system('cls' if sys.platform == "win32" else 'clear')


def _get_max_payload_kg(rocket: Rocket, payload: Payload) -> int:
    """Return the rocket's weight limit relevant to this payload's orbit types."""
    orbit_types = set(str(o) for o in payload.compatible_orbit_types)
    if orbit_types & GEO_ORBIT_TYPES:
        return rocket.max_payload_geo_kg
    return rocket.max_payload_leo_kg


def _orbit_label(payload: Payload) -> str:
    """Return 'GEO' or 'LEO' label for display."""
    orbit_types = set(str(o) for o in payload.compatible_orbit_types)
    if orbit_types & GEO_ORBIT_TYPES:
        return "GEO"
    return "LEO"


def add_payloads_to_rocket(rocket: Rocket, payloads: dict[str, Payload]) -> list[Payload]:
    payload_list = list(payloads.values())
    selected_index = 0
    selected_payloads: list[Payload] = []

    def current_mass() -> float:
        return sum(p.mass_kg for p in selected_payloads)

    def remaining_capacity(payload: Payload) -> float:
        limit = _get_max_payload_kg(rocket, payload)
        return limit - current_mass()

    def can_add(payload: Payload) -> bool:
        return payload.mass_kg <= remaining_capacity(payload)

    def is_selected(payload: Payload) -> bool:
        return payload in selected_payloads

    def print_menu():
        clear()
        leo_used = sum(
            p.mass_kg for p in selected_payloads
            if not (set(str(o) for o in p.compatible_orbit_types) & GEO_ORBIT_TYPES)
        )
        geo_used = sum(
            p.mass_kg for p in selected_payloads
            if set(str(o) for o in p.compatible_orbit_types) & GEO_ORBIT_TYPES
        )

        print(f"{BOLD}┌─ {rocket.name} ─ Payload Configuration ───────────────────────┐{RESET}")
        print(f"{BOLD}│{RESET}  LEO capacity : {GREEN}{leo_used:>6} kg{RESET} / {rocket.max_payload_leo_kg} kg  "
              f"│  GEO capacity : {GREEN}{geo_used:>6} kg{RESET} / {rocket.max_payload_geo_kg} kg  {BOLD}│{RESET}")
        print(f"{BOLD}└────────────────────────────────────────────────────────────────┘{RESET}\n")

        print(f"{GRAY}? Select payloads to add  [{len(selected_payloads)} selected]{RESET}\n")

        for i, payload in enumerate(payload_list):
            selected = is_selected(payload)
            addable = can_add(payload)
            orbit = _orbit_label(payload)

            checkbox = f"{GREEN}[✓]{RESET}" if selected else (
                f"{GRAY}[ ]{RESET}" if addable else f"{RED}[✗]{RESET}"
            )

            if i == selected_index:
                name_color = CYAN
                prefix = "❯"
            else:
                name_color = GRAY if not addable and not selected else RESET
                prefix = " "

            print(f"  {prefix} {checkbox} {name_color}{payload.name}{RESET}  "
                  f"{GRAY}[{orbit}] {payload.mass_kg} kg{RESET}")

            if i == selected_index:
                print(f"       {GRAY}{payload.description}{RESET}")
                remaining = remaining_capacity(payload)
                if selected:
                    print(f"       {GREEN}✓ Added — remove with Space{RESET}")
                elif addable:
                    print(f"       {CYAN}Capacity remaining after adding : {remaining - payload.mass_kg:.0f} kg{RESET}")
                else:
                    print(f"       {RED}✗ Insufficient capacity (needs {payload.mass_kg} kg, {remaining:.0f} kg left){RESET}")

        print(f"\n{GRAY}  ↑↓ navigate · Space select/deselect · Enter confirm · Q quit{RESET}")

        if selected_payloads:
            names = ", ".join(p.name for p in selected_payloads)
            print(f"\n{GREEN}  Selected : {names}{RESET}")

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
            up = key == b'\xe0H'
            down = key == b'\xe0P'
            space = key == b' '
            enter = key == b'\r'
            quit_ = key in (b'q', b'Q')
        else:
            key = read_key_unix()
            up = key == '\x1b[A'
            down = key == '\x1b[B'
            space = key == ' '
            enter = key == '\r'
            quit_ = key in ('q', 'Q')

        if up and selected_index > 0:
            selected_index -= 1
        elif down and selected_index < len(payload_list) - 1:
            selected_index += 1
        elif space:
            payload = payload_list[selected_index]
            if is_selected(payload):
                selected_payloads.remove(payload)
            elif can_add(payload):
                selected_payloads.append(payload)
        elif enter:
            break
        elif quit_:
            break

    clear()
    if selected_payloads:
        names = ", ".join(p.name for p in selected_payloads)
        print(f"{GRAY}? Payloads selected {CYAN}❯ {names}{RESET}\n")
    else:
        print(f"{GRAY}? Payloads selected {CYAN}❯ (none){RESET}\n")

    return selected_payloads