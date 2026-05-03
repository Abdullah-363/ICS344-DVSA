SCREENSHOTS FOR LESSON #5: Broken Access Control
=================================================

Place the following 3 screenshots in this folder:

1. exploit_proof.png
   → DynamoDB record showing:
     orderStatus: "paid", confirmationToken: "HACKED", totalAmount: "0"
     proving the order was marked paid without any payment
   (This is the DynamoDB get-item result from your report)

2. fix_deployed.png
   → Lambda editor showing the fixed admin_update_orders.py
     with the invoker validation check added
     and the green "Successfully updated" banner visible

3. fix_verified.png
   → Terminal showing:
     {"status": "err", "msg": "Unauthorized - must be invoked through billing workflow"}
     after attempting the direct Lambda invocation
