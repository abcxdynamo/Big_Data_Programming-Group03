from base.base_model import BaseModel, db


class User(BaseModel):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), unique=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('user_roles.id'))

    @property
    def fullname(self):
        return self.first_name + ' ' + self.last_name

    def __repr__(self):
        return f'<User {self.email}>'
