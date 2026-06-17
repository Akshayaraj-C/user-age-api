from datetime import date

def calculate_age_at(dob: date, target: date) -> int:
    """
    Computes age dynamically given a birth date and a target date.
    Allows easy and deterministic testing.
    """
    if dob > target:
        return 0

    age = target.year - dob.year

    # Check if the birthday has not happened yet in the target year
    if (target.month, target.day) < (dob.month, dob.day):
        age -= 1

    return max(0, age)

def calculate_age(dob: date) -> int:
    """
    Calculates age relative to today's date.
    """
    return calculate_age_at(dob, date.today())
