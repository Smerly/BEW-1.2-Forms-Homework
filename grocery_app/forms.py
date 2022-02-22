from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField, PasswordField, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL
from grocery_app.models import ItemCategory, GroceryStore, User
from grocery_app.extensions import bcrypt


class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""
    # - title - StringField
    # - address - StringField
    # - submit button
    title = StringField('Store Name', validators=[DataRequired(), Length(
        min=2, max=30)])
    address = StringField('Address', validators=[
                          DataRequired(), Length(min=10, max=60)])
    submit = SubmitField('Submit')

    pass


class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""
    # - name - StringField
    # - price - FloatField
    # - category - SelectField (specify the 'choices' param)
    # - photo_url - StringField
    # - store - QuerySelectField (specify the `query_factory` param)
    # - submit button

    name = StringField('Item_name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    category = SelectField('Category', choices=ItemCategory.choices())
    photo_url = StringField('Photo URL', validators=[DataRequired()])
    store = QuerySelectField('Store', query_factory=lambda: GroceryStore.query)
    submit = SubmitField('Submit')

    pass


class SignUpForm(FlaskForm):
    username = StringField('User Name',
                           validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('User Name',
                           validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError(
                'No user with that username. Please try again.')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password doesn\'t match. Please try again.')
