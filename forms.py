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


letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
           'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
           'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


class RandomPassword:

    def __init__(self):
        self.password_letter = [random.choice(letters) for _ in range(2)]
        self.password_symbol = [random.choice(symbols) for _ in range(2)]
        self.password_number = [random.choice(numbers) for _ in range(2)]

    def generate_password(self):
        password_list = self.password_number + self.password_letter + self.password_symbol
        random.shuffle(password_list)
        text_password = "".join(password_list)
        return text_password



