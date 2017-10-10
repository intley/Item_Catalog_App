from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Item

engine = create_engine('sqlite:///categoryitems.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Creating the administrator
user1 = User(name = "Rahul Rajendran", email = "intley@gmail.com", picture = "https://lh6.googleusercontent.com/-msPj9gj5aD8/AAAAAAAAAAI/AAAAAAAABlk/f02nmbpb4BM/photo.jpg")

session.add(user1)
session.commit()

# Categories Books and Items
category1 = Category(name = "Books", user = user1)

session.add(category1)
session.commit()

item1 = Item(name = "Da Vinci Code", description = "2003 mystery-detective novel by Dan Brown.", price = "10$", category = category1, user = user1)

session.add(item1)
session.commit()

item2 = Item(name = "Harry Potter and the Sorcerer's Stone", description = "1997 Fantasy novel by JK Rowling", price = "15$", category = category1, user = user1)

session.add(item2)
session.commit()

item3 = Item(name = "Harry Potter and the Chamber of Secrets", description = "1998 Fantasy novel by JK Rowling ", price = "15$", category = category1, user = user1)

session.add(item3)
session.commit()

# Category Movies and Items
category2 = Category(name = "Movies", user = user1)

session.add(category2)
session.commit()

category3 = Category(name = "Mobile Phones", user = user1)

session.add(category3)
session.commit()

#category4 = Category(name = "Laptops")

#session.add(category4)
#session.commit()

#category5 = Category(name = "Video Games")

#session.add(category5)
#session.commit()

#category6 = Category(name = "Consoles", user = user1)

#session.add(category6)
#session.commit()

#category7 = Category(name = "Sports")

#session.add(category7)
#session.commit()

#category8 = Category(name = "Music")

#session.add(category8)
#session.commit()

#category9 = Category(name = "Television Sets")

#session.add(category9)
#session.commit()

#category10 = Category(name = "Desktops")

#session.add(category10)
#session.commit()

# Items for each category

print "Added Category Items!"
