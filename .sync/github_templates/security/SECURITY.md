# Project Mu Security Policy

Project Mu is an open source firmware project that is leveraged by and combined into
other projects to build the firmware for a given product.  We build and maintain this
code with the intent that any consuming projects can use this code as-is.  If features
or fixes are necessary we ask that they contribute them back to the project.  **But**, that
said, in the firmware ecosystem there is a lot of variation and differientiation, and
the license in this project allows flexibility to use without contribution and therefore
any issues found here may or may not exist in products using Project Mu.  

## Supported Versions

Due to the usage model we generally only supply fixes to the most recent release branch (or main).
For a serious vulnerability we may patch older release branches.

## Additional Notes

Project Mu contains code that is available and/or originally authored in other
repositories (see <https://github.com/tianocore/edk2> as one such example).  For any
vulnerability found, we may be subject to their security policy and may need to work
with those groups to resolve amicably and patch the "upstream".  This might involve 
additional time to release and/or additional confidentiality requirements.

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead please use **Github Private vulnerability reporting**, which is enabled for each Project Mu
repository. This process is well documented by github in their documentation [here](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability#privately-reporting-a-security-vulnerability).

This process we will allow us to privately discuss the issue, collaborate on a solution, and then disclose the vulnerability.
