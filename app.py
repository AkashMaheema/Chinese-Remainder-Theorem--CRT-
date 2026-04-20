import streamlit as st

from src.crt import Congruence, solve_crt_with_trace

st.set_page_config(
    page_title="Chinese Remainder Theorem Explorer",
    page_icon="C",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top right, rgba(214, 114, 57, 0.12) 0%, transparent 34%),
            radial-gradient(circle at bottom left, rgba(46, 114, 89, 0.10) 0%, transparent 28%),
            var(--background-color);
        color: var(--text-color);
    }
    .panel {
        border: 1px solid rgba(127, 127, 127, 0.28);
        border-radius: 18px;
        padding: 1.2rem;
        background: var(--secondary-background-color);
        color: var(--text-color);
        box-shadow: 0 14px 30px rgba(0, 0, 0, 0.10);
    }
    .panel p,
    .panel li,
    .panel h1,
    .panel h2,
    .panel h3,
    .panel h4,
    .panel h5,
    .panel h6 {
        color: inherit;
    }
    .soft-label {
        font-size: 0.82rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        opacity: 0.7;
        margin-bottom: 0.35rem;
    }
    .equation-row {
        border: 1px solid rgba(127, 127, 127, 0.18);
        border-radius: 14px;
        padding: 0.6rem 0.8rem;
        background: rgba(255, 255, 255, 0.03);
        margin-bottom: 0.6rem;
    }
    .result-card {
        border-radius: 16px;
        padding: 1rem 1.1rem;
        margin-top: 1rem;
        background: linear-gradient(135deg, rgba(214, 114, 57, 0.14), rgba(46, 114, 89, 0.10));
        border: 1px solid rgba(214, 114, 57, 0.22);
    }
    .result-main {
        font-size: 1.2rem;
        font-weight: 700;
        margin: 0.2rem 0;
    }
    .result-sub {
        opacity: 0.82;
        margin: 0;
    }
    .step-shell {
        border: 1px solid rgba(127, 127, 127, 0.22);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        background: rgba(255, 255, 255, 0.03);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Chinese Remainder Theorem Explorer")
st.caption("Solve systems of congruences and see how each pair is combined.")

DEFAULT_REMAINDERS = [2, 3, 2, 1, 4, 5]
DEFAULT_MODULI = [3, 5, 7, 4, 9, 11]


def initialize_default_example() -> None:
    st.session_state.congruence_count = 3

    for index in range(3):
        st.session_state[f"remainder_{index}"] = str(DEFAULT_REMAINDERS[index])
        st.session_state[f"modulus_{index}"] = str(DEFAULT_MODULI[index])


def ensure_congruence_state(target_count: int) -> None:
    st.session_state.congruence_count = max(1, min(6, int(target_count)))

    for index in range(st.session_state.congruence_count):
        remainder_key = f"remainder_{index}"
        modulus_key = f"modulus_{index}"

        if remainder_key not in st.session_state:
            st.session_state[remainder_key] = str(DEFAULT_REMAINDERS[index])
        if modulus_key not in st.session_state:
            st.session_state[modulus_key] = str(DEFAULT_MODULI[index])


def parse_integer_input(value: str, label: str) -> int:
    try:
        return int(str(value).strip())
    except ValueError as exc:
        raise ValueError(f"{label} must be an integer") from exc


if "initialized_default_example" not in st.session_state:
    initialize_default_example()
    st.session_state.initialized_default_example = True

ensure_congruence_state(st.session_state.congruence_count)

left, right = st.columns([1.25, 0.95], gap="large")

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Understand the Mathematical Concept")
    st.markdown(
        """
The Chinese Remainder Theorem solves equations of the form:

- x ≡ a1 (mod n1)
- x ≡ a2 (mod n2)
- x ≡ a3 (mod n3)

Key idea:
- Combine two congruences into one equivalent congruence.
- Repeat until only one congruence remains.
- If a compatibility condition fails, the whole system has no solution.

When two congruences are compatible, their combined modulus is the least common multiple
of the two moduli.
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel" style="margin-top: 1rem;">', unsafe_allow_html=True)
    st.subheader("Try It")
    st.write("Build the system inline. Every change updates the solution immediately.")

    count_label, minus_col, count_col, plus_col = st.columns([2.2, 0.7, 1.1, 0.7])
    with count_label:
        st.markdown("<div class='soft-label'>Number of congruences</div>", unsafe_allow_html=True)
    with minus_col:
        if st.button("-", use_container_width=True, disabled=st.session_state.congruence_count <= 1):
            ensure_congruence_state(st.session_state.congruence_count - 1)
            st.rerun()
    with count_col:
        st.markdown(
            f"<div style='text-align:center; padding-top:0.35rem; font-weight:600;'>{st.session_state.congruence_count}</div>",
            unsafe_allow_html=True,
        )
    with plus_col:
        if st.button("+", use_container_width=True, disabled=st.session_state.congruence_count >= 6):
            ensure_congruence_state(st.session_state.congruence_count + 1)
            st.rerun()

    for index in range(st.session_state.congruence_count):
        st.markdown("<div class='equation-row'>", unsafe_allow_html=True)
        row = st.columns([0.9, 1.1, 0.5, 1.1, 0.2], vertical_alignment="center")
        with row[0]:
            st.markdown("**x ≡**")
        with row[1]:
            st.text_input(
                f"Remainder {index + 1}",
                key=f"remainder_{index}",
                label_visibility="collapsed",
            )
        with row[2]:
            st.markdown("**(mod**")
        with row[3]:
            st.text_input(
                f"Modulus {index + 1}",
                key=f"modulus_{index}",
                label_visibility="collapsed",
            )
        with row[4]:
            st.markdown("**)**")
        st.markdown("</div>", unsafe_allow_html=True)

    congruences: list[Congruence] = []
    solution = None
    modulus = None
    steps: list[dict[str, int | bool | str]] = []
    solve_error: str | None = None

    try:
        for index in range(st.session_state.congruence_count):
            remainder = parse_integer_input(
                st.session_state[f"remainder_{index}"],
                f"Remainder {index + 1}",
            )
            current_modulus = parse_integer_input(
                st.session_state[f"modulus_{index}"],
                f"Modulus {index + 1}",
            )
            congruences.append(Congruence(remainder, current_modulus))

        solution, modulus, steps = solve_crt_with_trace(congruences)
    except (TypeError, ValueError) as exc:
        solve_error = str(exc)

    if solve_error:
        st.error(solve_error)
    else:
        metric_left, metric_right = st.columns(2)
        metric_left.metric("Smallest solution", f"x = {solution} (mod {modulus})")
        metric_right.metric("General form", f"x = {solution} + {modulus}k")

        st.markdown(
            f"""
            <div class="result-card">
                <div class="soft-label">Live result</div>
                <p class="result-main">Smallest non-negative solution: x = {solution} (mod {modulus})</p>
                <p class="result-sub">All solutions are given by x = {solution} + {modulus}k, where k is any integer.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Worked Example")
    sample = [Congruence(2, 3), Congruence(3, 5), Congruence(2, 7)]
    sample_solution, sample_modulus, sample_steps = solve_crt_with_trace(sample)

    st.write("A classic CRT example that resolves to 23 modulo 105.")
    st.markdown(
        """
- x ≡ 2 (mod 3)
- x ≡ 3 (mod 5)
- x ≡ 2 (mod 7)
        """
    )
    st.markdown(
        f"""
        <div class="result-card">
            <div class="soft-label">Worked answer</div>
            <p class="result-main">x = {sample_solution} (mod {sample_modulus})</p>
            <p class="result-sub">Equivalent integer family: x = {sample_solution} + {sample_modulus}k</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
Takeaway:
- CRT reduces many congruences to one final congruence.
- Compatibility matters when moduli are not coprime.
- The final answer describes all integer solutions.
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="panel" style="margin-top: 1rem;">', unsafe_allow_html=True)
st.subheader("Combination Steps")

if solve_error:
    st.info("Enter a valid compatible system to see the full-width combination trace.")
elif steps:
    st.markdown('<div class="step-shell">', unsafe_allow_html=True)
    st.dataframe(steps, width="stretch", hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Only one congruence was provided, so no pairwise combination was needed.")

st.markdown("</div>", unsafe_allow_html=True)
