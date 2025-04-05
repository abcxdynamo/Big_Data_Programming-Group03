from email.policy import default

from base.base_model import BaseModel, db
from utils.time import utcnow


class StudentsGradesArchive(BaseModel):
    __tablename__ = 'students_grades_archive'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    archive_id = db.Column(db.Integer, db.ForeignKey('students_archive.id'), nullable=False)
    tp_course_id = db.Column(db.Integer, db.ForeignKey('term_program_courses.id'), nullable=False)
    grade = db.Column(db.Float, nullable=False)
    gpa = db.Column(db.Float, nullable=False, default=0.0)
    attendance_percent = db.Column(db.Numeric(5, 2), nullable=False)

    def __repr__(self):
        return f'<StudentsGradesArchive#{self.id}>'
