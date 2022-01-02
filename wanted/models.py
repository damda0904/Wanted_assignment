from wanted import db

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Company_name(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'))
    name = db.Column(db.String(100), nullable=False)
    language = db.Column(db.String(10), nullable=False)

class Company_tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'))
    tag = db.Column(db.String(200), nullable=False)
    language= db.Column(db.String(10), nullable=False)