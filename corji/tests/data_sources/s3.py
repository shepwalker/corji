import unittest

import requests

from corji.settings import Config
from corji.data_sources import s3


class S3DataSourceTestCase(unittest.TestCase):
    def test_sanity(self):
        assert True

    def test_large_s3_images_should_be_resized(self):
        s3.load()

        maximum_filesize = 100000
        s3_filename = '_test-large-image'

        # Even if resizing is disabled, if its greater than the max filesize we should resize it.
        Config.MAXIMUM_S3_FILESIZE = maximum_filesize
        Config.IMAGE_RESIZE = False

        large_url = 'http://jinqiaojs.com/hd/corgi-puppy-hd-wallpaper-high-definition-3la.jpg'
        response = requests.head(large_url)
        filesize_in_bytes = int(response.headers['content-length'])
        assert filesize_in_bytes > maximum_filesize

        result = s3.put(s3_filename, [large_url], override_existing_file=True)
        assert result

        s3_url = s3.get(s3_filename)
        response = requests.get(s3_url)
        filesize_in_bytes = int(response.headers['content-length'])
        assert filesize_in_bytes < maximum_filesize


if __name__ == '__main__':
    unittest.main()
