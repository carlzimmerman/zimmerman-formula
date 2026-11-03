# AZ6 — compensated lensing for a future slip test

κ = ½ FITTED; not theory closed

Pre-result. Record: ls LE1 and CRG1 lens inputs; git log lensing/slip; rg conformal/disformal/slip in UX1/AS2. Conformal-only extra lensing is already closed there. Instead derive an inner-mass-insensitive observable before choosing a slip rule. This is a diagnostic route, not a new gravity law or a claim to invent annular statistics.

Define U(R;R0)=DeltaSigma(R)-(R0/R)^2 DeltaSigma(R0), R>R0. Since DeltaSigma=2/R² integral_0^R Sigma(s)s ds-Sigma(R), all mass interior to R0 cancels. A constant sheet cancels as well. This is linear in measured shear if lens-source distance weights are matched. A varying redshift mix prevents automatic cancellation and must be measured.

Known answers on synthetic R0=1, R=2,4: compact point mass M=1 has DeltaSigma=M/(pi R²), giving U=0; SIS DeltaSigma=A/R, A=1 has U=A/R*(1-R0/R). Independently integrate Sigma=A/R to obtain DeltaSigma before combining. Absolute tolerances 1e-11. MUTATE use PLUS instead of subtraction: the point-mass test must fail by >0.01. Both footings: identity independent of a0; empirical scores remain NOT EVALUABLE. Output results.json predeclared. Synthetic amplitudes are test units, not astrophysical fitted coefficients.

Strict data gate before any observation grade: raw source ellipticities, response/weights and lens-source redshifts, with native distances and declared baryon inventory. The existing CRG1 crg1_lens.py contains a flat matter+constant distance conversion and TwoHalo numbers 0.6736,0.02237,0.1200. Do not execute/import it for a new result. Its ESD tables are already cosmology-processed; their existence is not raw-input clearance. LAM1 records an incomplete shear download. No new download allowed: record missing raw inputs in NEEDS_OWNER.md.

A gravitational-slip interpretation requires deriving lens potential W=(Phi+Psi)/2 and acceleration grad Phi from an action and matching the same tracer population. Free slip amplitudes/functions are FITTED, not a mechanism. Do not convert the record's approximately 0.09 dex discrepancy into a claimed measured slip.
