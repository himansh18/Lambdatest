1. Valid Login
ID	Scenario	Steps	Expected Result
LG-01	Login with valid credentials	Enter registered email and correct password, click Login	User is redirected to the dashboard/home page; session is created
LG-02	Login via Enter key	Enter valid credentials, press Enter	Same as LG-01
LG-03	Email case-insensitivity	Enter email in different case (e.g. USER@Example.com) with valid password	Login succeeds (if the spec treats email as case-insensitive)
LG-04	Leading/trailing spaces in email	Enter user@example.com with valid password	Input is trimmed and login succeeds, or a clear validation message is shown
LG-05	“Remember me” checked	Log in with the box checked, close and reopen the browser	Session persists per the configured duration
LG-06	“Remember me” unchecked	Log in, close the browser, reopen	User must log in again
LG-07	Redirect to intended page	Open a protected URL while logged out, log in	User lands on the originally requested page
LG-08	Password masking	Type in the password field	Characters are masked; the show/hide toggle works if present
2. Invalid Credentials
ID	Scenario	Steps	Expected Result
IC-01	Wrong password	Valid email, incorrect password	Generic error (“Invalid email or password”); no login
IC-02	Unregistered email	Non-existent email, any password	Same generic error as IC-01 (no account enumeration)
IC-03	Empty email	Leave email blank, enter password	Inline validation: email is required
IC-04	Empty password	Enter email, leave password blank	Inline validation: password is required
IC-05	Both fields empty	Click Login with nothing entered	Validation errors on both fields; no request sent (or a 400 response)
IC-06	Invalid email format	Enter user@ or user.com	Format validation message
IC-07	Case-sensitive password	Correct password with altered case	Login fails
IC-08	SQL injection	Enter ' OR '1'='1 in both fields	Login fails; no DB error exposed; input is sanitized
IC-09	XSS payload	Enter <script>alert(1)</script> in the email field	Script does not execute; input is escaped
IC-10	Very long input	Enter 1000+ characters in each field	Handled gracefully (validation error or truncation); no crash
IC-11	Disabled/deactivated account	Valid credentials for a deactivated user	Login denied with an appropriate message
IC-12	Unverified account	Valid credentials for an account with unverified email	Login denied or prompted to verify, per spec
IC-13	Error message timing	Compare response times for valid vs invalid email	No significant difference (prevents timing-based enumeration)
IC-14	Credentials not in URL	Submit login and inspect the request	Credentials are sent via POST body over HTTPS, never in the query string
3. Forgot Password
ID	Scenario	Steps	Expected Result
FP-01	Link navigation	Click “Forgot password?”	Reset request page opens
FP-02	Registered email	Submit a registered email	Confirmation message shown; reset email delivered
FP-03	Unregistered email	Submit an unknown email	Same neutral confirmation message as FP-02 (no enumeration); no email sent
FP-04	Empty/invalid email	Submit blank or malformed email	Validation error
FP-05	Reset link works	Click the link in the email	Reset form opens with the token validated
FP-06	Set new password	Enter a valid new password and confirmation	Password updated; success message; user can log in with the new password
FP-07	Old password invalidated	After reset, log in with the old password	Login fails
FP-08	Password policy	Enter a weak password on the reset form	Policy error shown (length, complexity)
FP-09	Mismatched confirmation	New password and confirm password differ	Validation error
FP-10	Expired token	Use the reset link after its expiry (e.g. 15–60 min)	“Link expired” message; option to request a new one
FP-11	Reused token	Use the same reset link a second time	Rejected as invalid or already used
FP-12	Tampered token	Modify characters in the token	Rejected; no information leaked
FP-13	Multiple requests	Request reset twice	Only the latest link is valid (or per spec); earlier link is invalidated
FP-14	Sessions after reset	Reset password while logged in elsewhere	Other active sessions are terminated
FP-15	Reset request rate limit	Submit many reset requests rapidly	Throttled to prevent email flooding
4. Session Expiry
ID	Scenario	Steps	Expected Result
SE-01	Idle timeout	Log in, stay idle past the timeout (e.g. 30 min)	Next action redirects to login with a “session expired” message
SE-02	Activity extends session	Perform actions before timeout elapses	Session stays active (if sliding expiry is used)
SE-03	Absolute timeout	Stay active beyond the maximum session lifetime	Forced re-login even with activity
SE-04	Expired session API call	Call an authenticated API with an expired token	401 response; client redirects to login
SE-05	Unsaved work on expiry	Expire the session mid-form	User sees a clear message; no silent data loss or partial submit
SE-06	Logout	Click Logout	Session destroyed server-side; cookie/token cleared
SE-07	Back button after logout	Press browser Back after logout	Protected page is not shown; redirected to login
SE-08	Reuse of old token	Replay a token captured before logout	Rejected (401)
SE-09	Multi-tab behavior	Log out in Tab A, interact in Tab B	Tab B detects the logout and redirects to login
SE-10	Session fixation	Compare session ID before and after login	A new session ID is issued on login
SE-11	Cookie flags	Inspect the session cookie	HttpOnly, Secure, and appropriate SameSite are set
SE-12	Concurrent sessions	Log in from two browsers	Behavior matches spec (both allowed, or the older one is terminated)
5. Brute-Force Lockout
ID	Scenario	Steps	Expected Result
BF-01	Failures below threshold	4 consecutive wrong passwords	Generic errors; account not locked
BF-02	Lockout at threshold	5 consecutive wrong passwords	Account locked or throttled; lockout message displayed
BF-03	Correct password while locked	After lockout, enter the right password	Login still denied until the lock expires or is reset
BF-04	Lockout expiry	Wait for the lockout duration (e.g. 15 min)	Login works again with correct credentials
BF-05	Counter reset on success	3 failures, then 1 success, then 3 failures	Account not locked (counter reset after success)
BF-06	Unlock via password reset	Locked account completes forgot-password flow	Account unlocked and new password works (if spec allows)
BF-07	Lockout on non-existent user	Repeated failures on an unknown email	Same behavior as for real accounts (no enumeration)
BF-08	IP-based rate limiting	20+ failed attempts across different usernames from one IP	IP throttled, receives 429 or CAPTCHA
BF-09	Distributed attempts	Same account attacked from multiple IPs	Account-level lockout still triggers
BF-10	CAPTCHA after failures	Reach the CAPTCHA threshold	CAPTCHA displayed and enforced server-side
BF-11	Lockout bypass attempts	Clear cookies, change user agent, or use a new tab	Lockout still enforced (server-side tracking)
BF-12	Lockout notification	Trigger lockout	User receives an email notification (if specified)
BF-13	Lockout message wording	Review the lockout message	Informs the user without revealing sensitive details
BF-14	Audit logging	Trigger failed attempts and lockout	Events logged with timestamp and IP
BF-15	Admin unlock	Admin unlocks a locked account	User can log in immediately