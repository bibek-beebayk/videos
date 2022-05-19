import datetime

# function to generate year choices
def get_year_choices():
    return [(r, r) for r in range(1984, datetime.date.today().year + 1)]


def get_current_year():
    return datetime.date.today().year