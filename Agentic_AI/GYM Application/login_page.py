
from flask import Flask, request, render_template_string, session
from hmac import compare_digest
import os

app = Flask(__name__)
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY", "change-this-demo-secret-key"
)

password = "Sravani@1234#"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cinematic Access</title>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    min-height: 100vh;
    font-family: Arial, sans-serif;
    background: #050711;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    position: relative;
}

/* Cinematic background */
body::before {
    content: "";
    position: absolute;
    inset: -50%;
    background:
        radial-gradient(circle at 30% 40%,
        rgba(0, 229, 255, 0.20), transparent 25%),
        radial-gradient(circle at 70% 60%,
        rgba(155, 70, 255, 0.25), transparent 30%);
    animation: atmosphere 10s ease-in-out infinite alternate;
}

@keyframes atmosphere {
    from { transform: translate(-3%, -2%) scale(1); }
    to   { transform: translate(3%, 2%) scale(1.15); }
}

.grid {
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.025) 1px, transparent 1px);
    background-size: 45px 45px;
    mask-image: linear-gradient(transparent, black, transparent);
}

.login-box {
    position: relative;
    z-index: 2;
    width: 390px;
    max-width: 92%;
    padding: 42px 35px;
    border: 1px solid rgba(0, 229, 255, .35);
    border-radius: 20px;
    background: rgba(10, 15, 32, .78);
    backdrop-filter: blur(18px);
    box-shadow:
        0 0 35px rgba(0, 229, 255, .12),
        inset 0 0 25px rgba(155, 70, 255, .05);
    animation: appear 1s ease both;
}

@keyframes appear {
    from { opacity: 0; transform: translateY(30px) scale(.96); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}

.logo {
    width: 75px;
    height: 75px;
    margin: 0 auto 22px;
    display: flex;
    justify-content: center;
    align-items: center;
    border: 1px solid #00e5ff;
    border-radius: 50%;
    font-size: 35px;
    box-shadow: 0 0 25px rgba(0,229,255,.35);
}

h1 {
    text-align: center;
    font-size: 28px;
    letter-spacing: 3px;
    text-transform: uppercase;
}

h1 span {
    color: #00e5ff;
    text-shadow: 0 0 15px rgba(0,229,255,.6);
}

.subtitle {
    text-align: center;
    margin: 12px 0 30px;
    color: #a4b0ca;
    font-size: 12px;
    letter-spacing: 2px;
    line-height: 1.7;
}

label {
    display: block;
    margin-bottom: 10px;
    font-size: 11px;
    color: #9ba8c8;
    letter-spacing: 2px;
}

input {
    width: 100%;
    padding: 15px;
    border: 1px solid #263650;
    border-radius: 8px;
    background: rgba(3, 7, 18, .8);
    color: white;
    font-size: 15px;
    outline: none;
    transition: .3s;
}

input:focus {
    border-color: #00e5ff;
    box-shadow: 0 0 15px rgba(0,229,255,.18);
}

button {
    width: 100%;
    padding: 15px;
    margin-top: 22px;
    border: none;
    border-radius: 8px;
    background: linear-gradient(100deg, #00c6e8, #8065ff);
    color: #050711;
    font-size: 13px;
    font-weight: bold;
    letter-spacing: 3px;
    cursor: pointer;
    transition: .3s;
}

button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 0 25px rgba(0,229,255,.35);
}

button:disabled {
    opacity: .4;
    cursor: not-allowed;
}

.message {
    margin-top: 22px;
    text-align: center;
    font-size: 13px;
    line-height: 1.6;
    overflow-wrap: anywhere;
}

.success { color: #50ffb0; }
.error { color: #ff637d; }

.remaining {
    margin-top: 18px;
    text-align: center;
    color: #8290ad;
    font-size: 12px;
}

.footer {
    text-align: center;
    margin-top: 30px;
    padding-top: 18px;
    border-top: 1px solid rgba(255,255,255,.08);
    color: #5e6b89;
    font-size: 10px;
    letter-spacing: 2px;
}

.scanline {
    position: absolute;
    top: -10%;
    left: 0;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg,
        transparent, rgba(0,229,255,.3), transparent);
    animation: scan 7s linear infinite;
    pointer-events: none;
}

@keyframes scan {
    to { top: 110%; }
}

@media (max-width: 480px) {
    .login-box { padding: 32px 24px; }
    h1 { font-size: 24px; }
}
</style>
</head>

<body>
<div class="grid"></div>
<div class="scanline"></div>

<div class="login-box">
    <div class="logo">◈</div>

    <h1>CINE<span>ACCESS</span></h1>
    <p class="subtitle">
        SECURE YOUR IDENTITY<br>
        AUTHORIZED ACCESS ONLY
    </p>

    <form method="POST">
        <label for="user">ACCESS PASSWORD</label>

        <input
            type="password"
            id="user"
            name="user"
            placeholder="Enter your password"
            autocomplete="current-password"
            required
            autofocus
            {% if locked or success %}disabled{% endif %}
        >

        <button type="submit"
            {% if locked or success %}disabled{% endif %}>
            {% if locked %}ACCESS LOCKED
            {% elif success %}ACCESS GRANTED
            {% else %}INITIALIZE LOGIN →{% endif %}
        </button>
    </form>

    {% if message %}
        <div class="message {{ status }}">{{ message }}</div>
    {% endif %}

    {% if not locked and not success %}
        <div class="remaining">
            ATTEMPTS REMAINING: {{ remaining }} / 3
        </div>
    {% endif %}

    <div class="footer">
        CINEMATIC SECURITY SYSTEM · FLASK
    </div>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    session.setdefault("attempts", 0)

    message = ""
    status = ""
    success = session.get("success", False)
    locked = session.get("locked", False)

    if request.method == "POST" and not locked and not success:
        user = request.form.get("user", "")

        if compare_digest(user, password):
            session["success"] = True
            success = True
            message = "✓ ACCESS GRANTED — LOGIN SUCCESSFUL"
            status = "success"
        else:
            session["attempts"] += 1

            if session["attempts"] >= 3:
                session["locked"] = True
                locked = True
                message = "✕ ACCESS DENIED — ACCOUNT LOCKED"
            else:
                remaining = 3 - session["attempts"]
                message = (
                    f"✕ INCORRECT PASSWORD — "
                    f"{remaining} ATTEMPT(S) REMAINING"
                )

            status = "error"

    if success and not message:
        message = "✓ ACCESS GRANTED — LOGIN SUCCESSFUL"
        status = "success"

    if locked and not message:
        message = "✕ ACCESS DENIED — ACCOUNT LOCKED"
        status = "error"

    remaining = max(0, 3 - session["attempts"])

    return render_template_string(
        HTML,
        message=message,
        status=status,
        remaining=remaining,
        locked=locked,
        success=success
    )

if __name__ == "__main__":
    app.run(debug=True)

