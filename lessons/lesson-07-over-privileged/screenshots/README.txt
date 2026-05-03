SCREENSHOTS FOR LESSON #7: Over-Privileged Functions
=====================================================

Place the following 3 screenshots in this folder:

1. exploit_proof.png
   → Terminal showing Policy1 with wildcard S3 resource:
     "arn:aws:s3:::*" and "arn:aws:s3:::*/*"
     AND Policy2 with wildcard DynamoDB: "table/*"
     proving excessive permissions
   (This is the get-role-policy output from your report)

2. blast_radius_proof.png
   → Terminal showing DynamoDB scan returning all customer orders
     including the "HACKED" confirmation token from Lesson #5
     proving the receipt function can read all data

3. fix_verified.png
   → Terminal showing:
     - Policy1 restricted to specific receipts bucket ARN
     - Attached policies showing AmazonSESFullAccess is GONE
     - Only AWSLambdaBasicExecutionRole remains
