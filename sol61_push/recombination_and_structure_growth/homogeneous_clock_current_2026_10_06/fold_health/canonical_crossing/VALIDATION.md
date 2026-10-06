# Validation

Authoritative run `main_c`: 9/9 symbolic checks pass. Expected-failing `control_density_c`: 8/9 pass, with the deleted clock-density compatibility term rejected. Both manifests validate against current inputs. These pass counts support the algebra; the analytic local theorem is proved in REPORT.md and independently audited separately.

Development preflights required rational cancellation before A=0 and symbolic simplification before matrix equality. The first runner command used a result path outside the required output directory; the second pair used a disallowed `..` input path. Those attempts were rejected before execution and produced no scientific evidence. The authoritative invocations use normalized repository paths and explicit result paths inside fresh run directories.

Wall limit 45 seconds, CPU limit 30 seconds, thread limit one. No random sampling or perturbation transfer integration is used.
