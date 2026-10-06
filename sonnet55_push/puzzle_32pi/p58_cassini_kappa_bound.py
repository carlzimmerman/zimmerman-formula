"""p58: Cassini's Q2 as a bound on kappa for OUR kernel in QUMOND (solver qumond_efe_multipole.py, observed Galactic field 2.146e-10 m/s^2 held fixed).
Q2(a0) for nu = sqrt(1+1/y) is monotonic; Hees+ 2014: Q2 = (3 +- 3)e-27 s^-2 -> 1 sigma upper 6e-27, 2 sigma upper 9e-27. kappa = a0 / (c sqrt(G rho_Lambda)) = 0.5 a0 / 9.3603e-11.
Checks: M Q2 rises monotonically with a0 over 1e-12..1.13e-10; B report kappa_max(1 sigma, 2 sigma) and the sigma of kappa = 1/2.
Run: python3 p58_cassini_kappa_bound.py | MUTATE=1 drops the external field to 10% (Q2 must change -> check E fails: Q2 at kappa=1/2 must equal the p57 value 2.195e-26 to 1%)
"""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qumond_efe_multipole import Field
import warnings; warnings.filterwarnings("ignore")
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
def nu1(y): return 1.0 / (y * (np.sqrt(1 + 1 / y) + 1))
ge = 2.146e-10 * (0.1 if MUTATE else 1.0)
a0s = np.array([1e-12, 2e-12, 5e-12, 1e-11, 2e-11, 4e-11, 6e-11, 8.32e-11, 9.3603e-11, 1.13e-10])
Q = np.array([Field(nu1, a, ge_obs_si=ge, Nr=4000, Nmu=256).Q2 for a in a0s])
for a, q in zip(a0s, Q): print(f"   a0 = {a:.3e}  kappa = {0.5*a/9.3603e-11:.3f}  Q2 = {q:.3e} s^-2  ({(q-3e-27)/3e-27:+.1f} sigma)")
check("E Q2 at kappa = 1/2 equals p57's 2.195e-26 to 1%", abs(Q[8] / 2.195e-26 - 1) < 0.01)
check("M Q2 rises monotonically with a0", np.all(np.diff(Q) > 0))
lk = lambda qlim: float(np.exp(np.interp(np.log(qlim), np.log(Q), np.log(a0s))))
for lab, ql in (("1 sigma", 6e-27), ("2 sigma", 9e-27), ("3 sigma", 1.2e-26)):
    a = lk(ql); print(f"   Cassini {lab}: a0 < {a:.2e} m/s^2, kappa < {0.5*a/9.3603e-11:.3f}")
print(f"   the galaxy values: gas points 8.3e-11 (kappa 0.44), SPARC ~1.08e-10 (0.58) -> Q2 {Q[7]:.2e} .. {Q[9]:.2e}")
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
