from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

from base.base_model import BaseModel, db


class TermProgramCourse(BaseModel):
    __tablename__ = 'term_program_courses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    term_id = db.Column(db.Integer, ForeignKey('terms.id'), nullable=False)
    program_id = db.Column(db.Integer, ForeignKey('programs.id'), nullable=False)
    course_id = db.Column(db.Integer, ForeignKey('courses.id'), nullable=False)
    instructor_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    section = db.Column(db.SmallInteger, default=1, nullable=False)

    # course = relationship("Course", backref="term_program_courses")

    __table_args__ = (
        UniqueConstraint('term_id', 'program_id', 'course_id', name='uq_term_program_course'),
    )

    def __repr__(self):
        return f'<TermProgramCourse {self.id}>'
