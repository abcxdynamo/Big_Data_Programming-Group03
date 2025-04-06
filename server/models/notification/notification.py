from email.policy import default

from base.base_model import BaseModel, db


class Notification(BaseModel):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text)
    read_status = db.Column(db.Boolean, default=False)
    create_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Notification#{self.id}>'
