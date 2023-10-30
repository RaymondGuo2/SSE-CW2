from app import process_query


def test_knows_about_dinosaurs():
    assert process_query("dinosaurs") == (
        "Dinosaurs ruled the Earth 200 million years ago"
    )


def test_does_not_know_about_asteroids():
    assert process_query("asteroids") == "Unknown"


def test_what_is_your_name():
    assert process_query("What is your name?") == "SSE_LEGENDS"


def test_first_addition():
    assert process_query("What is 71 plus 61?") == "132"


def test_multiply():
    assert process_query("What is 84 multiplied by 66?") == "5544"
