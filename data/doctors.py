from .db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

class Doctors(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'doctors'
    doc_id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True)
    doctor_fio = sqlalchemy.Column(sqlalchemy.String)
    direction = sqlalchemy.Column(sqlalchemy.String)
    hosp_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("hospitals.id"))
