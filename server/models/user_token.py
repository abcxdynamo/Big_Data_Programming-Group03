from base.base_model import BaseModel, db
from utils.common import generate_otp
from utils.time import utcnow, delta


def default_expiration():
    return utcnow() + delta(minutes=5)


class UserToken(BaseModel):
    __tablename__ = 'user_tokens'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    otp = db.Column(db.String(6), nullable=False, default=generate_otp)
    # OTP expires time
    expires = db.Column(db.DateTime, nullable=False, default=default_expiration)
    # generate JWT Token after validate OTP
    token = db.Column(db.String(255), nullable=True)

    def reset_expired(self):
        self.expires = default_expiration()
