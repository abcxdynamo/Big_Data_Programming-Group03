from flask import request

from services.notification_service import NotificationService
from base.base_blueprint import BaseBlueprint, OK
import time
from utils.model import to_dict_list

notification_bp = BaseBlueprint('notifications', __name__)


@notification_bp.route('/list/<int:user_id>', methods=['GET'])
def get_user_notifications(user_id):
    result = to_dict_list(NotificationService.get_user_notifications(user_id))
    print(result)
    return result


@notification_bp.route('/count_news/<int:user_id>', methods=['GET'])
def count_news_user_notifications(user_id):
    news_count = NotificationService.check_news(user_id)
    return {
        'news_count': news_count
    }


@notification_bp.route('/check_news/<int:user_id>', methods=['GET'])
def check_news_user_notifications(user_id):
    timeout = 30
    start_time = time.time()
    news_count = NotificationService.check_news(user_id)
    while news_count <= 0 and (time.time() - start_time) < timeout:
        time.sleep(1)  # Detect once per second
        news_count = NotificationService.check_news(user_id)
    return {
        'news_count': news_count
    }


@notification_bp.route('/<int:notification_id>', methods=['GET'])
def get_notification_info(notification_id):
    return NotificationService.get_notification_info(notification_id)


@notification_bp.route('/new', methods=['POST'])
def new_notification():
    NotificationService.new_notification(request.parsed_data)
    return OK


@notification_bp.route('/<int:notification_id>/read', methods=['POST'])
def read_notification(notification_id):
    NotificationService.read_notification(notification_id)
    return OK
