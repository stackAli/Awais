from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# -------------------------
# Routes for web pages
# -------------------------

@app.route("/")
def home():
    return render_template("home.html", page="Home")

@app.route("/GrowthSystems")
def about():
    return render_template("growth.html", page="Growth Systems")

@app.route("/successstories")
def successstories():
    return render_template("successstories.html", page="Success Stories")
@app.route("/contactus")
def contactus():
    return render_template("contactus.html", page="Get Started")





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
    
