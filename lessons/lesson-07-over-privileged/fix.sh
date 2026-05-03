#!/bin/bash
# Lesson #7: Over-Privileged Functions
# Fix: Apply Principle of Least Privilege to SendReceipt IAM Role

source ../../scripts/setup-variables.sh

echo "[*] Step 1 - Check current over-broad permissions"
echo "Attached policies:"
aws iam list-attached-role-policies --role-name $ROLE
echo ""
echo "Inline policies:"
aws iam list-role-policies --role-name $ROLE

echo ""
echo "[*] Step 2 - Show blast radius (can scan ALL orders)"
aws dynamodb scan --table-name DVSA-ORDERS-DB --region $REGION --max-items 3

echo ""
echo "[*] Step 3 - Fix Policy1: Restrict S3 to receipts bucket only"
aws iam put-role-policy \
  --role-name $ROLE \
  --policy-name SendReceiptFunctionRolePolicy1 \
  --policy-document '{"Statement":[{"Action":["s3:GetObject","s3:PutObject"],"Resource":["arn:aws:s3:::dvsa-receipts-bucket-629186529890-us-east-1","arn:aws:s3:::dvsa-receipts-bucket-629186529890-us-east-1/*"],"Effect":"Allow"}]}'

echo ""
echo "[*] Step 4 - Fix Policy2: Restrict DynamoDB to DVSA orders table only"
aws iam put-role-policy \
  --role-name $ROLE \
  --policy-name SendReceiptFunctionRolePolicy2 \
  --policy-document '{"Statement":[{"Action":["dynamodb:GetItem"],"Resource":["arn:aws:dynamodb:us-east-1:629186529890:table/DVSA-ORDERS-DB"],"Effect":"Allow"}]}'

echo ""
echo "[*] Step 5 - Remove AmazonSESFullAccess"
aws iam detach-role-policy \
  --role-name $ROLE \
  --policy-arn "arn:aws:iam::aws:policy/AmazonSESFullAccess"

echo ""
echo "[*] Verifying fixes..."
aws iam list-attached-role-policies --role-name $ROLE
aws iam get-role-policy --role-name $ROLE --policy-name SendReceiptFunctionRolePolicy1
