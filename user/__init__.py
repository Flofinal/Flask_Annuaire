from flask import Flask
from flask_mysqldb import MySQL
import logging

mysql = MySQL()


def create_app():
    app = Flask(__name__)
    app.config['MYSQL_HOST'] = 'db-test'
    app.config['MYSQL_USER'] = 'user'
    app.config['MYSQL_PASSWORD'] = 'password'
    app.config['MYSQL_DB'] = 'annuaire'
    app.config['SECRET_KEY'] = 'secret-key-goes-here'

    mysql.init_app(app)

    log = logging.getLogger('werkzeug')
    log.disabled = True

    logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', 
        datefmt='%d/%m/%Y %I:%M:%S %p', 
        filename='annuaire.log', 
        level=logging.INFO,
        filemode='w'
    )

    # blueprint for auth routes in our app
    from user.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app

