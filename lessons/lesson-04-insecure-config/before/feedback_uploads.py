# VULNERABLE VERSION - Before Fix (Lesson #4)
# Vulnerability 1: S3 bucket has all public access blocks disabled
# Vulnerability 2: os.system() used with unsanitized filename from S3 event
# Vulnerability 3: is_safe() function completely commented out

import json
import time
import boto3
import os
from botocore.exceptions import ClientError
from botocore.client import Config
import uuid
from urllib import parse


def lambda_handler(event, context):
    print(json.dumps(event))
    if "file" in event:
        s3 = boto3.client('s3', region_name=os.environ["AWS_REGION"],
                          endpoint_url=f'https://s3.{os.environ["AWS_REGION"]}.amazonaws.com',
                          config=Config(s3={'addressing_style': 'virtual'}))
        uuidv4 = str(uuid.uuid4())
        try:
            response = s3.generate_presigned_post(os.environ["FEEDBACK_BUCKET"],
                                                  uuidv4 + "_" + event["file"],
                                                  ExpiresIn=120
                                                  )
            print(response)
        except ClientError as e:
            print(str(e))
            return json.dumps({"status": "err", "msg": "could not get signed url"})

        return response

    elif "Records" in event:
        filename = parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"])
        if not is_safe(filename):
            return {"status": "error", "message": "invalid filename"}

        # VULNERABLE: os.system() with unsanitized filename allows OS command injection
        os.system("touch /tmp/{} /tmp/{}.txt".format(filename, filename))

    else:
        return {"status": "ok", "message": "Thank you."}


def is_safe(s):
    # VULNERABLE: safety check is completely commented out - always returns True
    # if s.find(";") > -1 or s.find("'") > -1 or s.find("|") > -1:
    #    return False
    return True
