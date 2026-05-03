SCREENSHOTS FOR LESSON #2: Broken Authentication
=================================================

Place the following 3 screenshots in this folder:

1. exploit_proof.png
   → Terminal showing the forged token returning User C's orders
     (different order-id 05c912cf-... and total $33)
   (This is Figure 9 from your report)

2. fix_deployed.png
   → Lambda editor showing the verifyCognitoJwt() function added
     with the green "Successfully updated the function" banner visible
   (This is Figure 10 from your report)

3. fix_verified.png
   → Terminal showing {"status": "err", "msg": "invalid token"}
     after attempting the exploit with the forged token
   (This is Figure 11 from your report)
