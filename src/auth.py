"""Teacher credential loading and password verification."""

import hashlib
import hmac
import json
from pathlib import Path


TEACHERS_FILE = Path(__file__).with_name("teachers.json")
PBKDF2_ITERATIONS = 310_000


def load_teachers() -> list[dict[str, str]]:
    with TEACHERS_FILE.open(encoding="utf-8") as file:
        teachers = json.load(file)
    if not isinstance(teachers, list):
        raise ValueError(f"{TEACHERS_FILE} must contain a JSON array")

    for teacher in teachers:
        if not isinstance(teacher, dict) or not all(
            isinstance(teacher.get(key), str)
            for key in ("username", "salt", "password_hash")
        ):
            raise ValueError(
                f"{TEACHERS_FILE} entries must include username, salt, "
                "and password_hash strings"
            )
        try:
            salt = bytes.fromhex(teacher["salt"])
            password_hash = bytes.fromhex(teacher["password_hash"])
        except ValueError as error:
            raise ValueError(
                f"{TEACHERS_FILE} contains invalid hex credential data"
            ) from error
        if not teacher["username"] or not salt or len(password_hash) != 32:
            raise ValueError(f"{TEACHERS_FILE} contains an invalid credential")

    return teachers


def hash_password(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    ).hex()


def verify_teacher_password(username: str, password: str) -> bool:
    for teacher in load_teachers():
        if not isinstance(teacher, dict) or teacher.get("username") != username:
            continue

        try:
            salt = bytes.fromhex(teacher["salt"])
            expected_hash = teacher["password_hash"]
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(
                f"Invalid credential entry for teacher {username!r}"
            ) from error

        actual_hash = hash_password(password, salt)
        return hmac.compare_digest(actual_hash, expected_hash)

    return False
