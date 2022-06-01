from django.contrib.auth.forms import forms, UserCreationForm, AuthenticationForm

from authapp.models import User, UserRoles, ContactingSupportTypes
from publicationapp.models import Publication

from phonenumber_field.formfields import PhoneNumberField
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget



class UserForm(forms.Form):
    role = forms.ModelChoiceField(queryset=UserRoles.objects.filter(), initial=1, label="Роль пользователя:", empty_label="Ещё не выбрано", required=False)
    username = forms.CharField(max_length=135, label="Никнейм:", widget=forms.TextInput(attrs={'placeholder': 'Ваш никнейм'}))
    photo = forms.ImageField(widget=forms.ClearableFileInput(attrs={'title': "Загрузите свою аватарку"}), label="Аватар пользователя:", required=False)
    bio = forms.CharField(max_length=135, label="Короткое самоописание или ваш актуальный статус:", widget=forms.TextInput(attrs={'placeholder': 'Короткое самоописание или статус'}), required=False)
    age = forms.IntegerField(label="Ваш возраст:", widget=forms.TextInput(attrs={'placeholder': "Ваш возраст", 'type': 'number'}), min_value=1, max_value=111)
    phone_number = PhoneNumberField(label="Ваш номер телефона:", widget=forms.TextInput(attrs={'placeholder': "Номер телефона"}))


class UserExpertForm(forms.Form):
    knowledge = forms.CharField(widget=CKEditorUploadingWidget(attrs={'placeholder': 'Расскажите о своём опыте работы, знаниях и особенностях. Например, как долго Вы работаете, с кем предпочтительно, какие у вас выполненные проекты (преветствуются ссылки на них), и а чём Вы больше всего компетентны.', 'title': 'Опишите свои опыт и навыки', }), max_length=5500, label="Стаж:", required=False)
    offer = forms.CharField(widget=CKEditorUploadingWidget(attrs={'placeholder': 'Опишите Вашу основную услугу для Вашей целевой аудитории ярко и ёмко.', 'title': 'Опишите свою услугу так, чтобы прям сейчас захотелось у вас эту услугу получить!', }), max_length=5500, label="Услуга:", required=False)
    site = forms.CharField(max_length=300, label="Сайт:", widget=forms.TextInput(attrs={'placeholder': 'Ваш сайт'}), required=False)
    bisness_phone_number = PhoneNumberField(label="Телефон для клиентов:", widget=forms.TextInput(attrs={'placeholder':"+7 800 555 35-55 – для клиентов"}), required=False)
    address = forms.CharField(max_length=300, label="Адрес:", widget=forms.TextInput(attrs={'placeholder': 'Адрес Вашего офиса'}), required=False)
    telegram = forms.CharField(max_length=300, label="Telegram:", widget=forms.TextInput(attrs={'placeholder': 'Telegram'}), required=False)
    whatsapp = forms.CharField(max_length=300, label="WhatsApp:", widget=forms.TextInput(attrs={'placeholder': 'WhatsApp'}), required=False)
    viber = forms.CharField(max_length=300, label="Viber:", widget=forms.TextInput(attrs={'placeholder': 'Viber'}), required=False)
    lol = forms.CharField(max_length=300, label="LifeOnLine:", widget=forms.TextInput(attrs={'placeholder': 'Профиль на LifeOnLine'}), required=False)
    vk = forms.CharField(max_length=300, label="ВКонтакте:", widget=forms.TextInput(attrs={'placeholder': 'Профиль во ВКонтакте'}), required=False)
    inst = forms.CharField(max_length=300, label="Instagram:", widget=forms.TextInput(attrs={'placeholder': 'Профиль в Instagram'}), required=False)
    ok = forms.CharField(max_length=300, label="Одноклассники:", widget=forms.TextInput(attrs={'placeholder': 'Профиль в Одноклассниках'}), required=False)
    twitter = forms.CharField(max_length=300, label="Twitter:", widget=forms.TextInput(attrs={'placeholder': 'Профиль в Twitter'}), required=False)
    other = forms.CharField(max_length=300, label="Дополнительно:", widget=forms.Textarea(attrs={'placeholder': 'Дополнительня контактная информация'}), required=False)


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


class UserPasswordForm(forms.Form):
    password = forms.CharField(label="Пароль:", widget=forms.TextInput(attrs={'placeholder': 'Пароль'}))


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = self.Meta.model._meta.get_field(field_name).verbose_name.capitalize if not 'password' in field_name else 'Пароль'

            field.help_text = ''
            field.label = ''


class BecomeATeammemberForm(forms.Form):
    desc = forms.CharField(error_messages = {
                 'required':"Ваше обращение должно быть содержательным, а не просто состоять из пробелов!"
                 }, widget=forms.Textarea(attrs={'placeholder':"Расскажите про себя и свой опыт", 'title':"Чем Вы хороши? Какими знаниями и опытом обладаете?"}), label="Расскажите о себе и своих умениях")
    photos = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'title':"Загрузите фотографии о себе"}), label="Если есть фотографии к заявке", required=False)


class BecomeAnAuthorForm(forms.Form):
    desc = forms.CharField(error_messages = {
                 'required':"Ваше обращение должно быть содержательным, а не просто состоять из пробелов!"
                 }, widget=forms.Textarea(attrs={'placeholder':"Расскажите, почему именно Вас нужно назначить автором публикаций. Может быть, Вы работали в стойбате 10 лет и знаете всё об устройстве дома? Или к примеру Вы — дизайнер, который не хочет придерживаться определённых стилей и воплощать своё виденье?", 'title':"Расскажите о себе: кто вы? Зачем вам быть автором? И в чём ваша полезность?"}), label="Расскажите о себе: кто вы? Зачем вам быть автором? И в чём ваша полезность?")
    photos = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'title':"Загрузите фотографии о себе"}), label="Если есть фотографии к заявке", required=False)


class SendToSupportForm(forms.Form):
    type = forms.ModelChoiceField(queryset=ContactingSupportTypes.objects.exclude(id=0), initial=32, label="Цель обращения", empty_label="Ещё не выбрано")
    complaint_account_id = forms.ModelChoiceField(queryset=User.objects.filter(), initial=0, label="Жалоба на пользователя", empty_label="Ещё не выбрано")
    complaint_pub_id = forms.ModelChoiceField(queryset=Publication.objects.filter(type__id__in=(11, 21, 31)), initial=0, label="Жалоба на публикацию", empty_label="Ещё не выбрано")
    desc = forms.CharField(error_messages = {
                 'required':"Ваше обращение должно быть содержательным, а не просто состоять из пробелов!"
                 }, widget=forms.Textarea(attrs={'placeholder':"Расскажите нам, что случилось?", 'title':"У вас какая-либо идея или проблема?"}), label="У вас какая-либо идея или проблема?")
    photos = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'title':"Загрузите фотографии к Вашему обращению"}), label="Если есть фотографии к Вашему обращению", required=False)
