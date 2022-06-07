
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.formats import localize
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image
from publicationapp.models import Publication


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
    seen_count = models.IntegerField(default=0, verbose_name='Просмотров страницы пользователя')
    following_for = models.ManyToManyField('User', related_name="users_in_follows", verbose_name='Пользователь, про кого подписчик получает уведомления')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs): # ужать аватарку для экономии пространства на сервере
       instance = super(User, self).save(*args, **kwargs)
       image = Image.open(self.photo.path)
       image.save(self.photo.path, quality=10, optimize=True)
       return instance

    @property
    def made_pubs_count(self):
        return Publication.objects.filter(author=self, type__id__in=[11, 21, 31]).count()

    @property
    def reported_count(self):
        return ContactingSupport.objects.filter(ask_additional_info=self.id, type=12).count()

    @property
    def noties_new(self):
        return Notifications.objects.filter(receiver=self).exclude(receiver_saw=self)

    @property
    def noties_old(self):
        return Notifications.objects.filter(receiver=self, receiver_saw=self)

    @property
    def noties_count(self):
        return self.noties_new.count() + self.noties_old.count()

    @property
    def all_noties_count(self):
        return Notifications.objects.filter(receiver=self).count()

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
    def expert_info(self):
        expert_info = ExpertInfo.objects.get(expert_account=self) if ExpertInfo.objects.filter(expert_account=self) else None
        return expert_info

    def __str__(self):
        return str(self.username) + ', ' + str(self.role)


class UserRoles(models.Model):
    id = models.PositiveIntegerField(primary_key=True, verbose_name='id роли')
    name = models.CharField(max_length=255, verbose_name='Наименование роли')

    class Meta:
        verbose_name = 'Роль пользователя'
        verbose_name_plural = 'Роли пользователей'

    def __str__(self):
        return self.name


class ExpertInfo(models.Model):
    expert_account = models.OneToOneField('User', on_delete=models.CASCADE, unique=True, verbose_name='Аккаунт эксперта')
    knowledge = RichTextUploadingField(blank=True, max_length=5500, null=True, verbose_name='Стаж', default='')
    offer = RichTextUploadingField(blank=True, max_length=5500, null=True, verbose_name='Список предлагаемых услуг', default='')
    bisness_phone_number = PhoneNumberField(null=True, blank=True, verbose_name="Рабочий номер телефона (для клиентов)")
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
        verbose_name = 'Информация о специалисте'
        verbose_name_plural = 'Информация о специалистах'

    @property
    def count_follovers(self):
        return User.objects.filter(following_for__id=self.expert_account.id).count()

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

    def __str__(self):
        return 'Expert ' + str(self.expert_account)


class ActionTypes(models.Model): # событий много рзных бывает, в будующем можно создать таблицу категорий типов для сортировки/чего-то ещё
    id = models.PositiveIntegerField(primary_key=True, verbose_name='id типа события')
    name = models.CharField(max_length=255, verbose_name='Наименование типа события')
    icon = models.FileField(upload_to='action_types_icons', validators=[FileExtensionValidator(['png', 'jpg', 'svg', 'gif'])], blank=True, null=True, verbose_name='Иконка типа события')

    class Meta:
        verbose_name = 'Тип события'
        verbose_name_plural = 'Типы событий'

    def __str__(self):
        return self.name

class Notifications(models.Model):
    when_happend = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания уведомления')
    type = models.ForeignKey('ActionTypes', on_delete=models.SET_NULL, verbose_name='Тип события', blank=False, null=True)
    preview = models.ImageField(upload_to='notifications_preview', blank=True, null=True, verbose_name='Превью уведомления', default='../../static/sources/SVG/logo_mini.svg')
    content = models.CharField(max_length=500, verbose_name='Содержание уведомления')
    hover_text = models.CharField(max_length=100, verbose_name='Подсказка при наведении на уведомление')
    url = models.CharField(max_length=500, blank=True, null=True, verbose_name='Ссылка')
    url_text = models.CharField(max_length=500, blank=True, null=True, verbose_name='Текст на ссылке')
    receiver = models.ManyToManyField('User', related_name="receiver", verbose_name='Получатели уведомления')
    receiver_saw = models.ManyToManyField('User', related_name="receiver_saw", verbose_name='Просмотревшие уведомление')

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ('-when_happend',)

    @property
    def get_preview(self):
        preview = self.preview.url if not 'static/sources/SVG/logo_mini.svg' in self.preview.url else '../../static/sources/SVG/logo_mini.svg'
        return preview

    @property
    def icon(self):
        return self.type.icon

    def __str__(self):
        return 'receiver: ' + str(list(self.receiver.values_list('username', flat=True))).replace("[", "").replace("]", "").replace("'", "") + ', noti: ' + str(self.content) + ', when: ' + str(self.when_happend)


class JournalActions(models.Model):
    type = models.ForeignKey('ActionTypes', on_delete=models.SET_NULL, verbose_name='Тип события', blank=False, null=True)
    when = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время события')
    action_person = models.ForeignKey('User', on_delete=models.SET_NULL, related_name="person", null=True, verbose_name='Действующее лицо')
    action_content = models.CharField(max_length=1500, verbose_name='Содержание события')
    action_subjects_list = models.CharField(max_length=500, verbose_name='Список объектов, попавших в событие')

    class Meta:
        verbose_name = 'Одно событие'
        verbose_name_plural = 'Журнал событий'

    @property
    def icon(self):
        return self.type.icon

    def __str__(self):
        return str(self.type) + ', ' + str(self.action_person) + ', ' + str(localize(self.when))


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
        verbose_name_plural = 'Фотографии к обращениям в поддержку'

    def __str__(self):
        return 'обращение в поддержку: '+ str(self.contacting_support_action) + ', к нему фото: '+ str(self.photo)


class ContactingSupportTypes(models.Model):
    id = models.PositiveIntegerField(primary_key=True, verbose_name='id вида обращения')
    name = models.CharField(max_length=255, verbose_name='Наименование вида обращения')

    class Meta:
        verbose_name = 'Тип обращения в поддержку'
        verbose_name_plural = 'Типы обращений в поддержку'

    def __str__(self):
        return self.name
