from django.conf import settings
from django.db import models
# from django.utils import timezone


class User(models.Model):
    nickname = models.CharField(max_length=50, unique=True)
    photo = models.ImageField(max_length=200, blank=True, null=True)
    role = models.OneToOneField('UserRoles', on_delete=models.SET_DEFAULT, default=1)
    bio = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveIntegerField()
    telephone = models.PositiveIntegerField(unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=250) # how to min_length=5 ?
    registration = models.DateTimeField(auto_now_add=True)
    last_entry = models.DateTimeField(auto_now=True)

    def new_last_entry(self):
        self.save()

    def __str__(self):
        return self.nickname + ', role: ' + str(self.role) + ', last entry: ' + str(self.last_entry)

class UserRoles(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    USER_ROLE_CHOICES = (
        (1, 'Watcher'),
        (2, 'Author'),
        (3, 'Admin'),
    )
    name = models.IntegerField(max_length=1, choices=USER_ROLE_CHOICES)

class UserSubscribes(models.Model):
    subscriber_id = models.ForeignKey('User', on_delete=models.CASCADE, unique=True) # как сделать самоудаление при удлении юзера????
    star_id = models.OneToOneField('User', on_delete=models.CASCADE)

    def __str__(self):
        return 'User with ID: ' + str(self.subscriber_id) + ', subscribes: ' + str(self.star_id)

class ExpertInfo(models.Model):
    expert_id = models.OneToOneField('User', on_delete=models.CASCADE, unique=True) # как сделать самоудаление при удлении юзера????
    count_follovers = models.PositiveIntegerField(default=0)
    knowledge = models.TextField(blank=True, null=True, max_length=255)
    offer = models.TextField(blank=True, null=True, max_length=255)
    site = models.CharField(blank=True, null=True, max_length=255)
    address = models.CharField(blank=True, null=True, max_length=255)
    telegram = models.PositiveIntegerField(blank=True, null=True, max_length=255)
    whatsapp = models.PositiveIntegerField(blank=True, null=True, max_length=255)
    viber = models.PositiveIntegerField(blank=True, null=True, max_length=255)
    vk = models.CharField(blank=True, null=True, max_length=255)
    inst = models.CharField(blank=True, null=True, max_length=255)
    ok = models.CharField(blank=True, null=True, max_length=255)
    fb = models.CharField(blank=True, null=True, max_length=255)
    other = models.CharField(blank=True, null=True, max_length=255)

    def count_follovers_changed(self, change_count):
        count_follovers += change_count
        self.save

    def __str__(self):
        return 'Expert with ID: ' + str(self.subscriber_id) + ', offer: ' + str(self.offer)

class Publication (models.Model):
    title = models.CharField(max_length=135)
    role = models.OneToOneField('PubRoles', on_delete=models.SET_NULL, null=True) # как сделать самоудаление при удлении юзера????
    preview = models.ImageField(max_length=200)
    content =  models.TextField()
    author_id = models.ForeignKey('User', on_delete=models.SET_NULL, null=True) # как сделать самоудаление при удлении юзера????
    pushed = models.DateTimeField(auto_now_add=True)
    seen_count = models.IntegerField(default=0)
    saved_count = models.IntegerField(default=0)
    reported_count = models.IntegerField(default=0)
    shared_count = models.IntegerField(default=0)
    average_age_watchers = models.IntegerField(default=0)
    average_age_savers = models.IntegerField(default=0)

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
        return 'Title: ' + str(self.title) + ', saved: ' + str(self.saved_count)

class PubRoles(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    PUB_ROLE_CHOICES = (
        (11, 'RepairPub'),
        (12, 'RepairLifehack'),
        (13, 'RepairBaseBook'),
        (21, 'DesignPub'),
        (22, 'DesignLifehack'),
        (31, 'ReportPub'),
        (32, 'ReportAccount'),
        (41, 'Notification'),
    )
    name = models.IntegerField(max_length=2, choices=PUB_ROLE_CHOICES)

    def __str__(self):
        return self.name

class SavedPubs (models.Model):
    when = models.DateTimeField(auto_now_add=True)
    saver_id = models.OneToOneField('User', on_delete=models.CASCADE) # как сделать самоудаление при удлении юзера????
    pub_id = models.ForeignKey('Publication', on_delete=models.CASCADE)

    def __str__(self):
        return 'saver id: ' + self.saver_id + ', saved pub: ' + self.pub_id

class SeenPubs (models.Model):
    when = models.DateTimeField(auto_now_add=True)
    watcher_id = models.OneToOneField('User', on_delete=models.CASCADE) # как сделать самоудаление при удлении юзера????
    pub_id = models.ForeignKey('Publication', on_delete=models.CASCADE)

    def __str__(self):
        return 'id seen by: ' + self.watcher_id + ', seen pub: ' + self.pub_id

# вероятно, класс PubHasTags можно было и вовсе не делать, обойдясь tag_id = ManyToManyField('Publication')
class PubHasTags (models.Model):
    pub_id = models.OneToOneField('Publication', on_delete=models.CASCADE) # как сделать самоудаление при удлении юзера????
    tag_id = models.ForeignKey('TagName', on_delete=models.CASCADE)

    def __str__(self):
        return 'pub id: ' + self.pub_id + ', tag id: ' + self.tag_id

class TagName (models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    pub_role = models.PositiveIntegerField()
    tag_category = models.CharField(max_length=255)
    tag_name = models.CharField(max_length=255)

    def __str__(self):
        return 'tag id: ' + self.id + ', pub role: ' + self.pub_role + ', tag category: ' + self.tag_category + ', tag name: ' + self.tag_name
