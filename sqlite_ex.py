from flask import *
from sqlalchemy import *
from sqlalchemy.sql import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    cle_util = Column(Integer,autoincrement=True,primary_key=True)
    email_util = Column(String)
    nom_util = Column(String)
    motpass = Column(String)
    info_uti = Column(String)

engine = create_engine('sqlite:///mabase.db', echo=True)

Base.metadata.create_all(engine)
