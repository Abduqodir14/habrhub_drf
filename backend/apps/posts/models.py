from django.db import models
from django.conf import settings
from core.utils import validate_image
from django.core.files import File
from io import BytesIO
from PIL import Image
from django.utils.text import slugify
from core.models import BaseModel


class Post(BaseModel):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField()
    rating = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    image = models.ImageField(
        upload_to="photos/%Y/%m/%d/", blank=True, validators=[validate_image]
    )
    thumbnail = models.ImageField(
        upload_to="thumbnails/%Y/%m/%d/", blank=True, validators=[validate_image]
    )
    category = models.CharField(max_length=255)

    def __str__(self):
        return "{} - {}".format(self.author, self.title)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_image(self):
        if self.image:
            return "https://127:0.0.1:8000" + self.image.url
        return ""

    def get_thumbnail(self):
        if self.thumbnail:
            return "https://127:0.0.1:8000" + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
            else:
                return ""

    def make_thumbnail(self, image, size=(150, 100)):
        img = Image.open(image)
        img.convert("RGB")
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, "JPEG", quality=80)
        thumbnail = File(thumb_io, name=image.name)
        return thumbnail


class Vote(models.Model):
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="votes")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.voter, self.post)

