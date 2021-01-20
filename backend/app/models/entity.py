from app import db


class Entity(db.Model):
    __tablename__ = 'discharge_labels'
    id = db.Column(db.Integer, primary_key=True)
    mention = db.Column(db.String(255))
    pos_b = db.Column(db.String(11))
    pos_e = db.Column(db.String(11))
    category = db.Column(db.String(255))
    decoration = db.Column(db.String(255))
    content_id = db.Column(db.String(11))
    editUser = db.Column(db.String(16))
    editTime = db.Column(db.String(13))

    def __repr__(self):
        return '<Role %r>' % self.mention
