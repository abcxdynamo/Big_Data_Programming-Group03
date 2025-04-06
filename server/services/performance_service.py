from models import PerformancePrediction
from sqlalchemy import and_
from datetime import datetime

class PerformanceService:
    @staticmethod
    def get_all_predictions():
        return PerformancePrediction.query.filter_by(is_deleted=False).order_by(PerformancePrediction.term_id).all()
    
    @staticmethod
    def get_predictions_by_student(student_id):
        return PerformancePrediction.query.filter_by(student_id=student_id, is_deleted=False).order_by(PerformancePrediction.term_id.asc()).all()

    @staticmethod
    def to_dict_list(results):
        return [
            {
                "student_id": r.student_id,
                "term_id": r.term_id,
                "predicted_gpa": float(r.predicted_gpa),
                "predicted_average": float(r.predicted_average),
                "prediction_date": r.prediction_date.isoformat() if r.prediction_date else None
            }
            for r in results
        ]
