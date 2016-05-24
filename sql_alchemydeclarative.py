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

    def serialize(self):
        return{
                'cle_util': self.cle_util,
                'email_util': self.email_util,
                'nom_util': self.nom_util,
                'motpass': self.motpass,
                'info_uti': self.info_uti
        }

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

class Topic(Base):
    __tablename__='topic'
    cle_top = Column(Integer,autoincrement=True,primary_key=True)
    name_top = Column(String)
    def serialize(self):
            return{
                    'cle_top': self.cle_top,
                    'name_top': self.name_top
            }

class Reltop(Base):
    __tablename__='reltop'
    cle_reltop = Column(Integer,autoincrement=True,primary_key=True)
    cle_top = Column(Integer,ForeignKey('topic.cle_top'))
    topic = relationship(Topic)
    cle_pub = Column(Integer,ForeignKey('publication.cle_pub'))
    publication = relationship(Publication)

engine = create_engine('sqlite:///mabase.db', echo=True)

Base.metadata.create_all(engine)
