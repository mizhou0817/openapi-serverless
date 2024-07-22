# app/routes/user_routes.py
from flask_openapi3 import APIBlueprint, Tag
from app.utils.response import (
    SuccessResponse,
    CreatedResponse,
    InternalServerErrorResponse,
    NoContentResponse
)
from sqlalchemy.exc import IntegrityError
from app.models.order import OrderModel
from app.schemas.user import UserBody, UserPath, UserResponse
from app.utils.extensions import db

blueprint_order = APIBlueprint('/order', __name__, url_prefix='/api')


class OrderRouter():
    account_tag = Tag(name='Order', description='Order Management')

    @staticmethod
    @blueprint_order.get(
        '/order',
        tags=[account_tag],
        summary='get user',
        responses={200: UserResponse}
    )
    def get_orders():
        orders = OrderModel.get_all_orders()
        return SuccessResponse(
            message='Orders retrieved successfully',
            data=[OrderModel.from_user_model(order) for order in orders]
        ).model_dump(), 200
