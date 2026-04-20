from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Congruence:
    remainder: int
    modulus: int


def _validate_integer(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    return value


def _validate_modulus(modulus: int, name: str) -> int:
    normalized = abs(_validate_integer(modulus, name))
    if normalized == 0:
        raise ValueError(f"{name} must be non-zero")
    return normalized


def normalize_congruence(remainder: int, modulus: int) -> Congruence:
    normalized_modulus = _validate_modulus(modulus, "modulus")
    normalized_remainder = _validate_integer(remainder, "remainder") % normalized_modulus
    return Congruence(normalized_remainder, normalized_modulus)


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    x = _validate_integer(a, "a")
    y = _validate_integer(b, "b")

    if y == 0:
        return abs(x), 1 if x >= 0 else -1, 0

    gcd_value, s1, t1 = extended_gcd(y, x % y)
    s = t1
    t = s1 - (x // y) * t1
    return gcd_value, s, t


def combine_congruences(
    first: Congruence,
    second: Congruence,
) -> tuple[Congruence | None, dict[str, int | bool | str]]:
    a1 = first.remainder % first.modulus
    n1 = first.modulus
    a2 = second.remainder % second.modulus
    n2 = second.modulus

    gcd_value, coefficient, _ = extended_gcd(n1, n2)
    difference = a2 - a1

    step: dict[str, int | bool | str] = {
        "Current Remainder": a1,
        "Current Modulus": n1,
        "Next Remainder": a2,
        "Next Modulus": n2,
        "GCD": gcd_value,
        "Difference": difference,
    }

    if difference % gcd_value != 0:
        step["Compatible"] = False
        step["Explanation"] = (
            f"Because gcd({n1}, {n2}) = {gcd_value} does not divide {difference}, "
            "the system has no solution."
        )
        return None, step

    reduced_difference = difference // gcd_value
    reduced_modulus = n2 // gcd_value
    multiplier = (reduced_difference * coefficient) % reduced_modulus
    combined_modulus = n1 // gcd_value * n2
    solution = (a1 + n1 * multiplier) % combined_modulus

    step["Compatible"] = True
    step["Multiplier"] = multiplier
    step["Combined Modulus"] = combined_modulus
    step["Combined Remainder"] = solution
    step["Explanation"] = (
        f"Since {gcd_value} divides {difference}, combine the congruences into "
        f"x ≡ {solution} (mod {combined_modulus})."
    )

    return Congruence(solution, combined_modulus), step


def solve_crt(congruences: list[Congruence]) -> tuple[int, int]:
    solution, modulus, _ = solve_crt_with_trace(congruences)
    return solution, modulus


def solve_crt_with_trace(
    congruences: list[Congruence],
) -> tuple[int, int, list[dict[str, int | bool | str]]]:
    if not congruences:
        raise ValueError("At least one congruence is required")

    normalized = [
        normalize_congruence(congruence.remainder, congruence.modulus)
        for congruence in congruences
    ]

    current = normalized[0]
    steps: list[dict[str, int | bool | str]] = []

    for next_congruence in normalized[1:]:
        combined, step = combine_congruences(current, next_congruence)
        steps.append(step)
        if combined is None:
            raise ValueError(step["Explanation"])
        current = combined

    return current.remainder, current.modulus, steps
