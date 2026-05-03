SCREENSHOTS FOR LESSON #6: Denial of Service
=============================================

Place the following 3 screenshots in this folder:

1. exploit_proof.png
   → CloudWatch metrics showing:
     Throttles: 22 for DVSA-ORDER-BILLING
     confirming 22 out of 50 requests were throttled
   (This is the CloudWatch metrics screenshot from your report)

2. fix_deployed.png
   → Terminal showing the usage plan created successfully:
     {"id": "ln6jts", "name": "DVSA-RateLimit",
      "throttle": {"burstLimit": 10, "rateLimit": 5.0}}

3. fix_verified.png
   → Terminal showing get-usage-plans confirming the rate limiting
     plan is active with burstLimit: 10 and rateLimit: 5
