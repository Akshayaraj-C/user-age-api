from datetime import date
from app.service import calculate_age_at

def test_birthday_passed():
    dob = date(1990, 5, 15)
    target = date(2023, 6, 20)
    assert calculate_age_at(dob, target) == 33

def test_birthday_not_passed():
    dob = date(1990, 8, 15)
    target = date(2023, 6, 20)
    assert calculate_age_at(dob, target) == 32

def test_birthday_today():
    dob = date(1990, 6, 20)
    target = date(2023, 6, 20)
    assert calculate_age_at(dob, target) == 33

def test_leap_year_birthday():
    # Born on Feb 29 2000, target is Feb 28 2004 (not yet Feb 29)
    assert calculate_age_at(date(2000, 2, 29), date(2004, 2, 28)) == 3
    # Born on Feb 29 2000, target is Feb 29 2004
    assert calculate_age_at(date(2000, 2, 29), date(2004, 2, 29)) == 4
    # Born on Feb 29 2000, target is Feb 28 2003 (non-leap year, hasn't reached March 1st or Feb 29)
    assert calculate_age_at(date(2000, 2, 29), date(2003, 2, 28)) == 2
    # Born on Feb 29 2000, target is March 1 2003
    assert calculate_age_at(date(2000, 2, 29), date(2003, 3, 1)) == 3

def test_future_date():
    dob = date(2025, 1, 1)
    target = date(2023, 6, 20)
    assert calculate_age_at(dob, target) == 0
