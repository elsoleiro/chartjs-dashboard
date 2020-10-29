from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, PasswordField, SubmitField, StringField, BooleanField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from chartjs_dashboard.models import User
import pandas as pd

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirmpassword = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Invalid username')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Invalid email')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')




class ActiveEHOForm(FlaskForm):
    activeEHOData = pd.read_csv('chartjs_dashboard/datasets/ActiveEHOConcernsYTDWWT.csv')
    activeEHOData = activeEHOData.fillna(0)
    x = list(activeEHOData.columns)

    date = SelectField('date', choices=x)
    val = IntegerField('val', [validators.DataRequired()])


class HighRiskSites(FlaskForm):
    highriskData = pd.read_csv('chartjs_dashboard/datasets/HighRiskSitesYTDWWT.csv')
    highriskData = highriskData.fillna(0)
    x = list(highriskData.columns)
    y = list(highriskData.iloc[0].values)
    data_tuples = dict(zip(x, y))
    y = [int(i) for i in y]

    labels = x
    values = y
    date = SelectField('date', choices=x)
    val = IntegerField('val')


class PersistentComplaints(FlaskForm):
    persistentComplaintsData = pd.read_csv('chartjs_dashboard/datasets/PersistentComplaintsYTDWWT.csv')
    persistentComplaintsData = persistentComplaintsData.fillna(0)
    x = list(persistentComplaintsData.columns)
    y = list(persistentComplaintsData.iloc[0].values)
    data_tuples = dict(zip(x, y))
    y = [int(i) for i in y]

    labels = x
    values = y
    date = SelectField('date', choices=x)
    val = IntegerField('val')

class LostTimeKPI(FlaskForm):
    kpiDashData = pd.read_csv('chartjs_dashboard/datasets/kpidash.csv')
    vals = list(kpiDashData.iloc[0].values)
    modifier = SelectField('modifier', choices=vals)
    val = StringField('val')    
