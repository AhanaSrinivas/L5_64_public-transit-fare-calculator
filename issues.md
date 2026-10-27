# Lab 5: Static Code Analysis — Issues

**Project:** Public Transit Fare Calculator
**Source file:** `fare_calculator.py`
**Tools:** Pylint, Bandit and Flake8

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| SSH host-key verification disabled | Security — High | 80 | Automatically trusting unknown SSH hosts may allow server impersonation. | Reject unknown host keys and configure trusted hosts. |
| Potential SSH command injection | Security — Medium | 82 | Concatenating a filename into a remote shell command may permit command injection. | Validate the filename and construct the remote command safely. |
| Unsafe XML parsing | Security — Medium | 2, 75 | Bandit flags the SAX parser because of potential XML security vulnerabilities. | Replace the vulnerable parser with its `defusedxml` equivalent. |
| Weak MD5 checksum | Security — Medium | 60 | MD5 is cryptographically weak for security-sensitive integrity checks. | Replace MD5 with SHA-256. |
| Daily cap not applied | Functional bug | 35–41 | The function returns the sum of fares without applying the daily cap. | Apply the intended cap to the total. |

## Notes

- Line numbers refer to the original source and may change after editing.
- Security findings are from the initial Bandit report.
- The daily-cap bug was identified by inspecting the source and observing program output.
- Other style and code-quality findings will also be addressed where required by the lab rubric.

