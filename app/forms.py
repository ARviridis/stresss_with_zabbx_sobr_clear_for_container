from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired

class LoginForm2(FlaskForm):
    username = StringField('UUsername', validators=[DataRequired()])
    password = PasswordField('PPassword', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class dev(FlaskForm):
    object1 = StringField('object1')
    object2 = StringField('object2')
    object3 = StringField('object3id')
    object4 = StringField('object4')
    object5 = StringField('object5')
    ppb = SubmitField('search')
    ppo = SubmitField('searcho')
    addb = SubmitField('add')
    gr_del_num = IntegerField()
    gr_del_num1 = IntegerField()