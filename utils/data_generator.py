import random
import string

from faker import Faker

faker = Faker()


class DataGenerator:

    @staticmethod
    def generate_random_email():
        random_string_length = random.randint(4, 32)
        random_string = ''.join(
            random.choices(string.ascii_lowercase + string.digits, k=random_string_length)
        )
        return f'{random_string}@gmail.com'

    @staticmethod
    def generate_wrong_random_email():
        max_length = 32
        random_email = DataGenerator.generate_random_email()

        wrong_email = f'WRONG_EMAIL_{random_email}'

        if len(wrong_email) > max_length:
            wrong_email = wrong_email[:max_length]

        return wrong_email

    @staticmethod
    def generate_random_name():
        return f'{faker.first_name()} {faker.last_name()}'

    @staticmethod
    def generate_random_password():
        lat_lower = string.ascii_lowercase
        lat_upper = string.ascii_uppercase

        cyr_lower = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
        cyr_upper = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

        digits = string.digits
        special = r"""?@#$%^&*_-+()[]{}><\/|"\'.,:;"""

        required = [
            random.choice(lat_lower + cyr_lower),
            random.choice(lat_upper + cyr_upper),
            random.choice(digits),
        ]

        all_chars = lat_lower + cyr_lower + lat_upper + cyr_upper + digits + special

        total_length = random.randint(8, 20)
        remaining_length = total_length - len(required)

        remaining = random.choices(all_chars, k=remaining_length)

        password = required + remaining
        random.shuffle(password)

        return ''.join(password)
