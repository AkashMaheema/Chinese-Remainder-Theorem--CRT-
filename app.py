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
            var(--background-color);
        color: var(--text-color);
    }
    .panel {
        border: 1px solid rgba(127, 127, 127, 0.28);
        border-radius: 14px;
        padding: 1.1rem;
        background: var(--secondary-background-color);
        color: var(--text-color);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.10);
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
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Chinese Remainder Theorem Explorer")
st.caption("Solve systems of congruences and see how each pair is combined.")

left, right = st.columns([1.2, 1], gap="large")

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
    st.write("Enter remainder and modulus for each congruence.")

    with st.form("crt-form"):
        count = st.number_input("Number of congruences", min_value=1, max_value=6, value=3, step=1)
        congruences: list[Congruence] = []

        for index in range(int(count)):
            col_a, col_n = st.columns(2)
            with col_a:
                remainder = st.number_input(
                    f"Remainder a{index + 1}",
                    value=[2, 3, 2, 1, 4, 5][index],
                    step=1,
                    format="%d",
                    key=f"remainder_{index}",
                )
            with col_n:
                modulus = st.number_input(
                    f"Modulus n{index + 1}",
                    value=[3, 5, 7, 4, 9, 11][index],
                    step=1,
                    format="%d",
                    key=f"modulus_{index}",
                )
            congruences.append(Congruence(int(remainder), int(modulus)))

        submitted = st.form_submit_button("Solve System")

    if submitted:
        try:
            solution, modulus, steps = solve_crt_with_trace(congruences)
            st.success(f"Smallest non-negative solution: x = {solution} (mod {modulus})")
            st.info(f"General solution: x = {solution} + {modulus}k, where k is any integer.")

            if steps:
                st.markdown("### Combination Steps")
                st.dataframe(steps, width="stretch", hide_index=True)
            else:
                st.info("Only one congruence was provided, so no pairwise combination was needed.")

        except (TypeError, ValueError) as exc:
            st.error(str(exc))

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Worked Example")
    sample = [Congruence(2, 3), Congruence(3, 5), Congruence(2, 7)]
    sample_solution, sample_modulus, sample_steps = solve_crt_with_trace(sample)

    st.write("Example system:")
    st.markdown(
        """
- x ≡ 2 (mod 3)
- x ≡ 3 (mod 5)
- x ≡ 2 (mod 7)
        """
    )
    st.dataframe(sample_steps, width="stretch", hide_index=True)
    st.success(f"Result: x = {sample_solution} + {sample_modulus}k")

    st.markdown(
        """
Takeaway:
- CRT reduces many congruences to one final congruence.
- Compatibility matters when moduli are not coprime.
- The final answer describes all integer solutions.
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)
