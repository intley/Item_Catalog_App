# Importing necessary libraries for SQLAlchemy and Creating a Database
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String(200), nullable = False)
    email = Column(String(200), nullable = False)
    picture = Column(String(300))

    @property
    def serialize(self):
        return {
        'name': self.name,
        'id': self.id,
        'email': self.email,
        'picture': self.picture
        }

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key = True)
    name = Column(String(200), nullable = False)
    #user_id = Column(Integer, ForeignKey('user.id'))
    #user = relationship(User)


    @property
    def serialize(self):
        return {
        'name': self.name,
        'id': self.id
        }

class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)
    date = Column(DateTime, nullable = False)
    description = Column(String(300))
    price = Column(String(8))
    item_id = Column(Integer, ForeignKey('category.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    category = relationship(Category)
    user = relationship(User)

    @property
    def serialize(self):
        return {
        'id': self.id,
        'name': self.name,
        'date': self.date,
        'description': self.description,
        'price': self.price,
        'category': self.category.name
        }

engine = create_engine('sqlite:///itemcatalog.db')

Base.metadata.create_all(engine)
