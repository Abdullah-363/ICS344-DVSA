# ICS-344 Course Project: DVSA Vulnerability Discovery and Remediation

**King Fahd University of Petroleum and Minerals (KFUPM)**  
**Course:** ICS-344: Information Security | **Term:** 252  
**Student:** Abdullah Almalki | **ID:** 202030200 |
**Team number:** 67 |
**Submission Type:** Individual  

---

## Project Overview

This repository contains all technical artifacts for the ICS-344 course project, which involved deploying the OWASP Damn Vulnerable Serverless Application (DVSA) on AWS, systematically identifying, exploiting, documenting, and fixing 10 official security vulnerabilities in a controlled, non-production environment.

**DVSA Website URL:**  
`http://dvsa-website-test-629186529890-us-east-1.s3-website.us-east-1.amazonaws.com`

**API Base URL:**  
`https://4r9u5ichx5.execute-api.us-east-1.amazonaws.com/dvsa`

**AWS Region:** `us-east-1`

---

## Architecture Overview

DVSA runs entirely on AWS using a serverless architecture:

```
Browser → Amazon CloudFront → S3 (Frontend)
Browser → API Gateway → Lambda Functions → DynamoDB / S3 / SQS
                                         → Amazon Cognito (Auth)
```

---

## Vulnerabilities Covered

| # | Lesson | Affected Component | Status |
|---|--------|--------------------|--------|
| 1+9 | Event Injection / Vulnerable Dependencies | DVSA-ORDER-MANAGER | ✅ Fixed |
| 2 | Broken Authentication (JWT Forgery) | DVSA-ORDER-MANAGER | ✅ Fixed |
| 3 | Sensitive Information Disclosure | S3 Receipts Bucket | ✅ Fixed |
| 4 | Insecure Cloud Configuration (OS Injection) | DVSA-FEEDBACK-UPLOADS | ✅ Fixed |
| 5 | Broken Access Control (Admin Bypass) | DVSA-ADMIN-UPDATE-ORDERS | ✅ Fixed |
| 6 | Denial of Service (Lambda Throttling) | DVSA-ORDER-BILLING | ✅ Fixed |
| 7 | Over-Privileged Functions (IAM) | SendReceipt IAM Role | ✅ Fixed |
| 8 | Logic Vulnerabilities (Race Condition) | DVSA-ORDER-BILLING | ✅ Fixed |
| 10 | Unhandled Exceptions (Stack Trace Leak) | DVSA-ORDER-GET | ✅ Fixed |

---

## Repository Structure

```
/
├── README.md
├── lessons/
│   ├── lesson-01-09-event-injection/
│   │   ├── before/order-manager.js          ← original vulnerable code
│   │   ├── after/order-manager.js           ← fixed code
│   │   ├── exploit.sh                       ← exploit command
│   │   └── screenshots/                     ← evidence screenshots
│   ├── lesson-02-broken-auth/
│   │   ├── before/order-manager.js
│   │   ├── after/order-manager.js
│   │   ├── exploit.sh
│   │   └── screenshots/
│   ├── lesson-03-sensitive-disclosure/
│   │   ├── exploit.sh
│   │   ├── fix.sh
│   │   └── screenshots/
│   ├── lesson-04-insecure-config/
│   │   ├── before/feedback_uploads.py
│   │   ├── after/feedback_uploads.py
│   │   ├── exploit.sh
│   │   └── screenshots/
│   ├── lesson-05-broken-access-control/
│   │   ├── before/admin_update_orders.py
│   │   ├── after/admin_update_orders.py
│   │   ├── exploit.sh
│   │   └── screenshots/
│   ├── lesson-06-dos/
│   │   ├── exploit.sh
│   │   ├── fix.sh
│   │   └── screenshots/
│   ├── lesson-07-over-privileged/
│   │   ├── fix.sh
│   │   └── screenshots/
│   ├── lesson-08-logic-vulnerability/
│   │   ├── before/order_billing.py
│   │   ├── after/order_billing.py
│   │   ├── exploit.sh
│   │   └── screenshots/
│   └── lesson-10-unhandled-exceptions/
│       ├── before/get_order.py
│       ├── after/get_order.py
│       ├── exploit.sh
│       └── screenshots/
└── scripts/
    └── setup-variables.sh                   ← common environment variables
```

---

## Setup & Prerequisites

### AWS Deployment
DVSA was deployed from the AWS Serverless Application Repository (SAR):
1. Navigate to AWS Console → Serverless Application Repository
2. Search for **OWASP DVSA**
3. Deploy with parameters: `AdminEmail` and `WebsiteBucketPrefix`
4. Region: `us-east-1`

### Local Tools Required
```bash
sudo apt update
sudo apt install -y curl python3 jq unzip
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o /tmp/awscliv2.zip
unzip -q /tmp/awscliv2.zip -d /tmp
sudo /tmp/aws/install
aws configure  # enter your Access Key ID, Secret, region: us-east-1, format: json
```

### Environment Variables
```bash
export API="https://4r9u5ichx5.execute-api.us-east-1.amazonaws.com/dvsa/order"
export RECEIPTS_BUCKET="dvsa-receipts-bucket-629186529890-us-east-1"
export FEEDBACK_BUCKET="dvsa-feedback-bucket-629186529890-us-east-1"
export ROLE="serverlessrepo-OWASP-DVSA-SendReceiptFunctionRole-bqAohJuMsvjP"
```

---

## Lesson Summaries

### Lesson #1 + #9: Event Injection / Vulnerable Dependencies
**Vulnerability:** `node-serialize` library deserializes attacker-controlled JavaScript functions embedded in JSON using `_$$ND_FUNC$$_` marker, enabling RCE.  
**Proof:** `FILE READ SUCCESS: You are reading the contents of my hacked file!` in CloudWatch logs.  
**Fix:** Removed `node-serialize`, replaced with `JSON.parse()`.

### Lesson #2: Broken Authentication
**Vulnerability:** JWT payload decoded without signature verification, allowing identity claims to be freely forged.  
**Proof:** Forged token returned User C's private orders using User B's token.  
**Fix:** Added `verifyCognitoJwt()` using Cognito JWKS public key verification.

### Lesson #3: Sensitive Information Disclosure
**Vulnerability:** S3 receipts bucket has all 4 public access block settings disabled with no bucket policy.  
**Proof:** Listed and downloaded all users' private receipts using AWS CLI with no authorization.  
**Fix:** Enabled all 4 S3 public access block settings.

### Lesson #4: Insecure Cloud Configuration
**Vulnerability:** Feedback S3 bucket allows unrestricted uploads. Lambda uses `os.system()` with filename directly. `is_safe()` is commented out.  
**Proof:** Uploaded file named `test; echo HACKED > /tmp/injected.txt` — command injection confirmed in CloudWatch.  
**Fix:** Hardened S3 bucket, enabled `is_safe()`, replaced `os.system()` with `subprocess.run()`.

### Lesson #5: Broken Access Control
**Vulnerability:** `DVSA-ADMIN-UPDATE-ORDERS` can be directly invoked by any authenticated user without admin role check.  
**Proof:** Direct Lambda invocation marked order as "paid" with token "HACKED" and total $0.  
**Fix:** Added invoker validation requiring requests from `DVSA-ORDER-BILLING` only.

### Lesson #6: Denial of Service
**Vulnerability:** No rate limiting on billing endpoint. Payment processor sleeps 2-4s, exhausting Lambda concurrency.  
**Proof:** 50 concurrent requests caused 22 Lambda throttles confirmed by CloudWatch metrics.  
**Fix:** Created API Gateway usage plan with `burstLimit=10, rateLimit=5`.

### Lesson #7: Over-Privileged Functions
**Vulnerability:** `DVSA-SEND-RECEIPT-EMAIL` role has wildcard S3/DynamoDB access and `AmazonSESFullAccess`.  
**Proof:** Used role permissions to scan entire `DVSA-ORDERS-DB` — all customer orders exposed.  
**Fix:** Restricted S3 to receipts bucket only, DynamoDB to `GetItem` on one table, removed `AmazonSESFullAccess`.

### Lesson #8: Logic Vulnerabilities (Race Condition)
**Vulnerability:** Billing function reads item list without locking the order, allowing concurrent updates during payment processing.  
**Proof:** Simultaneous billing (1 item) + update (5 items) — DynamoDB shows 5 items but payment for 1.  
**Fix:** Added DynamoDB `ConditionExpression` atomic lock setting status to 115 before billing begins.

### Lesson #10: Unhandled Exceptions
**Vulnerability:** Unhandled exceptions return full stack traces, file paths, and source code to clients.  
**Proof:** `{"errorType":"AttributeError","stackTrace":["File \"/var/task/get_order.py\", line 32..."]}` returned to client.  
**Fix:** Added centralized `try/except` blocks returning generic client-safe error messages.

---

## Important Notice

> DVSA is intentionally vulnerable and was deployed only in a non-production AWS account for legal classroom demonstration purposes as part of ICS-344 at KFUPM. All exploitation was performed in a controlled environment. This repository is the intellectual property of KFUPM/Course Instructors — Term 252 and is intended solely for educational purposes within ICS-344.
