from flask_openapi3 import APIBlueprint, Tag
from app.utils import create_keystore
from app.utils.response import (
    SuccessResponse,
    NoContentResponse
)
from app.models.ether_address import EtherAddressModel
from app.models.user import UserModel
from app.schemas.user import UserPath, UserResponse
from app.schemas.ether_address import EtherAddressResponse
from dotenv import load_dotenv
import os

load_dotenv()

blueprint_ether = APIBlueprint('/ether', __name__, url_prefix='/api')


class EtherRouter():
    account_tag = Tag(name='Ether', description='Ether Address Management')

    @staticmethod
    @blueprint_ether.get(
        '/addresses',
        tags=[account_tag],
        summary='get user ether address',
        responses={200: EtherAddressResponse}
    )
    def get_address():
        addresses = EtherAddressModel.get_all_address()
        return SuccessResponse(
            message='Ether Addresses retrieved successfully',
            data=addresses
        ).model_dump(), 200

    @staticmethod
    @blueprint_ether.get(
        '/address/<string:id>',
        tags=[account_tag],
        summary='get user ether address',
        responses={200: EtherAddressResponse}
    )
    def get_address_by_id(path: UserPath):
        if not UserModel.get_user_by_id(path.id):
            return NoContentResponse(message='User not found').model_dump(), 200
        addresses = EtherAddressModel.get_address_by_user_id(path.id)
        if not addresses:
            return NoContentResponse(message='Address not found').model_dump(), 200
        return SuccessResponse(
            message='Ether Addresses retrieved successfully',
            data=[EtherAddressResponse.from_ether_model(address) for address in addresses]
        ).model_dump(), 200

    @staticmethod
    @blueprint_ether.post(
        '/address/<string:id>',
        tags=[account_tag],
        summary='create ether address',
        responses={200: EtherAddressResponse}
    )
    def create_address(path: UserPath):
        if not UserModel.get_user_by_id(path.id):
            return NoContentResponse(message='User not found').model_dump(), 200
        key_json = create_keystore(os.getenv('PK'))
        ether = EtherAddressModel.create_address(key_json, path.id)
        return SuccessResponse(
            message='Ether address retrieved successfully',
            data=dict(EtherAddressResponse.from_ether_model(ether))
        ).model_dump(), 200
