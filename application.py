from flask import Flask, render_template, request, url_for, redirect
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

engine = create_engine('sqlite:///categoryitem.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/category/<int:category_id>/')
def categoryitem(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(Item).filter_by(item_id = category_id)
    return render_template('item.html', category = category, items = items)

@app.route('/category/<int:category_id>/new/', methods = ['GET', 'POST'])
def newItem(category_id):
    if request.method == 'POST':
        newitem = Item(request.form['name'], category_id = category_id)
        session.add(newitem)
        session.commit()
        return redirect(url_for('categoryitem', category_id = category_id))
    else:
        return render_template('newitem.html', category_id = category_id)

@app.route('/category/<int:category_id>/<int:item_id>/Edit')
def editItem(category_id, item_id):
    return "The selected item has been edited"

@app.route('/category/<int:category_id>/<int:item_id>/Delete')
def deleteItem(category_id, item_id):
    return "The selected item has been deleted"

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
