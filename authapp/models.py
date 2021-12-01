from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from publicationapp.models import Publication
# from repair_design_fields import settings

# user : password : role
# su1 : su1 : admin + superuser
# 18091ikhgc : zxzxzx12 : watcher

class User(AbstractUser):
    # USER_ROLE_CHOICES = (
    #     (0, 'SomethingGoesWrong'),
    #     (11, 'RepairPub'),
    #     (12', 'RepairLifehack'),
    #     (13, 'RepairBaseBook'),
    #     (21', 'DesignPub'),
    #     (22, 'DesignLifehack'),
    #     (31, 'ReportPub'),
    #     (32, 'ReportAccount'),
    #     (41, 'Notification'),
    # )

    photo = models.ImageField(upload_to='users_avatars', blank=True, null=True, default='users_avatars/no_avatar.png', verbose_name='Аватарка')
    role = models.ForeignKey('UserRoles', on_delete=models.SET_DEFAULT, default=1, verbose_name='Роль в ИС', blank=False)
    bio = models.CharField(max_length=100, blank=True, null=True, verbose_name='Самоописание/статус')
    age = models.PositiveIntegerField(verbose_name='Возраст')
    phone_number = models.PositiveIntegerField(null=True, blank=False, unique=True, verbose_name="Номер телефона")
    last_entry = models.DateTimeField(auto_now=True, verbose_name='Дата и время последней авторизации')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def new_last_entry(self):
        self.save()

    def __str__(self):
        return str(self.username) + ', ' + str(self.role)

class UserRoles(models.Model):
    # USER_ROLE_CHOICES = (
    #     (1, 'Watcher'),
    #     (2, 'Author'),
    #     (3, 'Admin'),
    # )choices=USER_ROLE_CHOICES
    id = models.PositiveIntegerField(primary_key=True, verbose_name='id роли')
    name = models.CharField(max_length=255, verbose_name='Значение роли')

    class Meta:
        verbose_name = 'Роль пользователя'
        verbose_name_plural = 'Роли пользователей'

    def __str__(self):
        return self.name

class UserSubscribes(models.Model):
    subscriber_id = models.ForeignKey('User', related_name="follower", on_delete=models.CASCADE, verbose_name='id подписчика')
    star_id = models.OneToOneField('User', related_name="star", on_delete=models.CASCADE, verbose_name='id пользователя, про чьи новые публикации подписчик получает уведомления')

    class Meta:
        verbose_name = 'Подписка пользователя'
        verbose_name_plural = 'Подписки пользователей'

    def __str__(self):
        return 'Subscriber ' + str(self.subscriber_id) + ' follows ' + str(self.star_id)

class ExpertInfo(models.Model):
    expert_id = models.OneToOneField('User', on_delete=models.CASCADE, unique=True, verbose_name='id эксперта')
    count_follovers = models.PositiveIntegerField(default=0, verbose_name='Количество подписчиков')
    knowledge = models.TextField(blank=True, null=True, max_length=255, verbose_name='Стаж')
    offer = models.TextField(blank=True, null=True, max_length=255, verbose_name='Какую услугу предлагает')
    site = models.CharField(blank=True, null=True, max_length=255, verbose_name='Ссылка на сайт')
    address = models.CharField(blank=True, null=True, max_length=255, verbose_name='Адрес')
    telegram = models.PositiveIntegerField(blank=True, null=True, verbose_name='Номер телефона, к которому привязан аккаунт Telegram')
    whatsapp = models.PositiveIntegerField(blank=True, null=True, verbose_name='Номер телефона, к которому привязан аккаунт WhatsApp')
    viber = models.PositiveIntegerField(blank=True, null=True, verbose_name='Номер телефона, к которому привязан аккаунт Viber')
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
        return 'Expert ' + str(self.subscriber_id) + ', offer: ' + str(self.offer)

class SavedPubs(models.Model):
    when = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время сохранения публикации')
    saver_id = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='id сохранившего')
    pub_id = models.OneToOneField('publicationapp.Publication', on_delete=models.CASCADE, verbose_name='id публикации', default=0)

    class Meta:
        verbose_name = 'Сохранённая публикация'
        verbose_name_plural = 'Сохранённые публикации'

    def __str__(self):
        return 'saver ' + str(self.saver_id) + ' saved pub ' + str(self.pub_id)

class SeenPubs(models.Model):
    when = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время просмотра публикации')
    watcher_id = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='id просмотревшего')
    pub_id = models.OneToOneField('publicationapp.Publication', on_delete=models.CASCADE, verbose_name='id публикации', default=0)

    class Meta:
        verbose_name = 'Просмотренная публикация'
        verbose_name_plural = 'Просмотренные публикации'

    def __str__(self):
        return 'pub ' + str(self.pub_id) + ' seen by ' + str(self.watcher_id)
