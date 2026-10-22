# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Teacher-only student signups and unregistration
- Teacher login sessions protected by an HTTP-only cookie

## Teacher Accounts

Teacher passwords are not stored in plaintext. Account entries in
`teachers.json` contain a random salt and a PBKDF2 password hash. To add a
teacher, run:

```sh
python src/create_teacher.py
```

The tool prompts for a username and a password of at least 12 characters.
Restart the server after adding or changing accounts. Keep `teachers.json`
restricted to trusted maintainers; the password hashes are still sensitive
authentication data.

Use HTTPS when deploying the application. The session cookie is marked
`Secure` for HTTPS requests and uses `HttpOnly` and `SameSite=Strict`.

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/auth/login`                                                     | Log in as a teacher and establish a session                         |
| GET    | `/auth/session`                                                   | Get the current teacher session                                     |
| POST   | `/auth/logout`                                                    | End the current teacher session                                     |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Teacher-only student signup                                         |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Teacher-only unregistration                                      |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.
