from flask import Flask, request, jsonify, render_template, Blueprint, redirect, url_for, flash
from models import db, Service, CaseStudy   # <-- import CaseStudy too

# -------------------------
# App setup
# -------------------------
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SECRET_KEY"] = "your_secret_key"

db.init_app(app)   # initialize db with this app

# -------------------------
# Services Blueprint
# -------------------------
services_bp = Blueprint("services", __name__)

@services_bp.route("/admin/services")
def admin_services():
    services = Service.query.order_by(Service.tier).all()
    case_studies = CaseStudy.query.all()
    return render_template("admin_services.html", services=services, case_studies=case_studies)

@services_bp.route("/admin/services/add", methods=["GET", "POST"])
def add_service():
    if request.method == "POST":
        service = Service(
            tier=request.form["tier"],
            title=request.form["title"],
            features=request.form["features"],
            impact=request.form["impact"],
            implementation=request.form["implementation"],
            investment=request.form["investment"],
            highlight="highlight" in request.form,
            premium="premium" in request.form
        )
        db.session.add(service)
        db.session.commit()
        flash("Service added successfully!", "success")
        return redirect(url_for("services.admin_services"))
    return render_template("add_service.html")

@services_bp.route("/admin/services/edit/<int:id>", methods=["GET", "POST"])
def edit_service(id):
    service = Service.query.get_or_404(id)
    if request.method == "POST":
        service.tier = request.form["tier"]
        service.title = request.form["title"]
        service.features = request.form["features"]
        service.impact = request.form["impact"]
        service.implementation = request.form["implementation"]
        service.investment = request.form["investment"]
        service.highlight = "highlight" in request.form
        service.premium = "premium" in request.form
        db.session.commit()
        flash("Service updated successfully!", "success")
        return redirect(url_for("services.admin_services"))
    return render_template("edit_service.html", service=service)

@services_bp.route("/admin/services/delete/<int:id>")
def delete_service(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    flash("Service deleted successfully!", "success")
    return redirect(url_for("services.admin_services"))

# -------------------------
# Case Studies Blueprint
# -------------------------
casestudies_bp = Blueprint("casestudies", __name__)

@casestudies_bp.route("/admin/casestudy")
def admin_case_study():
    return redirect(url_for("services.admin_services"))  # always use the same page

@casestudies_bp.route("/admin/casestudy/add", methods=["GET", "POST"])
def add_success_story():
    if request.method == "POST":
        case_study = CaseStudy(
            title=request.form["title"],
            challenge=request.form["challenge"],
            solution=request.form["solution"],
            results=request.form["results"],
            lottie_url=request.form["lottie_url"],
            button_url=request.form["button_url"]
        )
        db.session.add(case_study)
        db.session.commit()
        flash("Success story added successfully!", "success")
        return redirect(url_for("services.admin_services"))
    return render_template("add_case_study.html")

@casestudies_bp.route("/admin/casestudy/edit/<int:id>", methods=["GET", "POST"])
def edit_success_story(id):
    case_study = CaseStudy.query.get_or_404(id)
    if request.method == "POST":
        case_study.title = request.form["title"]
        case_study.challenge = request.form["challenge"]
        case_study.solution = request.form["solution"]
        case_study.results = request.form["results"]
        case_study.lottie_url = request.form["lottie_url"]
        case_study.button_url = request.form["button_url"]

        db.session.commit()
        flash("Success story updated successfully!", "success")
        return redirect(url_for("services.admin_services"))

    return render_template("edit_case_study.html", case_study=case_study)

@casestudies_bp.route("/admin/casestudy/delete/<int:id>")
def delete_success_story(id):
    case_study = CaseStudy.query.get_or_404(id)
    db.session.delete(case_study)
    db.session.commit()
    flash("Success story deleted successfully!", "success")
    return redirect(url_for("services.admin_services"))

# -------------------------
# Register Blueprints
# -------------------------
app.register_blueprint(services_bp)
app.register_blueprint(casestudies_bp)

# -------------------------
# Basic Pages
# -------------------------
@app.route("/")
def home():
    return render_template("home.html", page="Home")

@app.route("/GrowthSystems")
def growth_systems():
    services = Service.query.order_by(Service.tier).all()
    return render_template("growth.html", page="Growth Systems", services=services)

@app.route("/successstories")
def successstories():
    case_studies = CaseStudy.query.all()  # show all success stories
    return render_template(
        "successstories.html",
        page="Success Stories",
        case_studies=case_studies
    )

@app.route("/contactus")
def contactus():
    return render_template("contactus.html", page="Get Started")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    reply = f"You said: {user_message}"
    return jsonify({"reply": reply})

# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
