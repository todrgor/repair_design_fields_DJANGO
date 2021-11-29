from django.db import models
from authapp.models import User
# from repair_design_fields import settings

class Publication(models.Model):
    title = models.CharField(max_length=135, verbose_name='Заголовок публикации')
    role = models.OneToOneField('PubRoles', on_delete=models.SET_NULL, null=True)
    preview = models.ImageField(max_length=200, verbose_name='Превью')
    content_first_desc =  models.TextField(, verbose_name='Текст перед фотографиями')
    content_last_desc =  models.TextField(, verbose_name='Текст после фотографий')
    author_id = models.ForeignKey('User', on_delete=models.DO_NOTHING, null=True, verbose_name='Автор') # как сделать самоудаление при удлении юзера????
    pushed = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время публикации')
    seen_count = models.IntegerField(default=0, verbose_name='Сколько раз публикация была просмотрена')
    saved_count = models.IntegerField(default=0, verbose_name='Сколько раз публикация была сохранена')
    reported_count = models.IntegerField(default=0, verbose_name='Сколько раз на публикация было жалоб')
    shared_count = models.IntegerField(default=0, verbose_name='Сколько раз нажали поделиться публикацией')
    average_age_watchers = models.IntegerField(default=0, verbose_name='Средний возраст просмотревших')
    average_age_savers = models.IntegerField(default=0, verbose_name='Средний возраст сохранивших')

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pushed',)

    def opened(self):
        self.seen_count +=1
        self.save

    def reported(self):
        self.reported_count +=1
        self.save

    def shared(self):
        self.shared_count +=1
        self.save

    def saved(self):
        self.saved_count +=1
        self.save

    def ansaved(self):
        self.saved_count -=1
        self.save

    def __str__(self):
        return 'Title: ' + str(self.title) + ', role id: ' + str(self.role)

class PubPhotos(models.Model):
    id_pub = models.ForeignKey('Publication', verbose_name='id публикации')
    photo = models.ImageField(max_length=200, verbose_name='Фотографии публикации')

    class Meta:
        verbose_name = 'Фотография публикации'
        verbose_name_plural = 'Фотографии публикации'

    def __str__(self):
        return self.photo

class PubRoles(models.Model):
    # PUB_ROLE_CHOICES = (
    #     ('11', 'RepairPub'),
    #     ('12', 'RepairLifehack'),
    #     ('13', 'RepairBaseBook'),
    #     ('21', 'DesignPub'),
    #     ('22', 'DesignLifehack'),
    #     ('31', 'ReportPub'),
    #     ('32', 'ReportAccount'),
    #     ('41', 'Notification'),
    # )    choices=PUB_ROLE_CHOICES,
    id = models.PositiveIntegerField(primary_key=True, verbose_name='id роли')
    name = models.CharField(max_length=135, verbose_name='Значение роли')

    class Meta:
        verbose_name = 'Роль публикации'
        verbose_name_plural = 'Роли публикаций'

    def __str__(self):
        return self.name

# вероятно, класс PubHasTags можно было и вовсе не делать, обойдясь tag_id = ManyToManyField('Publication')
class PubHasTags(models.Model):
    pub_id = models.OneToOneField('Publication', on_delete=models.CASCADE, verbose_name='id публикации') # как сделать самоудаление при удлении юзера????
    tag_id = models.ForeignKey('TagName', on_delete=models.CASCADE, verbose_name='id тега')

    class Meta:
        verbose_name = 'Тег публикации'
        verbose_name_plural = 'Теги публикаций'

    def __str__(self):
        return 'pub id: ' + self.pub_id + ', tag id: ' + self.tag_id

class TagName(models.Model):
    id = models.PositiveIntegerField(primary_key=True, verbose_name='id тега')
    pub_role = models.PositiveIntegerField(, verbose_name='роль публикации')
    tag_category = models.CharField(max_length=255, verbose_name='категория')
    tag_name = models.CharField(max_length=255, verbose_name='значение тега')

    class Meta:
        verbose_name = 'Значение тега'
        verbose_name_plural = 'Значения тегов'

    def __str__(self):
        return 'tag id: ' + self.id + ', pub role: ' + self.pub_role + ', tag category: ' + self.tag_category + ', tag name: ' + self.tag_name
