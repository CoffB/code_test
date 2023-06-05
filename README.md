# code_test
Adesso kod test

Using Python 3.8.2

Dependencies:
  -fastapi
  -uvicorn
  -pillow
  -boto3

How to run:
  Run app.py, server is running on http://localhost:5000/


  http://localhost:5000/download
  POST
    {
      "aws_access_key_id": "your_key",
      "aws_secret_access_key": "your_secret_key",
      "bucket_name": "your_bucket",
      "region_name": "your_region"
    }
    
   http://localhost:5000/resize 
   GET
    
    
   Logfile is created automatically in the working folder with the name log.log. Images and thumbnails are also saved here.
