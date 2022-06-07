from django.db import models
# from authapp.models import User, ContactingSupport
import authapp
from repair_design_fields import settings
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
# from django.db.models.functions import Lower
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
import bleach

from django.db.models import Sum

class Publication(models.Model):
    title = models.CharField(max_length=135, verbose_name='Заголовок публикации')
    type = models.ForeignKey('PubTypes', on_delete=models.CASCADE, default=0, verbose_name='Вид публикации', blank=False)
    preview = models.FileField(max_length=200, upload_to='pub_media', validators=[FileExtensionValidator(['mp4', 'mov', 'png', 'jpg', 'jpeg', 'gif'])], verbose_name='Превью')
    content = RichTextUploadingField(blank=True, null=True, verbose_name='Контент', default='')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    pushed = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время публикации')
    tags = models.ManyToManyField('Tag', verbose_name='Теги публикции')
    cost_min = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, default=0, verbose_name='бюджет от')
    cost_max = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, default=1, verbose_name='бюджет до')
    shared_count = models.IntegerField(default=0, verbose_name='"Поделиться" нажато раз')

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pushed',)

    @property
    def seen_count(self):
        return SeenPubs.objects.filter(pub=self.id).count()

    @property
    def ununique_seen_count(self):
        count = 0
        for s in SeenPubs.objects.filter(pub=self.id):
            count += s.count
        return count

    @property
    def saved_count(self):
        return SavedPubs.objects.filter(pub=self.id).count()

    @property
    def save_percent(self):
        return self.saved_count/self.seen_count*100

    @property
    def reported_count(self):
        return authapp.models.ContactingSupport.objects.filter(ask_additional_info=self.id, type=11).count()

    @property
    def average_age_watchers(self):
        ages = (SeenPubs.objects.filter(pub=self.id).aggregate(Sum('watcher__age')))['watcher__age__sum']
        average_age_watchers = ages / self.seen_count if self.seen_count else 0
        return average_age_watchers

    @property
    def average_age_savers(self):
        ages = (SeenPubs.objects.filter(pub=self.id).aggregate(Sum('watcher__age')))['watcher__age__sum']
        average_age_savers = ages / self.saved_count if self.saved_count else 0
        return average_age_savers

    @property
    def unstyled_content(self):  # пройтись по content и убрать все стили, оставить просто текст
        return bleach.clean(self.content, tags=['script'], strip=True)

    @property
    def img_urls_list(self):  # пройтись по content и получить все img
        content = self.content
        img_urls_list = []
        is_taking_img_url = False

        for i in range(len(content)):
            if i+5 < len(content) and content[i:(i+5)] == 'src="':
                is_taking_img_url = True
                src = ''
                i+=5
                while is_taking_img_url:
                    src += content[i]
                    if is_taking_img_url and content[i] == '"' and content[(i-5):i] != 'src="':
                        is_taking_img_url = False
                        img_urls_list.append(src)
                    i+=1
        return img_urls_list

    @property
    def get_preview(self):  # вернуть preview или замену, если на превьюшке видео
        return 'pub_media/static/video_object_logo.svg' if self.preview.name.endswith(('.mp4', '.mov')) else self.preview.name

    @property
    def get_preview_url(self):  # вернуть url preview или замену, если на превьюшке видео
        return '/media/pub_media/static/video_object_logo.svg' if self.preview.name.endswith(('.mp4', '.mov')) else self.preview.url

    def __str__(self):
        return str(self.title) + ', ' + str(self.type)


class PubTypes(models.Model):
    id = models.PositiveIntegerField(primary_key=True, verbose_name='id типа')
    name = models.CharField(max_length=135, verbose_name='Наименование типа')

    class Meta:
        verbose_name = 'Тип публикации'
        verbose_name_plural = 'Типы публикаций'

    def __str__(self):
        return self.name


class SavedPubs(models.Model):
    when = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время сохранения публикации')
    saver = models.ForeignKey('authapp.User', on_delete=models.CASCADE, verbose_name='id сохранившего')
    pub = models.ForeignKey('Publication', on_delete=models.CASCADE, verbose_name='id публикации', default=0)

    class Meta:
        verbose_name = 'Сохранённая публикация'
        verbose_name_plural = 'Сохранённые публикации'

    def __str__(self):
        return 'saver ' + str(self.saver) + ' saved pub ' + str(self.pub)


class SeenPubs(models.Model):
    when = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последнего просмотра публикации')
    watcher = models.ForeignKey('authapp.User', on_delete=models.CASCADE, verbose_name='id просмотревшего')
    pub = models.ForeignKey('Publication', on_delete=models.CASCADE, verbose_name='id публикации', default=0)
    count = models.IntegerField(default=0, verbose_name='Сколько раз публикация была просмотрена')
    when_last_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последнего просмотра')

    class Meta:
        verbose_name = 'Просмотренная публикация'
        verbose_name_plural = 'Просмотренные публикации'

    def __str__(self):
        return 'pub ' + str(self.pub) + ' seen by ' + str(self.watcher)


class TagCategory(models.Model):
    name = models.CharField(max_length=135, verbose_name='Название категории')
    pub_type = models.ManyToManyField('PubTypes', verbose_name='Для какого типа публикации')

    class Meta:
        verbose_name = 'Категория тегов'
        verbose_name_plural = 'Категории тегов'

    def __str__(self):
        return (self.name + ' (' + str(list(self.pub_type.values_list('name', flat=True))).replace("[", "").replace("]", "").replace("'", "") + ')')


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование тега')
    category = models.ForeignKey('TagCategory', on_delete=models.CASCADE, verbose_name='Категория тега', blank=False)

    class Meta:
        verbose_name = 'Тег публикации'
        verbose_name_plural = 'Теги публикации'
        ordering = ('name',)

    def __str__(self):
        return (self.name + ' (' + str(self.category.name) + ')')
