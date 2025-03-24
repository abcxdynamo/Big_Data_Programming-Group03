from base.base_model import BaseModel, db


class Enrollment(BaseModel):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    term_id = db.Column(db.Integer, db.ForeignKey('terms.id'))
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'))
    status = db.Column(db.SmallInteger, default=1, nullable=False) # 1: enrolled 2:graduated

    def __repr__(self):
        return f'<Enrollment#{self.id} {self.student_id}-{self.term_id}-{self.program_id}>'
