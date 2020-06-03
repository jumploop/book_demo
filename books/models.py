from django.db import models


# Create your models here.
class Books(models.Model):
    name = models.CharField(max_length=30)
    author = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_books'
        verbose_name = '书籍'
        verbose_name_plural = '书籍'
