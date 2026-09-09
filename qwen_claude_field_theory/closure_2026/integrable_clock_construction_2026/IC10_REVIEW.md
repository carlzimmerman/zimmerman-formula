# Independent bounded IC10 review

2026-09-08. Read-only review by a separate agent, with only the current
action, implementation, tests and their definitions supplied. No files were
edited by the reviewer. Primary verdict: **computationally verified only in
the stated range**, with the load-bearing Legendre and conformal identities
established exactly. No actionable defect was found in the scoped claim.

Reviewed SHA-256 values:

    ic10_local_clock.py
    9f76d1355dae2a9bb7066bcdccd477b7364f5af08249bf4288352b2c6f4aef8d
    test_ic10_local_clock.py
    1268f0406798886509abb41124a6f7a481b669ad29850309a303f835133143f2
    IC10_LOCAL_CLOCK.md
    7714650a4133836a16bf17da1643c86ad93114ae5d35bbee7419931f01268dcb

The reviewer independently reconstructed the cancellations from the global
phase action, both stationary momentum equations and the off-homogeneous
conformal identity, including arbitrary shear and derivatives of w:

    Q_ij=exp(w) Ktilde_ij,
    det[partial(S,w)/partial(xi,u)]=xi.

The latter is exactly the excluded chart locus in the report. The fixed
canonical-clock-momentum auxiliary bracket was separately checked by solving
the Legendre equation and differencing its Hamiltonian. At S=0.15 it gives
A=58.2357645080571, agreeing with the implemented Schur expression to
3.37e-25. A separate Raychaudhuri check had residual 2.89e-28.

Independent pressure reconstruction from U,Lambda,a0² reproduced the five
reported samples. A 101-point scan on 0.1<=S<=0.2 retained positive PX,
Qclock,A,Hphysical, subluminal clock speed and eta=1. The upper crossing was
recovered at S=0.230723991364998 with cs²=0.242306706149330. This is
corroborating bounded review evidence, not an interval proof. The review's
inline exploratory scans are not new standalone archived scientific scripts;
the committed computation and tests are the primary reproducible evidence.

Exact test command, run in this construction directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_ic10_local_clock.py
```

Exit0; 7 tests passed in 3.892 seconds under Python3.9.6, SymPy1.14.0,
mpmath1.3.0. The main recorded runs separately use Python3.13.9 and
SymPy1.13.1. An initial review secant solve at the outside-plateau S=0.5
control failed; bracketed bisection resolved that numerical-method failure.

The review explicitly did not promote the vacuum plateau to full IC10:
the third mode is a separately counted clock, not a removed scalar;
matter-coupled characteristics, transition, strong coupling, global k=0/y=0,
galactic matching, PPN and realistic cosmology remain unproved.

Parallel Fable commits advanced HEAD from 0e20cf937 to aea949c58 during
review. The three audited input hashes remained unchanged. IC8 and IC9
received self-review and independent-formulation bridges, not this separate
IC10 review. Mathematical proofreading of the new reports checked local
notation, signs, units, links and displayed equations without rewriting any
prior frozen proof or treating proofreading as substantive certification.
