from base.base_model import BaseModel, db


class Course(BaseModel):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(128), nullable=False, unique=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(2048))

    def __repr__(self):
        return f'<Course#{self.id} {self.code} {self.name}>'
