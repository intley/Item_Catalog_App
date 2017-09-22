# Importing necessary libraries for SQLAlchemy and Creating a Database
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key = True)
    name = Column(String(200), nullable = False)

class Item(Base):
    __tablename__ = 'item'

    name = Column(String(100), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(300))
    price = Column(String(8))
    item_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        return {
        'name': self.name,
        'id': self.id,
        'description': self.description,
        'price': self.price
        }

engine = create_engine('sqlite:///categoryitem.db')
Base.metadata.create_all(engine)
