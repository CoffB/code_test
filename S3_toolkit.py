import boto3
import concurrent.futures
from botocore.exceptions import ClientError, EndpointConnectionError
from log_factory import LoggerFactory
import os


class AWSDownloader:
    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str, region_name: str):
        log_level = "INFO"
        self.LOG = LoggerFactory.get_logger("user", log_level)
        self.LOG.info("Init new AWS Downloader")
        self.s3 = boto3.client("s3",
                               aws_access_key_id=aws_access_key_id,
                               aws_secret_access_key=aws_secret_access_key,
                               region_name=region_name
                               )

    def download_all_objects_in_bucket(self, bucket_name: str):
        files = self.get_bucket_objects(bucket_name)
        responses = []
        for response in self.download_objects_parallel(bucket_name, files):
            responses.append(response)

            self.LOG.info(response)
        if all(isinstance(response, str) for response in responses):
            return "Download of files in bucket completed without errors"
        else:
            return "Download of files in bucket completed with errors"


    def get_bucket_objects(self, bucket_name: str):
        try:
            response = self.s3.list_objects_v2(Bucket=bucket_name)
        except ClientError as e:
            self.LOG.error(e)
            return e.response
        except EndpointConnectionError as e:
            self.LOG.error(e)
            return e

        self.LOG.info("File names fetched from bucket")
        file_names = [file["Key"] for file in response.get("Contents") if not file["Key"].endswith("/")]
        return file_names

    def download_object(self, file_name: str, bucket_name: str):
        name = file_name.split('/')[-1]
        if os.path.exists(name):
            self.LOG.warning(f"File {name} already exists. Saving new file as {name}_copy")
            name = name + "_copy"

        try:
            self.s3.download_file(
                bucket_name,
                file_name,
                name,
            )

        except ClientError as e:
            self.LOG.error(e)
            return e.response

        return f"{name} successfully downloaded"

    def download_objects_parallel(self, bucket_name: str, files):
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            self.LOG.info("New ThreadPoolExecutor created")
            future = [executor.submit(self.download_object, key, bucket_name) for key in files]
            for future in concurrent.futures.as_completed(future):
                exception = future.exception()

                if not exception:
                    yield future.result()
                else:
                    yield exception



if __name__ == "__main__":
    pass
