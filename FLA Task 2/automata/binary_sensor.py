"""Application 3: Binary Sensor Alert Validation DFA.

Purpose:
    Detect whether a binary sensor data sequence ends with two consecutive ones ('11').

Formal Definition (5-tuple DFA):
    M = (Q, Sigma, delta, q0, F)
    - Q: Set of states {q0, q1, q2, qD}
    - Sigma: Alphabet {'0', '1', <OTHER>}
    - delta: State transition function Q x Sigma -> Q
    - q0: Initial state (no trailing 1)
    - F: Set of accepting states {q2}

Rules:
    1. Alphabet contains only '0' and '1'.
    2. Input must end with '11'.
    3. Any binary prefix is permitted before the final '11'.
    4. Any non-binary character triggers a transition to the dead state qD.
    5. An empty string is rejected because it does not end with '11'.

States:
    q0 : Initial state / no trailing '1' (last symbol was '0' or start)
    q1 : Exactly one trailing '1'
    q2 : Last two symbols are '11' (accepting state; alert condition met)
    qD : Dead / rejecting sink state (encountered non-binary symbol)
"""

from typing import Tuple, List, Dict, Any


# Define DFA states
STATES = {"q0", "q1", "q2", "qD"}
INITIAL_STATE = "q0"
ACCEPTING_STATES = {"q2"}
VALID_ALPHABET = {"0", "1"}


def transition(current_state: str, symbol: str) -> str:
    """Computes the next state in the Binary Sensor DFA given the current state and symbol.

    Args:
        current_state: The current state ('q0', 'q1', 'q2', or 'qD').
        symbol: The character being processed ('0', '1', or invalid symbol).

    Returns:
        The next state according to the DFA transition function.
    """
    if current_state == "q0":
        # At q0: no trailing '1'
        if symbol == "0":
            return "q0"
        elif symbol == "1":
            return "q1"
        return "qD"

    elif current_state == "q1":
        # At q1: exactly one trailing '1'
        if symbol == "0":
            return "q0"
        elif symbol == "1":
            return "q2"  # Two consecutive ones reached!
        return "qD"

    elif current_state == "q2":
        # At q2: last two symbols were '11'
        if symbol == "0":
            return "q0"
        elif symbol == "1":
            return "q2"  # Sequence still ends with two ones (e.g. "...111")
        return "qD"

    elif current_state == "qD":
        # Trap / dead state: remains in qD on any symbol
        return "qD"

    return "qD"


def validate_binary_sensor(
    binary_str: str,
    verbose: bool = True
) -> Tuple[bool, List[Dict[str, Any]], str]:
    """Validates a binary stream symbol-by-symbol using the DFA.

    Args:
        binary_str: The binary sequence string to test.
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
        print("  DFA VALIDATION: Binary Sensor Alert (ends with '11')")
        print("=" * 55)
        print(f"Input Stream : '{binary_str}'")
        print(f"Initial State: {current_state}")
        print("-" * 55)
        print("State Transitions:")

    if not binary_str and verbose:
        print("  (Empty string - cannot end with '11')")

    for index, symbol in enumerate(binary_str, start=1):
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
        status_text = "ACCEPTED (Alert Condition Detected)" if is_accepted else "REJECTED (No Alert)"
        print(f"Final Result    : {status_text}")
        print("=" * 55 + "\n")

    return is_accepted, history, final_state


def is_valid_binary_sensor(binary_str: str) -> bool:
    """Convenience helper that returns True if the binary sequence ends with '11'.

    Args:
        binary_str: The binary sequence string.

    Returns:
        True if the sequence is accepted by the DFA, False otherwise.
    """
    accepted, _, _ = validate_binary_sensor(binary_str, verbose=False)
    return accepted
