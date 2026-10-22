"""Add a teacher account to the local teacher credential JSON file."""

import getpass
import json
import secrets

from auth import TEACHERS_FILE, hash_password, load_teachers


def main() -> None:
    username = input("Teacher username: ").strip()
    if not username:
        raise SystemExit("Username cannot be empty.")

    teachers = load_teachers()
    if any(teacher.get("username") == username for teacher in teachers):
        raise SystemExit(f"Teacher {username!r} already exists.")

    password = getpass.getpass("Teacher password (at least 12 characters): ")
    if len(password) < 12:
        raise SystemExit("Password must be at least 12 characters.")
    confirmation = getpass.getpass("Confirm password: ")
    if password != confirmation:
        raise SystemExit("Passwords do not match.")

    salt = secrets.token_bytes(16)
    teachers.append({
        "username": username,
        "salt": salt.hex(),
        "password_hash": hash_password(password, salt),
    })
    with TEACHERS_FILE.open("w", encoding="utf-8") as file:
        json.dump(teachers, file, indent=2)
        file.write("\n")

    print(f"Teacher {username!r} added.")


if __name__ == "__main__":
    main()
