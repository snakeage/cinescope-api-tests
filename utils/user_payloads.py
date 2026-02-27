from utils.data_generator import DataGenerator


def generate_register_payload():
    email = DataGenerator.generate_random_email()
    full_name = DataGenerator.generate_random_name()
    password = DataGenerator.generate_random_password()

    payload = {
        'email': email,
        'fullName': full_name,
        'password': password,
        'passwordRepeat': password
    }
    return payload, password


def generate_admin_user_payload():
    email = DataGenerator.generate_random_email()
    full_name = DataGenerator.generate_random_name()
    password = DataGenerator.generate_random_password()

    payload = {
        'email': email,
        'fullName': full_name,
        'password': password,
        'verified': True,
        'banned': False
    }
    return payload, password
