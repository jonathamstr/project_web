from sqlalchemy import create_engine
from sql_alchemydeclarative import User, Base
engine = create_engine('sqlite:///mabase.db', echo=True)
Base.metadata.bind = engine
from sqlalchemy.orm import sessionmaker

DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()
session.query(User).all()
person = session.query(User).first()
print(person.nom_util)
'''Ejemplo de Filtraje en Python sqlalchemy
session.query(Address).filter(Address.person == person).all()
[<sqlalchemy_declarative.Address object at 0x2ee3cd0>]
>>>
>>> # Retrieve one Address whose person field is point to the person object
>>> session.query(Address).filter(Address.person == person).one()
<sqlalchemy_declarative.Address object at 0x2ee3cd0>
>>> address = session.query(Address).filter(Address.person == person).one()
>>> address.post_code
u'00000'
'''
