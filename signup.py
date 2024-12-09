from database import db

class SignupInfo(db.Model):
    __tablename__ = "signup_info"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    zipcode = db.Column(db.String(20), nullable=False)
