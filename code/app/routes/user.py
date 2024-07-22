# app/routes/user_routes.py
from flask_openapi3 import APIBlueprint, Tag
from app.utils.response import (
    SuccessResponse,
    CreatedResponse,
    InternalServerErrorResponse,
    NoContentResponse
)
from sqlalchemy.exc import IntegrityError
from app.models.user import UserModel
from app.schemas.user import UserBody, UserPath, UserResponse
from app.utils.extensions import db

blueprint_user = APIBlueprint('/user', __name__, url_prefix='/api')


class UserRouter():
    account_tag = Tag(name='User', description='User Management')

    @staticmethod
    @blueprint_user.get(
        '/users',
        tags=[account_tag],
        summary='get user',
        responses={200: UserResponse}
    )
    def get_users():
        users = UserModel.get_all_users()
        return SuccessResponse(
            message='Users retrieved successfully',
            data=[UserResponse.from_user_model(user) for user in users]
        ).model_dump(), 200

    @staticmethod
    @blueprint_user.post(
        '/users',
        tags=[account_tag],
        summary='add user',
        responses={200: UserResponse, 500: InternalServerErrorResponse}
    )
    # Inside add_user method
    def add_user(body: UserBody):
        user = UserModel.from_dict({"mail": body.mail, "password": body.password})
        try:
            db.session.add(user)
            db.session.commit()
            return CreatedResponse(
                message="User created successfully",
                data=dict(UserResponse.from_user_model(user))
            ).model_dump(), 200
        except IntegrityError:
            db.session.rollback()
            return InternalServerErrorResponse(
                message="User creation failed, possibly due to duplicate entry"
            ).model_dump(), 200

    @staticmethod
    @blueprint_user.put(
        '/users/<string:id>',
        tags=[account_tag],
        summary='modify user',
        responses={200: SuccessResponse, 204: NoContentResponse}
    )
    def modify_user(path: UserPath, body: UserBody):
        user = UserModel.get_user_by_id(path.id)
        if not user:
            return NoContentResponse(message='User not found').model_dump(), 200
        user = UserModel.update_user(user, body.mail, body.password)

        try:
            db.session.commit()
            return SuccessResponse(
                message='User updated successfully',
                data={"user": UserResponse.from_user_model(user)}
            ).model_dump(), 200
        except IntegrityError:
            db.session.rollback()
            return InternalServerErrorResponse(
                message="User creation failed, possibly due to duplicate entry"
            ).model_dump(), 200
