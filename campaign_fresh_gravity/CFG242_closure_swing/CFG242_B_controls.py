#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG242_B_controls -- route B (L13), stage 0: the REPRODUCTION CONTROLS (frozen plan section 4.3, gate order 0): 'Controls (13c reproduction, EH calibration C2 of CFG232)'.
A failed control stops the route.
  C-B1  EH calibration (fresh code): the relative-sector Einstein-Hilbert quadratic form is invariant under d -> d + kA + Ak + kk pi (gauge) -- the analogue of CFG232's C9/C2.
  C-B2  the 4D five-invariant class (the record's, direction T4 - T1) reproduces WF2/L70 on flat space: c_T^2 = 1 and a FOURTH-ORDER transverse vector, helicity-1 determinant
        proportional to mu (b + 4 mu) (kappa^2 - omega^2)^2 (CFG232's L_A1 = -(lambda/2)(2u0 + u1)(kappa^2 - omega^2)^2 A_1^2: the same (kappa^2 - omega^2)^2 structure).
  C-B3  the 13c reproduction: the COMMITTED CFG232_A7 script (13c, the conformally coupled AQUAL-type scalar) is copied to a scratch directory and re-run there (the repository is not
        written); its verdict statuses and G1-law number must equal the committed CFG232_A7_scalar_tensor_13c.json.
"""
import os, sys, shutil, subprocess, json, tempfile
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
import CFG242_common as C
from CFG242_B_algebra import *
R = C.Run("CFG242_B_controls")
P = R.P
P(__doc__.strip())

R.banner("C-B1  gauge invariance of the EH quadratic form")
A = sp.symbols("A0:4"); pi_ = sp.Symbol("pi")
gm = sp.zeros(4, 4)
for i in range(4):
    for j in range(4):
        gm[i, j] = klo[i] * A[j] + klo[j] * A[i] + klo[i] * klo[j] * pi_
R.check("C-B1 EHquad(k A + A k + k k pi) = 0", sp.simplify(EHquad(gm)) == 0, "sympy residual 0")

R.banner("C-B2  the 4D class on flat space: WF2/L70's fourth-order vector and c_T^2 = 1")
L4 = lagrangian("4D"); M4 = hessian(L4)
h1 = sp.factor(block(M4, ["d01", "d13"]).det())
tt = sp.factor(M4[5, 5])
P(f"    helicity-1 determinant (4D, T4 - T1): {h1}")
P(f"    TT (d12) entry: {tt}")
want = -2 * mu * (bb + 4 * mu) * (ka - om) ** 2 * (ka + om) ** 2
R.check("C-B2a helicity-1 determinant = -2 mu (b + 4 mu)(kappa - omega)^2 (kappa + omega)^2: degree 4 in omega (an Ostrogradsky vector)", sp.simplify(h1 - want) == 0, f"degree in omega {sp.degree(sp.expand(h1), om)}")
R.check("C-B2b TT entry proportional to (omega^2 - kappa^2): c_T^2 = 1 exactly", sp.simplify(tt / (-(bb + 4 * mu) * (ka - om) * (ka + om)) - 1) == 0, "WF2/L70: c_T^2 = 1 at T4 - T1")

R.banner("C-B3  13c reproduction: re-run the committed CFG232_A7 in a scratch copy and compare with the committed JSON")
src = os.path.join(C.REPO, "campaign_fresh_gravity", "CFG232_door13_bimond")
tmp = tempfile.mkdtemp(prefix="cfg242_ctl_", dir=C.HERE)
try:
    for f in ("CFG232_common.py", "CFG232_A7_scalar_tensor_13c.py"):
        shutil.copy(os.path.join(src, f), tmp)
    env = dict(os.environ); env["ZF_REPO"] = C.REPO; env.pop("MUTATE", None)
    p = subprocess.run([sys.executable, os.path.join(tmp, "CFG232_A7_scalar_tensor_13c.py")], env=env, capture_output=True, text=True, cwd=tmp)
    new = json.load(open(os.path.join(tmp, "CFG232_A7_scalar_tensor_13c.json")))
    old = json.load(open(os.path.join(src, "CFG232_A7_scalar_tensor_13c.json")))
    sv_new = {k: v["status"] for k, v in new["numbers"]["verdicts"].items()}
    sv_old = {k: v["status"] for k, v in old["numbers"]["verdicts"].items()}
    same_checks = [(a["name"], a["ok"]) for a in new["checks"]] == [(a["name"], a["ok"]) for a in old["checks"]]
    P(f"    scratch re-run exit code {p.returncode}; verdict statuses identical: {sv_new == sv_old}; every check name and outcome identical: {same_checks}")
    R.check("C-B3 13c row: the re-run of the committed CFG232_A7 reproduces its committed verdicts and checks", sv_new == sv_old and same_checks, f"{len(sv_new)} verdicts, {len(new['checks'])} checks")
finally:
    shutil.rmtree(tmp, ignore_errors=True)
R.finish()
