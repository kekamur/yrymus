from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50, blank=True)
    contacts = models.CharField(max_length=50, blank=True)
    jenres = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to='images/', default='images/user.png')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Posts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Название', max_length=50)
    desc = models.CharField('Описание', max_length=300, blank=True)
    cover = models.ImageField(upload_to='images/', default='images/user.png')
    audiofile = models.FileField(upload_to='audio/', default='audio/default.mp3')
    date = models.DateTimeField(auto_now_add=True)


    def str(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
