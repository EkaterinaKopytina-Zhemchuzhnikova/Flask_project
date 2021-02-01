import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class RegistredPatients(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'registered_patients'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    snils = sqlalchemy.Column(sqlalchemy.Integer)
    patient_name = sqlalchemy.Column(sqlalchemy.String)
    date = sqlalchemy.Column(sqlalchemy.DATE)
    time = sqlalchemy.Column(sqlalchemy.Time)
    docid = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("doctors.docid"))
