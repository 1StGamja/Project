import random
from datetime import datetime, timedelta

def generate_birth_date():
    start_date = datetime(1950, 1, 1)
    end_date = datetime(2020, 12, 31)
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date.strftime('%y%m%d')

def generate_gender_code():
    return random.choice([1, 3, 2, 4, 5, 7, 6, 8])

def generate_institution_code():
    ranges = [
        (0, 8), (9, 12), (13, 15), (16, 18), (19, 25),
        (26, 34), (35, 39), (40, 40), (41, 43), (45, 47),
        (44, 44), (48, 54), (55, 64), (65, 66), (67, 70),
        (71, 81), (82, 84), (86, 91), (85, 85), (90, 90),
        (92, 95), (96, 96)
    ]
    region = random.choice(ranges)
    return str(random.randint(region[0], region[1])).zfill(2)

def generate_receipt_order():
    return str(random.randint(1, 9))

def calculate_verification_code(number):
    multipliers = [2, 3, 4, 5, 6, 7, 8, 9]
    sum = 0
    for i, digit in enumerate(number):
        sum += int(digit) * multipliers[i % len(multipliers)]

    remainder = sum % 11
    verification_code = 11 - remainder
    return str(verification_code) if verification_code < 10 else str(verification_code % 10)

def generate_number():
    birth_date = generate_birth_date()
    gender_code = str(generate_gender_code())
    institution_code = generate_institution_code()
    receipt_order = generate_receipt_order()

    number = birth_date + gender_code + institution_code + receipt_order
    verification_code = calculate_verification_code(number)
    return number + verification_code

generated_numbers = [generate_number() for _ in range(1000)]
print(generated_numbers)
