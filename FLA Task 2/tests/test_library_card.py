"""Unit tests for Application 1: Library Card ID Validation DFA.

Requirements:
- At least five accepted test cases.
- At least five rejected test cases.
"""

import pytest
from automata.library_card import validate_library_card, is_valid_library_card


# At least 5 accepted test cases specified in the report
ACCEPTED_CASES = [
    "L04",
    "L27",
    "L90",
    "L00",
    "L58",
    "L12",
    "L99",
]

# At least 5 rejected test cases specified in the report and edge cases
REJECTED_CASES = [
    "04",     # Missing leading 'L'
    "l27",    # Lowercase 'l' instead of uppercase 'L'
    "L2",     # Incomplete length (only one digit)
    "L275",   # Exceeds maximum length (three digits)
    "LA7",    # Non-digit character in digit position
    "L-7",    # Special character in digit position
    "",       # Empty string
    "L",      # Only prefix without digits
    "123",    # Only digits, no 'L'
    "LL1",    # Duplicate 'L'
]


@pytest.mark.parametrize("card_id", ACCEPTED_CASES)
def test_accepted_library_cards(card_id: str):
    """Verify that all valid library card IDs are accepted by the DFA."""
    is_accepted, history, final_state = validate_library_card(card_id, verbose=False)
    assert is_accepted is True, f"Expected '{card_id}' to be ACCEPTED"
    assert final_state == "q3", f"Expected final state 'q3', got '{final_state}'"
    assert len(history) == 3, f"Expected exactly 3 transitions, got {len(history)}"
    assert is_valid_library_card(card_id) is True


@pytest.mark.parametrize("card_id", REJECTED_CASES)
def test_rejected_library_cards(card_id: str):
    """Verify that all invalid library card IDs are rejected by the DFA."""
    is_accepted, _, final_state = validate_library_card(card_id, verbose=False)
    assert is_accepted is False, f"Expected '{card_id}' to be REJECTED"
    assert final_state != "q3", f"Final state should not be 'q3', got '{final_state}'"
    assert is_valid_library_card(card_id) is False


def test_library_card_transition_trace():
    """Verify exact step-by-step state transitions for 'L27'."""
    is_accepted, history, final_state = validate_library_card("L27", verbose=False)
    assert is_accepted is True
    assert final_state == "q3"
    assert len(history) == 3

    assert history[0] == {"step": 1, "from_state": "q0", "symbol": "L", "to_state": "q1"}
    assert history[1] == {"step": 2, "from_state": "q1", "symbol": "2", "to_state": "q2"}
    assert history[2] == {"step": 3, "from_state": "q2", "symbol": "7", "to_state": "q3"}


def test_library_card_dead_state_transition():
    """Verify transition to dead state qD on invalid symbol."""
    is_accepted, history, final_state = validate_library_card("LX5", verbose=False)
    assert is_accepted is False
    assert final_state == "qD"
    assert history[1]["to_state"] == "qD"
    assert history[2]["to_state"] == "qD"
