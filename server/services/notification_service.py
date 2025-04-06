from sqlalchemy import text
from sqlalchemy.dialects import mysql

from base.base_model import db_execute
from models import User, UserRole
from models import UserToken
from models.notification.notification import Notification
from utils.auth import generate_jwt_token, decode_jwt_token
from utils.common import send_email
from utils.time import utcnow


class NotificationService:

    @staticmethod
    def get_user_notifications(user_id):
        return (Notification.query
                .filter_by(user_id=user_id)
                .order_by(text("id desc"))
                .all())

    @staticmethod
    def check_news(user_id):
        result = db_execute("select count(*) cnt from notifications where user_id=:user_id and read_status=0", {
            "user_id": user_id
        })[0]
        return result["cnt"]

    @staticmethod
    def get_notification_info(notification_id):
        return Notification.query.filter_by(id=notification_id).first()

    @staticmethod
    def new_notification(data):
        (Notification(user_id=data['user_id'],
                      title=data['title'],
                      content=data['content'],
                      create_user_id=data['create_user_id'])
         .save())

    @staticmethod
    def read_notification(notification_id):
        notification = Notification.query.filter_by(id=notification_id).first()
        notification.read_status = True
        notification.save()
