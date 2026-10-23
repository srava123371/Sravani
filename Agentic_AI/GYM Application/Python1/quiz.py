
from flask import Flask, request, render_template_string

app = Flask(__name__)

questions = [
    {"q": "What is the capital of India?",
     "options": ["Mumbai", "New Delhi", "Chennai", "Kolkata"],
     "answer": "New Delhi"},

    {"q": "What is the capital of Andhra Pradesh?",
     "options": ["Amaravati", "Hyderabad", "Vijayawada", "Chennai"],
     "answer": "Amaravati"},

    {"q": "What is the capital of Telangana?",
     "options": ["Warangal", "Hyderabad", "Karimnagar", "Nizamabad"],
     "answer": "Hyderabad"},

    {"q": "What is the capital of Karnataka?",
     "options": ["Mysuru", "Bengaluru", "Mangaluru", "Hubballi"],
     "answer": "Bengaluru"},

    {"q": "What is the capital of Tamil Nadu?",
     "options": ["Madurai", "Chennai", "Salem", "Coimbatore"],
     "answer": "Chennai"},

    {"q": "What is the capital of Kerala?",
     "options": ["Kochi", "Kozhikode", "Thiruvananthapuram", "Thrissur"],
     "answer": "Thiruvananthapuram"},

    {"q": "What is the capital of Maharashtra?",
     "options": ["Pune", "Mumbai", "Nagpur", "Nashik"],
     "answer": "Mumbai"},

    {"q": "What is the capital of Gujarat?",
     "options": ["Surat", "Ahmedabad", "Gandhinagar", "Vadodara"],
     "answer": "Gandhinagar"},

    {"q": "What is the capital of Rajasthan?",
     "options": ["Jaipur", "Jodhpur", "Udaipur", "Ajmer"],
     "answer": "Jaipur"},

    {"q": "What is the capital of West Bengal?",
     "options": ["Howrah", "Kolkata", "Darjeeling", "Durgapur"],
     "answer": "Kolkata"},

    {"q": "What is the capital of Bihar?",
     "options": ["Gaya", "Patna", "Bhagalpur", "Muzaffarpur"],
     "answer": "Patna"},

    {"q": "What is the capital of Uttar Pradesh?",
     "options": ["Agra", "Kanpur", "Lucknow", "Varanasi"],
     "answer": "Lucknow"},

    {"q": "What is the capital of Madhya Pradesh?",
     "options": ["Indore", "Bhopal", "Gwalior", "Jabalpur"],
     "answer": "Bhopal"},

    {"q": "What is the capital of Odisha?",
     "options": ["Cuttack", "Puri", "Bhubaneswar", "Rourkela"],
     "answer": "Bhubaneswar"},

    {"q": "What is the capital of Assam?",
     "options": ["Guwahati", "Dispur", "Silchar", "Dibrugarh"],
     "answer": "Dispur"}
]

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Indian Capitals Quiz</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        * { box-sizing: border-box; }

        body {
            margin: 0;
            padding: 25px 12px;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #ff9933, white, #138808);
        }

        .container {
            max-width: 750px;
            margin: auto;
            padding: 25px;
            background: white;
            border-radius: 18px;
            box-shadow: 0 8px 25px #0002;
        }

        h1 {
            text-align: center;
            color: #172554;
        }

        .subtitle {
            text-align: center;
            color: #64748b;
        }

        .question {
            background: #f8fafc;
            padding: 18px;
            margin: 18px 0;
            border-left: 5px solid #ff9933;
            border-radius: 10px;
        }

        .option {
            display: block;
            padding: 10px;
            margin: 7px 0;
            border: 1px solid #ddd;
            border-radius: 8px;
            cursor: pointer;
        }

        .option:hover {
            background: #fff7ed;
        }

        input[type="radio"] {
            margin-right: 8px;
        }

        button, .retry {
            display: block;
            width: 100%;
            padding: 14px;
            border: none;
            border-radius: 9px;
            background: #172554;
            color: white;
            font-size: 17px;
            font-weight: bold;
            cursor: pointer;
            text-align: center;
            text-decoration: none;
        }

        button:hover, .retry:hover {
            background: #ea580c;
        }

        .result {
            margin-top: 25px;
            padding: 22px;
            border-radius: 12px;
            background: #ecfdf5;
            text-align: center;
        }

        .marks {
            font-size: 34px;
            font-weight: bold;
            color: #047857;
        }

        .correct { color: #15803d; }
        .wrong { color: #dc2626; }

        @media (max-width: 500px) {
            .container { padding: 15px; }
        }
    </style>
</head>

<body>
<div class="container">

    <h1>🇮🇳 Indian Capitals Quiz</h1>
    <p class="subtitle">15 Questions | 1 mark for each correct answer</p>

    <form method="POST">

        {% for q in questions %}
        {% set i = loop.index0 %}

        <div class="question">
            <h3>{{ loop.index }}. {{ q.q }}</h3>

            {% for option in q.options %}
            <label class="option">
                <input type="radio"
                       name="q{{ i }}"
                       value="{{ option }}"
                       {% if not submitted %}required{% endif %}
                       {% if submitted and answers[i] == option %}checked{% endif %}>
                {{ option }}
            </label>
            {% endfor %}

            {% if submitted %}
                {% if answers[i] == q.answer %}
                    <p class="correct">✓ Correct answer!</p>
                {% else %}
                    <p class="wrong">
                        ✗ Your answer:
                        {{ answers[i] if answers[i] else "Not answered" }}
                    </p>
                    <p class="correct">
                        Correct answer: {{ q.answer }}
                    </p>
                {% endif %}
            {% endif %}
        </div>
        {% endfor %}

        {% if not submitted %}
            <button type="submit">Submit Answers</button>
        {% endif %}

    </form>

    {% if submitted %}
    <div class="result" id="results">
        <h2>🎉 Your Final Results</h2>

        <p class="marks">{{ score }} / 15 Marks</p>

        <h3>Correct Answers: {{ correct }} / 15</h3>
        <h3>Wrong Answers: {{ wrong }}</h3>
        <h3>Percentage: {{ percentage }}%</h3>

        {% if score == 15 %}
            <h3>Excellent! Full marks! 🏆</h3>
        {% elif score >= 10 %}
            <h3>Very good! Keep it up! 👏</h3>
        {% elif score >= 5 %}
            <h3>Good try! Practice more. 👍</h3>
        {% else %}
            <h3>Keep learning. You can improve! 💪</h3>
        {% endif %}

        <a href="/" class="retry">Try Again</a>
    </div>
    {% endif %}

</div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    submitted = request.method == "POST"
    answers = [""] * len(questions)
    score = 0

    if submitted:
        for i, question in enumerate(questions):
            # Read the answer submitted for each question
            answers[i] = request.form.get(f"q{i}", "")

            # Award one mark for each correct answer
            if answers[i] == question["answer"]:
                score += 1

    correct = score
    wrong = len(questions) - correct
    percentage = round((score / len(questions)) * 100, 2)

    return render_template_string(
        HTML,
        questions=questions,
        submitted=submitted,
        answers=answers,
        score=score,
        correct=correct,
        wrong=wrong,
        percentage=percentage
    )


if __name__ == "__main__":
    app.run(debug=True)

