# Regular charged pressure parent and missing Gauss current

2026-10-20. This constructive route supplies a regular classical pressure
sector, not a full microscopic MOND action or vacuum selector. No scan or
target matching. These independently checked analytic results are not
currently formalized in Lean.

## Charged sextic scalar

In 2+1 dimensions, signature +--, write Psi=r exp(i theta) and

 L=|D Psi|^2-lambda6|Psi|^6/3
  =(partial r)^2+r^2X-lambda6r^6/3,
 X=(partial theta-eA)^2>0, lambda6>0.

Amplitude elimination gives r0^4=X/lambda6 and
P(X)=2X^(3/2)/(3sqrt(lambda6)). For electrochemical
mu=dot theta-eA0=eY>0 and layer density nu,

 P(Y)=gamma Y^3/6, gamma=4nu e^3/sqrt(lambda6),
 P=gamma Y^3/6-gamma Y|A|^2/4+...,
 mV^2(Y)=gamma Y/2.

This half is a vector/pressure relation, not kappa or xi. With an ungauged
phase or gauge probe, sigma=sqrt(2)delta r, pi=sqrt(2)r0 delta theta give

 L2=(partial sigma)^2/2-2mu^2sigma^2+(partial pi)^2/2+2mu sigma dot pi,
 H2=p_sigma^2/2+(p_pi-2mu sigma)^2/2
    +(|grad sigma|^2+|grad pi|^2)/2+2mu^2sigma^2,
 omega_+/-^2=k^2+4mu^2 +/- 2mu sqrt(k^2+4mu^2)>=0.

The light speed squared is 1/2; the gapped mode has gap squared 8mu^2,
while the radial fixed-phase mass parameter is 4mu^2. Both fronts are
luminal. The amplitude EFT needs |omega|,|k|<<mu, which fails at mu=0;
Cartesian Psi instead retains ordinary positive kinetic terms and a
nonnegative sextic potential at the origin. This is classical sector
regularity, not all-orders protection or full MOND completion.

With dynamical Maxwell fields AND a rigid neutralizer provisionally
provided, radial/longitudinal modes obey

 (omega^2-k^2-8mu^2)(omega^2-k^2-mV^2)-4mu^2k^2=0.

They are positive with luminal fronts, omitting neutralizer fluctuations.
The pressure-only vector theory also needs mV<<mu; fixed couplings do not
preserve this hierarchy as mu->0.

## Exact Gauss obstruction

A sole condensate has j0=2e r0^2mu>0. Homogeneous Maxwell Gauss law at
zero electric field excludes it without opposite charge. A sole Lorentz
pressure gives 2e^2Y P_X=0. A regular amplitude function F(Q), Q=|Psi|^2,
does not provide the MOND branch's negative gradient-dependent charge:

 L=Qe^2Y^2-lambda6Q^3/3-F(Q)h^2/2,
 amplitude: e^2Y^2-lambda6Q^2-F'(Q)h^2/2=0,
 Gauss: 2e^2QY=0.

Even after elimination, the envelope derivative is
partial_Y P_eff=2e^2Y Q_*(Y,h)>0 on every positive condensate branch.
For F(Q)=cQ, P_eff=2(e^2Y^2-ch^2/2)_+^(3/2)/(3sqrt(lambda6)); balancing
Gauss reaches zero amplitude. A truncated small-h expansion cannot
establish a nonzero solution outside its range. A-partial(arg Psi)/e
defines a phase EFT on r>0 but is singular at Psi=0. A regular charged
clock/current sector, with its current computed before amplitude
elimination and its fluctuations and gravitating stress checked, is missing.

## BMB: pressure normalization without vacuum selection

Prior overlap is K257, commit 4882e2ec6,
sol61_push/puzzle_32pi/critical_sextic_selector_2026_10_06/REPORT.md.
The earlier static-minimum failure was not rerun; this ensemble is timelike.
For canonical O(N), V=g6(phi^2)^3/(6N^2),

 g6=eta N^2/120, bar_eta=g6/(16pi^2), g6_BMB=16pi^2,
 beta_bar_eta=[24bar_eta^2-2pi^2bar_eta^3]/N+O(N^-2).

BMB is not the displayed finite-1/N beta zero (g6=192). A conditional
leading-N application charges one O(2) pair, leaving the N-2 spectator
determinant neutral at this order. With v=varphi^2/N,

 Omega/N=v(M-2pi v)^2/2+(2pi^2/3)v^3-mu^2v/2, v,M>=0.

The global minimum is v=mu/(2pi), M=mu, P=Nmu^3/(6pi), twice the naive
critical tree pressure. This is our conditional finite-charge application
of the leading-N functional, not the source's real-time MOND theorem.
The canonical tree embedding has lambda6=4g6/N^2; assigning an N=2 field
the large-N critical coupling is not a controlled quantum calculation.

At zero density V(0,M)=NM^3(1-bar_eta)/(24pi): criticality leaves arbitrary
M and zero relative vacuum energy. Leading-N stress is traceless, so a
Lorentz vacuum in three spacetime dimensions obeys 3epsilon=0. The charged
state instead has epsilon=2P and epsilon+P=mu n=3P>0. Neither supplies
positive same-state dark-energy vacuum energy. Pressure normalization does
not fix the compensating current, bulk embedding, crossover b or
epsilon_DE/(gamma b^3). Primary source locators are in SOURCES.md.
