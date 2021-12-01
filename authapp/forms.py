from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from authapp.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email',  'phone_number', 'age',  'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

            if not 'password' in field_name:
                field.widget.attrs['placeholder'] = self.Meta.model._meta.get_field(field_name).verbose_name.capitalize
            else:
                field.widget.attrs['placeholder'] = 'Пароль'
                if field_name == 'password2':
                    field.widget.attrs['placeholder'] = 'Повторите пароль'
            field.help_text = ''
            field.label = ''


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

            if not 'password' in field_name:
                field.widget.attrs['placeholder'] = self.Meta.model._meta.get_field(field_name).verbose_name.capitalize
            else:
                field.widget.attrs['placeholder'] = 'Пароль'

            field.help_text = ''
            field.label = ''
