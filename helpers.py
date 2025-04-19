from faker import Faker

fake = Faker(['ru_RU'])

def random_string(length=8):
    return fake.pystr(min_chars=length, max_chars=length)

def random_email():
    return fake.email()

def random_name():
    return fake.name()

def random_password(length=10):
    return fake.password(length=length)