from flask import render_template, Blueprint, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required

from aula import bcrypt
from aula.forms import UserLoginForm
from aula.models import select_users_by_cpr, get_posts_for_user

Login = Blueprint('Login', __name__)


@Login.route("/")
@Login.route("/home")
def home():
    if current_user.is_authenticated:
        posts = get_posts_for_user(current_user.get_id())
    else:
        posts = []
    return render_template('home.html', posts=posts)


@Login.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('Login.home'))

    form = UserLoginForm()
    # Først bekræft, at inputtet fra formen er gyldigt... (f.eks. ikke tomt)
    if form.validate_on_submit():
        user = select_users_by_cpr(form.cpr_num.data)
        # Derefter tjek om hashet af adgangskoden passer med det fra databasen...
        if user != None and bcrypt.check_password_hash(user[3], form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful.','success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Login.home'))
        else:
            flash('Login Unsuccessful. Please check identifier and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@Login.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('Login.home'))


@Login.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
