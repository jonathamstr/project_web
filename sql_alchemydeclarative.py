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

class Publication(Base):
    __tablename__='publication'
    cle_pub = Column(Integer,autoincrement=True,primary_key=True)
    cle_util = Column(Integer,ForeignKey('user.cle_util'))
    auteur = relationship(User)
    titre = Column(String)
    corps = Column(String)
    date = Column(DateTime,default=func.now())

class Commentaire(Base):
    __tablename__='commentaire'
    cle_comm = Column(Integer,autoincrement=True,primary_key=True)
    cle_pub = Column(Integer,ForeignKey('publication.cle_pub'))
    publication = relationship(Publication)
    cle_util = Column(Integer,ForeignKey('user.cle_util'))
    auteur = relationship(User)
    corps = Column(String)

engine = create_engine('sqlite:///mabase.db', echo=True)

Base.metadata.create_all(engine)
