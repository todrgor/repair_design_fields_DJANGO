from django.db import models
# from authapp.models import User
from repair_design_fields import settings
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
# from django.db.models.functions import Lower

class Publication(models.Model):
    title = models.CharField(max_length=135, verbose_name='Заголовок публикации')
    type = models.ForeignKey('PubTypes', on_delete=models.SET_DEFAULT, default=1, verbose_name='Вид публикации', blank=False)
    preview = models.FileField(max_length=200, upload_to='pub_media', validators=[FileExtensionValidator(['mp4', 'mov', 'png', 'jpg', 'jpeg', 'pdf'])], verbose_name='Превью')
    content_first_desc =  models.TextField(verbose_name='Текст перед фотографиями', default='')
    content_last_desc =  models.TextField(verbose_name='Текст после фотографий', blank=True, null=True, default='')
    tags = models.ManyToManyField('Tag', verbose_name='Теги публикции')
    cost_min = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, default=0, verbose_name='бюджет от')
    cost_max = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, default=1, verbose_name='бюджет до')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, verbose_name='Автор')
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
        return str(self.title) + ', ' + str(self.type)


class PubTypes(models.Model):
    id = models.PositiveIntegerField(primary_key=True, verbose_name='id типа')
    name = models.CharField(max_length=135, verbose_name='Значение типа')

    class Meta:
        verbose_name = 'Тип публикации'
        verbose_name_plural = 'Типы публикаций'

    def __str__(self):
        return self.name


class TagCategory(models.Model):
    name = models.CharField(max_length=135, verbose_name='Название категории')

    class Meta:
        verbose_name = 'Категория тегов'
        verbose_name_plural = 'Категории тегов'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name='Значение тега')
    pub_type = models.ManyToManyField('PubTypes', verbose_name='Тип публикации')
    category = models.ForeignKey('TagCategory', on_delete=models.CASCADE, verbose_name='Категория тега', blank=False)

    class Meta:
        verbose_name = 'Тег публикации'
        verbose_name_plural = 'Теги публикции'

    def __str__(self):
        return (self.name + ' (' + str(self.category.name) + ', ' + str(list(self.pub_type.values_list('name', flat=True))).replace("[", "").replace("]", "").replace("'", "") + ')')


# желательно, чтобы эти модели ниже
# вскоре оказались ненужными
class PubPhotos(models.Model):
    # нейминг: правильнее будет просто pub + переименовать во всём проекте

    id_pub = models.ForeignKey('Publication', verbose_name='id публикации', on_delete=models.CASCADE)
    photo = models.ImageField(max_length=200, upload_to='pub_media', verbose_name='Фотографии публикации')

    class Meta:
        verbose_name = 'Фотография публикации'
        verbose_name_plural = 'Фотографии публикации'

    def __str__(self):
        return str(self.photo) +' for '+ str(self.id_pub)
