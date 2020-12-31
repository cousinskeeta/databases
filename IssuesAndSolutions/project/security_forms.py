from flask_security.forms import LoginForm, RegisterForm
from wtforms import StringField
from wtforms.validators import DataRequired, Required

# class ExtendedLoginForm(LoginForm):
#     first_name = StringField('First Name', [Required()])
#     last_name = StringField('Last Name', [Required()])

class ExtendedRegisterForm(RegisterForm):
    name = StringField('name', [Required()])

# class ExtendedRegisterForm(RegisterForm):
#     first_name = StringField('First Name', [Required()])
#     last_name = StringField('Last Name', [Required()])

# class ExtendedRegisterForm(RegisterForm):
#     first_name = StringField('First Name', [Required()])
#     last_name = StringField('Last Name', [Required()])

# class ExtendedRegisterForm(RegisterForm):
#     first_name = StringField('First Name', [Required()])
#     last_name = StringField('Last Name', [Required()])

# class ExtendedRegisterForm(RegisterForm):
#     first_name = StringField('First Name', [Required()])
#     last_name = StringField('Last Name', [Required()])

# class ExtendedRegisterForm(RegisterForm):
#     first_name = StringField('First Name', [Required()])
#     last_name = StringField('Last Name', [Required()])

# class ExtendedRegisterForm(RegisterForm):
#     first_name = StringField('First Name', [Required()])
#     last_name = StringField('Last Name', [Required()])
