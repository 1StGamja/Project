import random
import string
from datetime import datetime

def generate_string():
    length = random.choice([13, 14])
    if length == 13:
        return ''.join(random.choices(string.digits, k=length))
    else:
        first_part = ''.join(random.choices(string.digits, k=6))
        middle = random.choice(string.ascii_letters + string.digits + string.punctuation)
        last_part = ''.join(random.choices(string.digits, k=7))
        return first_part + middle + last_part

def is_valid_date(year, month, day):
    try:
        datetime(year=year, month=month, day=day)
        return True
    except ValueError:
        return False

def generate_valid_date():
    while True:
        year = random.randint(0, 99)
        month = random.randint(1, 12)
        day = random.randint(1, 31)

        if is_valid_date(year, month, day):
            return f"{year:02}{month:02}{day:02}"

def main():
    for _ in range(50):
        random_string = generate_string()
        date_part = generate_valid_date()
        formatted_date = f"{date_part[:2]}-{date_part[2:4]}-{date_part[4:6]}"

        print(f"Generated string: {random_string}")
        print(f"Formatted date: {formatted_date}")
        print()

if __name__ == "__main__":
    main()
