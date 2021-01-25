from .db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

class Doctors(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'Doctors'
    doctors_id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True)
    doctors_name = sqlalchemy.Column(sqlalchemy.String)
    direction = sqlalchemy.Column(sqlalchemy.String)
    hospitals_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Hospitals.id"))
    hospitals = orm.relation('Hospitals')

    def __repr__(self):
        return f'<Doctors> {self.doctors_name}'