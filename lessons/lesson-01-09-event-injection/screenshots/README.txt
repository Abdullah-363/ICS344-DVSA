SCREENSHOTS FOR LESSON #1 + #9: Event Injection / Vulnerable Dependencies
==========================================================================

Place the following 3 screenshots in this folder:

1. exploit_proof.png
   → CloudWatch log showing:
     "FILE READ SUCCESS: You are reading the contents of my hacked file!"
   (This is Figure 2 from your report)

2. fix_deployed.png
   → Lambda editor showing the fixed code (JSON.parse replacing node-serialize)
     with the green "Successfully updated the function" banner visible
   (This is Figure 3 from your report)

3. fix_verified.png
   → CloudWatch log after fix showing NO "FILE READ SUCCESS" message
     (the exploit no longer works)
   (This is Figure 4 from your report)
