from models import User, UserRole
from models import UserToken
from utils.auth import generate_jwt_token, decode_jwt_token
from utils.common import send_email
from utils.time import utcnow


class UserService:

    @staticmethod
    def get_user_by_email(email):
        user = User.query.filter_by(email=email).first()
        assert user is not None, f"email {email} not found"
        return user

    @staticmethod
    def get_user_by_id(user_id):
        user = User.query.filter_by(id=user_id).first()
        assert user is not None, f"user_id#{user_id} not found"
        return user

    @staticmethod
    def query_user_list(query=None):
        if query is None:
            query = {}
        ids = query.get('ids')
        if not ids or len(ids) == 0:
            return []
        if isinstance(ids, str):
            # ids = list(map(int, ids.split(',')))
            ids = [int(x.strip()) for x in ids.split(',')]
        elif isinstance(ids, list):
            pass
        else:
            raise TypeError('ids must be a string or a list of ints')
        return User.query.filter(User.id.in_(ids)).all()


    @staticmethod
    def send_otp(email):
        user = UserService.get_user_by_email(email)

        # First check if there is an available OTP and make sure there is only one available OTP
        user_token = UserToken.query.filter(
            UserToken.user_id == user.id,
            UserToken.expires > utcnow(),
            UserToken.token.is_(None)
        ).first()
        if user_token:
            user_token.reset_expired()
        else:
            user_token = UserToken(user_id=user.id)
        user_token.save()

        # FIXME
        SEND_OTP_SUBJECT = f"SEND_OTP_SUBJECT"
        SEND_OPT_BODY = f"OTP: {user_token.otp}"
        send_email(email, SEND_OTP_SUBJECT, SEND_OPT_BODY)
        return user_token.otp

    @staticmethod
    def validate_otp(email, otp):
        user = UserService.get_user_by_email(email)
        user_token = (UserToken.query
                      .filter_by(user_id=user.id, otp=otp)
                      .filter(UserToken.expires >= utcnow(),
                              UserToken.token.is_(None))
                      .first())
        assert user_token is not None, f"Invalid credentials"
        user_role = UserRole.query.filter_by(id=user.role_id).first()
        # token = generate_jwt_token(user.email, user_role.name)
        token = generate_jwt_token({
            "user_id": user.id,
            "email": user.email,
            "role_id": user_role.id,
            "role_name": user_role.name
        })
        user_token.token = token
        user_token.save()
        return {
            "user_id": user.id,
            "email": user.email,
            "role_id": user_role.id,
            "role_name": user_role.name,
            "token": token
        }

    @staticmethod
    def test():
        email = "cc@conestogac.on.ca"
        print(email)
        otp = UserService.send_otp(email)
        print(otp)
        jwt_token = UserService.validate_otp(email, otp)
        print(jwt_token)
        decoded = decode_jwt_token(jwt_token)
        print(decoded)
        return decoded
