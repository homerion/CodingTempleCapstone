from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email (phone for moblie accounts)', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    email = StringField('Email',validators=[Email(),DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmpass = PasswordField('Confirm Password', validators=[DataRequired(),
    EqualTo('password',message='Passwords do not match')])
    create_user = SubmitField('Submit')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("That email already exists")
