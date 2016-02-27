from wtforms_alchemy import ModelForm
from json_web_token import User, AccessType


class UserForm(ModelForm):
    template = 'templates/forms/user.html'

    class Meta:
        model = User
        include = ['access_type_id']