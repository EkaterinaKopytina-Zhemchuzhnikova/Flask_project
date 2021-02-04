import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class RegistredPatients(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'registered_patients'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    snils = sqlalchemy.Column(sqlalchemy.Integer)
    patient_fio = sqlalchemy.Column(sqlalchemy.String)
    date = sqlalchemy.Column(sqlalchemy.Date)
    time = sqlalchemy.Column(sqlalchemy.String)
    doc_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("doctors.doc_id"))
