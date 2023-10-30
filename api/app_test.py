from app import process_query


def test_knows_about_dinosaurs():
    assert process_query("dinosaurs") == (
        "Dinosaurs ruled the Earth 200 million years ago"
        )


def test_does_not_know_about_asteroids():
    assert process_query("asteroids") == "Unknown"


def test_what_is_your_name():
    assert process_query("What is your name?") == "SSE_LEGENDS"

def first_addition():
    assert process_query("What is 71 plus 61?") == "132"

def largest_number1():
    assert process_query("Which of the following numbers is the largest: 87, 13, 84?") == "87"

def largest_number2():
    assert process_query("Which of the following numbers is the largest: 11, 78, 54?") == "78"

def largest_number3():
    assert process_query("Which of the following numbers is the largest: 8, 97, 77?") == "97"

def second_addition():
    assert process_query("What is 44 plus 42?") == "86"

def third_addition():
    assert process_query("What is 51 plus 48?") == "99"

def largest_number4():
    assert process_query("Which of the following numbers is the largest: 45, 70, 89?") == "89"