import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Reception(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'reception_date_time'
    doctors_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("doctors.doctors_id"), primary_key=True, )
    date_work = sqlalchemy.Column(sqlalchemy.DateTime)
    time = sqlalchemy.Column(sqlalchemy.Time)
    free = sqlalchemy.Column(sqlalchemy.BOOLEAN)
    doctors = orm.relation('Doctors')

    def __repr__(self):
        return f'<reception_date_time> {self.free}'
