"""Application 1: Library Card ID Validation DFA.

Purpose:
    Validate a library card ID consisting of an uppercase 'L' followed by
    exactly two digits (0-9).

Formal Definition (5-tuple DFA):
    M = (Q, Sigma, delta, q0, F)
    - Q: Set of states {q0, q1, q2, q3, qD}
    - Sigma: Alphabet of valid characters (letters, digits, symbols)
    - delta: State transition function Q x Sigma -> Q
    - q0: Initial state (start)
    - F: Set of accepting states {q3}

Rules:
    1. First character must be 'L'.
    2. Second and third characters must be digits ('0'-'9').
    3. Exactly three characters are allowed.
    4. Lowercase letters, extra characters, and special symbols are rejected.

States:
    q0 : Initial state (waiting for 'L')
    q1 : 'L' received (waiting for first digit)
    q2 : First digit received (waiting for second digit)
    q3 : Complete valid ID (accepting state)
    qD : Dead / rejecting sink state
"""

from typing import Tuple, List, Dict, Any


# Define the DFA states
STATES = {"q0", "q1", "q2", "q3", "qD"}
INITIAL_STATE = "q0"
ACCEPTING_STATES = {"q3"}


def transition(current_state: str, symbol: str) -> str:
    """Computes the next state in the Library Card DFA given the current state and symbol.

    Args:
        current_state: The current state of the DFA (e.g., 'q0', 'q1', etc.).
        symbol: The single character being processed.

    Returns:
        The next state according to the DFA transition function.
    """
    if current_state == "q0":
        # Initial state: must receive uppercase 'L'
        if symbol == "L":
            return "q1"
        return "qD"

    elif current_state == "q1":
        # State q1: expects first digit ('0' through '9')
        if symbol.isdigit():
            return "q2"
        return "qD"

    elif current_state == "q2":
        # State q2: expects second digit ('0' through '9')
        if symbol.isdigit():
            return "q3"
        return "qD"

    elif current_state == "q3":
        # State q3: already has 3 characters. Any extra symbol violates the length rule
        return "qD"

    elif current_state == "qD":
        # Trap / dead state: remains in qD on any input
        return "qD"

    # Default fallback to dead state
    return "qD"


def validate_library_card(card_id: str, verbose: bool = True) -> Tuple[bool, List[Dict[str, Any]], str]:
    """Validates a library card ID symbol-by-symbol using the DFA.

    Args:
        card_id: The string to be validated (e.g., "L04", "L27").
        verbose: Whether to print step-by-step transition details.

    Returns:
        A tuple of:
            - is_accepted (bool): True if accepted by the DFA, False otherwise.
            - history (list of dicts): Step-by-step transition history.
            - final_state (str): The state reached after consuming the input.
    """
    current_state = INITIAL_STATE
    history: List[Dict[str, Any]] = []

    if verbose:
        print("\n" + "=" * 55)
        print("  DFA VALIDATION: Library Card ID")
        print("=" * 55)
        print(f"Input String : '{card_id}'")
        print(f"Initial State: {current_state}")
        print("-" * 55)
        print("State Transitions:")

    # Process each symbol in the input string
    if not card_id and verbose:
        print("  (Empty input string - no transitions executed)")

    for index, symbol in enumerate(card_id, start=1):
        prev_state = current_state
        current_state = transition(current_state, symbol)
        step_info = {
            "step": index,
            "from_state": prev_state,
            "symbol": symbol,
            "to_state": current_state,
        }
        history.append(step_info)

        if verbose:
            print(f"  [Step {index}] State '{prev_state}' --( '{symbol}' )--> State '{current_state}'")

    final_state = current_state
    is_accepted = final_state in ACCEPTING_STATES

    if verbose:
        print("-" * 55)
        path = " -> ".join([INITIAL_STATE] + [step["to_state"] for step in history])
        print(f"Transition Path : {path}")
        print(f"Final State     : {final_state}")
        print(f"Accepting States: {sorted(list(ACCEPTING_STATES))}")
        status_text = "ACCEPTED" if is_accepted else "REJECTED"
        print(f"Final Result    : {status_text}")
        print("=" * 55 + "\n")

    return is_accepted, history, final_state


def is_valid_library_card(card_id: str) -> bool:
    """Convenience helper that returns True if the library card ID is accepted.

    Args:
        card_id: The string to test.

    Returns:
        True if the card ID is accepted by the DFA, False otherwise.
    """
    accepted, _, _ = validate_library_card(card_id, verbose=False)
    return accepted
