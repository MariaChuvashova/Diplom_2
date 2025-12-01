import random
import string


def generate_email():
    return f"user_{''.join(random.choices(string.ascii_letters + string.digits, k=8))}@test.com"


def generate_name():
    name = ''.join(random.choices(string.ascii_lowercase, k=5))
    return name


def generate_password():
    password = ''.join(random.choices(string.ascii_lowercase, k=10))
    return password
