from flask import Blueprint, render_template, flash, redirect, url_for, request
from ccsi.forms.forms import ApiRegForm, LoginForm, UserRegForm
from ccsi import db, bcrypt
from ccsi.db_models import User
from flask_login import login_user, logout_user, current_user, login_required
from ccsi.parsers import open_description_parser
from requests import get

forms = Blueprint('forms', __name__)


@forms.route("/api_reg", methods=['GET', 'POST'])
@login_required
def api_reg():
    """Formular to API registration """
    form = ApiRegForm()
    if form.validate_on_submit():
        api_params, _ = open_description_parser.decode_description(get(form.descriptor_url.data))
        flash(f'Description document parsed', 'success')
        return render_template('api_reg.html', title='Api registration', form=form, api_params=api_params)
    return render_template('api_reg.html', title='Api registration', form=form)


@forms.route("/login", methods=['GET', 'POST'])
def login():
    """Login into backoffice"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login successful', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        flash('Unsuccessful login. Please check your Username and Password', 'danger')
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Login', form=form)


@forms.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = UserRegForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account was created', 'success')
        return redirect(url_for('main.index'))
    return render_template('user_reg.html', title='Register', form=form)

@forms.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))