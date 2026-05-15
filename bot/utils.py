import re
from functools import wraps

def log_command(func):
    @wraps(func)
    def wrapper(message, *args, **kwargs):
        print(f"User {message.chat.id} used {message.text}")
        return func(message, *args, **kwargs)

    return wrapper


facts = [
    "Reading books improves memory.",
    "Books reduce stress.",
    "Libraries existed thousands of years ago."
]


def fact_generator():
    for fact in facts:
        yield fact


fact_gen = fact_generator()

def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)