from flask import Flask, render_template, request, jsonify
import math, time, hashlib

app = Flask(__name__)

def analyze_password(password):
    length = len(password)
    charset = 0
    if any(c.islower() for c in password): charset += 26
    if any(c.isupper() for c in password): charset += 26
    if any(c.isdigit() for c in password): charset += 10
    if any(c in "!@#$%^&*()_+-=[]{}|;:',.<>?/" for c in password): charset += 32

    entropy = round(length * math.log2(charset)) if charset > 0 else 0

    if entropy < 28:
        label = "Very Weak"
    elif entropy < 36:
        label = "Weak"
    elif entropy < 60:
        label = "Moderate"
    elif entropy < 128:
        label = "Strong"
    else:
        label = "Very Strong"

    crack_time = entropy ** 2
    return {
        "entropy": entropy,
        "strength_label": label,
        "crack_time": f"{crack_time} seconds"
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    password = request.json.get("password", "")
    result = analyze_password(password)
    entry_id = hashlib.sha1((password + str(time.time())).encode()).hexdigest()[:8]
    result["id"] = entry_id
    result["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    return jsonify(result)

@app.route("/report")
def report():
    return render_template("report.html", entries=[])

if __name__ == "__main__":
    app.run(debug=True)
