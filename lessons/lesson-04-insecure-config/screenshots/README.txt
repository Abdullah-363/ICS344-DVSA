SCREENSHOTS FOR LESSON #4: Insecure Cloud Configuration
=========================================================

Place the following 3 screenshots in this folder:

1. exploit_proof.png
   → CloudWatch log showing the S3 event with the malicious key:
     "key": "test%3B+echo+HACKED+%3E+/tmp/injected.txt"
     confirming the malicious filename was received and processed
   (This is Figure 19 or 20 from your report)

2. fix_deployed.png
   → Lambda editor showing the fixed feedback_uploads.py with:
     - is_safe() enabled and strengthened
     - subprocess.run() replacing os.system()
     with the green "Successfully updated" banner visible

3. fix_verified.png
   → CloudWatch log showing 8ms execution time after fix
     confirming the malicious filename was rejected immediately
