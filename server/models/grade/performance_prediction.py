from sqlalchemy import UniqueConstraint

from base.base_model import BaseModel, db
from utils.time import utcnow


class PerformancePrediction(BaseModel):
    __tablename__ = 'performance_predictions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    term_id = db.Column(db.Integer, db.ForeignKey('terms.id'))
    predicted_gpa = db.Column(db.Numeric(3, 2), nullable=False)
    predicted_average = db.Column(db.Numeric(5, 2), nullable=False)
    prediction_date = db.Column(db.DateTime, default=utcnow)

    __table_args__ = (
        UniqueConstraint('student_id', 'term_id', name='uq_student_term_prediction'),
    )

    def __repr__(self):
        return f'<PerformancePrediction#{self.id}>'
