from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from mysite.models import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        g = User.query.filter_by(name=username.data).first()
        if g:
            raise ValidationError("this username is already taken!")

    def validate_email(self, email):
        g = User.query.filter_by(email=email.data).first()
        if g:
            raise ValidationError("this email is already taken!")


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class Update_Form(FlaskForm):
    username = StringField('Username',
                           validators=[Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[Email()])
    p_img = FileField('update ur profile pic : ', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update Info')

    def validate_username(self, username):
        if username.data != current_user.name:
            g = User.query.filter_by(name=username.data).first()
            if g:
                raise ValidationError("this username is already taken!")

    def validate_email(self, email):
        if email.data != current_user.email:
            g = User.query.filter_by(email=email.data).first()
            if g:
                raise ValidationError("this email is already taken!")


class Postform(FlaskForm):
    title = StringField("title", validators=[DataRequired()])
    content = TextAreaField("content", validators=[DataRequired()])
    submit = SubmitField('Post')


class Reset_form(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('request reset password')

    def validate_email(self, email):
        g = User.query.filter_by(email=email.data).first()
        if g is None:
            raise ValidationError("this email is not registered yet!!")


class Reset_password(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('reset password')
