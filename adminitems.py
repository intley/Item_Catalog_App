from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Item

engine = create_engine('sqlite:///itemcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

admin = User(name = "Admin", email = "rahul.intley@gmail.com", picture = "https://lh4.googleusercontent.com/-5JjX9_cp3Ms/AAAAAAAAAAI/AAAAAAAAAAo/3x_zSD7DSpM/photo.jpg")

session.add(admin)
session.commit()

category2 = Category(name = "Movies")

session.add(category2)
session.commit()

#category2 = session.query(Category).(filter_by(name = "Movies"))
item1= Item(name = "The Godfather", description = "1972 Mafia Film by Francis Ford Coppola", price = "10$", category = category2, user = admin)
session.add(item1)
session.commit()

item2= Item(name = "The Shawshank Redemption", description = "1994 Prison Drama Starring Morgan Freeman and Tim Robbins", price = "8$", category = category2, user = admin)
session.add(item2)
session.commit()
