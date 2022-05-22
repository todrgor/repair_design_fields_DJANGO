from django.db import models
# from authapp.models import User
from repair_design_fields import settings
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
# from django.db.models.functions import Lower
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class Publication(models.Model):
    title = models.CharField(max_length=135, verbose_name='Заголовок публикации')
    type = models.ForeignKey('PubTypes', on_delete=models.SET_DEFAULT, default=0, verbose_name='Вид публикации', blank=False)
    preview = models.FileField(max_length=200, upload_to='pub_media', validators=[FileExtensionValidator(['mp4', 'mov', 'png', 'jpg', 'jpeg', 'gif'])], verbose_name='Превью')
    content = RichTextUploadingField(blank=True, null=True, verbose_name='Контент', default='')
    tags = models.ManyToManyField('Tag', verbose_name='Теги публикции')
    cost_min = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, default=0, verbose_name='бюджет от')
    cost_max = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, default=1, verbose_name='бюджет до')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    pushed = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время публикации')
    seen_count = models.IntegerField(default=0, verbose_name='Просмотров публикации')
    saved_count = models.IntegerField(default=0, verbose_name='Публикация была сохранена столько раз')
    reported_count = models.IntegerField(default=0, verbose_name='Жалоб на публикацию')
    shared_count = models.IntegerField(default=0, verbose_name='"Поделиться" нажато раз')
    average_age_watchers = models.IntegerField(default=0, verbose_name='Средний возраст просмотревших')
    average_age_savers = models.IntegerField(default=0, verbose_name='Средний возраст сохранивших')

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pushed',)

    @property
    def unstyled_content(self):  # пройтись по content и убрать все стили, оставить просто текст
        content = self.content
        to_remove = False

        for i in range(len(content)):
            if i < len(content):
                if content[i] == '<':
                    to_remove = True
                if to_remove:
                    if content[i] == '>':
                        to_remove = False
                    content = content[:i] +' '+ content[(i+1):]
        return content

    @property
    def img_urls_list(self):  # пройтись по content и получить все img
        content = self.content
        img_urls_list = []
        is_taking_img_url = False
        is_removing_style = False

        for i in range(len(content)):
            if i+5 < len(content):
                if content[i] == 's' and content[(i+1):(i+5)] == 'rc="':
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
        ordering = ('name',)

    def __str__(self):
        return (self.name + ' (' + str(self.category.name) + ', ' + str(list(self.pub_type.values_list('name', flat=True))).replace("[", "").replace("]", "").replace("'", "") + ')')
