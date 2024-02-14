from django.db import models
from PIL import Image, ImageOps


def resize_image(image_path, output_size=(200, 250)):
    img = Image.open(image_path)
    img.thumbnail(output_size)
    img.save(image_path)


class Product(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    qtty = models.CharField(max_length=100, blank=False, null=False)
    price = models.CharField(max_length=100, blank=False, null=False)
    desc = models.CharField(max_length=100, blank=False, null=False)
    image = models.ImageField(upload_to='media/static/images/shop/')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Check if the image field is not None
        if self.image:
            # Get the path of the uploaded image
            image_path = self.image.path

            # Attempt to resize the image
            try:
                # Resize the image to 200x250 pixels
                resize_image(image_path)
            except Exception as e:
                print(f"Error resizing image: {e}")
