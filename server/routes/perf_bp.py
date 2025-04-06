from flask import request, jsonify

from services.performance_service import PerformanceService
from base.base_blueprint import BaseBlueprint, OK
from utils.auth import auth_required
from utils.model import to_dict_list

perf_bp = BaseBlueprint('PerformancePrediction', __name__)

@perf_bp.route('/performance_predictions', methods=['GET'])
def get_performance_predictions():
    student_id = request.args.get('student_id')
    if student_id:
        records = PerformanceService.get_predictions_by_student(student_id)
    else:
        records = PerformanceService.get_all_predictions()

    return jsonify(PerformanceService.to_dict_list(records))
