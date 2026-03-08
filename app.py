import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score, load_high_score, save_high_score

# --- Session State Initialization ---
if "history" not in st.session_state:
    st.session_state.history = []

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "last_message" not in st.session_state:
    st.session_state.last_message = ""

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

# --- Session State Initialization (continued) ---
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

# FIX: Changed from 1 to 0 to fix off-by-one error in attempts counter
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# Feature 1: Display high score in sidebar
st.sidebar.caption(f"High Score: {load_high_score()}")

# Feature 2: Guess History Sidebar with Progress Bars
st.sidebar.header("Guess History")
valid_guesses = [g for g in st.session_state.history if isinstance(g, int)]
for i, guess in enumerate(valid_guesses, 1):
    # Calculate closeness: 1.0 means exact match, 0.0 means farthest
    closeness = 1 - abs(guess - st.session_state.secret) / (high - low)
    st.sidebar.progress(closeness)
    st.sidebar.caption(f"Guess {i}: {guess}")

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# FIX: Store hint message in session state so it persists across reruns
if "last_message" not in st.session_state:
    st.session_state.last_message = ""

# --- UI ---
st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: Added missing session state resets (status, score, history, last_message)
# Diagnosed in Phase 1, repaired using Copilot Agent mode
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.score = 0
    st.session_state.history = []
    st.session_state.last_message = ""  # FIX: clear hint on new game
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

# FIX: Display hint from session state so it persists across reruns
if show_hint and st.session_state.last_message:
    st.warning(st.session_state.last_message)

if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        # FIX: Increment attempts only on valid guess
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # FIX: Removed string conversion glitch that broke check_guess on even attempts
        # Claude caught this bug that Copilot missed
        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        # FIX: Store hint in session state so it persists across rerun
        st.session_state.last_message = message

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            # Feature 1: Save high score if beaten
            save_high_score(st.session_state.score)
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )
            else:
                # FIX: Only rerun if game is still going so hints have time to display
                st.rerun()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")