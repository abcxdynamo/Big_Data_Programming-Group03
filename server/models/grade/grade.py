from sqlalchemy import text

from base.base_model import BaseModel, db


class Grade(BaseModel):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tp_course_id = db.Column(db.Integer, db.ForeignKey('term_program_courses.id'))
    final_grade = db.Column(db.Float, nullable=False, default=0.0, server_default=text('0.0'))
    final_gpa = db.Column(db.Float, nullable=False, default=0.0, server_default=text('0.0'))
    feedback = db.Column(db.Text)

    def __repr__(self):
        return f'<Grade#{self.id}>'
