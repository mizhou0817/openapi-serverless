# app/routes/user_routes.py
from flask_openapi3 import APIBlueprint, Tag
from app.utils.response import (
    SuccessResponse,
    CreatedResponse,
    InternalServerErrorResponse,
    NoContentResponse
)
from sqlalchemy.exc import IntegrityError
from app.models.transaction import TransactionModel
from app.schemas.user import UserPath
from app.schemas.transaction import TransactionResponse
from app.utils.extensions import db

blueprint_transaction = APIBlueprint('/transaction', __name__, url_prefix='/api')


class TransactionRouter():
    account_tag = Tag(name='Transaction', description='Transaction Management')

    @staticmethod
    @blueprint_transaction.get(
        '/transactions/<string:id>',
        tags=[account_tag],
        summary='get transactions by user id',
        responses={200: TransactionResponse}
    )
    def get_transactions(path: UserPath):
        transactions = TransactionModel.get_txs_by_user_id(path.id)
        return SuccessResponse(
            message='Transaction retrieved successfully',
            data=[TransactionResponse.from_transaction_model(transaction) for transaction in transactions]
        ).model_dump(), 200
