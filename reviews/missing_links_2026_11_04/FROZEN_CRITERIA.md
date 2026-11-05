# Missing-links review: bounded branch check

Owner steering: distrust inherited verdicts; inspect the work for missing
links. This review includes the coordinator's AZC1 proposal. No historical
gate or manuscript will be rewritten. Base observed revision 97f1753e4a.

## Three source-link questions

1. Do FN1b/FN6 Gaussian filter results prove a v3s action result? Compare the
   operators and their declared domains; do not transfer grades without an
   equivalence proof.
2. Does CT14's s map to physical g/a0 in a screened background? Read the
   symbolic substitution and compare to D10's original field equation.
3. Does CT7 exclude every potential portal, or its specified backgrounds?
   Test the acknowledged constant-w exception by a self-consistent scalar
   plus baryonic-dust construction, not by prescribing an arbitrary w(t).

## Exact branch test, frozen before script/results

Units c=1, Mpl^2=1/(8piG). Canonical scalar, no bare Lambda, zero khronon
background charge, v3s response zero on homogeneous FRW. Let w=-beta with
0<beta<1, N=ln(scale factor), y=(phi-phi_star)/B>0,
B=2 Mpl sqrt(3(1-beta))/(3 beta).

Use V(y)=Vstar sinh(y)^[-2(1-beta)/beta] and
rho_phi=2V/(1+beta), rho_b/rho_phi=csch(y)^2.
Check the Friedmann, kinetic energy, baryon continuity, scalar continuity and
Klein-Gordon identities with y_N=(3 beta/2)tanh(y).
For a0^2=xi G V and xi=2 kappa^2/(1+beta), verify the exact density tie and
slope 1/2 on this branch. The coefficient is fitted, not derived.

SymPy exact identities must simplify to zero. Independent 60-digit
evaluation at beta in {1/3,2/3,9/10} and y in {1/10,1,3} must have normalized
residual <=1e-40. Nine points corroborate the identities; they do not establish
attraction, physical fit, or arbitrary-initial-condition behavior.

Known controls: direct canonical stress and separate dust conservation.
MUTATE kinetic: add +1 to the potential exponent without changing the
candidate branch; the KG/continuity consistency must fail.
MUTATE normalization: set xi=kappa^2 instead; absolute tie must fail for
beta<1 even though its logarithmic slope stays 1/2.

No full stability or observation grade. No tuning, scans, new downloads or
claims of novelty. One symbolic process, 60-second wall limit, 55-second CPU
limit, single-thread environment; portability limitations of the prior run
are already known. Pin sources and record raw output hashes.
