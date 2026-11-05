# Exact expression-comparison correction

The original run passed11 of12 checks. Its sole failure used Python
expression-tree equality for two algebraically equal presentations of
s^2(s-1)/(2(s+1)). Direct simplification of their difference is exactly zero.
The original script and failed run remain unchanged. saturation_v2.py
changes that assertion to an exact simplified-difference test. No equation,
domain, threshold, fixture or interpretation changes. The mutation is run
against the corrected version and must fail the predeclared two checks.
