# Chinese Remainder Theorem (CRT) Explorer

A Python + Streamlit project that solves systems of congruences using the Chinese Remainder Theorem, with a clear explanation and a step-by-step combination trace.

## Mathematical Concept

The Chinese Remainder Theorem is used to solve systems such as:

- x ≡ a1 (mod n1)
- x ≡ a2 (mod n2)
- x ≡ a3 (mod n3)

The solver combines congruences one pair at a time:

- Start with the first congruence
- Merge it with the next congruence into one equivalent congruence
- Continue until only one congruence remains
- If a gcd compatibility check fails at any stage, the system has no solution

This approach works for both pairwise coprime moduli and many non-coprime compatible systems.

## Features

- Solves one or more congruences
- Supports negative remainders by normalizing them
- Rejects zero moduli
- Detects inconsistent systems with no integer solution
- Shows every pairwise combination step in a readable table
- Includes a worked example for learning

## Project Structure

- app.py: Streamlit UI
- src/crt.py: CRT solver and trace logic
- tests/test_crt.py: Unit tests
- requirements.txt: Dependencies

## Run Locally

One-click on Windows:

- Double-click run_app.bat in the project folder.

1. Create and activate a virtual environment (recommended).
2. Install dependencies:
   python -m pip install -r requirements.txt
3. Start the app:
   python -m streamlit run app.py
4. Run tests:
   python -m pytest -q

## Example

For the system:

- x ≡ 2 (mod 3)
- x ≡ 3 (mod 5)
- x ≡ 2 (mod 7)

The smallest non-negative solution is:

- x = 23 (mod 105)
