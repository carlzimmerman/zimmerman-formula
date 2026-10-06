# Frozen computation evidence

Requested base and actual input-collection HEAD: `1db53a670a09a76c023e70784fddc5f351fb8a81`. All four current manifests were independently invoked through validate_manifest.py with --root; every validation succeeded. REPORT is excluded from runner inputs, and this file is a separate run summary. There are no superseded authoritative runs in this child; /tmp preflight is development-only.

| Run | Checks | Expected status |
|---|---|---|
| control_null_a | 33/34 | declared negative control |
| control_odd_a | 33/34 | declared negative control |
| control_time_a | 33/34 | declared negative control |
| main_a | 33/33 | pass |

The controls respectively reject retaining odd interior auxiliary stationarity, finite nonzero-null Hessian, and positive absolute timelike velocity curvature. These mutations deliberately add a false load-bearing claim; their nonzero process exit is expected and preserved.

Numerical tests use λ/y = (.001,1e−20), (.01,1e−20), (.01,1e−12), 60 decimal digits, 150 bisection steps, on the admitted local inverse chart. They corroborate the analytic asymptotics; no global source existence or full metric health claim follows.

Frozen mathematical artifact hashes:

- REPORT.md: `601d2679f84c79f5148e09575ee27c4e107b8a5e669393244919ff1c15aaab2e`.
- checks.py: `f82f8f49ab5163f1eed060b99208c540e1a3c4d2030f78994c4fd73c6d8ffb58`.
- contract.json: `587c2e38f8f4c5580de2530b2e04aa6326e5734dfaa62f98ba6c46753e9d38ce`.
- SOURCES.md: `dcceff7103b3ab23ea904ab682e58898d6848cee68a707ee6595232c23e839cc`.
- provenance.json: `e093ae8ab0c4c2fa3be5e5fb42d98462101a21043f1c8c39dbe6bb7d2d10a728`.
