"""Application 2: Machine Command Validation DFA.

Purpose:
    Validate sequences of machine commands using only the tokens 'GO' and 'STOP'.

Formal Definition (5-tuple DFA):
    M = (Q, Sigma, delta, q0, F)
    - Q: Set of states {q0, qA, qD}
    - Sigma: Alphabet of command tokens {GO, STOP, <OTHER>}
    - delta: State transition function Q x Sigma -> Q
    - q0: Initial state (no commands processed yet)
    - F: Set of accepting states {qA}

Rules:
    1. Only 'GO' and 'STOP' tokens are permitted.
    2. At least one command token must be present (non-empty sequence).
    3. Any number of valid commands can appear in any sequence.
    4. Unknown or incomplete tokens (e.g. 'START', 'PAUSE', 'STO', 'go') must be rejected.
    5. Tokens are case-sensitive (uppercase required).

States:
    q0 : Initial state (waiting for the first command)
    qA : Accepting state (at least one valid command received)
    qD : Dead / rejecting sink state (invalid or unknown token encountered)
"""

from typing import Tuple, List, Dict, Any, Union


# Define DFA states
STATES = {"q0", "qA", "qD"}
INITIAL_STATE = "q0"
ACCEPTING_STATES = {"qA"}
VALID_TOKENS = {"GO", "STOP"}


def transition(current_state: str, token: str) -> str:
    """Computes the next state in the Machine Command DFA given the current state and token.

    Args:
        current_state: The current state ('q0', 'qA', or 'qD').
        token: The command token being processed.

    Returns:
        The next state according to the DFA transition function.
    """
    if current_state == "q0":
        # From start: receiving a valid token moves to accepting state qA
        if token in VALID_TOKENS:
            return "qA"
        return "qD"

    elif current_state == "qA":
        # From qA: another valid token keeps the DFA in accepting state qA
        if token in VALID_TOKENS:
            return "qA"
        return "qD"

    elif current_state == "qD":
        # Trap / dead state: remains in qD for all subsequent tokens
        return "qD"

    return "qD"


def _normalize_input(commands: Union[str, List[str]]) -> List[str]:
    """Helper to convert input (string of space-separated tokens or list) to a list of tokens."""
    if isinstance(commands, str):
        # Split by whitespace into individual tokens
        trimmed = commands.strip()
        return trimmed.split() if trimmed else []
    elif isinstance(commands, (list, tuple)):
        return [str(token) for token in commands]
    return []


def validate_machine_commands(
    commands: Union[str, List[str]],
    verbose: bool = True
) -> Tuple[bool, List[Dict[str, Any]], str]:
    """Validates a sequence of machine commands token-by-token using the DFA.

    Args:
        commands: A space-separated string (e.g. "GO STOP") or list of tokens (e.g. ['GO', 'STOP']).
        verbose: Whether to print step-by-step transition details.

    Returns:
        A tuple of:
            - is_accepted (bool): True if accepted by the DFA, False otherwise.
            - history (list of dicts): Step-by-step transition history.
            - final_state (str): The state reached after consuming all tokens.
    """
    token_list = _normalize_input(commands)
    current_state = INITIAL_STATE
    history: List[Dict[str, Any]] = []

    if verbose:
        print("\n" + "=" * 55)
        print("  DFA VALIDATION: Machine Command Sequence")
        print("=" * 55)
        print(f"Input Tokens : {token_list}")
        print(f"Initial State: {current_state}")
        print("-" * 55)
        print("State Transitions:")

    if not token_list and verbose:
        print("  (Empty sequence - rule requires at least one command)")

    for index, token in enumerate(token_list, start=1):
        prev_state = current_state
        current_state = transition(current_state, token)
        step_info = {
            "step": index,
            "from_state": prev_state,
            "token": token,
            "to_state": current_state,
        }
        history.append(step_info)

        if verbose:
            print(f"  [Step {index}] State '{prev_state}' --( [{token}] )--> State '{current_state}'")

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


def is_valid_machine_commands(commands: Union[str, List[str]]) -> bool:
    """Convenience helper that returns True if the machine command sequence is accepted.

    Args:
        commands: A space-separated string or list of tokens.

    Returns:
        True if the sequence is accepted by the DFA, False otherwise.
    """
    accepted, _, _ = validate_machine_commands(commands, verbose=False)
    return accepted
