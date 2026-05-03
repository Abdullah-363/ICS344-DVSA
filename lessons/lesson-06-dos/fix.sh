#!/bin/bash
# Lesson #6: Fix - API Gateway rate limiting

source ../../scripts/setup-variables.sh

echo "[*] Creating API Gateway usage plan with rate limiting..."
aws apigateway create-usage-plan \
  --name "DVSA-RateLimit" \
  --throttle burstLimit=10,rateLimit=5 \
  --region $REGION

echo ""
echo "[*] Verifying usage plan..."
aws apigateway get-usage-plans --region $REGION
