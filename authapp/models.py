from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from publicationapp.models import Publication
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField

# user : password : role
# su1 : : admin + superuser
# 18091ikhgc : zxzxzx12 : watcher
# Astwim : request.POST : watcher
# authorONER : *_au_*thor : author
# NewUser : MOYproektTHEbest : watcher
# 222 : 222 : admin
# ksyu : 1212ks12 : Watcher
# Gleb_Olivki : GlebKrasavchik99 : Watcher
# Egor226 : Egor226 : author ????????????????
# rakamakafo : rakamakafo : author
# 18091 : 18091 : author

class User(AbstractUser):
    photo = models.ImageField(upload_to='users_avatars', blank=True, null=True, default='users_avatars/no_avatar.png', verbose_name='Аватарка')
    role = models.ForeignKey('UserRoles', on_delete=models.SET_DEFAULT, default=1, verbose_name='Роль в ИС', blank=False)
    bio = models.CharField(max_length=100, blank=True, null=True, verbose_name='Самоописание/статус')
    age = models.PositiveIntegerField(verbose_name='Возраст', null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(111)])
    phone_number = PhoneNumberField(null=True, blank=False, unique=True, verbose_name="Номер телефона")
    last_entry = models.DateTimeField(auto_now=True, verbose_name='Последняя авторизация')
    reported_count = models.IntegerField(default=0, verbose_name='Жалоб на пользователя')
    seen_count = models.IntegerField(default=0, verbose_name='Просмотров страницы пользователя')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    # def new_last_entry(self):
    #     self.save()

    @property
    def noties_new(self):
        return Notifications.objects.filter(user_receiver=self.pk, is_new=True).order_by('-when')

    @property
    def noties_old(self):
        return Notifications.objects.filter(user_receiver=self.pk, is_new=False).order_by('-when')[:20]

    @property
    def noties_count(self):
        return self.noties_new.count() + self.noties_old.count()

    @property
    def all_noties_count(self):
        return Notifications.objects.filter(user_receiver=self.pk).count()

    @property
    def new_noties_count(self):
        return self.noties_new.count()

    @property
    def is_only_one_superuser(self):
        if self.role.id != 4:
            return -1
        count = User.objects.filter(role=4).count()
        if count == 1:
            return True
        else:
            return False

    @property
    def made_pubs_count(self):
        return Publication.objects.filter(author=self, type__id__in=[11, 21, 31]).count()

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
    subscriber = models.ForeignKey('User', related_name="follower", on_delete=models.CASCADE, verbose_name='Подписчика')
    star = models.ForeignKey('User', related_name="star", on_delete=models.CASCADE, verbose_name='Пользователь, про чьи новые публикации подписчик получает уведомления')

    class Meta:
        verbose_name = 'Подписка пользователя'
        verbose_name_plural = 'Подписки пользователей'

    def __str__(self):
        return 'Subscriber ' + str(self.subscriber) + ' follows ' + str(self.star)


class ExpertInfo(models.Model):
    expert_account = models.OneToOneField('User', on_delete=models.CASCADE, unique=True, verbose_name='Аккаунт эксперта')
    count_follovers = models.PositiveIntegerField(default=0, verbose_name='Количество подписчиков')
    bisness_phone_number = PhoneNumberField(null=True, blank=True, verbose_name="Рабочий номер телефона (для клиентов)")
    knowledge = models.TextField(blank=True, null=True, max_length=5500, verbose_name='Стаж', default='')
    offer = models.TextField(blank=True, null=True, max_length=5500, verbose_name='Какую услугу предлагает', default='')
    site = models.CharField(blank=True, null=True, max_length=255, verbose_name='Ссылка на сайт', default='')
    address = models.CharField(blank=True, null=True, max_length=255, verbose_name='Адрес', default='')
    telegram = models.CharField(blank=True, null=True, max_length=255, verbose_name='Номер телефона, к которому привязан аккаунт Telegram', default='')
    whatsapp = models.CharField(blank=True, null=True, max_length=255, verbose_name='Номер телефона, к которому привязан аккаунт WhatsApp', default='')
    viber = models.CharField(blank=True, null=True, max_length=255, verbose_name='Номер телефона, к которому привязан аккаунт Viber', default='')
    lol = models.CharField(blank=True, null=True, max_length=255, verbose_name='Ссылка на профиль LifeOnLine', default='')
    vk = models.CharField(blank=True, null=True, max_length=255, verbose_name='Ссылка на профиль VK', default='')
    inst = models.CharField(blank=True, null=True, max_length=255, verbose_name='Ссылка на профиль Instagram', default='')
    ok = models.CharField(blank=True, null=True, max_length=255, verbose_name='Ссылка на профиль Одноклассники', default='')
    twitter = models.CharField(blank=True, null=True, max_length=255, verbose_name='Ссылка на профиль Facebook', default='')
    other = models.CharField(blank=True, null=True, max_length=255, verbose_name='Дополнительная контактная информация при необходимости', default='')

    class Meta:
        verbose_name = 'Экспертная информация о пользователе'
        verbose_name_plural = 'Экспертная информация о пользователе'

    @property
    def is_not_empty(self):
        empty_list = ['', None]
        answer = (
            not self.bisness_phone_number in empty_list or
            not self.knowledge in empty_list or
            not self.offer in empty_list or
            not self.site in empty_list or
            not self.address in empty_list or
            not self.telegram in empty_list or
            not self.whatsapp in empty_list or
            not self.viber in empty_list or
            not self.lol in empty_list or
            not self.vk in empty_list or
            not self.inst in empty_list or
            not self.ok in empty_list or
            not self.twitter in empty_list or
            not self.other in empty_list
        )
        return answer

    def count_follovers_changed(self, change_count):
        count_follovers += change_count
        self.save

    def __str__(self):
        return 'Expert ' + str(self.expert_account) + ', offer: ' + str(self.offer)


class SavedPubs(models.Model):
    when = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время сохранения публикации')
    saver = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='id сохранившего')
    pub = models.ForeignKey('publicationapp.Publication', on_delete=models.CASCADE, verbose_name='id публикации', default=0)

    class Meta:
        verbose_name = 'Сохранённая публикация'
        verbose_name_plural = 'Сохранённые публикации'

    def __str__(self):
        return 'saver ' + str(self.saver) + ' saved pub ' + str(self.pub)


class SeenPubs(models.Model):
    when = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время просмотра публикации')
    watcher = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='id просмотревшего')
    pub = models.ForeignKey('publicationapp.Publication', on_delete=models.CASCADE, verbose_name='id публикации', default=0)
    count = models.IntegerField(default=0, verbose_name='Сколько раз публикация была просмотрена')

    class Meta:
        verbose_name = 'Просмотренная публикация'
        verbose_name_plural = 'Просмотренные публикации'

    def __str__(self):
        return 'pub ' + str(self.pub) + ' seen by ' + str(self.watcher)


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
    asked_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name="made_question", verbose_name='Кто обратился в поддержку', null=True)
    ask_content = models.CharField(max_length=1555, verbose_name='Содержание обращения')
    ask_additional_info = models.IntegerField(verbose_name='Дополнительная информация к обращению', blank=True, null=True)
    when_asked = models.DateTimeField(verbose_name='Дата и время обращения в поддержку')
    answered_by = models.ForeignKey('User', on_delete=models.SET_NULL, related_name="made_answer", verbose_name='Ответ в лице поддержки от кого', blank=True, null=True)
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
