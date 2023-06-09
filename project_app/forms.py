from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, TextAreaField, FileField, SelectField
from wtforms.validators import Length, Regexp, DataRequired, EqualTo, Email
from wtforms import ValidationError
from models import User
from database import db


class RegisterForm(FlaskForm):
    class Meta:
        csrf = False

    firstname = StringField('First Name', validators=[Length(1, 10)])

    lastname = StringField('Last Name', validators=[Length(1, 20)])

    email = StringField('Email', [
        Email(message='Not a valid email address.'),
        DataRequired()])

    password = PasswordField('Password', [
        DataRequired(message="Please enter a password."),
        EqualTo('confirmPassword', message='Passwords must match and be between 6 and 10 characters')
    ])

    confirmPassword = PasswordField('Confirm Password', validators=[
        Length(min=6, max=10),
        Regexp('(?=.*[A-Z])(?=.*[!,@,#,$,%,^,&,*,(,),?])(?=.*\d).+', message="Password must contain at least 1 capital letter, special character, and number") 
        #search for at least 1 capital letter, special character, and number
        #cases:
            #num,cap,spec   a1bAc!
            #num,spec,cap   ab1!Aa
            #cap,num,spec   aAb1!a
            #cap,spec,num   aAb!1a
            #spec,num,cap   ab!1Aa
            #spec,cap,num   ab!Ac1
    ])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).count() != 0:
            raise ValidationError('Username already in use.')


class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    email = StringField('Email', [
        Email(message='Not a valid email address.'),
        DataRequired()])

    password = PasswordField('Password', [
        DataRequired(message="Please enter a password.")])

    submit = SubmitField('Submit')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).count() == 0:
            raise ValidationError('Incorrect username or password.')


class InputTextForm(FlaskForm):
    class Meta:
        csrf = False

    input_text = TextAreaField('Enter text')

    attach_text_file = FileField('Upload text file')

    attach_image_file = FileField('Upload image file')

    algorithm_choice = SelectField('Algorithm:', validate_choice=False, choices=[(0, 'Distance'), (1, 'Bag of Words')])

    sentence_resolution = SelectField('Resolution:', validate_choice=False, choices=[(1, '1 Sentence'), (2, '2 Sentences'), (3, '3 Sentences')])

    genre_choice = SelectField('Genre:', validate_choice=False, default="news",
                               choices=[("news", "News Article"), ("blog", "Blog Post"),
                                        ("dialogue", "Dialogue"), ("tutorial", "Tutorial"),
                                        ("fiction", "Fiction"), ("xsum", "One Sentence Summary")])

    model_choice = SelectField('Suggested Model:', validate_choice=False, choices=[('bart-cnn-25-6-5', "Bart-Large-CNN"), ('pegasus-cnn-25-6-5',
                                                                                    "Pegasus-Large-CNN"), ('flan-t5-25-6-5', "Flan-T5-Base")])

    sentence_extraction_button = SubmitField('Sentence Extraction')

    transformer_model_button = SubmitField('Transformer Models')

    submit_text = SubmitField('Submit')

    #username = TextAreaField('Username')

    '''{{form.input_text}} <br/>
        {{form.attach_text_file}}<br/>
        {{form.attach_image_file}}<br/>
        <!--p><input type="submit" value="Summarize"/></p-->
        {{ form.submit_text}}
    </div>
    <div>
        {{form.algorithm_choice}}<br/>
        {{form.sentence_resolution}}<br/>'''