# FGF-018: conditional error-box robustness accepted

Coordinator read the report and two derivation records, verified required
result fields and all listed hashes, and validated both numerical manifests.
Result SHA256:
`ca49202b987c98431b2361bfad8d172ec5bef139ae5252ca3179835c367f9098`.

The extremum directions follow directly from positive masses, monotone force
laws and log-linear endpoint interpolation: minimum slope uses L2/U1, while
minimum residual uses lower hydrostatic-equivalent mass and upper gas/star
masses. These analytic formulas cover the declared knot boxes, evaluated in
binary64 without a directed-rounding certification claim.

Accept the computed robustness checkpoint: all 189 gas intervals have
s_min>1 (minimum 1.0847944099720517), and all 252 original plus 2268 midpoint
shell/branch evaluations have positive Delta_min (minimum
1.6206692315737158e-11 m/s²). One such interior shell suffices for the stated
steady, source-free spherical-flow contradiction with decreasing extra
pressure. Positivity of Delta at every unsampled radius is not asserted.

The result is nonvacuous on the tested support. A644's hydro box fails an
optional full-raw-support monotonicity condition involving outer radii, but
that empty extra family was not used to obtain the rectangular certificate;
the native interpolation support needed for 100–1000 kpc admits monotone
realizations. Preserve the explicit hydrostatic-equivalent force interpretation.

The minimum gas-error inflation factor 1.591752955 marks loss of the strict
s>1 certificate, not a sigma value or a repaired flow. At s=1 and Delta>0 the
Euler contradiction still holds. Quoted-error semantics, joint coverage,
systematics, interpolation derivatives and the pressure reconstruction remain
conditional inputs. No observational confidence or whole-theory exclusion
is accepted. Next work must constrain those inputs, not repeat central slopes.
