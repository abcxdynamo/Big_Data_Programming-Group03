from sqlalchemy import func, text

from base.base_model import BaseModel, db
from utils.time import utcnow


class StudentsArchive(BaseModel):
    __tablename__ = 'students_archive'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_email = db.Column(db.String(128), nullable=False)
    student_first_name = db.Column(db.String(128), nullable=False)
    student_last_name = db.Column(db.String(128), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)
    cgpa = db.Column(db.Numeric(3, 2), nullable=False)
    graduation_date = db.Column(db.Date, nullable=False)
    career = db.Column(db.String(300), nullable=False, default='Others', server_default='Others')
    archived_date = db.Column(db.DateTime, nullable=False, default=utcnow, server_default=text('CURRENT_TIMESTAMP'))

    def __repr__(self):
        return f'<StudentsArchive#{self.id}>'
