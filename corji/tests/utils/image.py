from io import BytesIO
import os
import unittest

from PIL import Image
import requests

from corji.utils.image import (
    get_content_type_header,
    resize_image
)

class ImageUtilsTestCase(unittest.TestCase):
    def test_image_identification(self):
        test_png = requests.get("http://i.imgur.com/OacBzQQ.png")
        test_jpg = requests.get("https://i.imgur.com/T0vc7TU.jpg")
        test_nonsense = requests.get("http://pugandchalice.com/")
        png_header = get_content_type_header(test_png)
        jpg_header = get_content_type_header(test_jpg)
        nonsense_header = get_content_type_header(test_nonsense)
        assert jpg_header == "image/jpeg"
        assert png_header == "image/png"
        assert nonsense_header == "image/jpeg"

    def test_image_resize(self):
        os.environ["IMAGE_RESIZE_PIXELS"] = str(150)
        test_jpg = requests.get("https://i.imgur.com/qRWH5.jpg")
        image = resize_image(test_jpg.content)
        file_photodata = BytesIO(image)
        working_image = Image.open(file_photodata)
        edited_width = working_image.size[0]
        print(edited_width)
        assert edited_width == 300



if __name__ == '__main__':
    unittest.main()
