from flask import flash
#--flask wtf
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from warships_blog.classes import User

#-- Forms para login/register


#-Estas clases con variables las llamaremos en las paguinas que queramos hacer un formulario

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("Introduce un nombre de usuario valido")])
    #email = StringField('Email', validators=[DataRequired("Introduce un mail valido"), Email()])
    password = PasswordField('Password', validators=[DataRequired("Contraseña")])
    submit = SubmitField('Login')
    
class RegistrationForm(FlaskForm):    
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign_Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            flash('Error Register. El USERNAME ya esta siendo usado, selecciona otro', 'danger')#este msg sale en el html del cliente,, lo de danger es el tipo de error, en danger saldra de color rojo, info azul etc...
            raise ValidationError('El USERNAME ya esta siendo usado, selecciona otro')#este msg sale en la terminal

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            flash('Error Register. El EMAIL ya esta siendo usado, selecciona otro', 'danger')
            raise ValidationError('El EMAIL ya esta siendo usado, selecciona otro.')


