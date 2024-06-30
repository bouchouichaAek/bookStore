from django.db import models
from django.contrib.auth.models import AbstractUser
from books.models import Book
from django.utils.translation import gettext_lazy as _
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


# Create your models here.


class User(AbstractUser):
    GENDER = [
        ("ذكر", "ذكر"),
        ("أنثى", "أنثى"),
    ]

    email = models.EmailField(unique=True, verbose_name="البريد الإلكتروني")
    picture = models.ImageField(_('User picture'),
                                upload_to='picture users', blank=True)
    gender = models.CharField(max_length=20,
                              choices=GENDER, verbose_name="User Gender", blank=True)
    birthday = models.DateField(auto_now=False, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'مستخدم'
        verbose_name_plural = 'المستخدمين'

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.picture:
            # Resize and crop the image into a square
            self.picture = self.resize_and_crop_image(
                self.picture)

        super(User, self).save(*args, **kwargs)

    def resize_and_crop_image(self, image_field):
        # Open the original image
        img = Image.open(image_field)

        # Calculate the aspect ratio of the original image
        width, height = img.size
        aspect_ratio = width / height

        # Define the size for the square image (adjust as needed)
        size = 300

        # Calculate new dimensions for resizing while maintaining the aspect ratio
        if width > height:
            new_width = size
            new_height = int(size / aspect_ratio)
        else:
            new_height = size
            new_width = int(size * aspect_ratio)

        # Resize the image while maintaining the aspect ratio
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Create a square thumbnail by cropping
        left = (new_width - size) / 2
        top = (new_height - size) / 2
        right = (new_width + size) / 2
        bottom = (new_height + size) / 2
        img = img.crop((left, top, right, bottom))

        # Save the modified image back to the field
        output = BytesIO()
        img.save(output, 'JPEG', quality=90)
        output.seek(0)

        image_field.file = ContentFile(output.read())

        return image_field


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'الكتاب الذي أعجب به المستخدم'
        verbose_name_plural = 'الكتب الذي أعجبول بهم المستخدمين'



class Subscriptions(models.Model):
   subscriber_email =  models.EmailField(_("Subscriber Email"), max_length=254)

   class Meta:
       verbose_name = 'المشترك'
       verbose_name_plural = 'المشتركين'
   def __str__(self):
       return self.subscriber_email
   