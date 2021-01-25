import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'jobs'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    job = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    collaborators = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.today)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.today)
    is_finished = sqlalchemy.Column(sqlalchemy.BOOLEAN, nullable=True)
    user = orm.relation('User')
    categories = orm.relation("Category",
                              secondary="association",
                              backref="jobs")

    def __repr__(self):
        return f'<Job> {self.job}'
