import re

def is_valid_package_name(name: str) -> bool:
    return bool(re.match(r'^[a-zA-Z0-9_.-]{1,100}$', name))
