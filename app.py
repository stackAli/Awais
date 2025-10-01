import os
from flask import Flask, request, jsonify, render_template, Blueprint, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from models import db, Service, CaseStudy, ContactInfo   # <-- added ContactInfo model

# -------------------------
# App setup
# -------------------------
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SECRET_KEY"] = "your_secret_key"

# Upload settings
UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db.init_app(app)

# -------------------------
# Admin Auth (one user only)
# -------------------------
ADMIN_USERNAME = "admin"
# store hashed password instead of plain text
ADMIN_PASSWORD_HASH = generate_password_hash("admin123")  # change your password here!

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            flash("Please log in to access admin.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session["logged_in"] = True
            flash("Logged in successfully!", "success")
            return redirect(url_for("services.admin_services"))
        else:
            flash("Invalid credentials", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("Logged out successfully!", "info")
    return redirect(url_for("login"))

# -------------------------
# Helpers
# -------------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# -------------------------
# Services Blueprint
# -------------------------
services_bp = Blueprint("services", __name__)

@services_bp.route("/admin/services")
@login_required
def admin_services():
    services = Service.query.order_by(Service.tier).all()
    case_studies = CaseStudy.query.all()
    contact = ContactInfo.query.first()
    return render_template("admin_services.html", services=services, case_studies=case_studies, contact=contact)

@services_bp.route("/admin/services/add", methods=["GET", "POST"])
@login_required
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
@login_required
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
@login_required
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
@login_required
def admin_case_study():
    return redirect(url_for("services.admin_services"))

@casestudies_bp.route("/admin/casestudy/add", methods=["GET", "POST"])
@login_required
def add_success_story():
    if request.method == "POST":
        image_file = request.files.get("image")
        filename = None

        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image_file.save(filepath)

        case_study = CaseStudy(
            title=request.form["title"],
            challenge=request.form["challenge"],
            solution=request.form["solution"],
            results=request.form["results"],
            lottie_url=request.form["lottie_url"],
            button_url=request.form["button_url"],
            image_url=filename
        )

        db.session.add(case_study)
        db.session.commit()
        flash("Success story added successfully!", "success")
        return redirect(url_for("services.admin_services"))

    return render_template("add_case_study.html")

@casestudies_bp.route("/admin/casestudy/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_success_story(id):
    case_study = CaseStudy.query.get_or_404(id)

    if request.method == "POST":
        case_study.title = request.form["title"]
        case_study.challenge = request.form["challenge"]
        case_study.solution = request.form["solution"]
        case_study.results = request.form["results"]
        case_study.lottie_url = request.form["lottie_url"]
        case_study.button_url = request.form["button_url"]

        image_file = request.files.get("image")
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image_file.save(filepath)
            case_study.image_url = f"/static/uploads/{filename}"

        db.session.commit()
        flash("Success story updated successfully!", "success")
        return redirect(url_for("services.admin_services"))

    return render_template("edit_case_study.html", case_study=case_study)

@casestudies_bp.route("/admin/casestudy/delete/<int:id>")
@login_required
def delete_success_story(id):
    case_study = CaseStudy.query.get_or_404(id)
    db.session.delete(case_study)
    db.session.commit()
    flash("Success story deleted successfully!", "success")
    return redirect(url_for("services.admin_services"))

# -------------------------
# Contact Info (Admin only)
# -------------------------
@services_bp.route("/admin/contact/update", methods=["POST"])
@login_required
def update_contact():
    contact = ContactInfo.query.first()
    if not contact:
        contact = ContactInfo(email="", phone="", hours="")
        db.session.add(contact)
        db.session.commit()

    contact.email = request.form.get("contact_email")
    contact.phone = request.form.get("contact_phone")
    contact.hours = request.form.get("contact_hours")
    db.session.commit()

    flash("Contact info updated successfully!", "success")
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

@app.route("/InteractiveDemo")
def interactive_demo():
    contact = ContactInfo.query.first()
    return render_template(
        "interactive_demo.html",
        page="Interactive Demo",
        contact_email=contact.email if contact else "hello@yourdomain.com",
        contact_phone=contact.phone if contact else "+1234567890",
        contact_hours=contact.hours if contact else "Mon-Fri, 9AM-6PM EST"
    )

@app.route("/successstories")
def successstories():
    case_studies = CaseStudy.query.all()
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
