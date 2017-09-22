from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

engine = create_engine('sqlite:///categoryitem.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/category/<int:category_id>/item/JSON')
def categoryitemJSON(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(Item).filter_by(item_id = category_id).all()
    return jsonify(categoryitems=[i.serialize for i in items])

#Need to fix, taking default category as 1
@app.route('/category/<int:category_id>/item/<int:item_id>/JSON')
def itemJSON(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(item.serialize)

@app.route('/')
@app.route('/category/')
def categories():
    categories = session.query(Category).all()
    return render_template('category.html', category = categories)

#@app.route('/category/new', methods = ['GET', 'POST'])
#def newCategory():
#    if request.method == 'POST':
#        newcat = Category(name = request.form['name'])
#        session.add(newcat)
#        session.commit()
#        flash("New Category has been created!")
#        return redirect(url_for('categories'))
#    else:
#        return render_template('newcategory.html')

@app.route('/category/<int:category_id>/')
def categoryitem(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(Item).filter_by(item_id = category_id)
    return render_template('item.html', category = category, items = items)

@app.route('/category/<int:category_id>/new/', methods = ['GET', 'POST'])
def newItem(category_id):
    if request.method == 'POST':
        newitem = Item(name = request.form['name'], item_id = category_id)
        session.add(newitem)
        session.commit()
        flash("New Item has been created!")
        return redirect(url_for('categoryitem', category_id = category_id))
    else:
        return render_template('newitem.html', category_id = category_id)

@app.route('/category/<int:category_id>/<int:item_id>/Edit', methods = ['GET', 'POST'])
def editItem(category_id, item_id):
    editeditem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        editeditem.name = request.form['name']
        session.add(editeditem)
        session.commit()
        flash("Item has been edited!")
        return redirect(url_for('categoryitem', category_id = category_id))
    else:
        return render_template('edititem.html', category_id = category_id, item_id = item_id, item = editeditem)

@app.route('/category/<int:category_id>/<int:item_id>/Delete', methods = ['GET', 'POST'])
def deleteItem(category_id, item_id):
    itemtodelete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemtodelete)
        session.commit()
        flash("Item has been deleted!")
        return redirect(url_for('categoryitem', category_id = category_id))
    else:
        return render_template('deleteitem.html', category_id = category_id, item_id = item_id, item = itemtodelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
