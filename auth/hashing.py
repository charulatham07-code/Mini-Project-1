# This file contains a function that hashes passwords.
# Hashing means converting the password to a scrambled form
# so even we cannot see the real password.


import hashlib

def hash_password(password: str) -> str:
    # Convert password to SHA-256 hash
    return hashlib.sha256(password.encode()).hexdigest()

