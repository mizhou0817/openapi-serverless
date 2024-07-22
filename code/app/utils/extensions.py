from flask_sqlalchemy import SQLAlchemy


class SingletonDB:
    _instance = None
    db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonDB, cls).__new__(cls)
            cls.db = SQLAlchemy()
        return cls._instance

    @staticmethod
    def init_app(app):
        SingletonDB.db.init_app(app)

db_instance = SingletonDB()
db = db_instance.db