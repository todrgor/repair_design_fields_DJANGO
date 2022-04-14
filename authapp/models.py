from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from publicationapp.models import Publication
from django.core.validators import MaxValueValidator, MinValueValidator
# from repair_design_fields import settings

# user : password : role
# su1 : : admin + superuser
# 18091ikhgc : zxzxzx12 : watcher
# Astwim : generatorseen : watcher
# authorONE : *_au_*thor : author
# NewUser : MOYproektTHEbest : watcher
# ksyu : 1212ks12 : Watcher
# Gleb_Olivki : GlebKrasavchik99 : Watcher

class User(AbstractUser):
    # last_entry работает странно и ненадёжно

    photo = models.ImageField(upload_to='users_avatars', blank=True, null=True, default='users_avatars/no_avatar.png', verbose_name='Аватарка')
    role = models.ForeignKey('UserRoles', on_delete=models.SET_DEFAULT, default=1, verbose_name='Роль в ИС', blank=False)
    bio = models.CharField(max_length=100, blank=True, null=True, verbose_name='Самоописание/статус')
    age = models.PositiveIntegerField(verbose_name='Возраст', null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(140)])
    phone_number = models.PositiveIntegerField(null=True, blank=False, unique=True, verbose_name="Номер телефона", validators=[MinValueValidator(1), MaxValueValidator(99999999999)])
    last_entry = models.DateTimeField(auto_now=True, verbose_name='Дата и время последней авторизации')
    reported_count = models.IntegerField(default=0, verbose_name='Сколько раз на пользователя было жалоб')
    seen_count = models.IntegerField(default=0, verbose_name='Сколько раз пользователя просматривали')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    # def new_last_entry(self):
    #     self.save()

    @property
    def noties_new(self):
        # user = User.objects.get(id=self.pk)
        noties_new = Notifications.objects.filter(user_receiver=self.pk, is_new=True).order_by('-when')
        return noties_new

    @property
    def noties_old(self):
        noties_old = Notifications.objects.filter(user_receiver=self.pk, is_new=False).order_by('-when')[:20]
        return noties_old

    @property
    def noties_count(self):
        user = User.objects.get(id=self.pk)
        noties_count = user.noties_new.count() + user.noties_old.count()
        return noties_count

    @property
    def new_noties_count(self):
        user = User.objects.get(id=self.pk)
        new_noties_count = user.noties_new.count()
        return new_noties_count

    def __str__(self):
        return str(self.username) + ', ' + str(self.role)


class UserRoles(models.Model):
    id = models.PositiveIntegerField(primary_key=True, verbose_name='id роли')
    name = models.CharField(max_length=255, verbose_name='Значение роли')

    class Meta:
        verbose_name = 'Роль пользователя'
        verbose_name_plural = 'Роли пользователей'

    def __str__(self):
        return self.name


class UserSubscribes(models.Model):
    # переделать нейминг и ввести правки в весь проект

    subscriber_id = models.ForeignKey('User', related_name="follower", on_delete=models.CASCADE, verbose_name='id подписчика')
    star_id = models.ForeignKey('User', related_name="star", on_delete=models.CASCADE, verbose_name='id пользователя, про чьи новые публикации подписчик получает уведомления')

    class Meta:
        verbose_name = 'Подписка пользователя'
        verbose_name_plural = 'Подписки пользователей'

    def __str__(self):
        return 'Subscriber ' + str(self.subscriber_id) + ' follows ' + str(self.star_id)


class ExpertInfo(models.Model):
    # переделать нейминг и ввести правки в весь проект

    expert_id = models.OneToOneField('User', on_delete=models.CASCADE, unique=True, verbose_name='id эксперта')
    count_follovers = models.PositiveIntegerField(default=0, verbose_name='Количество подписчиков')
    knowledge = models.TextField(blank=True, null=True, max_length=1500, verbose_name='Стаж')
    offer = models.TextField(blank=True, null=True, max_length=1500, verbose_name='Какую услугу предлагает')
    site = models.CharField(blank=True, null=True, max_length=255, verbose_name='Ссылка на сайт')
    address = models.CharField(blank=True, null=True, max_length=255, verbose_name='Адрес')
    telegram = models.CharField(blank=True, null=True, max_length=255, verbose_name='Номер телефона, к которому привязан аккаунт Telegram')
    whatsapp = models.CharField(blank=True, null=True, max_length=255, verbose_name='Номер телефона, к которому привязан аккаунт WhatsApp')
    viber = models.CharField(blank=True, null=True, max_length=255, verbose_name='Номер телефона, к которому привязан аккаунт Viber')
    vk = models.CharField(blank=True, null=True, max_length=255, verbose_name='Ссылка на профиль ВК')
    inst = models.CharField(blank=True, null=True, max_length=255, verbose_name='Ссылка на профиль Инстаграм')
    ok = models.CharField(blank=True, null=True, max_length=255, verbose_name='Ссылка на профиль Одноклассники')
    fb = models.CharField(blank=True, null=True, max_length=255, verbose_name='Ссылка на профиль facebook')
    other = models.CharField(blank=True, null=True, max_length=255, verbose_name='Дополнительная контактная информация при необходимости')

    class Meta:
        verbose_name = 'Экспертная информация о пользователе'
        verbose_name_plural = 'Экспертная информация о пользователе'

    def count_follovers_changed(self, change_count):
        count_follovers += change_count
        self.save

    def __str__(self):
        return 'Expert ' + str(self.expert_id) + ', offer: ' + str(self.offer)


class SavedPubs(models.Model):
    # переделать нейминг и ввести правки в весь проект

    when = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время сохранения публикации')
    saver_id = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='id сохранившего')
    pub_id = models.ForeignKey('publicationapp.Publication', on_delete=models.CASCADE, verbose_name='id публикации', default=0)

    class Meta:
        verbose_name = 'Сохранённая публикация'
        verbose_name_plural = 'Сохранённые публикации'

    def __str__(self):
        return 'saver ' + str(self.saver_id) + ' saved pub ' + str(self.pub_id)


class SeenPubs(models.Model):
    # переделать нейминг и ввести правки в весь проект

    when = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время просмотра публикации')
    watcher_id = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='id просмотревшего')
    pub_id = models.ForeignKey('publicationapp.Publication', on_delete=models.CASCADE, verbose_name='id публикации', default=0)
    count = models.IntegerField(default=0, verbose_name='Сколько раз публикация была просмотрена')

    class Meta:
        verbose_name = 'Просмотренная публикация'
        verbose_name_plural = 'Просмотренные публикации'

    def __str__(self):
        return 'pub ' + str(self.pub_id) + ' seen by ' + str(self.watcher_id)


class Notifications(models.Model):
    when = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания уведомления')
    user_receiver = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='id получателя уведомлении')
    noti_for_user = models.ForeignKey('publicationapp.Publication', on_delete=models.CASCADE, verbose_name='id публикации-уведомления', default=0)
    is_new = models.BooleanField(default=True, verbose_name='Уведомление новое?')

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return 'user_receiver: ' + str(self.user_receiver) + ', noti_for_user: ' + str(self.noti_for_user) + ', when: ' + str(self.when)


class ContactingSupport(models.Model):
    title = models.CharField(max_length=99, verbose_name='Заголовок события', default='000')
    asked_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name="made_question", verbose_name='Кто обратился в поддержку')
    ask_content = models.CharField(max_length=1555, verbose_name='Содержание обращения')
    ask_additional_info = models.IntegerField(verbose_name='Дополнительная информация к обращению', blank=True, null=True)
    when_asked = models.DateTimeField(verbose_name='Дата и время обращения в поддержку')
    answered_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name="made_answer", verbose_name='Ответ в лице поддержки от кого', blank=True, null=True)
    answer_content = models.CharField(max_length=1555, verbose_name='Содержание ответа', blank=True, null=True)
    answer_additional_info = models.IntegerField(verbose_name='Дополнительная информация к ответу', blank=True, null=True)
    when_answered = models.DateTimeField(verbose_name='Дата и время ответа на обращение', blank=True, null=True)
    type = models.ForeignKey('ContactingSupportTypes', on_delete=models.SET_DEFAULT, default=0, verbose_name='Вид обращения в поддержку', blank=False)

    class Meta:
        verbose_name = 'Обращение в поддержку'
        verbose_name_plural = 'Обращения в поддержку'
        ordering = ('-when_asked',)

    def __str__(self):
        return self.title


class ContactingSupportPhotos(models.Model):
    contacting_support_action = models.ForeignKey('ContactingSupport', verbose_name='id обращения', on_delete=models.CASCADE)
    photo = models.ImageField(max_length=200, upload_to='contacting_support_media', verbose_name='Фотография обращения')

    class Meta:
        verbose_name = 'Фотография к обращению в поддержку'
        verbose_name_plural = 'Фотографии к обращению в поддержку'

    def __str__(self):
        return 'обращение в поддержку: '+ str(self.contacting_support_action) + ', к нему фото: '+ str(self.photo)


class ContactingSupportTypes(models.Model):
    id = models.PositiveIntegerField(primary_key=True, verbose_name='id вида обращения')
    name = models.CharField(max_length=255, verbose_name='Значение вида обращения')

    class Meta:
        verbose_name = 'Вид обращения в поддержку'
        verbose_name_plural = 'Виды обращений в поддержку'

    def __str__(self):
        return self.name
