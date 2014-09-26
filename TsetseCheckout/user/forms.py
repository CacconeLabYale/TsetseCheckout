from flask.ext import uploads

from flask_wtf import Form, RecaptchaField
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired

from .models import User


class RegisterForm(Form):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Verify password', [DataRequired(), EqualTo('password', message='Passwords must match')])

    pi_name = StringField("PI's Name", validators=[DataRequired(), Length(min=3, max=25)])
    pi_email = StringField("PI's Email", validators=[DataRequired(), Email(), Length(min=6, max=40)])

    # recaptcha = RecaptchaField()

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True


