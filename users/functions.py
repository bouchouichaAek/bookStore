from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


def resize_and_crop_image(image_field):
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
