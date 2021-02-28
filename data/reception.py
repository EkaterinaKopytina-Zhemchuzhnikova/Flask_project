import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Reception(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'reception'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    doc_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("doctors.doc_id"))
    date_work = sqlalchemy.Column(sqlalchemy.Date)
    time = sqlalchemy.Column(sqlalchemy.String)
    free = sqlalchemy.Column(sqlalchemy.BOOLEAN)
