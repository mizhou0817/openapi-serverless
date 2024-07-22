# coding: utf-8
from __future__ import absolute_import

from sqlalchemy.orm import declared_attr
from sqlalchemy import inspect
from .user import UserModel
from .ether_address import EtherAddressModel
from .order import OrderModel
from .transaction import TransactionModel
from app.utils.extensions import db

# Import models into model package
__all__ = ['UserModel', 'EtherAddressModel', 'OrderModel', 'TransactionModel']
db.create_all()
