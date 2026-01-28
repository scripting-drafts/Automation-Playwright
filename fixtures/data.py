import random
import string
from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str
    password: str

def rand_email() -> str:
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"qa.{suffix}@example.com"

def rand_name() -> str:
    return "GerardQA"
