from wanted import db

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name_ko = db.Column(db.String(50), nullable=True, unique=True)
    company_name_en = db.Column(db.String(50), nullable=True, unique=True)
    company_name_ja = db.Column(db.String(50), nullable=True, unique=True)
    tag_ko = db.Column(db.String(50), nullable=True)
    tag_en = db.Column(db.String(50), nullable=True)
    tag_ja = db.Column(db.String(50), nullable=True)