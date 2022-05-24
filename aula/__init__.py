from flask import Flask
import psycopg2
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fc089b9218301ad987914c53481bff04'
# set your own database
db = "dbname='aula' user='postgres' host='127.0.0.1' password = 'UIS'"
conn = psycopg2.connect(db)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from aula.Login.routes import Login
# from bank.Customer.routes import Customer
# from bank.Employee.routes import Employee
# from bank.Pax.routes import Pax
app.register_blueprint(Login)
# app.register_blueprint(Customer)
# app.register_blueprint(Employee)
# app.register_blueprint(Pax)

#from bank import routes