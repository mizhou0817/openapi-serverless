from datetime import datetime
from sqlalchemy import Column, String, BigInteger, DateTime, JSON
from app.utils.snowflake_id_generator import snowflake_id_generator
from app.utils.extensions import db
from app.models.base_model import BaseModel


class EtherAddressModel(db.Model, BaseModel):
    __tablename__ = 'ether_addresses'
    # id = Column(BigInteger, primary_key=True, default=snowflake.generate)
    id = Column(BigInteger, primary_key=True, default=snowflake_id_generator.generate_id)
    user_id = Column(String(120), nullable=False)
    address = Column(String(64), index=True, unique=True)
    low_case_address = Column(String(64), index=True, unique=True)
    keystore = Column(JSON, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    @staticmethod
    def get_all_address():
        addresses = db.session.query(EtherAddressModel.address).all()
        return [address[0] for address in addresses]


    @staticmethod
    def get_address_by_user_id(user_id):
        return EtherAddressModel.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_user_id_by_address(address):
        return EtherAddressModel.query.filter_by(address=address).first()

    @staticmethod
    def create_address(keystore, user_id):
        ether_address = EtherAddressModel.from_dict({
            "keystore": keystore,
            "address": "0x" + keystore["address"],
            "low_case_address": "0x" + keystore["address"].lower(),
            "user_id": user_id
        })
        db.session.add(ether_address)
        db.session.commit()
        print(ether_address)
        print(type(ether_address))
        return ether_address
