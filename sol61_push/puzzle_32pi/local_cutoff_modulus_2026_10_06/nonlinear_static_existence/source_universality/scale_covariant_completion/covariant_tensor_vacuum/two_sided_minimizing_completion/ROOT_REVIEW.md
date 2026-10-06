# Root reconciliation — source envelope and null jets

Reviewed 2026-10-06 at base HEAD `1db53a670a09a76c023e70784fddc5f351fb8a81`.

I read the frozen action, fixed-invariant elimination and peer reconstruction. The fixed-x chain subtracts `(2y e_T)^2/x_y` from M_TT, so the energy curvature is positive on the admitted stationary chart even though mixed derivatives at the origin diverge. The parity examples concern retained auxiliary equations, not guessed eliminated functions: odd remainder with the same potential has M_T<0 for every positive T.

I separately evaluated the exact SymPy null-jet limit for z=(w²−v²)/(4 chi a0²). The result is `−sqrt(2) v^(3/2)/(64 a0³ chi^(3/2))`, equal to the report's `−(v/(2 chi a0²))^(3/2)/16`. Higher powers cannot remove this leading singularity. The obstruction is to a C² open-neighborhood eliminated invariant action. Existence of a second derivative at the zero jet is compatible with this result. No full constraint ghost conclusion follows from the pure-TT coefficient sign.

All four current manifests independently validate; main33/33 and three controls33/34 are independently reviewed. REPORT and the fresh peer review are pinned below. The original vacuum-coefficient/source-to-cosmology goal remains open. A positive foliation invariant is a changed-operator route, not a repair by arbitrary negative continuation.

REPORT.md SHA256 `601d2679f84c79f5148e09575ee27c4e107b8a5e669393244919ff1c15aaab2e`.

INDEPENDENT_REVIEW.md SHA256 `70a790bce3d10b543262fcea7fb71f82b4558143ae8564f656e75b5afdc2b1a2`.
