from flask import Flask, render_template, request, url_for, redirect, flash, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"

engine = create_engine('sqlite:///categoryitem.db')
Base.metadata.bind = engine


DBSession = sessionmaker(bind = engine)
session = DBSession()

#Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html')

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

@app.route('/category/<string:category_name>/JSON')
def categoryitemJSON(category_id):
    category = session.query(Category).filter_by(name = category_name).one()
    items = session.query(Item).filter_by(item_id = category_id).all()
    return jsonify(categoryitems=[i.serialize for i in items])

#Need to fix, taking default category as 1
@app.route('/category/<string:category_name>/<int:item_id>/JSON')
def itemJSON(category_name, item_id):
    category = session.query(Category).filter_by(name = category_name)
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(item.serialize)

@app.route('/')
@app.route('/categories/')
def categories():
    categories = session.query(Category).all()
    return render_template('category.html', categories = categories)

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

@app.route('/category/<string:category_name>/')
def categoryitem(category_name):
    category = session.query(Category).filter_by(name = category_name).one()
    items = session.query(Item).filter_by(item_id = category.id)
    return render_template('item.html', category = category, items = items)

@app.route('/category/<string:category_name>/New/', methods = ['GET', 'POST'])
def newItem(category_name):
    category = session.query(Category).filter_by(name = category_name).one()
    if request.method == 'POST':
        newitem = Item(name = request.form['name'], description = request.form['description'], price = request.form['price'], item_id = category.id)
        session.add(newitem)
        session.commit()
        flash("New Item has been created!")
        return redirect(url_for('categoryitem', category_name = category.name))
    else:
        return render_template('newitem.html', category = category)

@app.route('/category/<string:category_name>/<int:item_id>/Edit', methods = ['GET', 'POST'])
def editItem(category_name, item_id):
    category = session.query(Category).filter_by(name = category_name).one()
    editeditem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        editeditem.name = request.form['name']
        editeditem.description = request.form['description']
        editeditem.price = request.form['price']
        session.add(editeditem)
        session.commit()
        flash("Item has been edited!")
        return redirect(url_for('categoryitem', category_name = category.name))
    else:
        return render_template('edititem.html', category = category, item_id = item_id, item = editeditem)

@app.route('/category/<string:category_name>/<int:item_id>/Delete', methods = ['GET', 'POST'])
def deleteItem(category_name, item_id):
    itemtodelete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemtodelete)
        session.commit()
        flash("Item has been deleted!")
        return redirect(url_for('categoryitem', category_name = category_name))
    else:
        return render_template('deleteitem.html', category_name = category_name, item_id = item_id, item = itemtodelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
