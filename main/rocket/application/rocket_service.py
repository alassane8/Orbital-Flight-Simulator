import sys
import os

CYAN = "\033[1;36m"
GRAY  = "\033[90m"
RESET = "\033[0m"

def clear():
    os.system('cls' if sys.platform == "win32" else 'clear')

def select_rocket(rockets: dict) -> object:
    rocket_list = list(rockets.values())
    selected = 0

    def print_menu():
        clear()
        print(f"{GRAY}? Choose a rocket for simulation{RESET}\n")
        for i, rocket in enumerate(rocket_list):
            if i == selected:
                print(f"{CYAN}❯ {rocket.name} | {rocket.manufacturer}")
                print(f"  {rocket.description}")
                print(f"  Compatible orbits:")
                for orbit in rocket.compatible_orbit_types:
                    print(f"    · {orbit}")
                print(RESET, end="")
            else:
                print(f"{GRAY}  {rocket.name} | {rocket.manufacturer}{RESET}")
        print(f"\n{GRAY}  ↑↓ to navigate · Enter to confirm{RESET}")

    if sys.platform == "win32":
        import msvcrt
        while True:
            print_menu()
            key = msvcrt.getch()
            if key == b'\xe0':
                key = msvcrt.getch()
                if key == b'H' and selected > 0:
                    selected -= 1
                elif key == b'P' and selected < len(rocket_list) - 1:
                    selected += 1
            elif key == b'\r':
                break
    else:
        import tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                print_menu()
                key = sys.stdin.read(1)
                if key == '\x1b':
                    key += sys.stdin.read(2)
                    if key == '\x1b[A' and selected > 0:
                        selected -= 1
                    elif key == '\x1b[B' and selected < len(rocket_list) - 1:
                        selected += 1
                elif key == '\r':
                    break
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    clear()
    print(f"{GRAY}? Choose a rocket for simulation {CYAN}❯ {rocket_list[selected].name}{RESET}\n")
    return rocket_list[selected]