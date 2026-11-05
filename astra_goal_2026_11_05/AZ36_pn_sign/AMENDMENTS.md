# A1 — matter shift completion, pre-computation

After criteria59adccf59f, before any graded script/run: the background
matter variations alone do not specify its quadratic shift contribution.
Ignoring that contribution would put rho_m+p_r spuriously into the
eliminated radial kinetic denominator. Retain it explicitly.

Use a static minimally coupled scalar chi(r), with arbitrary V(chi), as an
exact covariant check: rho_m+p_r=chi'^2/A². Its ADM action contributes
+A³r²(rho_m+p_r)b²/(2N). Verify this term and its cancellation against the
matter part of the background Einstein identity. The vacuum exterior
result is independent of any matter completion. The frozen-matter radial
sub-block with this scalar is not the full coupled scalar/matter spectrum.

The finite z-grid checks this cancellation rather than treating a source's
first variations as its complete perturbation action. The full PN-sign
target, all pass/fail lines, precision tolerances and mutation are unchanged.
This is a declared additional consistency check, not a post-result repair.

# A2 — stable lapse-offset diagnostic, POST-RESULT

The main run passes26/28 checks. Its float64/80-digit comparisons miss the
1e-12 line by maxima1.8182e-12 canonical and1.5271e-12 alt. The40/80-digit
pair agrees below1.04e-37 and all symbolic identities pass. The worst
samples have y=1e-12 and N=0.999998, where converting the decimal lapse to
binary and then subtracting from1 magnifies its input rounding in the dust
term. The original failures and original output trees remain unchanged.

Before this separate diagnostic runs, freeze two checks with the unchanged
1e-12 line: (a) compare the original binary64 expression to80-digit
evaluation of those exact binary64 inputs; (b) evaluate the decimal-input
formula in binary64 using delta_N=1-N formed as an exact Decimal difference
and then rounded once, rather than subtracting two nearly equal binary64
numbers. Check both main and mutant rows, all samples and both footings.
This diagnoses the representation/cancellation error; it cannot turn an
incomplete nonspherical proof into a PASS or erase a frozen numerical miss.
