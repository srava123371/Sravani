
from flask import Flask, request, redirect, url_for, session, render_template_string
import os
import secrets

app = Flask(__name__)

# Secret key for login sessions
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)

# Login credentials
inbuilt_user_name = "Sravani"
inbuilt_user_password = "Sravani@1234#"


# ---------------- LOGIN PAGE ----------------
LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>Nova | Login</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    font-family: Arial, sans-serif;
    color: white;
    background:
        radial-gradient(circle at top left, #273b7c, transparent 45%),
        radial-gradient(circle at bottom right, #762d80, transparent 45%),
        #080b16;
}

.card {
    width: 100%;
    max-width: 410px;
    padding: 38px;
    border: 1px solid #ffffff30;
    border-radius: 25px;
    background: #171b30eF;
    box-shadow: 0 20px 70px #0008;
}

.logo {
    width: 65px;
    height: 65px;
    margin: 0 auto 20px;
    display: grid;
    place-items: center;
    border-radius: 20px;
    font-size: 32px;
    background: linear-gradient(135deg, #5785ff, #bd4bea);
}

h1 { text-align: center; margin-bottom: 10px; }
.subtitle { text-align: center; color: #a7afcb; margin-bottom: 30px; }

label {
    display: block;
    margin: 18px 0 9px;
    font-size: 13px;
}

input {
    width: 100%;
    padding: 14px;
    color: white;
    border: 1px solid #414866;
    border-radius: 11px;
    background: #ffffff08;
    outline: none;
}

input:focus { border-color: #9885ff; }

button {
    width: 100%;
    padding: 15px;
    margin-top: 25px;
    color: white;
    font-size: 15px;
    font-weight: bold;
    border: none;
    border-radius: 11px;
    cursor: pointer;
    background: linear-gradient(100deg, #557cff, #a34be9);
}

button:hover { opacity: .88; }

.error {
    margin-top: 18px;
    color: #ff9daa;
    text-align: center;
    font-size: 14px;
}

.footer {
    margin-top: 25px;
    color: #858eaa;
    text-align: center;
    font-size: 11px;
}
</style>
</head>

<body>
<div class="card">
    <div class="logo">✦</div>
    <h1>Welcome Back</h1>
    <p class="subtitle">Sign in to enter your digital world</p>

    <form method="POST" action="/">
        <label>USERNAME</label>
        <input
            type="text"
            name="username"
            placeholder="Enter username"
            autocomplete="username"
            required>

        <label>PASSWORD</label>
        <input
            type="password"
            name="password"
            placeholder="Enter password"
            autocomplete="current-password"
            required>

        <button type="submit">LOGIN →</button>
    </form>

    {% if error %}
        <div class="error">{{ error }}</div>
    {% endif %}

    <div class="footer">✧ NOVA SECURE LOGIN ✧</div>
</div>
</body>
</html>
"""


# ---------------- DASHBOARD PAGE ----------------
DASHBOARD_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>Nova | Dashboard</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    min-height: 100vh;
    padding: 25px;
    color: white;
    font-family: Arial, sans-serif;
    background:
        radial-gradient(circle at top right, #423075, transparent 40%),
        radial-gradient(circle at bottom left, #183f66, transparent 40%),
        #090c18;
}

nav {
    max-width: 1050px;
    margin: auto;
    padding: 15px 0 25px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #ffffff25;
}

.brand { font-size: 25px; font-weight: bold; letter-spacing: 2px; }
.brand span { color: #b69aff; }

.logout {
    color: white;
    text-decoration: none;
    padding: 11px 18px;
    border: 1px solid #ffffff35;
    border-radius: 10px;
}

.logout:hover { background: #a34be9; }

main { max-width: 1050px; margin: 50px auto; }

.hero {
    padding: 38px;
    border: 1px solid #ffffff25;
    border-radius: 24px;
    background: #ffffff09;
    box-shadow: 0 20px 60px #0004;
}

.eyebrow { color: #b69aff; letter-spacing: 3px; font-size: 12px; }

h1 { font-size: clamp(32px, 5vw, 52px); margin: 20px 0; }

.name {
    color: #c5a5ff;
}

p { color: #a9b2cd; line-height: 1.8; }

.status {
    display: inline-block;
    margin-top: 12px;
    padding: 10px 15px;
    color: #80ffc0;
    border: 1px solid #278a62;
    border-radius: 30px;
    background: #123b2d;
    font-size: 13px;
}

h2 { margin: 35px 0 20px; }

.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

.tile {
    padding: 25px;
    border: 1px solid #ffffff20;
    border-radius: 20px;
    background: #ffffff09;
    transition: .3s;
}

.tile:hover {
    transform: translateY(-6px);
    border-color: #9b81ff;
}

.symbol { font-size: 32px; }
.tile h3 { margin-top: 22px; }

footer {
    max-width: 1050px;
    margin: auto;
    text-align: center;
    color: #77819d;
    font-size: 12px;
}

@media(max-width: 700px) {
    .grid { grid-template-columns: 1fr; }
    .hero { padding: 25px; }
    main { margin-top: 30px; }
}
</style>
</head>

<body>
<nav>
    <div class="brand">✦ NOVA<span>.</span></div>
    <a class="logout" href="/logout">LOGOUT ↗</a>
</nav>

<main>
    <section class="hero">
        <div class="eyebrow">YOUR PERSONAL DASHBOARD</div>

        <h1>
            Login Successful!<br>
            Welcome, <span class="name">{{ username }}</span> ✨
        </h1>

        <p>
            You have successfully logged in.<br>
            Welcome to your own digital universe!
        </p>

        <div class="status">● AUTHENTICATED SUCCESSFULLY</div>
    </section>

    <h2>Your Dashboard</h2>

    <section class="grid">
        <div class="tile">
            <div class="symbol">👤</div>
            <h3>My Profile</h3>
            <p>Welcome to your personal account.</p>
        </div>

        <div class="tile">
            <div class="symbol">🚀</div>
            <h3>Explore</h3>
            <p>Your space for new projects and ideas.</p>
        </div>

        <div class="tile">
            <div class="symbol">⚙️</div>
            <h3>Settings</h3>
            <p>Your dashboard is ready to customize.</p>
        </div>
    </section>
</main>

<footer>NOVA · PYTHON + FLASK · YOUR DIGITAL SPACE</footer>
</body>
</html>
"""


# ---------------- LOGIN ROUTE ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if (
            username == inbuilt_user_name
            and password == inbuilt_user_password
        ):
            session["username"] = username

            # IMPORTANT: open the dashboard page
            return redirect(url_for("dashboard"))

        return render_template_string(
            LOGIN_PAGE,
            error="❌ Invalid username or password. Try again."
        )

    return render_template_string(LOGIN_PAGE, error="")


# ---------------- DASHBOARD ROUTE ----------------
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template_string(
        DASHBOARD_PAGE,
        username=session["username"]
    )


# ---------------- LOGOUT ROUTE ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    print("Nova Login Application Started!")
    print("Open http://127.0.0.1:5000")
    app.run(debug=False)

