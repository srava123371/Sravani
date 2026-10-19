
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

# Permission to send emails only
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

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
    font-weight: bold;
}
input, select {
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
        <label>Member Name</label>
        <input type="text" name="name"
               placeholder="Enter member name" required>

        <label>Member Email</label>
        <input type="email" name="email"
               placeholder="member@example.com" required>

        <label>Membership Plan</label>
        <select name="plan" required>
            <option value="Monthly">Monthly</option>
            <option value="Quarterly">Quarterly (3 months)</option>
            <option value="Half-Yearly">Half-Yearly (6 months)</option>
            <option value="Yearly">Yearly (12 months)</option>
        </select>

        <label>Membership Start Date</label>
        <input type="date" name="start_date"
               value="{{ today }}" required>

        <button type="submit">Register & Send Email</button>
    </form>

    <footer>Python · Flask · Gmail API · HTML · CSS</footer>
</div>
</body>
</html>
"""


def get_gmail_service():
    """Authorize Gmail once and reuse the saved token."""
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json", SCOPES
        )

    if creds and not creds.has_scopes(SCOPES):
        creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("credentials.json"):
                raise FileNotFoundError(
                    "credentials.json is missing. "
                    "Download it from Google Cloud."
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def send_gym_email(name, recipient, plan, start_date):
    """Send a membership confirmation using Gmail API."""
    service = get_gmail_service()

    email = EmailMessage()
    email["To"] = recipient
    email["Subject"] = "Gym Membership Confirmation"

    email.set_content(
        f"""Hello {name},

Welcome to our gym!

Your membership details are:

Member Name: {name}
Membership Plan: {plan}
Start Date: {start_date}

Thank you for joining us.
We look forward to helping you achieve your fitness goals!

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

                message_id = send_gym_email(
                    name, recipient, plan, start_date
                )

                message = (
                    f"Membership email sent successfully to "
                    f"{recipient}. Message ID: {message_id}"
                )

            except ValueError:
                message = "Please select a valid start date."
            except Exception as error:
                print("Gmail error:", repr(error))
                message = (
                    "Email could not be sent. Check credentials, "
                    "OAuth settings, internet connection, and "
                    "the terminal error."
                )

    return render_template_string(
        HTML, message=message, today=date.today().isoformat()
    )


if __name__ == "__main__":
    print("Starting Gym Management System...")
    print("Open http://127.0.0.1:5000")
    app.run(debug=False)
