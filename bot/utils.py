import re
from functools import wraps

def log_command(func):
    @wraps(func)
    def wrapper(message, *args, **kwargs):
        print(f"User {message.chat.id} used {message.text}")
        return func(message, *args, **kwargs)

    return wrapper


facts = [
    "Libraries existed thousands of years ago.",
    "Reading for six minutes can reduce physical stress levels by 67%",
    "The fastest readers can process over 25,000 words per minute.",
    "India currently ranks as the world's most well-read nation by hours spent."
]


def fact_generator():
    for fact in facts:
        yield fact


fact_gen = fact_generator()

def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)