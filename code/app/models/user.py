from datetime import datetime
from sqlalchemy import Column, String, BigInteger, DateTime
from app.utils.snowflake_id_generator import snowflake_id_generator
from app.utils.extensions import db
from app.models.base_model import BaseModel
from app.schemas.user import UserResponse


class UserModel(db.Model, BaseModel):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, default=snowflake_id_generator.generate_id)
    mail = Column(String(64), index=True, unique=True)
    password = Column(String(120), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        return user if user else None

    @staticmethod
    def update_user(user, new_mail=None, new_password=None):
        if new_mail:
            user.mail = new_mail
        if new_password:
            user.password = new_password
        return user
