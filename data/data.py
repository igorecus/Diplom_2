from helpers import random_password

DEFAULT_PASSWORD = random_password(12)

ALREADY_EXISTS_ERROR = "User already exists"
REQUIRED_FIELDS_ERROR = "Email, password and name are required fields"
AUTH_ERROR = "You should be authorised"
INVALID_CREDENTIALS_ERROR = "email or password are incorrect"
NO_INGREDIENTS_ERROR = "Ingredient ids must be provided"