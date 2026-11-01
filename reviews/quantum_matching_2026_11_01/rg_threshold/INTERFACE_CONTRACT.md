# TP02 improved interface controls

Freeze before running `check_interface.py`. Use the two-loop gamma/gauge
coefficients independently reconstructed in rg_derivation/check_rg.py and
its completed seven-case raw49-field contraction run_001. The threshold
implementation uses the untouched TP01 full spectrum, with arbitrary f and
Q restored by exact mass-dimensional scaling.

For e=.03, f0=Q0=1, X0=7.367143721278508*sqrt(e/31)/e, compare32 and64
RK4 characteristic steps in two-loop running. Test the exact T/X field
dictionary, its RG integrated counterpart, gcrit departure, fixed limit,
and the all-threshold one-loop Q derivative. Reference-scale partial
schemes are fixed, rg1, rg2 and rg2log. At eta=.5,1,2 compare their explicit
scale spread and the reduction when CS-required reduced two-loop scale
logs are added about the central Qm(X0). No finite two-loop potential or
finite angular kinetic matching is supplied by this operation.

Compute direct50-digit U/F log derivatives at one displaced reference
field state1.2*X0, and independently compare five-point stencil h=.002.
Check identity F=(Delta(t)/lambda(t)^2)X(t)^2 and retain F and its
log derivatives for the matter agent. Threshold scaleQm=sqrt(e/31+(eX0)^2)
is a numerical prescription, not an action input. One thread,120wall/110CPU
seconds, measured RSS and fresh v2 manifest. Any failed numerical control
is preserved before changing implementation or tolerances.
