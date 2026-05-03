SCREENSHOTS FOR LESSON #10: Unhandled Exceptions
=================================================

Place the following 3 screenshots in this folder:

1. exploit_proof.png
   → Terminal showing the full stack trace response:
     errorMessage: 'bool' object has no attribute 'lower'
     errorType: AttributeError
     stackTrace: File "/var/task/get_order.py", line 32...
   (This is Figure 43 from your report)

2. fix_deployed.png
   → Lambda editor showing the fixed get_order.py with
     try/except blocks and safe isAdmin type handling
     and the green "Successfully updated" banner visible

3. fix_verified.png
   → Terminal showing before AND after in one screenshot:
     Before: full stack trace
     After: {"status": "err", "msg": "could not find order"}
   (This is Figure 45 from your report)
