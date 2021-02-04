from .db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

class Refer(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'refer'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    snils = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("patients.snils"))
    refer_text = sqlalchemy.Column(sqlalchemy.TEXT)
