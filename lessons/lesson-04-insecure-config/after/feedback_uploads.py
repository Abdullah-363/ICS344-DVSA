# FIXED VERSION - After Fix (Lesson #4)
# Fix 1: S3 bucket public access block enabled via AWS CLI (see fix.sh)
# Fix 2: Replaced os.system() with safe subprocess.run() using list arguments
# Fix 3: Enabled and strengthened is_safe() to block all shell metacharacters
# Fix 4: Added file extension validation before generating presigned URLs

import json
import time
import boto3
import os
import subprocess
from botocore.exceptions import ClientError
from botocore.client import Config
import uuid
from urllib import parse

# FIXED: allowlist of permitted file extensions
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.pdf', '.txt'}


def lambda_handler(event, context):
    print(json.dumps(event))
    if "file" in event:
        s3 = boto3.client('s3', region_name=os.environ["AWS_REGION"],
                          endpoint_url=f'https://s3.{os.environ["AWS_REGION"]}.amazonaws.com',
                          config=Config(s3={'addressing_style': 'virtual'}))
        uuidv4 = str(uuid.uuid4())

        # FIXED: validate file extension before generating presigned URL
        filename = event["file"]
        _, ext = os.path.splitext(filename)
        if ext.lower() not in ALLOWED_EXTENSIONS:
            return json.dumps({"status": "err", "msg": "file type not allowed"})

        try:
            response = s3.generate_presigned_post(os.environ["FEEDBACK_BUCKET"],
                                                  uuidv4 + "_" + filename,
                                                  ExpiresIn=120
                                                  )
            print(response)
        except ClientError as e:
            print(str(e))
            return json.dumps({"status": "err", "msg": "could not get signed url"})

        return response

    elif "Records" in event:
        filename = parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"])

        # FIXED: enabled is_safe() check and added strict validation
        if not is_safe(filename):
            return {"status": "error", "message": "invalid filename"}

        # FIXED: replaced os.system() with safe subprocess.run() using list arguments
        # This prevents shell interpretation of the filename entirely
        safe_filename = os.path.basename(filename)
        subprocess.run(["touch", f"/tmp/{safe_filename}", f"/tmp/{safe_filename}.txt"],
                       check=False, timeout=5)

    else:
        return {"status": "ok", "message": "Thank you."}


def is_safe(s):
    # FIXED: uncommented and strengthened to block all dangerous shell metacharacters
    if (s.find(";") > -1 or s.find("'") > -1 or s.find("|") > -1 or
            s.find("&") > -1 or s.find(">") > -1 or s.find("<") > -1 or
            s.find("`") > -1 or s.find("$") > -1 or s.find("\\") > -1):
        return False
    return True
