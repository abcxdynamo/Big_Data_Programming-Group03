from base.base_model import BaseModel, db


class Attendance(BaseModel):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tp_course_id = db.Column(db.Integer, db.ForeignKey('term_program_courses.id'))
    attendance_in_percent = db.Column(db.Numeric(5, 2), nullable=False)

    def __repr__(self):
        return f'<Attendance#{self.id}>'
