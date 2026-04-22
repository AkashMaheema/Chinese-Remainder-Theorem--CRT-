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
    /* Remove default Streamlit top padding and margins */
    .block-container {
        padding-top: 4rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* Clean up the navbar so the 3-dot menu floats on top of our custom navbar */
    [data-testid="stHeader"] {
        background-color: transparent !important;
        z-index: 1000000 !important;
        pointer-events: none !important;
    }
    
    [data-testid="stToolbar"] {
        pointer-events: auto !important;
    }
    
    /* Hide ONLY the deploy button, keep the 3-dot menu */
    .stDeployButton, 
    [data-testid="stDeployButton"], 
    [data-testid="stAppDeployButton"],
    .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_,
    .viewerBadge_link__1S137 {
        display: none !important;
    }
    
    /* Custom Full Width Navbar */
    .custom-navbar {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 60px;
        background-color: var(--background-color);
        border-bottom: 1px solid rgba(127, 127, 127, 0.15);
        z-index: 999999;
        display: flex;
        justify-content: flex-end;
        align-items: center;
        padding: 0 6.5rem 0 3rem;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        background-color: rgba(var(--background-color), 0.8);
        pointer-events: auto;
    }
    
    .custom-navbar a {
        text-decoration: none;
        color: var(--text-color);
        opacity: 0.6;
        margin-left: 2.5rem;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        transition: opacity 0.2s ease;
        pointer-events: auto;
    }
    
    .custom-navbar a:hover {
        opacity: 1;
    }
    
    /* Typography and creative spacing */
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }
    .header-text {
        font-size: 3.5rem;
        font-weight: 800;
        line-height: 1.1;
        letter-spacing: -0.03em;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
        color: var(--text-color);
    }
    .sub-header-text {
        font-size: 1.25rem;
        font-weight: 300;
        opacity: 0.6;
        margin-bottom: 2.5rem;
        letter-spacing: 0.02em;
    }
    
    /* Editorial sections instead of boxes */
    .editorial-section {
        margin-bottom: 2rem;
    }
    .editorial-title {
        font-size: 1rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        opacity: 0.5;
        border-bottom: 1px solid rgba(127, 127, 127, 0.2);
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    
    /* Equation styling (flat and blending) */
    .equation-list {
        display: flex;
        align-items: center;
        font-size: 1.5rem;
        font-weight: 300;
        margin: 0.2rem 0;
    }
    .eq-symbol {
        opacity: 0.4;
        font-weight: 200;
    }
    
    /* Creative Result Area - Big Numbers, No Boxes */
    .result-showcase {
        margin-top: 3rem;
        border-left: 4px solid var(--text-color);
        padding-left: 2rem;
    }
    .result-live {
        font-size: 2.5rem;
        font-weight: 700;
        line-height: 1.2;
        letter-spacing: -0.02em;
    }
    .result-meta {
        font-size: 1rem;
        font-weight: 400;
        opacity: 0.6;
        margin-top: 0.5rem;
    }
    
    /* Custom Streamlit Metrics overrides (make them flat text instead of blocks) */
    [data-testid="stMetric"] {
        padding: 0 !important;
        border: none !important;
    }
    [data-testid="stMetricLabel"] {
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.8rem;
        opacity: 0.5;
    }
    [data-testid="stMetricValue"] {
        font-size: 2.2rem;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    
    /* Cleaner inputs overrides */
    [data-testid="stTextInput"] {
        max-width: 100px;
    }
    div[data-baseweb="input"] {
        border-top: none;
        border-left: none;
        border-right: none;
        border-radius: 0;
        background: transparent !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# Custom Full-Width Top Navbar (with native 3-dot menu floating on top)
# Removed Source Code button


st.markdown('<div class="header-text">Chinese Remainder Theorem.</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header-text">Explore congruences through minimalist, interactive calculations.</div>', unsafe_allow_html=True)

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

left, center, right = st.columns([1, 1.25, 1], gap="large")

with left:
    st.markdown('<div class="editorial-section">', unsafe_allow_html=True)
    st.markdown('<div class="editorial-title">Overview</div>', unsafe_allow_html=True)
    st.markdown(
        """
        The **Chinese Remainder Theorem** solves simultaneous equations 
        of the form `x ≡ a (mod n)`.

        Each step cleanly combines two compatible congruences into one. 
        When moduli are not coprime, a compatibility condition must be met, 
        or the whole system has no solution.
        """
    )
    st.markdown(
        """
        *Example (Answers to 23 modulo 105):*
        - x ≡ 2 (mod 3)
        - x ≡ 3 (mod 5)
        - x ≡ 2 (mod 7)
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)

with center:
    st.markdown('<div class="editorial-section">', unsafe_allow_html=True)
    st.markdown('<div class="editorial-title">Interactive Tool</div>', unsafe_allow_html=True)

    header_row = st.columns([2, 1, 1])
    with header_row[0]:
        st.markdown("<span style='opacity:0.5; font-size:0.85rem; text-transform:uppercase;'>Equations</span>", unsafe_allow_html=True)
    with header_row[1]:
        if st.button("-", use_container_width=True, disabled=st.session_state.congruence_count <= 1):
            ensure_congruence_state(st.session_state.congruence_count - 1)
            st.rerun()
    with header_row[2]:
        if st.button("+", use_container_width=True, disabled=st.session_state.congruence_count >= 6):
            ensure_congruence_state(st.session_state.congruence_count + 1)
            st.rerun()

    st.write("") # Spacing

    for index in range(st.session_state.congruence_count):
        row = st.columns([0.4, 0.4, 0.4, 0.4, 0.3], vertical_alignment="center")
        with row[0]:
            st.markdown("<div class='equation-list' style='justify-content:flex-end;'><span class='eq-symbol'>x ≡</span></div>", unsafe_allow_html=True)
        with row[1]:
            st.text_input(
                f"Remainder {index + 1}",
                key=f"remainder_{index}",
                label_visibility="collapsed",
            )
        with row[2]:
            st.markdown("<div class='equation-list' style='justify-content:center;'><span class='eq-symbol'>mod</span></div>", unsafe_allow_html=True)
        with row[3]:
            st.text_input(
                f"Modulus {index + 1}",
                key=f"modulus_{index}",
                label_visibility="collapsed",
            )
        with row[4]:
            st.markdown("<div class='equation-list'><span class='eq-symbol'></span></div>", unsafe_allow_html=True) # empty margin match

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
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="editorial-section">', unsafe_allow_html=True)
    st.markdown('<div class="editorial-title">Live Result</div>', unsafe_allow_html=True)
    
    if solve_error:
        st.markdown('<span style="opacity:0.5">-</span>', unsafe_allow_html=True)
    else:
        st.markdown(
            f"""
            <div class="result-showcase">
                <div class="result-live">x = {solution}<br/><span style="opacity:0.4; font-size:1.5rem;">mod {modulus}</span></div>
                <div class="result-meta">Generalized: x = {solution} + {modulus}k</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="editorial-section" style="margin-top: 1rem;">', unsafe_allow_html=True)
st.markdown('<div class="editorial-title">How we got the answer</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div style="font-size: 0.95rem; opacity: 0.8; margin-bottom: 1rem;">
    The Chinese Remainder Theorem works by combining pairs of congruences one by one. Check the table below to see the math behind joining each pair of equations until reaching the final result.
    </div>
    """,
    unsafe_allow_html=True,
)

if solve_error:
    st.info("Input a valid compatible system to reveal combination steps.")
elif steps:
    st.dataframe(steps, width="stretch", hide_index=True)
else:
    st.markdown("<span style='opacity:0.5'>Only one congruence provided.</span>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
