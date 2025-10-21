from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, URL, Length, Email
from flask_ckeditor import CKEditorField

class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

class RegisterForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Length(max=100, message="Email must be 100 characters long"), Email(message="Must be a valid email")])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=100,  message="Password must not be above 100 characters")])
    username = StringField("Username", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Length(max=100, message="Email must be 100 characters long"), Email(message="Must be a valid email")])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=100, message="Password must not be above 100 characters")])
    submit = SubmitField("Register")

class CommentForm(FlaskForm):
    comment = CKEditorField("Comment", validators=[DataRequired(), Length(max=500, message="Comment must not exceed 500 character cout")])
    submit = SubmitField("Submit Comment")