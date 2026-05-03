#!/bin/bash
# ICS-344 DVSA Project - Common Environment Variables
# Run: source scripts/setup-variables.sh

export API="https://4r9u5ichx5.execute-api.us-east-1.amazonaws.com/dvsa/order"
export RECEIPTS_BUCKET="dvsa-receipts-bucket-629186529890-us-east-1"
export FEEDBACK_BUCKET="dvsa-feedback-bucket-629186529890-us-east-1"
export ROLE="serverlessrepo-OWASP-DVSA-SendReceiptFunctionRole-bqAohJuMsvjP"
export REGION="us-east-1"
export ACCOUNT_ID="629186529890"

# User IDs (from decoded JWT tokens)
export USER_B="8438d4d8-00c1-70f5-c662-63b5a414fec6"  # Attacker
export USER_C="d4087408-3041-70a3-fc31-c751444d19f1"  # Victim

echo "Variables set. Now export your tokens:"
echo "  export TOKEN_B=\"paste User B token here\""
echo "  export TOKEN_C=\"paste User C token here\""
