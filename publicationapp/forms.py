from django import forms
from publicationapp.models import *

class PubForm(forms.Form):
    title = forms.CharField(max_length=135, label="Заголовок:", widget=forms.TextInput(attrs={'placeholder': 'Введите короткий интересный заголовок'}))
    preview = forms.FileField(label="Превью:", widget=forms.ClearableFileInput(attrs={'title':"Загрузите превью публикации"}))
    content_first_desc = forms.CharField(widget=forms.Textarea(attrs={'placeholder':"Сделайте текстовое описание Вашей публикации. Расскажите о важном.", 'title':"Сдеайте текстовое описание Вашей публикации. Расскажите о важном."}), label="Описание перед фотографиями:")
    photo = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'title':"Загрузите фотографии по теме публикации"}), label="Фотографии публикации:", required=False)
    content_last_desc = forms.CharField(widget=forms.Textarea(attrs={'placeholder':"Сделайте текстовое описание Вашей публикации. Расскажите о важном.",'title':"Сделайте текстовое описание Вашей публикации. Расскажите о важном."}), label="Описание после фотографий:", required=False)
    type = forms.ModelChoiceField(queryset=PubTypes.objects.filter(id__in=(11, 21, 31)), initial=0, label="Вид публикации:", empty_label="Ещё не выбрано")

    cost_min = forms.IntegerField(label="Финансовые затраты от, ₽:", widget=forms.TextInput(attrs={'placeholder':"0"}))
    cost_max = forms.IntegerField(label="Финансовые затраты до, ₽:", widget=forms.TextInput(attrs={'placeholder':"15000000000"}))
