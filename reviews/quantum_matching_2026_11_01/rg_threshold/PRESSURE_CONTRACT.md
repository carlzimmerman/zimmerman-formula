# Weak threshold/RG waterbag comparator

Frozen before scans. Trial equal couplings e={.01,.03,.05,.1} at Q0=1,
f0=1, g0=sqrt(29/200)e. Execute one bounded run per e. Match Q=eta Qm(X0)
with Qm=sqrt(e/31+(eX0)^2). Schemes: fixed; rg1 ateta1; rg2 ateta.5,1,2;
rg2log ateta.5,2 (eta1 is identical to rg2central).

Retain all full one-loop thresholds, all running couplings/dimensional f
and field transport. The rg2log supplement is the reduced-CS two-loop Q
log completion about central Qm, not a known finite two-loop threshold
function. Its missing central finite potential and finite angular kinetic
threshold are explicit uncalculated remainders. No scale-spread result is
used as a rigorous bound on those functions.

For each scheme bracket the nearby minimum in X/Xmin_TP01=.7..1.3,
compressibility boundary in X/Xmin_new=1.01..1.6 and radial endpoint in
1.5..2.5. Use the old assumed waterbag portal for these comparator roots:
Us=0, Uss-3Us=0 and Uss+2Us=0 respectively. Five-point log stencils use
h=.002 at50digits. Brent's coordinate solver uses float64 brackets with
rtol2e-12 and absolute xtol1e-12; function values use50digits. A missing
bracket is a retained physical/noncoverage outcome, not an automatic pass
or retuned search. Direct mpmath derivatives independently check the
computed roots and one X/Xmin=1.2 witness for every scheme. Positive-source
and radial-stability signs must accompany pressure sign at that witness.

At each pressure boundary derive normalized density using the unchanged
conditional map rho/rho_*=[Us exp(2s)/(3Bcurv)]^(3/5), s=ln(X/Xmin),
Bcurv=Uss(Xmin)/9; no phase level is chosen. Record actual running ratios,
RK32/64 refinement at central minimum, explicit scale variation, direct
versus stencil derivative errors, peak RSS, outcomes and nonclaims.
One thread,180wall/170CPU seconds and fresh version2 records. Contracts and
the independent beta2 contraction evidence are immutable inputs.
