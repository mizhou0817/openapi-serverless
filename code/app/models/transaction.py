from datetime import datetime

from app.utils.snowflake_id_generator import snowflake_id_generator
from app.utils.extensions import db
from app.models.base_model import BaseModel
from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    DateTime,
    DECIMAL,
    UniqueConstraint,
    desc
)


class TransactionModel(db.Model, BaseModel):
    __tablename__ = 'transactions'

    id = Column(BigInteger, primary_key=True, default=snowflake_id_generator.generate_id)
    user_id = Column(BigInteger, nullable=False)
    transaction_hash = Column(String(67), nullable=False)
    log_index = Column(Integer, nullable=False)
    contract_address = Column(String(43), nullable=False)
    name = Column(String(10), nullable=False)
    symbol = Column(String(10), nullable=False)
    decimals = Column(Integer, nullable=False)
    network = Column(String(10), nullable=False)
    from_address = Column(String(43), nullable=False)
    to_address = Column(String(43), nullable=False)
    value = Column(DECIMAL(10, 2), nullable=False)
    block_hash = Column(String(67), nullable=False)
    block_number = Column(Integer)
    confirmations = Column(Integer, nullable=False, default=0)
    status = Column(Integer, nullable=False, default=0)
    tx_timestamp = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint('transaction_hash', 'log_index', name='_transaction_log_uc'),)

    @staticmethod
    def create_transaction(tx: dict):
        query = TransactionModel.query.filter_by(transaction_hash=tx["transaction_hash"])
        if "log_index" in tx:
            query = query.filter_by(log_index=tx["log_index"])
        transaction = query.first()

        if transaction:
            for key, value in tx.items():
                setattr(transaction, key, value)
        else:
            transaction = TransactionModel(**tx)
        db.session.add(transaction)
        db.session.commit()
        return transaction

    @staticmethod
    def get_pending_tx():
        return TransactionModel.query.filter(TransactionModel.confirmations < 10).order_by(desc(TransactionModel.tx_timestamp)).first()

    def get_txs_by_user_id(user_id: str):
        return TransactionModel.query.filter_by(user_id=user_id).order_by(desc(TransactionModel.tx_timestamp)).all()
