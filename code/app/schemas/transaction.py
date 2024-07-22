from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class TransactionResponse(BaseModel):
    id: str = Field(..., description="id")
    user_id: str = Field(..., description="user id")
    transaction_hash: str = Field(..., description="transaction hash")
    log_index: int = Field(..., description="log index")
    contract_address: str = Field(..., description="contract address")
    name: str = Field(..., description="name")
    symbol: str = Field(..., description="symbol")
    network: str = Field(..., description="network")
    from_address: str = Field(..., description="from address")
    to_address: str = Field(..., description="to address")
    value: float = Field(..., description="value")
    block_hash: str = Field(..., description="block hash")
    confirmations: int = Field(..., description="confirmations")
    status: int = Field(..., description="status")
    tx_timestamp: datetime = Field(..., description="tx timestamp")

    @classmethod
    def from_transaction_model(cls, transaction):
        return cls(
            id=str(transaction.id),
            user_id=str(transaction.user_id),
            transaction_hash=transaction.transaction_hash,
            log_index=transaction.log_index,
            contract_address=transaction.contract_address,
            name=transaction.name,
            symbol=transaction.symbol,
            network=transaction.network,
            from_address=transaction.from_address,
            to_address=transaction.to_address,
            value=transaction.value,
            block_hash=transaction.block_hash,
            confirmations=transaction.confirmations,
            status=transaction.status,
            tx_timestamp=transaction.tx_timestamp
        )
