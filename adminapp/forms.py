from django import forms

class AnswerForm(forms.Form):
    answer = forms.CharField(error_messages = {
                 'required':"Ответ должен быть содержательным, а не просто состоять из пробелов!"
                 }, widget=forms.Textarea(attrs={'placeholder':"Пользователь получит в уведомлении этот ответ. Расскажите о принятых решениях для этого обращения в поддержку",'title':"Сделайте ответ на обращение"}), label="Ответ обратившумуся пользователю")
