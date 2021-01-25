import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Hospitals(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'Hospitals'
    hospitals_id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    hospitals_name = sqlalchemy.Column(sqlalchemy.String)
    location = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return f'<Hospitals> {self.hospitals_name}'
