# Autonomous encounter and retention tests

Base 2e20ebd591. Keep the scalar action fixed. Replace imposed sinusoid with a
collective separation X, density d(X)=40+16(1+X²)^(-5/2), orbital potential
U=-B/sqrt(1+X²), kinetic mass M=B T². This is a conservative rigid-profile,
one-cell encounter reduction, not a hydrodynamical or cosmological merger.
Bound orbit starts at X=sqrt(24), Xdot=0, orbital energy -B/5; B=1e-4 is an
illustrative nonrelativistic energy budget in D units, not fitted to clusters.
T=.03,.1,.3,1,3,10 explores speed sensitivity, not a new physical constant.
Start scalar q=1e-6,p=0; integrate 30 uncoupled orbital periods. Independently
check total energy, orbital-to-field work equality and exact budget Efield<=H+B.
Repeat at two tolerances. Use a larger-seed control to expose feedback sign
mutation, and zero seed to check invariance. No stopping-phase optimization.

Use prior 35 gas-shell d values at HJ=1.8e-18/s for WKB retention thresholds:
m_in²=(d-8)/4, m_out²=5.76. Compute escape kinetic fractions and the Einstein
lapse contrast needed to retain a locally at-rest excitation. Shell averages
are not continuous profiles. No numerical escape time or trapped fraction is
claimed. Compare dimensionless lapse requirements with Newtonian speed proxies
only as a scale comparison; no new gravity fit or galaxy likelihood.
