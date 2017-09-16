from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item

engine = create_engine('sqlite:///categoryitem.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Items for Books
category1 = Category(name = "Books")

session.add(category1)
session.commit()

item1 = Item(name = "Da Vinci Code", description = "2003 mystery-detective novel by Dan Brown.", price = "10$", category = category1)

session.add(item1)
session.commit()

item2 = Item(name = "Harry Potter and the Sorcerer's Stone", description = "1997 Fantasy novel by JK Rowling", price = "15$", category = category1)

session.add(item2)
session.commit()

item3 = Item(name = "Harry Potter and the Chamber of Secrets", description = "1998 Fantasy novel by JK Rowling ", price = "15$", category = category1)

session.add(item3)
session.commit()

item4 = Item(name = "Harry Potter and the Goblet of Fire", description = "2000 Fantasy novel by JK Rowling", price = "20$", category = category1)

session.add(item4)
session.commit()

item5 = Item(name = "Harry Potter and the Half-Blood Prince", description = "2005 Fantasy novel by JK Rowling", price = "20$", category = category1)

session.add(item5)
session.commit()

item6 = Item(name = "Harry Potter and the Deathy Hallows", description = "2007 Fantasy novel by JK Rowling", price = "25$", category = category1)

session.add(item6)
session.commit()

item7 = Item(name = "Game of Thrones", description = "1996 Epic Fantasy novel by George RR Martin", price = "20$", category = category1)

session.add(item7)
session.commit()

item8 = Item(name = "A Storm of Swords", description = "2005 Epic Fantasy novel by George RR Martin", price = "30$", category = category1)

session.add(item8)
session.commit()

item9 = Item(name = "The Winds of Winter", description = "2018 Epic Fantasy novel by George RR Martin", price = "50$", category = category1)

session.add(item9)
session.commit()

item10 = Item(name = "The Perks of being a Wallflower", description = "2007 coming of age novel by Stephen Chbosky", price = "12$", category = category1)

session.add(item10)
session.commit()

# Items for Movies
category2 = Category(name = "Movies")

session.add(category2)
session.commit()

item1= Item(name = "The Godfather", description = "1972 Mafia Film by Francis Ford Coppola", price = "10$", category = category2)

session.add(item1)
session.commit()

item2= Item(name = "The Shawshank Redemption", description = "1994 Prison Drama Starring Morgan Freeman and Tim Robbins", price = "8$", category = category2)

session.add(item2)
session.commit()

item3= Item(name = "The Dark Knight", description = "2008 Batman is driven to the limit facing his nemesis, the Joker", price = "12$", category = category2)

session.add(item3)
session.commit()

item4= Item(name = "IT", description = "2017 Clown Horror Movie starring Bill Skarsgard", price = "9$", category = category2)

session.add(item4)
session.commit()

item5= Item(name = "The Avengers", description = "A team of superheroes come together to combat an evil alient threat", price = "14$", category = category2)

session.add(item5)
session.commit()

item6= Item(name = "Speed", description = "A out of control bus armed with a bomb cannot be stopped while demands are being made by the terrorist", price = "12$", category = category2)

session.add(item6)
session.commit()

item7= Item(name = "The Matrix", description = "A virus program threatens to take control over reality through the neural network program called the Matrix", price = "10$", category = category2)

session.add(item7)
session.commit()

item8= Item(name = "Good Will Hunting", description = "Matt Damon stars as the anxious introverted genius with his interactions with a psychiatrist.", price = "15$", category = category2)

session.add(item8)
session.commit()

item9 = Item(name = "Finding Nemo", description = "Merlin a clownfish has to find his son nemo with the help of another fish Dory.", price = "16$", category = category2)

session.add(item9)
session.commit()

item10 = Item(name = "Ratatouille", description = "A rat with a talent for cooking begins his secret quest to cook for a famous restaurant", price = "10$", category = category2)

session.add(item10)
session.commit()

# Items for Mobile Phones
category3 = Category(name = "Mobile Phones")

session.add(category3)
session.commit()

item1 = Item(name = "Apple iPhone X", description = "Apple's Flagship phone with a 5.8 inch bezel-less display", price = "999$", category = category3)

session.add(item1)
session.commit()

item2 = Item(name = "Apple iPhone 8", description = "Wireless Charging, Apple's premium phone", price = "699$", category = category3)

session.add(item2)
session.commit()

item3 = Item(name = "Apple iPhone 8 Plus", description = "A bigger display version of the iPhone 8", price = "799$", category = category3)

session.add(item3)
session.commit()

item4 = Item(name = "Google Pixel", description = "Google's Flagship phone", price = "649$", category = category3)

session.add(item4)
session.commit()

item5 = Item(name = "OnePlus 5", description = "OnePlus's flagship phone with Dual Cameras", price = "449$", category = category3)

session.add(item5)
session.commit()

item6 = Item(name = "Samsung Galaxy 8", description = "Infinity Display with Iris-Scan Authentication", price = "649$", category = category3)

session.add(item6)
session.commit()

item7 = Item(name = "LG G6", description = "LG's new bezel-less phone", price = "549$", category = category3)

session.add(item7)
session.commit()

item8 = Item(name = "Samsung Galaxy Note 8", description = "Note Samsung with the stylus", price = "749$", category = category3)

session.add(item8)
session.commit()

item9 = Item(name = "HTC One X", description = "HTC's latest phone", price = "349$", category = category3)

session.add(item9)
session.commit()

item10 = Item(name = "Xiaomei Mei 3", description = "Fingerprint, Xiaomei's new phone", price = "199$", category = category3)

session.add(item10)
session.commit()

# Adding Items for Laptops
category4 = Category(name = "Laptops")

session.add(category4)
session.commit()

item1 = Item(name = "Apple Macbook Pro", description = "Laptop for Professionals", price = "1499$", category = category4)

session.add(item1)
session.commit()

item2 = Item(name = "Apple Macbook Air", description = "Light weight Laptop ", price = "799$", category = category4)

session.add(item2)
session.commit()

item3 = Item(name = "Apple Macbook", description = "Laptop for Students", price = "1299$", category = category4)

session.add(item3)
session.commit()

item4 = Item(name = "Microsoft Surface Laptop", description = "Laptop for Professionals", price = "1099$", category = category4)

session.add(item4)
session.commit()

item5 = Item(name = "Microsoft Surface Pro 4", description = "Tablet and Laptop for Students", price = "699$", category = category4)

session.add(item5)
session.commit()

# Adding Items for Games
category5 = Category(name = "Video Games")

session.add(category5)
session.commit()

item1 = Item(name = "Uncharted 4", description = "Adventure Game", price = "59$", category = category5)

session.add(item1)
session.commit()

item2 = Item(name = "Crysis ", description = "Shooting Game", price = "19$", category = category5)

session.add(item2)
session.commit()

item3 = Item(name = "Gears of War", description = "Third Person Shooter", price = "39$", category = category5)

session.add(item3)
session.commit()

item4 = Item(name = "Halo", description = "Space First Person Shooter", price = "49$", category = category5)

session.add(item4)
session.commit()

item5 = Item(name = "Fifa 18", description = "Soccer Game", price = "49$", category = category5)

session.add(item5)
session.commit()

item6 = Item(name = "Forza Motorsport", description = "Racing Game", price = "29$", category = category5)

session.add(item6)
session.commit()

# Adding Items for Consoles
category6 = Category(name = "Consoles")

session.add(category6)
session.commit()

item1 = Item(name = "Xbox One X", description = "Premium Console, World's most powerful console.", price = "499$", category = category6)

session.add(item1)
session.commit()

item2 = Item(name = "Xbox One S", description = "Slim Console, Easy to get gaming", price = "299$", category = category6)

session.add(item2)
session.commit()

item3 = Item(name = "PlayStation 4 Pro", description = "4k Gaming, for the Players", price = "399$", category = category6)

session.add(item3)
session.commit()

item4 = Item(name = "PlayStation 4 Slim", description = "Slim Playstation, 1080p Gaming", price = "299$", category = category6)

session.add(item4)
session.commit()

item5 = Item(name = "Nintendo 3DS", description = "Handheld Gaming with 3D Functionality", price = "149$", category = category6)

session.add(item5)
session.commit()

item6 = Item(name = "Nintendo Switch", description = "Handheld or using a screen, it's your choice", price = "349$", category = category6)

session.add(item6)
session.commit()

item7 = Item(name = "Kinect for Xbox One", description = "Motion Tracking Component for Xbox One", price = "149$", category = category6)

session.add(item7)
session.commit()

# Adding items for Sports
category7 = Category(name = "Sports")

session.add(category7)
session.commit()

item1 = Item(name = "Cricket Bat", description = "A bat to play Cricket, English willow", price = "40$", category = category7)

session.add(item1)
session.commit()

item2 = Item(name = "Baseball Bat", description = "Finest Metal Crafted Baseball Bat by Titan", price = "80$", category = category7)

session.add(item2)
session.commit()

item3 = Item(name = "Spalding Baskbetball", description = "NBA Official Basketball", price = "50$", category = category7)

session.add(item3)
session.commit()

item4 = Item(name = "Gym Gloves", description = "Gloves to wear while carrying weight", price = "20$", category = category7)

session.add(item4)
session.commit()

item5 = Item(name = "Table Tennis Paddle", description = "A paddle to play table tennis ", price = "60$", category = category7)

session.add(item5)
session.commit()

item6 = Item(name = "Jordan 3 Shoes", description = "Jordan's new 3 series", price = "150$", category = category7)

session.add(item6)
session.commit()

item7 = Item(name = "Curry 30 Shoes", description = "Curry's latest 4 series shoes", price = "200$", category = category7)

session.add(item7)
session.commit()

item8 = Item(name = "Golden State Warriors Jersey", description = "Golden State's Nike Jersey", price = "100$", category = category7)

session.add(item8)
session.commit()

item9 = Item(name = "Sports Water Bottle", description = "A water bottle", price = "10$", category = category7)

session.add(item9)
session.commit()

# Adding items for Music
category8 = Category(name = "Music")

session.add(category8)
session.commit()

item1 = Item(name = "Adele - 21", description = "Adele's Grammy Award Winning Album", price = "15$", category = category8)

session.add(item1)
session.commit()

item2 = Item(name = "Led Zeppelin - Coda", description = "Led Zepp's classic album", price = "10$", category = category8)

session.add(item2)
session.commit()

item3 = Item(name = "Guns N Roses - Appetite for Destruction", description = "Guns N Roses most iconic album", price = "29$", category = category8)

session.add(item3)
session.commit()

item4 = Item(name = "Pink Floyd - The Wall", description = "The classic Pink Floyd Album", price = "20$", category = category8)

session.add(item4)
session.commit()

item5 = Item(name = "Pink Floyd - The Dark Side of the Moon", description = "The top rated Billboard Album", price = "50$", category = category8)

session.add(item5)
session.commit()

item6 = Item(name = "Oasis - Wonderwall", description = "Oasis's famous track", price = "10$", category = category8)

session.add(item6)
session.commit()

item7 = Item(name = "Katy Perry - Teenage Dream", description = "Katy Perry's latest pop album", price = "7$", category = category8)

session.add(item7)
session.commit()

item8 = Item(name = "Imagine Dragons - Night Visions", description = "Alternative Rock Album", price = "12$", category = category8)

session.add(item8)
session.commit()

# Adding items for Television Sets
category9 = Category(name = "Television Sets")

session.add(category9)
session.commit()

item1 = Item(name = "Sony Bravia 4K TV", description = "42 inch 4k tv", price = "499$", category = category9)

session.add(item1)
session.commit()

item2 = Item(name = "Samsung Curved TV", description = "50 inch curved tv", price = "699$", category = category9)

session.add(item2)
session.commit()

item3 = Item(name = "Panasonic Boom Box", description = "60 inch tv with industry leading sound", price = "999$", category = category9)

session.add(item3)
session.commit()

item4 = Item(name = "LG Smart TV", description = "32 inch lg tv with android ", price = "299$", category = category9)

session.add(item4)
session.commit()

item5 = Item(name = "Micromax Smart TV", description = "36 inch tv with embedded microOS", price = "199$", category = category9)

session.add(item5)
session.commit()

# Adding items for Desktops
category10 = Category(name = "Desktops")

session.add(category10)
session.commit()

item1= Item(name = "HP Omen", description = "HP's mean gaming PC", price = "799$", category = category10)

session.add(item1)
session.commit()

item2= Item(name = "Alienware M6", description = "Alienware's gaming PC", price = "1099$", category = category10)

session.add(item2)
session.commit()

item3= Item(name = "Dell XPS", description = "Dell's gaming PC", price = "999$", category = category10)

session.add(item3)
session.commit()

item4= Item(name = "Apple iMac", description = "Apple's multimedia Desktop", price = "1299$", category = category10)

session.add(item4)
session.commit()

print "Added Lots of Category Items!"
