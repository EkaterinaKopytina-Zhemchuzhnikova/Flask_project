from .db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

class Doctors(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'doctors'
    docid = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True)
    doctorsname = sqlalchemy.Column(sqlalchemy.String)
    direction = sqlalchemy.Column(sqlalchemy.String)
    hospid = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("hospitals.id"))
