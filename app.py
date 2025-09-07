from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# -------------------------
# Routes for web pages
# -------------------------

@app.route("/")
def home():
    return render_template("home.html", page="Home")

@app.route("/about")
def about():
    return render_template("about.html", page="About Us")

@app.route("/admin")
def admin():
    return render_template("admin.html", page="Admin")

@app.route("/contact")
def contact():
    return render_template("contact.html", page="Contact Us")

@app.route("/services")
def services():
    return render_template("services.html", page="Services")

@app.route("/casestudies")
def case_studies():
    return render_template("casestudies.html", page="Case Studies")

# -------------------------
# Example API
# -------------------------

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    reply = f"You said: {user_message}"
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
