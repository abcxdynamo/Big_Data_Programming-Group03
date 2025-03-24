from base.base_model import BaseModel, db


class Program(BaseModel):
    __tablename__ = 'programs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)
    description=db.Column(db.Text)
    co_op = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Program {self.name}>'
