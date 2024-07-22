from datetime import datetime
from sqlalchemy import Column, String, BigInteger, DateTime
from app.utils.snowflake_id_generator import snowflake_id_generator
from app.utils.extensions import db
from app.models.base_model import BaseModel
from app.schemas.user import UserResponse


class OrderModel(db.Model, BaseModel):
    __tablename__ = 'orders'
    id = Column(BigInteger, primary_key=True, default=snowflake_id_generator.generate_id)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    @staticmethod
    def get_all_orders():
        return OrderModel.query.all()
