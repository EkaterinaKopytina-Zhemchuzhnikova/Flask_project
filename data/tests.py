import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Tests(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'tests'
    patient_snils = sqlalchemy.Column(sqlalchemy.Integer,
                                      sqlalchemy.ForeignKey("patients.snils"), primary_key=True)
    ready = sqlalchemy.Column(sqlalchemy.BOOLEAN)
    num_file = sqlalchemy.Column(sqlalchemy.Integer)

