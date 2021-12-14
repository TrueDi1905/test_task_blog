from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    heading = models.TextField(verbose_name='Заголовок',
                               help_text='Укажите название поста',
                               max_length=100)
    text = models.TextField(verbose_name='Текст',
                            help_text='Напишите содержимое поста')
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts', verbose_name='Автор')

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.heading[:15]


class ReadPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='posts_read',
                             verbose_name='Прочитанный пост')
    reader = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reader',
                               verbose_name='Прочитавший пользователь')

    def __str__(self):
        return f'(Пользователь{self.reader}, прочитал пост {self.post})'


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')
