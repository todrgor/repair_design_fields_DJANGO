from django import forms

class AnswerForm(forms.Form):
    answer = forms.CharField(error_messages = {
                 'required':"Ответ должен быть содержательным, а не просто состоять из пробелов!"
                 }, widget=forms.Textarea(attrs={'placeholder':"Пользователь получит в уведомлении этот ответ. Расскажите о принятых решениях для этого обращения в поддержку",'title':"Сделайте ответ на обращение"}), label="Ответ обратившумуся пользователю")


class AnswerToReportForm(forms.Form):
    answer = forms.CharField(error_messages = {
                 'required':"Ответ должен быть содержательным, а не просто состоять из пробелов!"
                 }, widget=forms.Textarea(attrs={'placeholder':"Автор жалобы и объект жалобы (либо его автор) получат в уведомлении это сообщение. Так можно предупредить его или попросить что-то предпринять.",'title':"Напишите пользователям"}), label="Обращение к пользователю")
    # is_just_answer = forms.BooleanField(initial=True, label="Просто отправить ответ (всё ниже не сработает)", required=False)
    is_delete_pub = forms.BooleanField(initial=False, label="Удалить публикацию", required=False)
    is_deny_rules = forms.BooleanField(initial=False, label="Лишить пользователя/автора публикации его роли", required=False)
    is_delete_account = forms.BooleanField(initial=False, label="Удалить учётную запись пользователя/автора публикции", required=False)
