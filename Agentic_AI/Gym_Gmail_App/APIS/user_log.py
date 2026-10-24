from flask import Flask, request, render_template_string

app = Flask(__name__)

# Demo credentials
inbuilt_user_name = "Sravani"
inbuilt_user_password = "Sravani@1234#"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Nova | Secure Login</title>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: 'Segoe UI', Arial, sans-serif;
    color: white;
    background:
        radial-gradient(ellipse at 15% 20%,
        #253c75 0%, transparent 40%),
        radial-gradient(ellipse at 85% 80%,
        #652b72 0%, transparent 40%),
        #080b16;
    padding: 20px;
    overflow-x: hidden;
}

.orb {
    position: fixed;
    width: 240px;
    height: 240px;
    border-radius: 50%;
    filter: blur(75px);
    opacity: .45;
    pointer-events: none;
}

.orb.one {
    background: #477bff;
    top: 5%;
    left: 5%;
}

.orb.two {
    background: #bb43f2;
    bottom: 5%;
    right: 5%;
}

.login-card {
    width: 100%;
    max-width: 420px;
    position: relative;
    padding: 42px 35px;
    border: 1px solid rgba(255,255,255,.17);
    border-radius: 25px;
    background: rgba(18, 22, 42, .76);
    backdrop-filter: blur(22px);
    box-shadow: 0 25px 80px rgba(0,0,0,.5);
    animation: appear .8s ease;
}

@keyframes appear {
    from {
        opacity: 0;
        transform: translateY(25px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.logo {
    width: 66px;
    height: 66px;
    margin: 0 auto 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 29px;
    border-radius: 20px;
    background: linear-gradient(135deg, #5285ff, #b44df0);
    box-shadow: 0 0 35px rgba(100,105,255,.45);
}

h1 {
    text-align: center;
    font-size: 30px;
    letter-spacing: 1px;
}

.subtitle {
    text-align: center;
    color: #a6aec8;
    font-size: 13px;
    margin: 10px 0 30px;
}

label {
    display: block;
    margin: 18px 0 9px;
    color: #dfe4f8;
    font-size: 13px;
    font-weight: 600;
}

.input-box {
    display: flex;
    align-items: center;
    border: 1px solid #353c59;
    border-radius: 12px;
    background: rgba(255,255,255,.045);
    transition: .3s;
}

.input-box:focus-within {
    border-color: #8a83ff;
    box-shadow: 0 0 16px rgba(112,105,255,.18);
}

.input-box input {
    width: 100%;
    min-width: 0;
    padding: 15px 13px;
    color: white;
    font-size: 14px;
    background: transparent;
    border: none;
    outline: none;
}

.input-box input::placeholder {
    color: #777f9e;
}

.field-icon {
    padding-left: 14px;
    color: #a5a9ff;
}

.eye {
    padding: 10px;
    cursor: pointer;
    color: #a5a9ff;
    background: transparent;
    border: none;
}

.login-btn {
    width: 100%;
    margin-top: 27px;
    padding: 15px;
    border: none;
    border-radius: 12px;
    color: white;
    font-size: 15px;
    font-weight: bold;
    letter-spacing: .5px;
    cursor: pointer;
    background: linear-gradient(100deg, #557cff, #a34be9);
    box-shadow: 0 8px 25px rgba(102,92,255,.3);
    transition: .3s;
}

.login-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 32px rgba(125,92,255,.5);
}

.message {
    margin-top: 18px;
    padding: 12px;
    text-align: center;
    border-radius: 10px;
    font-size: 13px;
    line-height: 1.5;
}

.success {
    color: #8dffc5;
    border: 1px solid #267c59;
    background: rgba(23,160,100,.12);
}

.error {
    color: #ff9caa;
    border: 1px solid #85394b;
    background: rgba(200,50,75,.12);
}

.footer {
    margin-top: 28px;
    text-align: center;
    color: #78819e;
    font-size: 11px;
    letter-spacing: 1px;
}

.secure {
    margin-top: 19px;
    text-align: center;
    color: #a2abc4;
    font-size: 12px;
}

@media (max-width: 480px) {
    .login-card {
        padding: 32px 23px;
    }
    h1 {
        font-size: 26px;
    }
}
</style>
</head>

<body>

<div class="orb one"></div>
<div class="orb two"></div>

<main class="login-card">

    <div class="logo">✦</div>

    <h1>Welcome Back</h1>
    <p class="subtitle">
        Sign in to continue to your secure space
    </p>

    <form method="POST" autocomplete="off">

        <label for="username">USERNAME</label>
        <div class="input-box">
            <span class="field-icon">♙</span>
            <input
                type="text"
                id="username"
                name="username"
                placeholder="Enter your username"
                required
                autocomplete="username">
        </div>

        <label for="password">PASSWORD</label>
        <div class="input-box">
            <span class="field-icon">▣</span>
            <input
                type="password"
                id="password"
                name="password"
                placeholder="Enter your password"
                required
                autocomplete="current-password">
            <button
                class="eye"
                type="button"
                onclick="togglePassword()"
                aria-label="Show or hide password">◉</button>
        </div>

        <button class="login-btn" type="submit">
            SIGN IN &nbsp; →
        </button>

    </form>

    {% if message %}
        <div class="message {{ status }}" role="status">
            {{ message }}
        </div>
    {% endif %}

    <div class="secure">✧ &nbsp; YOUR SPACE. YOUR SECURITY.</div>

    <div class="footer">
        NOVA LOGIN SYSTEM · POWERED BY FLASK
    </div>

</main>

<script>
function togglePassword() {
    const password = document.getElementById("password");

    password.type =
        password.type === "password" ? "text" : "password";
}
</script>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    status = ""

    if request.method == "POST":
        user_name = request.form.get("username", "").strip()
        user_password = request.form.get("password", "")

        if (
            user_name == inbuilt_user_name
            and user_password == inbuilt_user_password
        ):
            message = "Login successful! Welcome, " + user_name + "!"
            status = "success"
        else:
            message = "Invalid username or password. Please try again."
            status = "error"

    return render_template_string(
        HTML,
        message=message,
        status=status
    )

if __name__ == "__main__":
    print("Starting Nova Login System...")
    print("Open http://127.0.0.1:5000 in your browser")
    app.run(debug=False)
