from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    #result = check_guess(50, 50) # just expects a string
    outcome, message = check_guess(50, 50) # expects a tuple
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    #result = check_guess(60, 50) # just expects a string
    outcome, message = check_guess(60, 50) # expects a tuple
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    #result = check_guess(40, 50)
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


def test_guess_too_high_with_message():
    # If secret is 50 and guess is 60, should return "Too High" with message "📉 Go LOWER!"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"


def test_guess_too_low_with_message():
    # If secret is 50 and guess is 40, should return "Too Low" with message "📈 Go HIGHER!"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"
