from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


# Create a form to register new users
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    username = StringField("Usuario", validators=[DataRequired()])
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


