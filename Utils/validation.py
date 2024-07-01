import re

from Auth.auth import pwd_context


def word_length(min_value: int, max_value: int, string: str):
    pattern = r'^\w{' + str(min_value) + ',' + str(max_value) + r'}$'
    return bool(re.match(pattern, string))


def domain(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email, re.IGNORECASE))


def valid_password(password: str) -> bool:
    if word_length(8, 20, password):
        return False
    pattern = r'^.*[!@#$%^&*:;,.?].*$'
    matches = re.findall(pattern, password, flags=re.IGNORECASE)
    return bool(matches)


def verify_password(given_string: str, password: str):
    return pwd_context.verify(given_string, password)
