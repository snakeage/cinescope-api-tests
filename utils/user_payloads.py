from models.admin_models import AdminCreateUserRequest
from models.register_models import RegisterUserRequest
from utils.data_generator import DataGenerator


def generate_register_payload():
    email = DataGenerator.generate_random_email()
    full_name = DataGenerator.generate_random_name()
    password = DataGenerator.generate_random_password()

    model = RegisterUserRequest(
        email=email, full_name=full_name, password=password, password_repeat=password
    )
    return model, password


def generate_admin_user_payload():
    email = DataGenerator.generate_random_email()
    full_name = DataGenerator.generate_random_name()
    password = DataGenerator.generate_random_password()

    model = AdminCreateUserRequest(
        email=email, full_name=full_name, password=password, verified=True, banned=False
    )
    return model, password
