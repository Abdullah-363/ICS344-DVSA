#!/bin/bash
# Lesson #3: Fix - Enable S3 public access block on receipts bucket

source ../../scripts/setup-variables.sh

echo "[*] Enabling all 4 S3 public access block settings..."
aws s3api put-public-access-block \
  --bucket $RECEIPTS_BUCKET \
  --public-access-block-configuration \
  "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

echo ""
echo "[*] Verifying fix..."
aws s3api get-public-access-block --bucket $RECEIPTS_BUCKET

echo ""
echo "[*] Testing unauthenticated access (should be denied)..."
aws s3 ls s3://$RECEIPTS_BUCKET/2026/ --recursive --no-sign-request
