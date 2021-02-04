import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Tests(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'tests'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    patient_snils = sqlalchemy.Column(sqlalchemy.Integer,
                                      sqlalchemy.ForeignKey("patients.snils"))
    ready = sqlalchemy.Column(sqlalchemy.BOOLEAN)
    num_file = sqlalchemy.Column(sqlalchemy.Integer)

