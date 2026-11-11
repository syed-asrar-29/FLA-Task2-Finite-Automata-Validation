# Designing Automata for Real-Time Applications
### A Case Study of Three Finite-Automata Validation Systems
**Course:** Formal Language and Automata (FLA) — Academic Task 2 Report Implementation

---

## 1. Project Overview

This project implements three **Deterministic Finite Automata (DFA)** validators using Python 3. Deterministic finite automata provide exact, mathematical models of computation characterized by:
- $O(n)$ deterministic linear runtime (processing each token or symbol exactly once),
- $O(1)$ constant memory overhead,
- Zero backtracking or recursion.

These characteristics make finite automata the industry standard for mission-critical, real-time systems such as lexical analyzers, protocol checkers, hardware controllers, and telemetric stream filters.

The project strictly implements step-by-step state transition logic, rejecting regular expression shortcuts in favor of pure automata execution.

---

## 2. Project Objectives

1. Model real-world validation problems into formal Deterministic Finite Automata (DFAs).
2. Implement symbol-by-symbol / token-by-token DFA transition functions in beginner-friendly, clean Python.
3. Trace and visualize state transitions dynamically during evaluation.
4. Verify behavioral correctness using comprehensive automated unit testing with `pytest`.
5. Provide visual state diagrams for all three automata showing initial states, transitions, accepting states (double circles), and rejecting sink states.

---

## 3. Technologies Used

- **Language:** Python 3 (Python 3.10+)
- **Testing Framework:** `pytest` (automated testing across 57 test scenarios)
- **Visualization:** `matplotlib` (diagram and academic PDF generation)
- **Architecture:** Modular Python package (`automata/`) with an interactive CLI (`main.py`)

---

## 4. The Three Applications

### Application 1: Library Card ID Validation

- **File:** [`automata/library_card.py`](automata/library_card.py)
- **Purpose:** Validate library card identification strings adhering to the lexical pattern of uppercase `'L'` followed by exactly two digits (`0`–`9`).
- **Lexical Rules:**
  1. The first character must strictly be `'L'`.
  2. The second and third characters must be decimal digits (`0`–`9`).
  3. The identifier must be exactly three characters in length.
  4. Lowercase letters (`'l'`), non-digits, extra trailing characters, and special characters must transition to the dead/reject state.

#### Formal 5-Tuple Definition:
$$M_1 = (Q, \Sigma, \delta, q_0, F)$$
- $Q = \{q_0, q_1, q_2, q_3, q_D\}$
- $\Sigma = \{ 'L', '0'\text{--}'9', \text{other} \}$
- $q_0 = \text{Initial State}$
- $F = \{q_3\}$ (Accepting State)

#### States Description:
| State | Type | Description |
|---|---|---|
| `q0` | Initial | Initial state; awaiting uppercase `'L'`. |
| `q1` | Intermediate | `'L'` received; awaiting first digit (`0`–`9`). |
| `q2` | Intermediate | First digit received; awaiting second digit (`0`–`9`). |
| `q3` | **Accepting** | Exactly two digits received after `'L'`; valid card ID. |
| `qD` | Dead / Sink | Invalid character received or length exceeded. Non-recoverable. |

#### State Transition Table:
| Current State | Input: `'L'` | Input: `'0'`–`'9'` | Input: Other / Extra |
|---|---|---|---|
| `q0` | `q1` | `qD` | `qD` |
| `q1` | `qD` | `q2` | `qD` |
| `q2` | `qD` | `q3` | `qD` |
| `q3` | `qD` | `qD` | `qD` |
| `qD` | `qD` | `qD` | `qD` |

#### State Diagram:
![Library Card DFA](diagrams/library_card_dfa.png)

---

### Application 2: Machine Command Validation

- **File:** [`automata/machine_command.py`](automata/machine_command.py)
- **Purpose:** Validate streams of operational commands dispatched to an automated machine controller.
- **Protocol Rules:**
  1. Only `GO` and `STOP` command tokens are accepted.
  2. At least one command must be present (the empty sequence is rejected).
  3. Commands can appear in any order and any frequency.
  4. Any unknown, misspelled, or lowercase token (e.g. `START`, `PAUSE`, `go`) immediately transitions to the dead/reject state.

#### Formal 5-Tuple Definition:
$$M_2 = (Q, \Sigma, \delta, q_0, F)$$
- $Q = \{q_0, q_A, q_D\}$
- $\Sigma = \{ \text{"GO"}, \text{"STOP"}, \langle\text{OTHER}\rangle \}$
- $q_0 = \text{Initial State}$
- $F = \{q_A\}$ (Accepting State)

#### States Description:
| State | Type | Description |
|---|---|---|
| `q0` | Initial | Initial state; no commands received yet. |
| `qA` | **Accepting** | At least one valid command (`GO` or `STOP`) received. |
| `qD` | Dead / Sink | Invalid, unknown, or lowercase token encountered. Non-recoverable. |

#### State Transition Table:
| Current State | Token: `"GO"` | Token: `"STOP"` | Token: Other / Invalid |
|---|---|---|---|
| `q0` | `qA` | `qA` | `qD` |
| `qA` | `qA` | `qA` | `qD` |
| `qD` | `qD` | `qD` | `qD` |

#### State Diagram:
![Machine Command DFA](diagrams/machine_command_dfa.png)

---

### Application 3: Binary Sensor Alert Validation

- **File:** [`automata/binary_sensor.py`](automata/binary_sensor.py)
- **Purpose:** Monitor a binary sensor telemetry bitstream and trigger an alert condition whenever the stream ends with two consecutive ones (`11`).
- **Telemetry Rules:**
  1. Alphabet consists strictly of binary symbols `0` and `1`.
  2. The sequence must end with `11` to be accepted.
  3. Any binary prefix before the trailing `11` is permitted.
  4. Any non-binary character (e.g. `'A'`, `'2'`, `'#'`) transitions to the dead/reject state.
  5. The empty string is rejected because it does not end with `11`.

#### Formal 5-Tuple Definition:
$$M_3 = (Q, \Sigma, \delta, q_0, F)$$
- $Q = \{q_0, q_1, q_2, q_D\}$
- $\Sigma = \{ '0', '1', \langle\text{OTHER}\rangle \}$
- $q_0 = \text{Initial State}$
- $F = \{q_2\}$ (Accepting / Alert State)

#### States Description:
| State | Type | Description |
|---|---|---|
| `q0` | Initial | No trailing `'1'` (either stream start or last bit was `'0'`). |
| `q1` | Intermediate | Exactly one trailing `'1'` received. |
| `q2` | **Accepting** | Sequence ends with two consecutive ones (`11`). Alert triggered. |
| `qD` | Dead / Sink | Non-binary character encountered. Non-recoverable. |

#### State Transition Table:
| Current State | Input: `'0'` | Input: `'1'` | Input: Non-binary symbol |
|---|---|---|---|
| `q0` | `q0` | `q1` | `qD` |
| `q1` | `q0` | `q2` | `qD` |
| `q2` | `q0` | `q2` | `qD` |
| `qD` | `qD` | `qD` | `qD` |

#### State Diagram:
![Binary Sensor DFA](diagrams/binary_sensor_dfa.png)

---

## 5. Sample Inputs and Execution Outputs

### Application 1: Library Card ID
- **Accepted Cases:**
  - `L04` $\rightarrow q_0 \xrightarrow{L} q_1 \xrightarrow{0} q_2 \xrightarrow{4} q_3$ **[ACCEPTED]**
  - `L27` $\rightarrow q_0 \xrightarrow{L} q_1 \xrightarrow{2} q_2 \xrightarrow{7} q_3$ **[ACCEPTED]**
  - `L90`, `L00`, `L58` **[ACCEPTED]**
- **Rejected Cases:**
  - `04` (missing prefix `'L'`) $\rightarrow q_0 \xrightarrow{0} q_D$ **[REJECTED]**
  - `l27` (lowercase `'l'`) $\rightarrow q_0 \xrightarrow{l} q_D$ **[REJECTED]**
  - `L2` (length $< 3$, ends at $q_2 \notin F$) **[REJECTED]**
  - `L275` (length $> 3$, $q_3 \xrightarrow{5} q_D$) **[REJECTED]**
  - `LA7` (letter in digit slot, $q_1 \xrightarrow{A} q_D$) **[REJECTED]**
  - `L-7` (symbol in digit slot, $q_1 \xrightarrow{-} q_D$) **[REJECTED]**

### Application 2: Machine Command Sequence
- **Accepted Cases:**
  - `[GO]` $\rightarrow q_0 \xrightarrow{\text{GO}} q_A$ **[ACCEPTED]**
  - `[STOP]` $\rightarrow q_0 \xrightarrow{\text{STOP}} q_A$ **[ACCEPTED]**
  - `[GO, STOP]` $\rightarrow q_0 \xrightarrow{\text{GO}} q_A \xrightarrow{\text{STOP}} q_A$ **[ACCEPTED]**
  - `[STOP, GO]`, `[GO, GO, STOP]` **[ACCEPTED]**
- **Rejected Cases:**
  - `[]` (empty sequence, remains in $q_0 \notin F$) **[REJECTED]**
  - `[START]` $\rightarrow q_0 \xrightarrow{\text{START}} q_D$ **[REJECTED]**
  - `[GO, PAUSE]` $\rightarrow q_0 \xrightarrow{\text{GO}} q_A \xrightarrow{\text{PAUSE}} q_D$ **[REJECTED]**
  - `[STO]`, `[GO, HALT, STOP]`, `[go]` **[REJECTED]**

### Application 3: Binary Sensor Alert
- **Accepted Cases:**
  - `11` $\rightarrow q_0 \xrightarrow{1} q_1 \xrightarrow{1} q_2$ **[ACCEPTED]**
  - `011` $\rightarrow q_0 \xrightarrow{0} q_0 \xrightarrow{1} q_1 \xrightarrow{1} q_2$ **[ACCEPTED]**
  - `1011` $\rightarrow q_0 \xrightarrow{1} q_1 \xrightarrow{0} q_0 \xrightarrow{1} q_1 \xrightarrow{1} q_2$ **[ACCEPTED]**
  - `00011`, `111` ($q_2 \xrightarrow{1} q_2$) **[ACCEPTED]**
- **Rejected Cases:**
  - `""` (empty string, ends at $q_0 \notin F$) **[REJECTED]**
  - `1` (ends at $q_1 \notin F$) **[REJECTED]**
  - `10` (ends at $q_0 \notin F$) **[REJECTED]**
  - `110` ($q_2 \xrightarrow{0} q_0 \notin F$) **[REJECTED]**
  - `1010` (ends at $q_0 \notin F$) **[REJECTED]**
  - `11A` ($q_2 \xrightarrow{A} q_D$) **[REJECTED]**

---

## 6. Project Directory Structure

```
FLA-Task2-Finite-Automata-Validation/
│
├── README.md                     # Comprehensive project documentation
├── requirements.txt              # Project dependencies (pytest, matplotlib)
├── main.py                       # Interactive CLI menu application
├── generate_diagrams.py          # Generator for DFA state diagrams
├── generate_report_pdf.py        # Generator for academic Task 2 PDF report
│
├── automata/                     # Modular DFA engine implementations
│   ├── __init__.py               # Automata package exports
│   ├── library_card.py           # Application 1: Library card ID DFA
│   ├── machine_command.py        # Application 2: Machine command DFA
│   └── binary_sensor.py          # Application 3: Binary sensor alert DFA
│
├── diagrams/                     # High-resolution generated DFA diagrams
│   ├── library_card_dfa.png      # State diagram for Library Card DFA
│   ├── machine_command_dfa.png   # State diagram for Machine Command DFA
│   └── binary_sensor_dfa.png     # State diagram for Binary Sensor DFA
│
├── tests/                        # Automated unit tests using pytest
│   ├── __init__.py
│   ├── test_library_card.py      # Tests for Application 1
│   ├── test_machine_command.py   # Tests for Application 2
│   └── test_binary_sensor.py     # Tests for Application 3
│
└── docs/
    └── Task2_Report.pdf          # Full academic report PDF
```

---

## 7. Installation and Setup

### Prerequisites
- Python 3.8 or higher installed on your system.

### Step 1: Clone or Navigate to the Repository
```bash
git clone https://github.com/your-username/FLA-Task2-Finite-Automata-Validation.git
cd FLA-Task2-Finite-Automata-Validation
```

### Step 2: (Optional) Create a Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

---

## 8. How to Run the Project

Launch the interactive CLI menu:
```bash
python main.py
```

### Example Menu Interface:
```
========================================
FINITE AUTOMATA VALIDATION SYSTEM
========================================
1. Library Card ID Validation
2. Machine Command Validation
3. Binary Sensor Alert Validation
4. Exit
========================================
Enter your choice (1-4): 1

--- Application 1: Library Card ID Validation ---
Rule: Must start with uppercase 'L' followed by exactly two digits (e.g. L04, L27).
Enter Library Card ID (or press Enter for empty): L27

=======================================================
  DFA VALIDATION: Library Card ID
=======================================================
Input String : 'L27'
Initial State: q0
-------------------------------------------------------
State Transitions:
  [Step 1] State 'q0' --( 'L' )--> State 'q1'
  [Step 2] State 'q1' --( '2' )--> State 'q2'
  [Step 3] State 'q2' --( '7' )--> State 'q3'
-------------------------------------------------------
Transition Path : q0 -> q1 -> q2 -> q3
Final State     : q3
Accepting States: ['q3']
Final Result    : ACCEPTED
=======================================================
```

---

## 9. How to Execute Tests

Run the full automated test suite using `pytest`:

```bash
# Run all tests with verbose output
python -m pytest -v

# Run tests for a specific validator
python -m pytest tests/test_library_card.py -v
python -m pytest tests/test_machine_command.py -v
python -m pytest tests/test_binary_sensor.py -v
```

All 57 test cases pass with 100% test coverage across both valid and invalid inputs.

---

## 10. Regenerating Diagrams and PDF Report

If you modify states or styling, regenerate the diagrams and academic report with:

```bash
# Regenerate DFA PNG diagrams
python generate_diagrams.py

# Regenerate Task2_Report.pdf in docs/
python generate_report_pdf.py
```

---

## 11. Academic Conclusion

By formalizing string and token validation through Deterministic Finite Automata, this project demonstrates:
1. **Mathematical Rigor:** Clear equivalence between regular languages, state-transition tables, and software automata.
2. **Deterministic Predictability:** Every input symbol maps to exactly one state transition, eliminating catastrophic backtracking.
3. **Robust Sink Handling:** Trapping invalid transitions into state `qD` guarantees that corrupted or malicious sequences are immediately quarantined.
