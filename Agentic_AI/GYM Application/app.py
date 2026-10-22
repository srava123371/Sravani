
import os
import base64
import re
from datetime import date
from email.message import EmailMessage

from flask import Flask, request, render_template_string
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

app = Flask(__name__)

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Gym Management System</title>

<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #101827, #233b55);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
}

.container {
    background: white;
    width: 100%;
    max-width: 520px;
    padding: 30px;
    border-radius: 16px;
    box-shadow: 0 12px 35px #0005;
}

h1 { text-align: center; color: #16263e; }
p { text-align: center; color: #64748b; }

label {
    display: block;
    margin-top: 15px;
    margin-bottom: 5px;
    font-weight: bold;
}

input, select {
    display: block;
    width: 100%;
    padding: 12px;
    margin-top: 7px;
    border: 1px solid #cbd5e1;
    border-radius: 7px;
    font-size: 15px;
}

button {
    width: 100%;
    margin-top: 22px;
    padding: 14px;
    border: none;
    border-radius: 7px;
    background: #0f766e;
    color: white;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
}

button:hover { background: #115e59; }

.message {
    padding: 12px;
    margin-top: 15px;
    border-radius: 7px;
    background: #ecfdf5;
    color: #065f46;
    overflow-wrap: anywhere;
}

footer {
    margin-top: 20px;
    text-align: center;
    font-size: 12px;
    color: #64748b;
}
</style>
</head>

<body>
<div class="container">
    <h1>GYM MANAGEMENT</h1>
    <p>Register a member and send a Gmail confirmation</p>

    {% if message %}
    <div class="message">{{ message }}</div>
    {% endif %}

    <form method="POST">
        <label for="name">Member Name</label>
        <input id="name" type="text" name="name"
               placeholder="Enter member name" required>

        <label for="email">Member Email</label>
        <input id="email" type="email" name="email"
               placeholder="member@example.com" required>

        <label for="plan">Membership Plan</label>
        <select id="plan" name="plan" required>
            <option value="Monthly">Monthly</option>
            <option value="Quarterly">Quarterly (3 months)</option>
            <option value="Half-Yearly">Half-Yearly (6 months)</option>
            <option value="Yearly">Yearly (12 months)</option>
        </select>

        <label for="start_date">Membership Start Date</label>
        <input id="start_date" type="date" name="start_date"
               value="{{ today }}" required>

        <button type="submit">Register &amp; Send Email</button>
    </form>

    <footer>Python · Flask · Gmail API · HTML · CSS</footer>
</div>
</body>
</html>
"""


def get_gmail_service():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(
            TOKEN_FILE, SCOPES
        )

    if creds and not creds.has_scopes(SCOPES):
        raise RuntimeError(
            "Saved token has the wrong Gmail permission. "
            "Stop the app, delete token.json, and authorize again."
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    "credentials.json not found beside app.py."
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def send_gym_email(name, recipient, plan, start_date):
    service = get_gmail_service()

    email = EmailMessage()
    email["To"] = recipient
    email["Subject"] = "Gym Membership Confirmation"

    email.set_content(
        f"""Hello {name},

Welcome to our gym!

Your membership details:
Member Name: {name}
Membership Plan: {plan}
Start Date: {start_date}

Thank you for joining our gym.

Regards,
Gym Management Team
"""
    )

    encoded_email = base64.urlsafe_b64encode(
        email.as_bytes()
    ).decode("utf-8")

    result = service.users().messages().send(
        userId="me",
        body={"raw": encoded_email}
    ).execute()

    return result.get("id")


@app.route("/", methods=["GET", "POST"])
def home():
    message = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        recipient = request.form.get("email", "").strip()
        plan = request.form.get("plan", "").strip()
        start_date = request.form.get("start_date", "").strip()

        if not name or not plan:
            message = "Please fill in all required fields."

        elif not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+", recipient
        ):
            message = "Please enter a valid email address."

        else:
            try:
                date.fromisoformat(start_date)

            except ValueError:
                message = "Please select a valid start date."

            else:
                try:
                    message_id = send_gym_email(
                        name, recipient, plan, start_date
                    )
                    message = (
                        f"Email sent successfully to {recipient}. "
                        f"Message ID: {message_id}"
                    )

                except Exception as error:
                    app.logger.exception("Gmail sending failed")
                    message = (
                        f"Email error: {type(error).__name__}: "
                        f"{str(error)[:500]}"
                    )

    return render_template_string(
        HTML,
        message=message,
        today=date.today().isoformat()
    )


if __name__ == "__main__":
    print("Starting Gym Management System...")
    print("Open http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)

