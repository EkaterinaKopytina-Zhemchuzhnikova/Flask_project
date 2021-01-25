import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class LoginPatients(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'PatientsSnils'
    patients_snils = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True)
    patients_fio = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return f'{self.patients_fio}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)