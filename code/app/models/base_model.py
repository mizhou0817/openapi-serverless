# app/models/base_model.py
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import inspect


class BaseModel:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    @classmethod
    def from_dict(cls, dict_data):
        return cls(**dict_data)