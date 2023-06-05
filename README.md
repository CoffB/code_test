Using Python 3.8.2

Dependencies: <br />
  -fastapi <br />
  -uvicorn <br />
  -pillow <br />
  -boto3 <br />
  -httpx <br />

## How to run:
  Run app.py, server is running on http://localhost:5000/

  To download files from bucket to working folder: <br />
  http://localhost:5000/download <br />
  POST<br />
    {
      "aws_access_key_id": "your_key", <br />
      "aws_secret_access_key": "your_secret_key", <br />
      "bucket_name": "your_bucket", <br />
      "region_name": "your_region" <br />
    }
    
   To resize images in working folder <br />
   http://localhost:5000/resize <br />
   GET
    
   ## Logging 
   Logfile is created automatically in the working folder with the name log.log.
   
   ## Testing
   Run test files for each coresponding file.
