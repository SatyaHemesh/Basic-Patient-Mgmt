from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField,
    IntegerField, TextAreaField, DateField,
    DecimalField, SelectField
)
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, NumberRange


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=100)])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

class PatientForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(max=255)])
    age = IntegerField("Age", validators=[Optional(), NumberRange(min=0)])
    gender = SelectField("Gender", choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")])
    phone = StringField("Phone", validators=[Optional(), Length(max=20)])
    address = TextAreaField("Address", validators=[Optional()])
    submit = SubmitField("Save Patient")

class VisitForm(FlaskForm):
    reason = TextAreaField("Reason for Visit", validators=[Optional()])
    diagnosis = TextAreaField("Diagnosis", validators=[Optional()])
    treatment = TextAreaField("Treatment", validators=[Optional()])
    fees_paid = FloatField("Fees Paid", validators=[Optional(), NumberRange(min=0)])
    submit = SubmitField("Save Visit")
