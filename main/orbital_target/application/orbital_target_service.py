import sys
import os

from orbital_target.domain.orbital_target import OrbitalTarget
from rocket.domain.rocket import Rocket

CYAN = "\033[1;36m"
GRAY = "\033[90m"
RESET = "\033[0m"

def clear():
    os.system('cls' if sys.platform == "win32" else 'clear')

def select_orbital_target(rocket: Rocket, orbital_targets: dict[OrbitalTarget]) -> OrbitalTarget:
    compatible_orbit_type = list(rocket.compatible_orbit_types)
    selected_orbit = 0

    def print_orbit_menu():
        clear()
        print(f"{GRAY}? Choose a desired orbit type{RESET}\n")
        for i, orbit in enumerate(compatible_orbit_type):
            if i == selected_orbit:
                print(f"{CYAN}❯ {orbit}{RESET}")
            else:
                print(f"{GRAY}  {orbit}{RESET}")
        print(f"\n{GRAY}  ↑↓ to navigate · Enter to confirm{RESET}")

    # Select desired orbit from compatible orbit types
    if sys.platform == "win32":
        import msvcrt
        while True:
            print_orbit_menu()
            key = msvcrt.getch()
            if key == b'\xe0':
                key = msvcrt.getch()
                if key == b'H' and selected_orbit > 0:
                    selected_orbit -= 1
                elif key == b'P' and selected_orbit < len(compatible_orbit_type) - 1:
                    selected_orbit += 1
            elif key == b'\r':
                break
    else:
        import tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                print_orbit_menu()
                key = sys.stdin.read(1)
                if key == '\x1b':
                    key += sys.stdin.read(2)
                    if key == '\x1b[A' and selected_orbit > 0:
                        selected_orbit -= 1
                    elif key == '\x1b[B' and selected_orbit < len(compatible_orbit_type) - 1:
                        selected_orbit += 1
                elif key == '\r':
                    break
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    desired_orbit = compatible_orbit_type[selected_orbit]
    clear()
    print(f"{GRAY}? Choose a desired orbit type {CYAN}❯ {desired_orbit}{RESET}\n")

    # Get all orbital_targets matching the selected orbit type
    filtered_targets = [t for t in orbital_targets.values() if t.orbit_type == desired_orbit]
    selected_target = 0

    def print_target_menu():
        clear()
        print(f"{GRAY}? Choose an orbital target{RESET}\n")
        for i, target in enumerate(filtered_targets):
            if i == selected_target:
                print(f"{CYAN}❯ {target.name}")
                print(f"  {target.description}")
                print(f"  Perigee: {target.altitude_perigee_km} km · Apogee: {target.altitude_apogee_km} km · Inclination: {target.inclination_deg}°{RESET}")
            else:
                print(f"{GRAY}  {target.name}{RESET}")
        print(f"\n{GRAY}  ↑↓ to navigate · Enter to confirm{RESET}")

    # Select orbital target from filtered list
    if sys.platform == "win32":
        import msvcrt
        while True:
            print_target_menu()
            key = msvcrt.getch()
            if key == b'\xe0':
                key = msvcrt.getch()
                if key == b'H' and selected_target > 0:
                    selected_target -= 1
                elif key == b'P' and selected_target < len(filtered_targets) - 1:
                    selected_target += 1
            elif key == b'\r':
                break
    else:
        import tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                print_target_menu()
                key = sys.stdin.read(1)
                if key == '\x1b':
                    key += sys.stdin.read(2)
                    if key == '\x1b[A' and selected_target > 0:
                        selected_target -= 1
                    elif key == '\x1b[B' and selected_target < len(filtered_targets) - 1:
                        selected_target += 1
                elif key == '\r':
                    break
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    clear()
    print(f"{GRAY}? Choose an orbital target {CYAN}❯ {filtered_targets[selected_target].name}{RESET}\n")
    return filtered_targets[selected_target]