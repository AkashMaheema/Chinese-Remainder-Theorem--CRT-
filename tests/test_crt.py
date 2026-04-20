import pytest

from src.crt import Congruence, combine_congruences, extended_gcd, solve_crt, solve_crt_with_trace


def test_extended_gcd_returns_bezout_identity():
    gcd_value, s, t = extended_gcd(30, 18)
    assert gcd_value == 6
    assert 30 * s + 18 * t == gcd_value


def test_solve_crt_for_pairwise_coprime_moduli():
    solution, modulus = solve_crt(
        [Congruence(2, 3), Congruence(3, 5), Congruence(2, 7)]
    )

    assert solution == 23
    assert modulus == 105


def test_solve_crt_for_non_coprime_but_compatible_moduli():
    solution, modulus = solve_crt(
        [Congruence(1, 4), Congruence(3, 6)]
    )

    assert solution == 9
    assert modulus == 12


def test_solve_crt_rejects_inconsistent_system():
    with pytest.raises(ValueError):
        solve_crt([Congruence(1, 2), Congruence(2, 4)])


def test_solve_crt_normalizes_negative_remainders():
    solution, modulus = solve_crt(
        [Congruence(-1, 5), Congruence(3, 7)]
    )

    assert modulus == 35
    assert solution % 5 == 4
    assert solution % 7 == 3


def test_solve_crt_rejects_empty_input():
    with pytest.raises(ValueError):
        solve_crt([])


def test_combine_congruences_returns_trace_data():
    combined, step = combine_congruences(Congruence(2, 3), Congruence(3, 5))

    assert combined == Congruence(8, 15)
    assert step["Compatible"] is True
    assert step["Combined Remainder"] == 8
    assert step["Combined Modulus"] == 15


def test_trace_rows_match_final_solution():
    solution, modulus, steps = solve_crt_with_trace(
        [Congruence(2, 3), Congruence(3, 5), Congruence(2, 7)]
    )

    assert solution == 23
    assert modulus == 105
    assert len(steps) == 2
    assert steps[-1]["Combined Remainder"] == 23
    assert steps[-1]["Combined Modulus"] == 105
