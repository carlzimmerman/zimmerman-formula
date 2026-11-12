#!/usr/bin/env python3
"""BI1 AMENDMENT A1 (f661cc7517): carrier (iii), bimetric. sympy: K(f) from K^-1 = [[1, f], [f, 1]], eigenvalues and the ghost-free range;
field equations and the effective couplings; the explicit-f stress divergence -(dL/df) grad f. Numbers: a_switch = |gPhi||gPhi_chi||grad f| /
(4 pi G rho_chi) for an L* galaxy (SS1 primary halo, cosmic mean outside R200) at 0.1-3 Mpc vs a0 and the law's g, both footings.
    python3 bi1_a1.py   -> bi1_a1.json / bi1_a1.out
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json, math
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..")); sys.path.insert(0, os.path.join(REPO, "closure_2026_11_09", "SS1_self_shielded_conversion"))
_a = sys.argv; sys.argv = [_a[0]]
import ss1_core as C
sys.argv = _a
L = []
def P(s): print(s, flush=True); L.append(str(s))
RES = dict(amendment="f661cc7517", criteria="91e81dcd76", note="TEST lane; adopts nothing; kappa = 1/2 FITTED; not theory closed")
f, Gs, rb, rc = sp.symbols("f G rho_b rho_chi", real=True); Kinv = sp.Matrix([[1, f], [f, 1]]); K = sp.simplify(Kinv.inv())
ev = [sp.simplify(e) for e in K.eigenvals().keys()]
pos = sp.solve_univariate_inequality(sp.And(*[e > 0 for e in ev]).args[0], f) if False else None
srcv = sp.Matrix([rb, rc]); lap = sp.simplify(Kinv * 4 * sp.pi * Gs * srcv)                # (lap Phi, lap Phi_chi) = 4 pi G K^-1 (rho_b, rho_chi)
gP, gC = sp.symbols("gPhi gPhi_chi", real=True); gv = sp.Matrix([gP, gC]); Lf = -(1 / (8 * sp.pi * Gs)) * (gv.T * K * gv)[0]; dLdf = sp.simplify(sp.diff(Lf, f))
RES["iii_symbolic"] = dict(K=str(K), eigenvalues=[str(e) for e in ev], ghost_free="|f| < 1 (both eigenvalues 1/(1 - f), 1/(1 + f) positive)", field_equations=str(lap), dL_df=str(dLdf),
                           conservation="d_j T^{ij}_field = -(dL/df) d_i f with f = f(Xi(x)): conserved only if Xi is a dynamical local field whose stress carries (dL/df) grad f; the record's Xi (Yukawa-smoothed dispersion) is a functional, not a field")
P(f"(iii) K(f) = {K}; eigenvalues {ev}: ghost-free iff |f| < 1; lap(Phi, Phi_chi) = {list(lap)} (standard self-gravity, symmetric cross weight f); dL/df = {dLdf}")
P("(iii)(a) conservation: d_j T^ij = -(dL/df) d_i f, so Xi must be a local field carrying it. The unswitched class (constant f; AX1's bimetric grading) has no such term; the switch adds a new scalar degree of freedom with that coupling.")
G, MS, KPC, MPC = 6.6743e-11, 1.98892e30, 3.0857e19, 3.0857e22; A0 = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}
Q15 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX15_cmb_primary_likelihood", "qx15.json")))
for foot, a0 in A0.items():
    th = Q15["footings"][foot]["main"]["theta"]; h = float(Q15["footings"][foot]["main"]["h"]); OB, OD = th["omega_b"], th["omega_d"]; R = OD / OB; Om = (OB + OD) / h ** 2
    rhoc = 3 * (100 * h * 1e3 / MPC) ** 2 / (8 * math.pi * G); rbar = OD / h ** 2 * rhoc; Mb = 8e10; H = C.halo(Mb, R, h, Om, z=0.0); rows = []
    for r in (0.1, 0.3, 1.0, 3.0):
        rk = r * 1000; rm = r * MPC; gb = G * Mb * MS / rm ** 2
        Mchi = float(H["Menc"](rk)) * MS + (rbar * 4 * math.pi / 3 * (rm ** 3 - (H["R200"] * KPC) ** 3) if rk > H["R200"] else 0.0); gc = G * Mchi / rm ** 2
        rho = (H["fchi"] * H["M200"] / (4 * math.pi * H["R200"] * rk ** 2) * MS / KPC ** 3) if rk < H["R200"] else rbar
        a_sw = gb * gc * (1 / (1.5 * MPC)) / (4 * math.pi * G * rho); glaw = 0.5 * gb + math.sqrt(0.25 * gb * gb + a0 * gb)
        rows.append(dict(r_Mpc=r, g_b=gb, g_chi=gc, rho_chi=rho, a_switch=a_sw, over_a0=a_sw / a0, over_law=a_sw / glaw))
    worst = max(x["over_law"] for x in rows); st = "FAIL" if worst > 1e-3 else "PASS"
    RES[foot] = dict(rows=rows, worst_over_law=worst, B0_iii=st, R200_kpc=H["R200"])
    P(f"[{foot}] (iii)(b) a_switch at 0.1 / 0.3 / 1 / 3 Mpc: " + " / ".join(f"{x['a_switch']:.1e}" for x in rows) + " m/s^2 = " + " / ".join(f"{x['over_a0']:.2g}" for x in rows) + " a0 = "
      + " / ".join(f"{x['over_law']:.2g}" for x in rows) + f" of the law's g (line 1e-3) -> B0(iii) {st}; overall label: " + ("FAIL at B0 (all three carriers)" if st == "FAIL" else "carrier (iii) passes B0: usual gates next (amendment)"))
json.dump(RES, open(os.path.join(HERE, "bi1_a1.json"), "w"), indent=1, default=str); open(os.path.join(HERE, "bi1_a1.out"), "w").write("\n".join(L) + "\n")
