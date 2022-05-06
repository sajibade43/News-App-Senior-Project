from flask import Flask
from flask_mail import Mail

app = Flask(__name__)

app.secret_key = 'key'

app.config['MYSQL_DATABASE_HOST'] = 'database-2.c66o8xpkeycc.us-east-1.rds.amazonaws.com'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'blue0918'
app.config['MYSQL_DATABASE_DB'] = 'SP_login'


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config["MAIL_USE_TLS"] = True
app.config['MAIL_USERNAME'] = 'spnews89@gmail.com'
app.config['MAIL_PASSWORD'] = 'Blue0918!'
app.config['DEBUG'] = True

mail = Mail(app)