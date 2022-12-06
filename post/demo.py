
from PIL import Image, ImageDraw, ImageFont

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
        this_image.save(self.image.path, optimize=True,
                        quality=95)