import hashlib

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from __init__ import app, mail
from flask import request, render_template, session, url_for
from flask_login import UserMixin
from flask_mail import Message
import pymysql
from passlib.hash import sha256_crypt
from werkzeug.utils import redirect


class User(UserMixin):
    def __init__(self, _id, first_name, last_name, username, password, email, business, entertainment, general, health,
                 science,
                 sports, technology, keywords, about_me):

        self.id = _id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email
        self.business = business
        self.entertainment = entertainment
        self.general = general
        self.health = health
        self.science = science
        self.sports = sports
        self.technology = technology
        self.keywords  = keywords
        self.about_me = about_me

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id).encode(encoding='UTF-8', errors='strict')

    def profilePicture(self, size):
        digest = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    # Retrieve a user based on the field given
    @classmethod
    def getUser(cls, db, input, field):
        connection = db.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM users WHERE " + field + " = %s"
        cursor.execute(query, (input,))
        row = cursor.fetchone()
        if row:
            user = cls(*list(row.values()))
        else:
            user = None
        connection.close()
        return user

    # Change a value for that particular User
    @classmethod
    def changeValue(cls, db, input, field, user_id):
        connection = db.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = "UPDATE users SET " + field + " = %s WHERE user_id = %s"
        cursor.execute(query, (input, user_id,))
        connection.commit()

    # Generate a token
    def generate_token(self, expires=600):
        serial = Serializer(app.config['SECRET_KEY'], expires_in=expires)
        return serial.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_token(token, db):
        serial = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = serial.loads(token)["user_id"]
        except:
            return None
        return User.getUser(db, user_id, 'id')


def getPreference(preference):
    if request.form.get(preference):
        return True
    else:
        print(preference + " = FALSE")
        return False


def getCheckBox(preference, db, username):
    if request.form.get(preference + "_yes"):
        User.changeValue(db, 1, preference, username)
    elif request.form.get(preference + "_no"):
        User.changeValue(db, 0, preference, username)
    else:
        None

def getKeyWords(key_wrds):
    if request.form.get("keywords"):
        return key_wrds
    else:
        return None
        #print("no keywords inputted")

def registerUser(db):
    data = ""
    if request.method == 'POST' and request.form.get("firstName") and request.form.get("lastName") \
            and request.form.get("username") and request.form.get("password") and request.form.get("password2") \
            and request.form.get("email"):

        # User Profile Properties
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        username = request.form['username']
        password = sha256_crypt.hash(request.form['password'])
        email = request.form['email']

        # User Article Preferences Properties
        business = getPreference("business_checkbox")
        entertainment = getPreference("entertainment_checkbox")
        general = getPreference("general_checkbox")
        health = getPreference("health_checkbox")
        science = getPreference("science_checkbox")
        sports = getPreference("sports_checkbox")
        technology = getPreference("technology_checkbox")

        #User Keywords
        keywords = getKeyWords(request.form['keywords'])
        print(keywords)

        if not business and not entertainment and not general and not health and not science and not sports and not \
                technology:
            general = True

        if User.getUser(db, username, "username"):
            data = "A user with the username already exists"
            return render_template('signup-form.html', data=data), 400

        if User.getUser(db, email, "email"):
            data = "A user with the email already exists"
            return render_template('signup-form.html', data=data), 400

        connection = db.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = "INSERT INTO users VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)"
        cursor.execute(query, (
            first_name, last_name, username, password, email, business, entertainment, general, health, science, sports,
            technology, keywords,))
        connection.commit()
        data = "User created successfully!"
        return render_template('signup-form.html', data=data), 201

    elif request.method == 'POST':
        data = "Please fill out the form!"
        return render_template('signup-form.html', data=data), 400

    else:
        data = "The server has encountered a situation it does not know how to handle."
        return render_template('signup-form.html', data=data), 500


def signIn(db):
    if request.method == 'POST' and request.form.get("username") and request.form.get("password"):
        username = request.form['username']
        password = request.form['password']
        user = User.getUser(db, username, "username")
        if user and sha256_crypt.verify(password, user.password):
            session['logged_in'] = True
            session['user'] = request.form['username']
            session['id'] = user.id
            return redirect(url_for('homepage')), 301
        else:
            msg = "Error. Invalid username or password"
            return render_template("login-form.html", data=msg), 401
    elif request.method == 'POST':
        msg = "Fill out the form!"
        return render_template("login-form.html", data=msg), 400
    else:
        data = "The server has encountered a situation it does not know how to handle."
        return render_template('signup-form.html', data=data), 500


def getHomePage(username, db):
    user = User.getUser(db, username, "username")
    return render_template("homepage.html", user=user, _external=True)


def userProfile(username, db):
    user = User.getUser(db, username, "username")
    return render_template("user-profile.html", user=user, _external=True)


def send_mail(user):
    token = user.generate_token()
    msg = Message(subject="Password Reset Request", recipients=[user.email], sender="spnews89@gmail.com")
    msg.body = f'''
    To reset your password. Please follow the link below.
    
    http://127.0.0.1:5000{url_for('reset_token', token=token)}
    If you didn't send a password reset request. Please ignore this message.
    
    '''
    mail.send(msg)


def forgotPassword(db):
    msg = "if an account exists for that email address, we have sent you an email with a link to reset your password."
    if request.method == 'POST' and request.form.get("email"):
        email = request.form['email']
        user = User.getUser(db, email, "email")
        if user:
            send_mail(user)
        return render_template('password_reset.html', msg=msg), 200


def resetPassword(token, db):
    user = User.verify_token(token, db)
    if user is None:
        return redirect(url_for('resetpage'))
    if request.method == 'POST' and request.form.get("password"):
        password = sha256_crypt.hash(request.form['password'])
        User.changeValue(db, password, "password", user.id)
        data = "Password changed! Please login!"
        return render_template('password_change.html', data=data)
    return render_template('password_change.html')


def editProfile(username, db):
    user = User.getUser(db, username, "username")
    if request.method == 'POST' and request.form.get("firstName") or request.form.get("lastName") or \
            request.form.get("aboutMe") or request.form.get("business_yes") or request.form.get("business_no") \
            or request.form.get("entertainment_yes") or request.form.get("entertainment_no") or request.form.get(
        "general_yes") \
            or request.form.get("general_no") or request.form.get("health_yes") or request.form.get("health_no") \
            or request.form.get("science_yes") or request.form.get("science_no") or request.form.get("sports_yes") \
            or request.form.get("sports_no") or request.form.get("technology_yes") or request.form.get("technology_no") \
            or request.form.get("keyWord"):
        first_name = request.form['firstName']
        if first_name:
            User.changeValue(db, first_name, "first_name", user.id)
        
        last_name = request.form['lastName']
        if last_name:
            User.changeValue(db, last_name, "last_name", user.id)
        
        about_me = request.form['aboutMe']
        if about_me:
            User.changeValue(db, about_me, "about_me", user.id)

        keywords = request.form['keyWord']
        if keywords:
            User.changeValue(db, keywords, "keywords", user.id)

        getCheckBox("business", db, user.id)
        getCheckBox("entertainment", db, user.id)
        getCheckBox("general", db, user.id)
        getCheckBox("health", db, user.id)
        getCheckBox("science", db, user.id)
        getCheckBox("sports", db, user.id)
        getCheckBox("technology", db, user.id)
        data = "User Profile has been successfully updated"

        return render_template('settings.html', data=data), 200
    elif request.method == 'POST':
        data = "You haven't filled out anything"
        return render_template("settings.html", data=data), 400
    else:
        data = "The server has encountered a situation it does not know how to handle."
        return render_template('settings.html', data=data), 500


def changePassword(username, db):
    user = User.getUser(db, username, "username")
    if request.method == 'POST' and request.form.get("currentPassword") and request.form.get("password"):
        current_password = request.form['currentPassword']
        if sha256_crypt.verify(current_password, user.password):
            new_password = sha256_crypt.hash(request.form['password'])
            User.changeValue(db, new_password, "password", user.id)
            data = "Password has successfully changed!"
            return render_template('edit_password.html', data=data), 200
        else:
            data = "Wrong password"
            return render_template('edit_password.html', data=data), 400
    elif request.method == 'POST':
        data = "Fill out the form!"
        return render_template("edit_password.html", data=data), 400
    else:
        data = "The server has encountered a situation it does not know how to handle."
        return render_template('edit_password.html', data=data), 500