from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import current_user


# Logic for registering a new user
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=35)])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


# logic for ensuring login details are correct
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


# logic for updating a users password
class PasswordUpdateForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
                             DataRequired(), Length(min=6)])
    new_password_repeat = PasswordField(
        'Repeat New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')

    def validate_old_password(self, old_password):
        if not check_password_hash(current_user.password_hash, old_password.data):
            raise ValidationError('Incorrect old password.')
