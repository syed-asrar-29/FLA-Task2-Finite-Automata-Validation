"""Finite Automata Validation System - Main Command Line Interface.

Project Title:
    Designing Automata for Real-Time Applications –
    A Case Study of Three Finite-Automata Validation Systems.

Course:
    Formal Language and Automata (FLA) - Task 2
"""

import sys
from automata.library_card import validate_library_card
from automata.machine_command import validate_machine_commands
from automata.binary_sensor import validate_binary_sensor


def display_menu() -> None:
    """Prints the main interactive menu for the application."""
    print("========================================")
    print("FINITE AUTOMATA VALIDATION SYSTEM")
    print("========================================")
    print("1. Library Card ID Validation")
    print("2. Machine Command Validation")
    print("3. Binary Sensor Alert Validation")
    print("4. Exit")
    print("========================================")


def run_library_card_app() -> None:
    """Handles user input and execution for Application 1: Library Card ID."""
    print("\n--- Application 1: Library Card ID Validation ---")
    print("Rule: Must start with uppercase 'L' followed by exactly two digits (e.g. L04, L27).")
    user_input = input("Enter Library Card ID (or press Enter for empty): ")
    validate_library_card(user_input, verbose=True)


def run_machine_command_app() -> None:
    """Handles user input and execution for Application 2: Machine Command Validation."""
    print("\n--- Application 2: Machine Command Validation ---")
    print("Rule: Sequence of space-separated tokens; only 'GO' and 'STOP' allowed (e.g. 'GO STOP').")
    user_input = input("Enter command sequence: ")
    validate_machine_commands(user_input, verbose=True)


def run_binary_sensor_app() -> None:
    """Handles user input and execution for Application 3: Binary Sensor Alert."""
    print("\n--- Application 3: Binary Sensor Alert Validation ---")
    print("Rule: Binary sequence of '0' and '1' that must end with consecutive ones '11' (e.g. 1011).")
    user_input = input("Enter binary sequence: ")
    validate_binary_sensor(user_input, verbose=True)


def main() -> None:
    """Main program loop providing a CLI menu to run DFA validators."""
    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            run_library_card_app()
        elif choice == "2":
            run_machine_command_app()
        elif choice == "3":
            run_binary_sensor_app()
        elif choice == "4":
            print("\nExiting Finite Automata Validation System. Goodbye!")
            sys.exit(0)
        else:
            print(f"\n[Error] Invalid choice '{choice}'. Please select an option between 1 and 4.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user. Exiting...")
        sys.exit(0)
