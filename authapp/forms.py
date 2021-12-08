from django.contrib.auth.forms import forms, UserCreationForm, AuthenticationForm

from authapp.models import User

class UserForm(forms.Form):
    username = forms.CharField(max_length=135, label="Никнейм:", widget=forms.TextInput(attrs={'placeholder': 'Ваш никнейм'}))
    photo = forms.ImageField(widget=forms.ClearableFileInput(attrs={'title':"Загрузите свою аватарку"}), label="Аватар пользователя:", required=False)
    bio = forms.CharField(max_length=135, label="Короткое самоописание или ваш актуальный статус:", widget=forms.TextInput(attrs={'placeholder': 'Короткое самоописание или статус'}), required=False)
    age = forms.IntegerField(label="Ваш возраст:", widget=forms.TextInput(attrs={'placeholder':"Ваш возраст"}))
    phone_number = forms.IntegerField(label="Ваш номер телефона:", widget=forms.TextInput(attrs={'placeholder':"Номер телефона"}))

class UserExpertForm(forms.Form):
    knowledge = forms.CharField(max_length=1500, label="Стаж:", widget=forms.Textarea(attrs={'placeholder': 'Расскажите о своём опыте работы, знаниях и особенностях. Например, как долго Вы работаете, с кем предпочтительно, какие у вас выполненные проекты (преветствуются ссылки на них), и а чём Вы больше всего компетентны.', 'title': 'Опишите свои опыт и навыки', }), required=False)
    offer = forms.CharField(max_length=1500, label="Услуга:", widget=forms.Textarea(attrs={'placeholder': 'Опишите Вашу основную услугу для Вашей целевой аудитории ярко и ёмко.', 'title': 'Опишите свою услугу так, чтобы прям сейчас захотелось у вас эту услугу получить!', }), required=False)
    site = forms.CharField(max_length=300, label="Сайт:", widget=forms.TextInput(attrs={'placeholder': 'Ваш сайт'}), required=False)
    address = forms.CharField(max_length=300, label="Адрес:", widget=forms.TextInput(attrs={'placeholder': 'Адрес Вашего офиса'}), required=False)
    telegram = forms.CharField(max_length=300, label="Телеграм:", widget=forms.TextInput(attrs={'placeholder': 'Телеграм'}), required=False)
    whatsapp = forms.CharField(max_length=300, label="WhatsApp:", widget=forms.TextInput(attrs={'placeholder': 'WhatsApp'}), required=False)
    viber = forms.CharField(max_length=300, label="Viber:", widget=forms.TextInput(attrs={'placeholder': 'Viber'}), required=False)
    vk = forms.CharField(max_length=300, label="Вконтакте:", widget=forms.TextInput(attrs={'placeholder': 'Профиль вконтакте'}), required=False)
    inst = forms.CharField(max_length=300, label="Instagram:", widget=forms.TextInput(attrs={'placeholder': 'Профиль в Instagram'}), required=False)
    ok = forms.CharField(max_length=300, label="Сайт:", widget=forms.TextInput(attrs={'placeholder': 'Профиль в Одноклассниках'}), required=False)
    fb = forms.CharField(max_length=300, label="Сайт:", widget=forms.TextInput(attrs={'placeholder': 'Профиль на Facebook'}), required=False)
    other = forms.CharField(max_length=300, label="Сайт:", widget=forms.TextInput(attrs={'placeholder': 'Если понадобится указать дополнительную информацию'}), required=False)

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
