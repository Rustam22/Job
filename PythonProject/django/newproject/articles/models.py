from django.db import models

# Create your models here.


class Article(models.Model):
    title = models.TextField(max_length=254)
    body = models.TextField()
    likes = models.IntegerField()


class Comment(models.Model):
    text = models.TextField()
    article = models.ForeignKey(
        'Article',
        on_delete=models.CASCADE
    )


