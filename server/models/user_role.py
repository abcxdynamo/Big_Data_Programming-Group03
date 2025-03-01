from base.base_model import BaseModel, db


class UserRole(BaseModel):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'