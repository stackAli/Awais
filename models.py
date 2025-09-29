from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()   # define db here

class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    tier = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    features = db.Column(db.Text, nullable=True)   # store list as text (split by line or JSON)
    impact = db.Column(db.Text, nullable=True)
    implementation = db.Column(db.String(100), nullable=True)
    investment = db.Column(db.String(100), nullable=True)
    highlight = db.Column(db.Boolean, default=False)
    premium = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Service {self.tier}: {self.title}>"
class CaseStudy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    challenge = db.Column(db.Text, nullable=False)
    solution = db.Column(db.Text, nullable=False)
    results = db.Column(db.Text, nullable=False)
    lottie_url = db.Column(db.String(500))
    image_url = db.Column(db.String(500))  # NEW
    button_url = db.Column(db.String(500))
