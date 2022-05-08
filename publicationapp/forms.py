from django import forms
from publicationapp.models import *
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class PubForm(forms.Form):
    title = forms.CharField(max_length=135, label="Заголовок:", widget=forms.TextInput(attrs={'placeholder': 'Введите короткий интересный заголовок'}))
    type = forms.ModelChoiceField(queryset=PubTypes.objects.filter(id__in=(11, 21, 31)), initial=0, label="Вид публикации:", empty_label="Ещё не выбрано")
    preview = forms.FileField(label="Превью:", widget=forms.ClearableFileInput(attrs={'title':"Загрузите превью публикации"}), required=False)
    content = forms.CharField(widget=CKEditorUploadingWidget())
    cost_min = forms.IntegerField(label="Финансовые затраты от, ₽:", widget=forms.TextInput(attrs={'placeholder':"0"}))
    cost_max = forms.IntegerField(label="Финансовые затраты до, ₽:", widget=forms.TextInput(attrs={'placeholder':"15000000000"}))
