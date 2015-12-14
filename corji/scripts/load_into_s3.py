import threading
from queue import Queue

import botocore
import boto3
import boto3.s3

from corji.data_sources import(
    google_spreadsheets,
    s3
)
from corji.logging import Logger
from corji.settings import Config


logger = Logger(Config.LOGGER_NAME,
                Config.LOG_PATH,
                Config.LOG_NAME)
SPREADSHEET_URL = Config.SPREADSHEET_URL
corgis = {}


def worker():
    while True:
        item = queue.get()
        if item is None:
            break
            
        try:
            s3.put(item, corgis[item])
        except Exception as e:
            logger.error("Error!", e)
        finally:
            queue.task_done()

def create_bucket_if_not_exist():
    aws_s3_client = boto3.client("s3")
    aws_s3_resource = boto3.resource("s3")
    relevant_buckets= [bucket for bucket in aws_s3_resource.buckets.all() if(bucket.name==Config.AWS_S3_CACHE_BUCKET_NAME)]
    if not relevantBuckets:
        aws_s3_client.create_bucket(Bucket=Config.AWS_S3_CACHE_BUCKET_NAME, CreateBucketConfiguration={
            'LocationConstraint': Config.AWS_DEFAULT_REGION})

# TODO: Better sysout. ("20% (9/180) complete, that kind of thing.")
# TODO: if bucket doesn't exist, make it exist
if __name__ == "__main__":
    logger.debug("Spreadsheet URL defined: %s", SPREADSHEET_URL)
    
    create_bucket_if_not_exist()
    google_spreadsheets.load(SPREADSHEET_URL)
    s3.load()
    corgis = google_spreadsheets.corgis

    queue = Queue()
    for emoji in corgis:
        queue.put(emoji)

    thread_count = 10
    for thread_num in range(thread_count):
        thread = threading.Thread(target=worker)
        thread.daemon = True
        thread.start()
    queue.join()
