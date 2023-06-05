from fastapi import FastAPI, Response, Request, HTTPException
import uvicorn
from pydantic import BaseModel
import S3_toolkit
import media_toolkit

app = FastAPI()


class Payload(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str
    bucket_name: str
    region_name: str


@app.get('/')
def get_root():
    return Response("Server running!")


@app.post('/download')
def download(payload: Payload):
    aws_access_key_id = payload.aws_access_key_id
    aws_secret_access_key = payload.aws_secret_access_key
    region_name = payload.region_name
    bucket_name = payload.bucket_name

    downloader = S3_toolkit.AWSDownloader(aws_access_key_id, aws_secret_access_key, region_name)

    return downloader.download_all_objects_in_bucket(bucket_name)


@app.get('/resize')
def resize():
    image_resizer = media_toolkit.ImageResizer()
    return Response(image_resizer.resize_all())


if __name__ == '__main__':
    uvicorn.run("app:app", host='0.0.0.0', port=5000, workers=4, reload=True)