
from flask import Flask, request, render_template_string

app = Flask(__name__)

questions = [
    {"q": "What is the capital of India?", "options": ["Mumbai", "New Delhi", "Chennai", "Kolkata"], "answer": "New Delhi"},
    {"q": "What is the capital of Andhra Pradesh?", "options": ["Amaravati", "Hyderabad", "Vijayawada", "Visakhapatnam"], "answer": "Amaravati"},
    {"q": "What is the capital of Telangana?", "options": ["Warangal", "Karimnagar", "Hyderabad", "Nizamabad"], "answer": "Hyderabad"},
    {"q": "What is the capital of Karnataka?", "options": ["Mysuru", "Bengaluru", "Mangaluru", "Hubballi"], "answer": "Bengaluru"},
    {"q": "What is the capital of Tamil Nadu?", "options": ["Madurai", "Coimbatore", "Chennai", "Salem"], "answer": "Chennai"},
    {"q": "What is the capital of Kerala?", "options": ["Kochi", "Kozhikode", "Thrissur", "Thiruvananthapuram"], "answer": "Thiruvananthapuram"},
    {"q": "What is the capital of Maharashtra?", "options": ["Pune", "Mumbai", "Nagpur", "Nashik"], "answer": "Mumbai"},
    {"q": "What is the capital of Gujarat?", "options": ["Surat", "Ahmedabad", "Gandhinagar", "Vadodara"], "answer": "Gandhinagar"},
    {"q": "What is the capital of Rajasthan?", "options": ["Jaipur", "Jodhpur", "Udaipur", "Ajmer"], "answer": "Jaipur"},
    {"q": "What is the capital of West Bengal?", "options": ["Darjeeling", "Kolkata", "Howrah", "Durgapur"], "answer": "Kolkata"},
    {"q": "What is the capital of Bihar?", "options": ["Gaya", "Patna", "Bhagalpur", "Muzaffarpur"], "answer": "Patna"},
    {"q": "What is the capital of Uttar Pradesh?", "options": ["Kanpur", "Varanasi", "Lucknow", "Agra"], "answer": "Lucknow"},
    {"q": "What is the capital of Madhya Pradesh?", "options": ["Indore", "Gwalior", "Jabalpur", "Bhopal"], "answer": "Bhopal"},
    {"q": "What is the capital of Odisha?", "options": ["Cuttack", "Puri", "Bhubaneswar", "Rourkela"], "answer": "Bhubaneswar"},
    {"q": "What is the capital of Assam?", "options": ["Guwahati", "Dispur", "Silchar", "Dibrugarh"], "answer": "Dispur"}
]

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Indian Capitals Quiz</title>
    <style>
        * { box-sizing: border-box; }

        body {
            margin: 0;
            min-height: 100vh;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #ff9933, #ffffff, #138808);
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 25px;
        }

        .container {
            background: white;
            width: 100%;
            max-width: 650px;
            padding: 35px;
            border-radius: 22px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.2);
        }

        h1 {
            text-align: center;
            color: #172554;
            margin-top: 0;
        }

        .subtitle {
            text-align: center;
            color: #64748b;
            margin-bottom: 25px;
        }

        .question {
            background: #f8fafc;
            padding: 20px;
            border-radius: 14px;
            margin-bottom: 18px;
            border-left: 5px solid #ff9933;
        }

        .question h3 {
            margin-top: 0;
            color: #1e293b;
        }

        label {
            display: block;
            padding: 10px;
            margin: 7px 0;
            border: 1px solid #e2e8f0;
            border-radius: 9px;
            cursor: pointer;
            transition: 0.2s;
        }

        label:hover {
            background: #fff7ed;
            border-color: #ff9933;
        }

        input[type="radio"] {
            margin-right: 10px;
            accent-color: #ea580c;
        }

        button {
            width: 100%;
            padding: 15px;
            background: #172554;
            color: white;
            font-size: 17px;
            font-weight: bold;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            margin-top: 10px;
        }

        button:hover {
            background: #ea580c;
        }

        .result {
            text-align: center;
            background: #ecfdf5;
            padding: 20px;
            border-radius: 12px;
            margin-top: 22px;
            color: #065f46;
        }

        .result h2 { margin-top: 0; }

        .restart {
            display: block;
            text-align: center;
            margin-top: 18px;
            color: #1d4ed8;
            text-decoration: none;
            font-weight: bold;
        }

        @media (max-width: 500px) {
            .container { padding: 20px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🇮🇳 Indian Capitals Quiz</h1>
        <p class="subtitle">Test your knowledge of Indian state capitals!</p>

        <form method="POST">
            {% for item in questions %}
                <div class="question">
                    <h3>{{ loop.index }}. {{ item.q }}</h3>
                    {% for option in item.options %}
                        <label>
                            <input type="radio"
                                   name="q{{ loop.index0 }}"
                                   value="{{ option }}"
                                   required>
                            {{ option }}
                        </label>
                    {% endfor %}
                </div>
            {% endfor %}

            <button type="submit">Submit Answers</button>
        </form>

        {% if score is not none %}
            <div class="result">
                <h2>Your Score: {{ score }} / {{ questions|length }}</h2>
                {% if score == questions|length %}
                    <p>Excellent! All answers are correct! 🎉</p>
                {% elif score >= questions|length // 2 %}
                    <p>Good job! Keep learning! 👏</p>
                {% else %}
                    <p>Keep practicing. You can do it! 💪</p>
                {% endif %}
                <p>Percentage: {{ (score * 100 / questions|length)|round(1) }}%</p>
                <a class="restart" href="/">Try Again</a>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    score = None

    if request.method == "POST":
        score = 0

        for i, item in enumerate(questions):
            user_answer = request.form.get(f"q{i}", "")
            if user_answer == item["answer"]:
                score += 1

    return render_template_string(
        HTML,
        questions=questions,
        score=score
    )


if __name__ == "__main__":
    app.run(debug=True)
