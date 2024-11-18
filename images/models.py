from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


# Create your models here.
class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='images_create')

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField(max_length=200)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    users_like = models.ManyToManyField(User,
                                        related_name='images_liked',
                                        blank=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not  self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)