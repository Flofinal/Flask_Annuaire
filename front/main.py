import json

import requests
from flask import Blueprint, render_template, url_for, request, flash
from flask_login import login_required, logout_user, login_user, current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import redirect
import os

from front.models import User

main = Blueprint('main', __name__)
headers = {
    'Content-Type': 'application/json'
}

url_path="http://user:5001/"

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/<variable>/adminpass',methods=['GET', 'POST'])
def adminpass(variable):
    return render_template('changePassUser.html',variable=variable)

@main.route('/login')
def login():
    return render_template('login.html')


@main.route('/deleteCurrentUser')
def deleteCurrentUser():
    return render_template('deleteCurrentUser.html')

@main.route('/signup')
def signupPage():
    return render_template('signup.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@main.route('/feed')
@login_required
def feed():
    url = url_path+"getuser"
    payload = json.dumps(
        dict(id=current_user.id)
    )
    r = requests.post(url, headers=headers, data=payload)
    res = r.json()
    if res["result"] == "nf":
        return render_template('feed.html')
    dictionary = json.loads(res["result"])
    return render_template('feed.html', user=dictionary)


@main.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    numero = request.form.get('numero')
    url = url_path+"signup_auth"
    payload = json.dumps(
        dict(email=email, name=name, password=password,numero=numero)
    )
    r = requests.post(url, headers=headers, data=payload)
    res = r.json()
    if current_user.is_authenticated:
        if res["result"] == "ok" and current_user.role == "admin":
            flash('Création réussite', "is-success")
        return redirect(url_for('main.signup'))
    if res["result"] == "try":
        flash('Email existe déjà', "is-danger")
        return redirect(url_for('main.signup'))
    if res["result"] == "ok":
        return redirect(url_for('main.login'))


@main.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    url = url_path+"login_auth"
    payload = json.dumps(
        dict(email=email, password=password)
    )

    r = requests.post(url, headers=headers, data=payload)
    res = r.json()
    if res["result"] == "wrong":
        flash('Mauvais mot de passe', "is-danger")
        return redirect(url_for('main.login'))  # if the user doesn't exist or password is wrong, reload the page
    dictionary = json.loads(res["result"])
    user = User(id=dictionary["id"],
                email=dictionary["email"],
                password=dictionary["password"],
                name=dictionary["name"], numero=dictionary["numero"],role=dictionary["role"])
    login_user(user, remember=remember)
    return redirect(url_for('main.feed'))


@main.route('/profile', methods=['POST'])
@login_required
def profile_pwd():
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    password3 = request.form.get('password3')
    if password3 != password2:
        flash("Les mots de passe sont différents", "is-danger")
        return redirect(url_for('main.profile'))
    if not check_password_hash(current_user.password, password1):
        flash('Mauvais mot de passe', "is-danger")
        return redirect(url_for('main.profile'))
    url = url_path+"profile_auth"
    payload = json.dumps(
        dict(email=current_user.email, password=password3)
    )
    r = requests.post(url, headers=headers, data=payload)
    res = r.json()
    if res["result"] == "ok":
        flash("Changement réussi", "is-success")
        return redirect(url_for('main.profile'))


@main.route('/recherche', methods=['POST'])
@login_required
def recherche():
    url = url_path+"getname"
    name = request.form.get('name')
    payload = json.dumps(
        dict(name=name)
    )
    r = requests.post(url, headers=headers, data=payload)
    res = r.json()
    if res["result"] == "nf":
        return render_template('feed.html',user=[])
    dictionary = json.loads(res["result"])
    return render_template('feed.html', user=dictionary)


@main.route('/supprimer', methods=['POST'])
@login_required
def supprimer():
    url = url_path+"deleteUser"
    email = request.form.get('supprimer')
    payload = json.dumps(
        dict(email=email)
    )
    r = requests.post(url, headers=headers, data=payload)
    res = r.json()
    return redirect(url_for('main.feed'))

@main.route('/promouvoir', methods=['POST'])
@login_required
def promouvoir():
    url = url_path+"promouvoir"
    email = request.form.get('promouvoir')
    payload = json.dumps(
        dict(email=email)
    )
    r = requests.post(url, headers=headers, data=payload)
    res = r.json()
    return redirect(url_for('main.feed'))

@main.route('/retrograder', methods=['POST'])
@login_required
def retrograder():
    url = url_path+"retrograder"
    email = request.form.get('retrograder')
    payload = json.dumps(
        dict(email=email)
    )
    r = requests.post(url, headers=headers, data=payload)
    res = r.json()
    return redirect(url_for('main.feed'))

@main.route('/changepass', methods=['POST'])
@login_required
def changepass():
    url = url_path+"profile_auth"
    email = request.form.get('changepass')
    password = request.form.get('password')
    payload = json.dumps(
        dict(email=email,password=password)
    )
    r = requests.post(url, headers=headers, data=payload)
    res = r.json()
    return redirect(url_for('main.feed'))


@main.route('/deleteUser', methods=['POST'])
@login_required
def deleteUser():
    url = url_path+"deleteUser"
    payload = json.dumps(
        dict(email=current_user.email)
    )
    r = requests.post(url, headers=headers, data=payload)
    res = r.json()
    return redirect(url_for('main.logout'))