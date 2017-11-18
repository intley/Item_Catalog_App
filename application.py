# Import modules
from flask import Flask, render_template, request, url_for, redirect, flash, jsonify

from sqlalchemy import create_engine, desc, DateTime
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item

from flask import session as login_session
import random, string
import datetime

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

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

#Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE = state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
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

    user_id = getUserId(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
        login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    print login_session['picture']
    return output


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserId(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        response = redirect(url_for('categories'))
        flash("You are now logged out.")
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/')
@app.route('/categories/')
def categories():
    categories = session.query(Category).all()
    if 'username' not in login_session:
        admin_email = "rahul.intley@gmail.com"
        admin_id = getUserId(admin_email)
        a_items = session.query(Item).filter_by(user_id = admin_id).all()
        return render_template('pub_category.html', categories = categories, user_id = admin_id, items = a_items)
    else:
        log_id = getUserId(login_session['email'])
        u_items = session.query(Item).filter_by(user_id = log_id)
        return render_template('user_category.html', categories = categories, items = u_items)


@app.route('/categories/<string:category_name>/', methods = ['GET', 'POST'])
def useritems(category_name):
    category = session.query(Category).filter_by(name = category_name).one()
    admin_email = "rahul.intley@gmail.com"
    admin_id = getUserId(admin_email)
    a_items = session.query(Item).filter_by(item_id = category.id, user_id = admin_id).all()
    if 'username' not in login_session:
        return render_template('publicitems_category.html', category = category, items = a_items)
    else:
        log_id = getUserId(login_session['email'])
        item = session.query(Item).filter_by(item_id = category.id, user_id = log_id).all()
        return render_template('useritems_category.html', category = category, items = item)

@app.route('/categories/<string:category_name>/<string:item_name>/', methods = ['GET', 'POST'])
def showItem(category_name, item_name):
    category = session.query(Category).filter_by(name = category_name).one()
    admin_email = "rahul.intley@gmail.com"
    admin_id = getUserId(admin_email)
    if 'username' not in login_session:
        a_item = session.query(Item).filter_by(item_id = category.id, user_id = admin_id, name = item_name).one()
        return render_template('public_items.html', category = category, item = a_item)
    else:
        log_id = getUserId(login_session['email'])
        item = session.query(Item).filter_by(item_id = category.id, user_id = log_id, name = item_name).one()
        return render_template('user_item.html', category = category, item = item)


@app.route('/categories/<string:category_name>/New/', methods = ['GET', 'POST'])
def newItem(category_name):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(name = category_name).one()
    if request.method == 'POST':
        user_id = getUserId(login_session['email'])
        newitem = Item(name = request.form['name'],
                       description = request.form['description'],
                       price = request.form['price'],
                       item_id = category.id,
                       date=datetime.datetime.now(),
                       user_id = user_id)
        session.add(newitem)
        session.commit()
        flash("New Item has been created!")
        return redirect(url_for('useritems', category_name = category.name))
    else:
        return render_template('newitem.html', category = category)

@app.route('/categories/<string:category_name>/<int:item_id>/Edit', methods = ['GET', 'POST'])
def editItem(category_name, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(name = category_name).one()
    user_id = getUserId(login_session['email'])
    editeditem = session.query(Item).filter_by(id=item_id, user_id = user_id).one()
    if request.method == 'POST':
        editeditem.name = request.form['name']
        editeditem.description = request.form['description']
        editeditem.price = request.form['price']
        editeditem.date = datetime.datetime.now()
        session.add(editeditem)
        session.commit()
        flash("Item has been edited!")
        return redirect(url_for('showItem', category_name = category.name, item_name = editeditem.name))
    else:
        return render_template('edititem.html', category = category, item_id = item_id, item = editeditem)

@app.route('/categories/<string:category_name>/<int:item_id>/Delete', methods = ['GET', 'POST'])
def deleteItem(category_name, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    user_id = getUserId(login_session['email'])
    itemtodelete = session.query(Item).filter_by(id=item_id, user_id = user_id).one()
    if request.method == 'POST':
        session.delete(itemtodelete)
        session.commit()
        flash("Item has been deleted!")
        return redirect(url_for('useritems', category_name = category_name))
    else:
        return render_template('deleteitem.html', category_name = category_name, item_id = item_id, item = itemtodelete)

@app.route('/categories/<string:category_name>/JSON')
def categoryitemJSON(category_name):
    category = session.query(Category).filter_by(name = category_name).one()
    admin_email = "rahul.intley@gmail.com"
    admin_id = getUserId(admin_email)
    a_items = session.query(Item).filter_by(item_id = category.id, user_id = admin_id).all()
    if 'username' not in login_session:
        return jsonify(categoryitems=[i.serialize for i in a_items])
    else:
        log_id = getUserId(login_session['email'])
        items = session.query(Item).filter_by(item_id = category.id, user_id = log_id).all()
        return jsonify(categoryitems=[i.serialize for i in items])


@app.route('/categories/<string:category_name>/<string:item_name>/JSON')
def itemJSON(category_name, item_name):
    category = session.query(Category).filter_by(name = category_name).one()
    admin_email = "rahul.intley@gmail.com"
    admin_id = getUserId(admin_email)
    a_item = session.query(Item).filter_by(item_id = category.id, name = item_name, user_id = admin_id).all()
    if 'username' not in login_session:
        return jsonify(item = [i.serialize for i in a_item])
    else:
        log_id = getUserId(login_session['email'])
        item = session.query(Item).filter_by(item_id = category.id, name = item_name, user_id = log_id).all()
        return jsonify(item = [i.serialize for i in item])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
