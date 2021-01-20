from app import db


class Content(db.Model):
    __tablename__ = 'discharge_record'
    id = db.Column(db.Integer, primary_key=True)
    medical_treatment = db.Column(db.String(2048))

    def __repr__(self):
        return '<Role %r>' % self.content
