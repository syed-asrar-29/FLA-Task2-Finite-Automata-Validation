"""Unit tests for Application 3: Binary Sensor Alert Validation DFA.

Requirements:
- At least five accepted test cases.
- At least five rejected test cases.
"""

import pytest
from automata.binary_sensor import validate_binary_sensor, is_valid_binary_sensor


# At least 5 accepted test cases specified in the report
ACCEPTED_CASES = [
    "11",
    "011",
    "1011",
    "00011",
    "111",
    "101011",
    "0011",
]

# At least 5 rejected test cases specified in the report and edge cases
REJECTED_CASES = [
    "",       # Empty string
    "1",      # Single one (needs two consecutive ones)
    "10",     # Ends with zero
    "110",    # Contains 11 but ends with zero
    "1010",   # Alternating, ends with zero
    "11A",    # Contains non-binary character 'A'
    "0",      # Single zero
    "1001",   # Ends with single one preceded by zero
    "1101",   # Ends with 01, not 11
    "abc",    # Completely non-binary
]


@pytest.mark.parametrize("binary_str", ACCEPTED_CASES)
def test_accepted_binary_sensor(binary_str: str):
    """Verify that all sequences ending in '11' are accepted by the DFA."""
    is_accepted, history, final_state = validate_binary_sensor(binary_str, verbose=False)
    assert is_accepted is True, f"Expected '{binary_str}' to be ACCEPTED"
    assert final_state == "q2", f"Expected final state 'q2', got '{final_state}'"
    assert is_valid_binary_sensor(binary_str) is True


@pytest.mark.parametrize("binary_str", REJECTED_CASES)
def test_rejected_binary_sensor(binary_str: str):
    """Verify that all sequences not ending in '11' or invalid are rejected by the DFA."""
    is_accepted, _, final_state = validate_binary_sensor(binary_str, verbose=False)
    assert is_accepted is False, f"Expected '{binary_str}' to be REJECTED"
    assert final_state != "q2", f"Final state should not be 'q2', got '{final_state}'"
    assert is_valid_binary_sensor(binary_str) is False


def test_binary_sensor_transition_trace():
    """Verify step-by-step state transitions for '1011'."""
    is_accepted, history, final_state = validate_binary_sensor("1011", verbose=False)
    assert is_accepted is True
    assert final_state == "q2"
    assert len(history) == 4

    assert history[0] == {"step": 1, "from_state": "q0", "symbol": "1", "to_state": "q1"}
    assert history[1] == {"step": 2, "from_state": "q1", "symbol": "0", "to_state": "q0"}
    assert history[2] == {"step": 3, "from_state": "q0", "symbol": "1", "to_state": "q1"}
    assert history[3] == {"step": 4, "from_state": "q1", "symbol": "1", "to_state": "q2"}


def test_binary_sensor_triple_one_transition():
    """Verify state remains in q2 when receiving a third consecutive '1' ('111')."""
    is_accepted, history, final_state = validate_binary_sensor("111", verbose=False)
    assert is_accepted is True
    assert final_state == "q2"
    assert history[2] == {"step": 3, "from_state": "q2", "symbol": "1", "to_state": "q2"}


def test_binary_sensor_dead_state_transition():
    """Verify transition to dead state qD on invalid symbol ('11A')."""
    is_accepted, history, final_state = validate_binary_sensor("11A", verbose=False)
    assert is_accepted is False
    assert final_state == "qD"
    assert history[2]["to_state"] == "qD"
