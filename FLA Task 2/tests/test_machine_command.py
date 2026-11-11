"""Unit tests for Application 2: Machine Command Validation DFA.

Requirements:
- At least five accepted test cases.
- At least five rejected test cases.
"""

import pytest
from automata.machine_command import validate_machine_commands, is_valid_machine_commands


# At least 5 accepted test cases specified in the report
ACCEPTED_CASES = [
    ["GO"],
    ["STOP"],
    ["GO", "STOP"],
    ["STOP", "GO"],
    ["GO", "GO", "STOP"],
    "GO STOP",          # Space-separated string format
    "STOP GO GO STOP",  # Longer valid string sequence
]

# At least 5 rejected test cases specified in the report and edge cases
REJECTED_CASES = [
    [],                      # Empty list
    "",                      # Empty string
    "   ",                   # Whitespace only
    ["START"],               # Unknown command token
    ["GO", "PAUSE"],         # Mixed with unknown token
    ["STO"],                 # Incomplete token
    ["GO", "HALT", "STOP"],  # Embedded unknown token
    ["go"],                  # Lowercase token rejected
    "GO PAUSE",              # String format with invalid token
]


@pytest.mark.parametrize("commands", ACCEPTED_CASES)
def test_accepted_machine_commands(commands):
    """Verify that all valid command sequences are accepted by the DFA."""
    is_accepted, history, final_state = validate_machine_commands(commands, verbose=False)
    assert is_accepted is True, f"Expected {commands} to be ACCEPTED"
    assert final_state == "qA", f"Expected final state 'qA', got '{final_state}'"
    assert len(history) >= 1, "Expected at least 1 transition"
    assert is_valid_machine_commands(commands) is True


@pytest.mark.parametrize("commands", REJECTED_CASES)
def test_rejected_machine_commands(commands):
    """Verify that all invalid command sequences are rejected by the DFA."""
    is_accepted, _, final_state = validate_machine_commands(commands, verbose=False)
    assert is_accepted is False, f"Expected {commands} to be REJECTED"
    assert final_state != "qA", f"Final state should not be 'qA', got '{final_state}'"
    assert is_valid_machine_commands(commands) is False


def test_machine_command_transition_trace():
    """Verify step-by-step state transitions for ['GO', 'STOP']."""
    is_accepted, history, final_state = validate_machine_commands(["GO", "STOP"], verbose=False)
    assert is_accepted is True
    assert final_state == "qA"
    assert len(history) == 2

    assert history[0] == {"step": 1, "from_state": "q0", "token": "GO", "to_state": "qA"}
    assert history[1] == {"step": 2, "from_state": "qA", "token": "STOP", "to_state": "qA"}


def test_machine_command_dead_state_transition():
    """Verify transition to dead state qD upon encountering invalid token."""
    is_accepted, history, final_state = validate_machine_commands(["GO", "HALT", "STOP"], verbose=False)
    assert is_accepted is False
    assert final_state == "qD"
    assert history[0]["to_state"] == "qA"
    assert history[1]["to_state"] == "qD"
    assert history[2]["to_state"] == "qD"
