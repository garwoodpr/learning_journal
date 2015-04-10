from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
	UnicodeText
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Text(255), unique=True)
    body = Column(UnicodeText)
    created = Column(DateTime, default=datetime.now)
    edited = Column(DateTime, default=datetime.now)

Index('my_index', MyModel.name, unique=True, mysql_length=255)
