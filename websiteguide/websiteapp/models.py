from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
# Create your models here.

class UserInfo(AbstractUser):
    username = models.CharField(verbose_name='Имя пользователя', max_length=100, unique=True)
    alias = models.CharField(verbose_name='Имя', max_length=100,null=True)
    email = models.EmailField(verbose_name='Электронная почта', max_length=100, blank=True, null=True)
    phone = models.IntegerField(verbose_name='Телефон', blank=True, null=True)
    is_active = models.BooleanField(verbose_name='Активный', default=True)
    is_superuser = models.BooleanField(verbose_name='Суперпользователь', default=False)
    is_staff = models.BooleanField(verbose_name='Разрешить вход в панель администратора', default=False)
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    modified = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    deleted = models.BooleanField(verbose_name='Удаленный', default=False)

    @staticmethod
    def make_password(plain_password: str) -> str:
        return make_password(plain_password, hasher='pbkdf2_sha256')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = verbose_name



class WebSiteGroup(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа веб-сайтов'
        verbose_name_plural = verbose_name


class WebSite(models.Model):
    icon = models.CharField(max_length=100,default='default.png')
    path = models.CharField(max_length=1024)
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=256, null=True, blank=True)
    website_group = models.ForeignKey(WebSiteGroup, on_delete=models.CASCADE, related_name='websites')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Веб-сайт'
        verbose_name_plural = verbose_name
