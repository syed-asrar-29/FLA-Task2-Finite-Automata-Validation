"""Automata package for Formal Language and Automata (FLA) Task 2.

This package contains three Deterministic Finite Automata (DFA) implementations:
1. Library Card ID Validation (library_card)
2. Machine Command Validation (machine_command)
3. Binary Sensor Alert Validation (binary_sensor)
"""

from automata.library_card import validate_library_card, is_valid_library_card
from automata.machine_command import validate_machine_commands, is_valid_machine_commands
from automata.binary_sensor import validate_binary_sensor, is_valid_binary_sensor

__all__ = [
    "validate_library_card",
    "is_valid_library_card",
    "validate_machine_commands",
    "is_valid_machine_commands",
    "validate_binary_sensor",
    "is_valid_binary_sensor",
]
