from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField
import random


# Create a form to register new users
class RegisterForm(FlaskForm):
    name = StringField("Nombre", validators=[DataRequired()])
    lastname = StringField("Apellido", validators=[DataRequired()])
    city = StringField("Ciudad", validators=[DataRequired()])
    username = StringField("Usuario", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Registrar")


# Create a form to login existing users
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Acceder")


# Create a form to add comments
class CommentForm(FlaskForm):
    comment_text = CKEditorField("Comentarios", validators=[DataRequired()])
    submit = SubmitField("Comentar")


# Create a form to change password
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Contraseña actual", validators=[DataRequired()])
    new_password = PasswordField("Nueva contraseña", validators=[DataRequired()])
    verificate_password = PasswordField("Valide contraseña", validators=[DataRequired()])
    submit = SubmitField("Cambiar")





