import json
import requests
from flask import Flask
from flask_login import LoginManager
import os

from front.models import User

url_path="http://10.20.0.2:5001/"



def create_app():
    print(url_path)
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    # blueprint for non-auth parts of app
    from front.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        url = url_path+"load_user2"

        payload = json.dumps(
            dict(id_user=user_id)
        )
        headers = {
            'Content-Type': 'application/json'
        }
        r = requests.post(url, headers=headers, data=payload)
        res = r.json()
        if res["result"] != "nf":
            dictionary = json.loads(res["result"])
            user = User(id=dictionary["id"],
                        email=dictionary["email"],
                        password=dictionary["password"],
                        name=dictionary["name"],numero=dictionary["numero"],role=dictionary["role"])
            return user

    return app
