from django import forms
from publicationapp.models import *

class PubForm(forms.Form):
    preview = forms.FileField()
    title = forms.CharField(max_length=135)
    content_first_desc = forms.CharField(widget=forms.Textarea())
    photo = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    content_last_desc = forms.CharField(widget=forms.Textarea())
    role = forms.CharField(max_length=135)

    cost_min = forms.IntegerField()
    cost_max = forms.IntegerField()
    tag_repair_what = forms.CharField(max_length=135)
    tag_repair_what_to = forms.CharField(max_length=135)
    tag_repair_by_what = forms.CharField(max_length=135)
    tag_repair_where = forms.CharField(max_length=135)
    tag_design_room = forms.CharField(max_length=135)
    tag_design_style = forms.CharField(max_length=13)
    tag_lifehack_lifesphere = forms.CharField(max_length=135)
