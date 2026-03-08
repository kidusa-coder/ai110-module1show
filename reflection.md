# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- **Bug 1: New Game doesn't fully reset the game**
- Expected: Clicking "New Game" should reset everything and let me play again.
- Actual: The "You already won" message never disappeared, and submitting a new guess did nothing.

- **Bug 2: Attempts counter never updated**
- Expected: Each time I submitted a guess, the attempts counter should
  decrease by 1.
- Actual: It stayed frozen at 8 the entire time, never reflecting my actual remaining attempts.

- **Bug 3: Show Hint checkbox had no effect**
- Expected: Toggling "Show Hint" on or off should control whether
  I see feedback after guessing.
- Actual: Whether checked or unchecked, no meaningful feedback appeared.

---

## 2. How did you use AI as a teammate?

- COpilot & Claude
- Correct AI suggestion: Copilot correctly identified the 3 missing session state resets (status, score, history) consistently across 2 separate chat sessions.
- Incorrect suggestion: In prompt 1, copilot suggested resetting to 1, but in prompt 3 it said attempts should be 0. It contradicted itself. I used claude to fix this error by moving attempts after validation.

---

## 3. Debugging and testing your fixes

- Ran pytest with 5 tests, all passing after fixing the tuple return value mismatch in existing tests
- Manually verified all fixes in the live streamlit app
- conftest.py was needed to fix ModuleNotFoundError because pytest couldn't find logic_utils from the tests folder.
- AI helped me generate the two new message checking tests.

---

## 4. What did you learn about Streamlit and state?

- random.randint() was being called every return, generating new search each time.
- Imagine everytime you clicked a button on a website, the whole page reloaded from scratch and forgot everything. It is that without session state.
- CHange made was:
  if "secret" not in st.session_state:
  st.session_state.secret = random.randint(low, high)

---

## 5. Looking ahead: your developer habits

- always running tests after every fix, using comments for every change made
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- verify AI suggestions against each other, test before accepting it.
- That AI suggestions should always be tested and verified before use.
