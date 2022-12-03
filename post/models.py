import os.path

from django.db import models
from account.models import CustomUser
from .utility import upload_dir_path
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Create your models here.
BASE_DIR = Path(__file__).resolve().parent.parent

PRIVACY_CHOICES = (
    ("1", "PUBLIC"),
    ("2", "FOLLOWERS"),
    ("3", "PRIVATE"),
)


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_dir_path)
    caption = models.CharField(max_length=2056, blank=True)
    privacy = models.CharField(max_length=2, default=2, choices=PRIVACY_CHOICES)

    def __str__(self):
        return self.user.username + " " + str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        width, height = img.size
        TARGET_WIDTH = 566
        coefficient = width / 566
        new_height = height / coefficient
        this_image = img.resize((int(TARGET_WIDTH), int(new_height)), Image.Resampling.LANCZOS)

        this_image_width, this_image_height = this_image.size

        draw = ImageDraw.Draw(this_image)
        text = "@" + str(self.user.username)
        shadowcolor = "black"
        fillcolor = "white"
        font = ImageFont.truetype(os.path.join(BASE_DIR, "static_files/font/AlexBrush-Regular.ttf"), 25)
        text_width, text_height = draw.textsize(text, font)
        margin = 10
        x = this_image_width - text_width - margin
        y = this_image_height - text_height - margin

        draw.text((x - 1, y), text, font=font, fill=shadowcolor)
        draw.text((x + 1, y), text, font=font, fill=shadowcolor)
        draw.text((x, y - 1), text, font=font, fill=shadowcolor)
        draw.text((x, y + 1), text, font=font, fill=shadowcolor)

        draw.text((x, y), text, font=font, fill=fillcolor)
        # this_image.show()
        this_image.save(self.image.path, optimize=True,
                        quality=95)
