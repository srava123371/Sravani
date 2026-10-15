from flask import Flask, request, render_template_string
import urllib.request
import urllib.parse
import json

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Weather Now</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            padding: 30px 15px;
            min-height: 100vh;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #dbeafe, #ede9fe, #cffafe);
            color: #172554;
        }

        .container {
            max-width: 700px;
            margin: 30px auto;
            background: white;
            padding: 30px;
            border-radius: 22px;
            box-shadow: 0 10px 35px #00000015;
        }

        h1 {
            text-align: center;
            margin-bottom: 8px;
        }

        .subtitle {
            text-align: center;
            color: #64748b;
            margin-bottom: 25px;
        }

        form {
            display: flex;
            gap: 10px;
        }

        input {
            flex: 1;
            min-width: 0;
            padding: 14px;
            border: 1px solid #cbd5e1;
            border-radius: 10px;
            font-size: 16px;
        }

        button {
            padding: 14px 18px;
            border: none;
            border-radius: 10px;
            background: #2563eb;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover {
            background: #1d4ed8;
        }

        .error {
            margin-top: 20px;
            padding: 12px;
            background: #fee2e2;
            color: #b91c1c;
            border-radius: 10px;
        }

        .report {
            margin-top: 28px;
        }

        .location {
            font-size: 22px;
            font-weight: bold;
        }

        .condition {
            color: #2563eb;
            margin-top: 8px;
        }

        .temperature {
            font-size: 55px;
            font-weight: bold;
            margin: 20px 0 5px;
        }

        .feels {
            color: #64748b;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            margin-top: 25px;
        }

        .card {
            padding: 16px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 13px;
        }

        .label {
            color: #64748b;
            font-size: 13px;
            margin-bottom: 8px;
        }

        .value {
            font-size: 18px;
            font-weight: bold;
            overflow-wrap: anywhere;
        }

        h3 {
            margin-top: 28px;
            color: #475569;
            font-size: 15px;
        }

        footer {
            text-align: center;
            color: #94a3b8;
            font-size: 12px;
            margin-top: 25px;
        }

        @media (max-width: 480px) {
            form {
                flex-direction: column;
            }

            button {
                width: 100%;
            }

            .container {
                padding: 20px;
            }

            .temperature {
                font-size: 45px;
            }
        }
    </style>
</head>

<body>
<div class="container">

    <h1>🌤️ Weather Now</h1>
    <p class="subtitle">Live weather report for any city</p>

    <form method="POST">
        <input
            type="text"
            name="city"
            placeholder="Enter city, e.g. Mysuru"
            value="{{ city }}"
            required
        >
        <button type="submit">Get Weather</button>
    </form>

    {% if error %}
        <div class="error">{{ error }}</div>
    {% endif %}

    {% if weather %}
        <div class="report">

            <div class="location">📍 {{ weather.location }}</div>
            <div class="condition">{{ weather.condition }}</div>

            <div class="temperature">
                {{ weather.temperature }}°C
            </div>

            <div class="feels">
                Feels like {{ weather.feels }}°C
            </div>

            <h3>CURRENT WEATHER</h3>

            <div class="grid">
                <div class="card">
                    <div class="label">💧 Humidity</div>
                    <div class="value">{{ weather.humidity }}%</div>
                </div>

                <div class="card">
                    <div class="label">💨 Wind Speed</div>
                    <div class="value">{{ weather.wind }} km/h</div>
                </div>

                <div class="card">
                    <div class="label">☁️ Cloud Cover</div>
                    <div class="value">{{ weather.cloud }}%</div>
                </div>

                <div class="card">
                    <div class="label">🌧️ Precipitation</div>
                    <div class="value">{{ weather.rain }} mm</div>
                </div>

                <div class="card">
                    <div class="label">⬆️ Today's High</div>
                    <div class="value">{{ weather.high }}°C</div>
                </div>

                <div class="card">
                    <div class="label">⬇️ Today's Low</div>
                    <div class="value">{{ weather.low }}°C</div>
                </div>

                <div class="card">
                    <div class="label">🌅 Sunrise</div>
                    <div class="value">{{ weather.sunrise }}</div>
                </div>

                <div class="card">
                    <div class="label">🌇 Sunset</div>
                    <div class="value">{{ weather.sunset }}</div>
                </div>
            </div>
        </div>
    {% endif %}

    <footer>Weather data by Open-Meteo · Free API</footer>
</div>
</body>
</html>
"""


def fetch_json(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "WeatherNow/1.0"}
    )
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def get_weather(city):
    # Find the city's latitude and longitude
    query = urllib.parse.urlencode({
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    })

    places = fetch_json(
        "https://geocoding-api.open-meteo.com/v1/search?" + query
    ).get("results", [])

    if not places:
        return None

    place = places[0]

    # Get current weather and today's forecast
    params = urllib.parse.urlencode({
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "current": (
            "temperature_2m,relative_humidity_2m,"
            "apparent_temperature,precipitation,weather_code,"
            "cloud_cover,wind_speed_10m"
        ),
        "daily": (
            "temperature_2m_max,temperature_2m_min,"
            "sunrise,sunset"
        ),
        "timezone": place.get("timezone", "auto"),
        "forecast_days": 1
    })

    data = fetch_json(
        "https://api.open-meteo.com/v1/forecast?" + params
    )

    current = data["current"]
    daily = data["daily"]

    descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Heavy drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Rain showers",
        81: "Moderate rain showers",
        82: "Heavy rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with heavy hail"
    }

    location = ", ".join(
        item for item in [
            place.get("name"),
            place.get("admin1"),
            place.get("country")
        ] if item
    )

    return {
        "location": location,
        "condition": descriptions.get(
            current["weather_code"], "Weather condition unavailable"
        ),
        "temperature": current["temperature_2m"],
        "feels": current["apparent_temperature"],
        "humidity": current["relative_humidity_2m"],
        "wind": current["wind_speed_10m"],
        "cloud": current["cloud_cover"],
        "rain": current["precipitation"],
        "high": daily["temperature_2m_max"][0],
        "low": daily["temperature_2m_min"][0],
        "sunrise": daily["sunrise"][0].split("T")[-1],
        "sunset": daily["sunset"][0].split("T")[-1]
    }


@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = None
    city = ""

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        if city:
            try:
                weather = get_weather(city)

                if weather is None:
                    error = "City not found. Please enter another city."

            except Exception:
                error = (
                    "Unable to get weather. "
                    "Check your internet connection and try again."
                )

    return render_template_string(
        HTML,
        weather=weather,
        error=error,
        city=city
    )


if __name__ == "__main__":
    app.run(debug=True)
