from django import forms
from publicationapp.models import *
from authapp.models import User
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class PubForm(forms.Form):
    author = forms.ModelChoiceField(queryset=User.objects.filter(role__in=[2, 4]), initial=0, label="Автор публикации:", empty_label="Ещё не выбрано", required=False)
    title = forms.CharField(max_length=135, label="Заголовок:", widget=forms.TextInput(attrs={'placeholder': 'Введите короткий интересный заголовок'}))
    type = forms.ModelChoiceField(queryset=PubTypes.objects.filter(id__in=(11, 21, 31)), initial=0, label="Тип публикации:", empty_label="Ещё не выбрано")
    preview = forms.FileField(label="Превью:", widget=forms.ClearableFileInput(attrs={'title':"Загрузите превью публикации"}), required=False)
    content = forms.CharField(widget=CKEditorUploadingWidget(), required=False)
    cost_min = forms.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(99999999999)], label="Финансовые затраты от, ₽:", widget=forms.TextInput(attrs={'placeholder':"0"}))
    cost_max = forms.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(99999999999)], label="Финансовые затраты до, ₽:", widget=forms.TextInput(attrs={'placeholder':"99999999999"}))
