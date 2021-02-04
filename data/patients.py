import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class LoginPatients(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'patients'
    snils = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    patient_fio = sqlalchemy.Column(sqlalchemy.String)
    hospital = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("hospitals.id"))
