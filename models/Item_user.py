from config.database import db

class ItemUser(db.Model):
    __tablename__ = 'item_users'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(80), nullable=False)
    percentage = db.Column(db.String(120), nullable=False)
    image = db.Column(db.Text(), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 

    user = db.relationship('User', backref=db.backref('item_users', lazy=True))  

    def __repr__(self):
        return f'<ItemUser {self.label}>'
