from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_urlsafe
from housing_finder_app.models import User
from housing_finder_app.models import db
from housing_finder_app.auth.forms import LoginForm, RegisterForm
from dotenv import load_dotenv
import asyncio
from housing_finder_app.common.mail import send_email
from smtplib import SMTPException
from flask import current_app

load_dotenv(".env")

user_bp = Blueprint('user', __name__)


# REGISTER USER SECTION
@user_bp.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user email is already present in the database.
        user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
        if user:
            # User already exists
            flash("Ya estas registrado, ve e inicia sección!")
            return redirect(url_for('user.login'))

        new_user = User(
            name=form.name.data,
            lastname=form.lastname.data,
            city=form.city.data,
            email=form.email.data,
            password=generate_password_hash(
                password=form.password.data,
                method="pbkdf2:sha256",
                salt_length=8
            ),
            username=form.username.data,
            photo="static/images/profile.png"
        )
        db.session.add(new_user)
        db.session.commit()
        # This line will authenticate the user with Flask-Login
        login_user(new_user)
        return redirect(url_for("index.home"))
    return render_template("register.html", form=form, current_user=current_user)


# LOGIN USER SECTION
@user_bp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        user = User.query.filter((User.email == form.email_user.data) | (User.username == form.email_user.data)).first()
        # Email doesn't exist
        if not user:
            flash('El correo no existe, por favor trate de nuevo.')
            return redirect(url_for('user.register'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Contraseña incorrecta, por favor trate de nuevo.')
            return redirect(url_for('user.login'))
        else:
            login_user(user)
            return redirect(url_for("index.home"))
    return render_template("login.html", form=form, current_user=current_user)


# LOGOUT USER SECTION
@user_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.home'))


# FORGOT PASSWORD SECTION
@user_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == "POST":
        user = db.session.execute(db.select(User).where(User.email == request.form["email"].lower())).scalar()
        # Verify email correspond to a user registered
        if not user:
            flash("El correo no se registra en nuestra base de datos, por favor trate de nuevo.")
            return redirect(url_for('user.forgot_password'))
        # generate a new and temporal password
        temporal_password = token_urlsafe(8)
        # send the password for email
        try:
            send_email(subject=f'NO-REPLY: Tu nueva contraseña',
                       sender=current_app.config['DONT_REPLY_FROM_EMAIL'],
                       recipients=[request.form["email"].lower(), ],
                       text_body=f'Tu nueva contraseña es: {temporal_password}'
                       )
            # store this password on database
            new_password = generate_password_hash(
                password=temporal_password,
                method="pbkdf2:sha256",
                salt_length=8
            )
            user.password = new_password
            db.session.commit()
            flash("Tu nueva contraseña fue enviada a tu correo")

        except SMTPException:
             flash("Algo salió mal y no se pudo enviar el correo")
        return redirect(url_for('user.login'))
    return render_template("forgot_password.html")

