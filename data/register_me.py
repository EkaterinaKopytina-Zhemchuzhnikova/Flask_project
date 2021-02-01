from .db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

class Register_me(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'register_me'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True) # TODO: autoincrement
    fio = sqlalchemy.Column(sqlalchemy.String)
    snils = sqlalchemy.Column(sqlalchemy.Integer)
    phone = sqlalchemy.Column(sqlalchemy.String)
    sex = sqlalchemy.Column(sqlalchemy.String)