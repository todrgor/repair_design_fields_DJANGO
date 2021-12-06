from django import forms
from publicationapp.models import *

class PubForm(forms.Form):
    title = forms.CharField(max_length=135, label="Заголовок:", widget=forms.TextInput(attrs={'placeholder': 'Введите короткий интересный заголовок'}))
    preview = forms.FileField(label="Превью:", widget=forms.ClearableFileInput(attrs={'title':"Загрузите превью публикации"}))
    content_first_desc = forms.CharField(widget=forms.Textarea(attrs={'placeholder':"Сделайте текстовое описание Вашей публикации. Расскажите о важном.", 'title':"Сдеайте текстовое описание Вашей публикации. Расскажите о важном."}), label="Описание перед фотографиями:")
    photo = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'title':"Загрузите фотографии по теме публикации"}), label="Фотографии публикации:")
    content_last_desc = forms.CharField(widget=forms.Textarea(attrs={'placeholder':"Сделайте текстовое описание Вашей публикации. Расскажите о важном.",'title':"Сделайте текстовое описание Вашей публикации. Расскажите о важном."}), label="Описание после фотографий:", required=True)
    role = forms.ModelChoiceField(queryset=PubRoles.objects.filter(id__in=(11, 21, 31)), initial=0, label="Вид публикации:", empty_label="Ещё не выбрано")

    cost_min = forms.IntegerField(label="Бюджет на ремонт от, ₽:", widget=forms.TextInput(attrs={'placeholder':"0"}))
    cost_max = forms.IntegerField(label="Бюджет на ремонт до, ₽:", widget=forms.TextInput(attrs={'placeholder':"15000000000"}))

    tag_repair_what_to = forms.ModelChoiceField(queryset=TagName.objects.filter(tag_category="Ремонт чего"), initial=0, widget=forms.Select(attrs={'class':'repair'}), label="Ремонт: Ремонт чего:", empty_label="Ещё не выбрано")
    tag_repair_by_what = forms.ModelChoiceField(queryset=TagName.objects.filter(tag_category="Инструмент"), initial=0, widget=forms.Select(attrs={'class':'repair'}), label="Ремонт: Инструмент:", empty_label="Ещё не выбрано")
    tag_repair_where = forms.ModelChoiceField(queryset=TagName.objects.filter(tag_category="В помещении"), initial=0, widget=forms.Select(attrs={'class':'repair'}), label="Ремонт: В помещении:", empty_label="Ещё не выбрано")
    tag_design_room = forms.ModelChoiceField(queryset=TagName.objects.filter(tag_category="Комната"), initial=0, widget=forms.Select(attrs={'class':'design'}), label="Дизайн: Комната:", empty_label="Ещё не выбрано")
    tag_design_style = forms.ModelChoiceField(queryset=TagName.objects.filter(tag_category="Основной стиль"), initial=0, widget=forms.Select(attrs={'class':'design'}), label="Дизайн: Основной стиль:", empty_label="Ещё не выбрано")
    tag_lifehack_lifesphere = forms.ModelChoiceField(queryset=TagName.objects.filter(tag_category="В сфере жизни"), widget=forms.Select(attrs={'class':'lifehack'}), initial=0, label="Лайфхак: В сфере жизни:", empty_label="Ещё не выбрано")
