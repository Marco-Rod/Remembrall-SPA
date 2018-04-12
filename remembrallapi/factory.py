from sqlalchemy import Column, Integer, Unicode, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from models import User
POSTGRES = {
        'user':'postgres',
        'pw': '',
        'db':'remembrall',
        'host': 'localhost',
        'port': '5432',
}

engine = create_engine('postgresql://%(user)s:\%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES)
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

import factory

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = session   # the SQLAlchemy session object

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: u'User %d' % n)