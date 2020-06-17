from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class MakeTip(models.Model):
    author = models.ForeignKey(User, related_name='tips', on_delete=models.CASCADE)
    title = models.CharField(max_length=63)
    post_pic = models.FileField(upload_to='media', blank=True, help_text='Selecciona video')
    creativity = models.IntegerField(default=0, null=True)
    sexy = models.IntegerField(default=0, null=True)
    quality = models.IntegerField(default=0, null=True)
    outfit = models.IntegerField(default=0, null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def total_creativity(self):
        return self.creativity

    def total_sexy(self):
        return self.sexy

    def total_quality(self):
        return self.quality

    def total_outfit(self):
        return self.outfit


    # def post_info_summary(self):
    #     len_info = len(self.info)
    #     if len_info > 480:
    #         return self.info[:480]+' . . . .continue'
    #     else:
    #         return self.info

    def get_absolute_url(self):
        return reverse('tips:tip_detail', kwargs={'pk': self.pk})


class LikeUserList(models.Model):
    post = models.ForeignKey(MakeTip, related_name='members', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class DownVoteUserList(models.Model):
    post = models.ForeignKey(MakeTip, related_name='members_down', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username