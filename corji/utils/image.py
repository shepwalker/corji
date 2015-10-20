import imghdr
from io import BytesIO

from corji.settings import Config

def get_content_type_header(response):
    """Given a requests response from an image download, attempts to
    determine the proper content-type header. Falls back to image/jpeg
    if valid header can't be found."""
    detected_content_type = imghdr.what("blerg", h=response.content)
    content_header = detected_to_header_mapping.get(
        detected_content_type, None)
    if not content_header:
        if response.headers['content-type'] in accepted_mime_types:
            return response.headers['content-type']
        else:
            return 'image/jpeg'
    else:
        return content_header


def resize_image(original_image):
    file_photodata = BytesIO(original_image)
    working_image = Image.open(file_photodata)
    
    original_width = working_image.size[0]
    original_length = working_image.size[1]
    resize_width = Config.IMAGE_RESIZE_PIXELS
    resize_ratio = original_width/resize_width
    resize_length = int(original_length/resize_ratio)

    working_image = working_image.resize(
        (resize_width, resize_length), resample=Image.ANTIALIAS)

    target_buffer = BytesIO()
    working_image.save(target_buffer, "JPEG")

    picture_body = target_buffer.getvalue()

    return picture_body

accepted_mime_types = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif']

detected_to_header_mapping = {
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif'
}
