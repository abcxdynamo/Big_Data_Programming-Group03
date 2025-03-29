from base.base_model import BaseModel, db


class Grade(BaseModel):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    term_id = db.Column(db.Integer, db.ForeignKey('terms.id'))
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    final_grade = db.Column(db.Float, nullable=False, default=0.0)

    def __repr__(self):
        return f'<Grade#{self.id} {self.term_id} {self.program_id} {self.course_id}>'
