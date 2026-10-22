#!/usr/bin/env python3
"""E2_field_equation -- which nonlinear Poisson equation does the framework's own static action give at L* -> 0,
and what happens to D7b (Cassini Q2), D2 (wide-binary gamma_v) and D7c (family no-go) when it is used.

Part 1 (sympy): PAPER49's Lagrangian  L = -|grad Phi - K P|^2/2K - rho Phi - W_rem(u)  (gamma = 0) and the static
weak-field A33/DSF-21 form  -|grad Phi|^2/2K + P.grad Phi - W_full(u) - rho Phi  give
    (Phi)  div(grad Phi - K P) = K rho,      (P)  grad Phi - K P = R(u) P_hat,  R = u^2/(a0 - u)
=>  K P = u(|grad Phi|) grad Phi/|grad Phi|  and  div[ mu(|grad Phi|/a0) grad Phi ] = K rho,  mu = x/(1+x):  AQUAL.
The action makes grad Phi curl-free; it does NOT make h = grad Phi - K P curl-free (QUMOND's assumption).
Part 2: Route A (axisymmetric AQUAL/QUMOND, `aqual_axi.py`) and Route B (3-D FFT AQUAL/QUMOND, `aqual_fft.py`).
Frozen criteria: FROZEN_CRITERIA.md (commit 021ee82abb).  --mutate: AQUAL replaced by QUMOND everywhere.
Deterministic, no network, single thread.  kappa = 1/2 FITTED.
"""
import json
import math
import os
import gc
import resource
import sys
import time

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import aqual_axi as RA  # noqa: E402
import aqual_fft as RB  # noqa: E402

MUTATE = "--mutate" in sys.argv
TAG = "_MUTATE" if MUTATE else ""
OUT_TXT = os.path.join(HERE, f"e2_field_equation{TAG}.out")
OUT_JSON = os.path.join(HERE, f"e2_field_equation_results{TAG}.json")
AQ = "QUMOND" if MUTATE else "AQUAL"          # the mutation: the hidden-ingredient error itself

# ------------------------------------------------------------------ inputs (labelled in FROZEN_CRITERIA.md)
GM = 1.32712440018e20
AU = 1.495978707e11
R_SAT = 9.5826 * AU
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
GNE_A60 = 6.913e-11
GE_KIN = {"E1": 1.9 * 9.36e-11, "E2": 2.2 * 9.36e-11, "E3": 2.6 * 9.36e-11}
EL = ("E0", "E1", "E2", "E3")
H_LO, H_HI = -3.0e-27, 9.0e-27
P_LO, P_HI = -2.0e-27, 5.2e-27
BN11 = (3.8e-26, 1.2e-10, 1.9e-10)
YT_ROWS = [None, 60.0, 66.3803, 77.876, 140.0]
G = 6.67430e-11
MSUN = 1.98892e30
KAU = 1e3 * AU
GEXT = {"PREREG_primary": 1.778e-10, "PREREG_alt": 2.078e-10}
RES_A = dict(Nr_per_dec=60, Nt=96)            # Route A production grid (K5 tests it)
NB, MB = (256, 11)                            # Route B production grid (K8 tests 192/8 vs 256/11)

D7B = json.load(open(os.path.join(REPO, "doors_push_2026_10_22/D7b_cassini_Q2/d7b_cassini_q2_results.json")))
D7C = json.load(open(os.path.join(REPO, "doors_push_2026_10_22/D7c_q2_rar_gate/d7c_q2_rar_gate_results.json")))
D2 = json.load(open(os.path.join(REPO, "doors_push_2026_10_22/D2_wide_binary_fork/d2_wide_binary_fork_results.json")))

lines, CHECKS, RES = [], [], {"lane": "E2_field_equation", "mutate": MUTATE, "aqual_mode_used": AQ}
T0 = time.time()


def say(s=""):
    print(s, flush=True)
    lines.append(s)


def check(cid, ok, value, thr, note=""):
    CHECKS.append(dict(id=cid, passed=bool(ok), value=value, threshold=thr, note=note))
    say(f"{cid} {'PASS' if ok else 'FAIL'} {value} {thr}   {note}")


say("=" * 100)
say("E2_field_equation -- the action's own field equation at L* -> 0, and D7b / D2 / D7c recomputed with it"
    + ("   [MUTATE: AQUAL replaced by QUMOND]" if MUTATE else ""))
say("=" * 100)

# ================================================================== Part 1: derivation (sympy)
x, y, z = sp.symbols("x y z", real=True)
K, a0s, u, g = sp.symbols("K a0 u g", positive=True)
Phi = sp.Function("Phi")(x, y, z)
rho = sp.Function("rho")(x, y, z)
Px, Py, Pz = [sp.Function(n)(x, y, z) for n in ("P_x", "P_y", "P_z")]
Pv = sp.Matrix([Px, Py, Pz])
gradPhi = sp.Matrix([sp.diff(Phi, v) for v in (x, y, z)])
uu = K * sp.sqrt(Px ** 2 + Py ** 2 + Pz ** 2)
W_full_u = (a0s ** 2 / K) * (-u / a0s - sp.log(1 - u / a0s))
W_rem_u = W_full_u - u ** 2 / (2 * K)
# K dW_full/du = a0 u/(a0-u) and R = K dW_rem/du = u^2/(a0-u)
k_wfull = sp.simplify(K * sp.diff(W_full_u, u) - a0s * u / (a0s - u))
R_u = sp.simplify(K * sp.diff(W_rem_u, u))
k_R = sp.simplify(R_u - u ** 2 / (a0s - u))
hv = gradPhi - K * Pv
L49 = -(hv.dot(hv)) / (2 * K) - rho * Phi - W_rem_u.subs(u, uu)
LA33 = -(gradPhi.dot(gradPhi)) / (2 * K) + Pv.dot(gradPhi) - W_full_u.subs(u, uu) - rho * Phi
k1b_same = sp.simplify(sp.expand(L49 - LA33))
from sympy.calculus.euler import euler_equations  # noqa: E402
eqs = euler_equations(L49, [Phi, Px, Py, Pz], [x, y, z])
# Phi equation: should be  div(grad Phi - K P) - K rho = 0  (up to an overall factor)
div_h = sum(sp.diff(hv[i], v) for i, v in enumerate((x, y, z)))
phi_eq = sp.simplify(eqs[0].lhs * K + (div_h - K * rho))   # eqs[0]: -rho + div(h)/K ... (sign checked below)
phi_eq2 = sp.simplify(eqs[0].lhs * K - (div_h - K * rho))
phi_ok = (phi_eq == 0) or (phi_eq2 == 0)
# P equation (x comp): h_x - R(u) P_x/|P| = 0
Pn = sp.sqrt(Px ** 2 + Py ** 2 + Pz ** 2)
p_target = hv[0] - R_u.subs(u, uu) * Px / Pn
p_eq = sp.simplify(eqs[1].lhs - p_target)
p_eq2 = sp.simplify(eqs[1].lhs + p_target)
p_ok = (p_eq == 0) or (p_eq2 == 0)
# algebraic solution: u(g) = a0 g/(a0+g) solves g - u - R(u) = 0 (h parallel to grad Phi) ; mu = 1 - u/g = g/(a0+g)
ug = a0s * g / (a0s + g)
k_balance = sp.simplify(g - ug - R_u.subs(u, ug))
k_mu = sp.simplify((1 - ug / g) - (g / a0s) / (1 + g / a0s))
# general 3-D check (not only spherical): non-symmetric Phi, P from the algebraic solution, numeric residual of
#   [div(grad Phi - K P) - K rho]  minus  [div(mu grad Phi) - K rho]
Phi_t = sp.sin(x) * sp.exp(y / 3) + x ** 2 * z + 0.3 * y * z ** 3 + 2.0 * x
gP = sp.Matrix([sp.diff(Phi_t, v) for v in (x, y, z)])
gm = sp.sqrt(gP.dot(gP))
Kv, a0v = 4 * sp.pi * 0.37, 1.3
Pt = (a0v * gm / (a0v + gm)) / Kv * gP / gm
lhs1 = sum(sp.diff(gP[i] - Kv * Pt[i], v) for i, v in enumerate((x, y, z)))
lhs2 = sum(sp.diff((gm / a0v) / (1 + gm / a0v) * gP[i], v) for i, v in enumerate((x, y, z)))
rng = np.random.default_rng(20261022)
pts = rng.uniform(-1.5, 1.5, size=(6, 3))
f1 = sp.lambdify((x, y, z), lhs1 - lhs2, "numpy")
fscale = sp.lambdify((x, y, z), lhs2, "numpy")
res3d = max(abs(float(f1(*p))) / max(1.0, abs(float(fscale(*p)))) for p in pts)
# the P equation at the algebraic solution, same field: h - R(u) P_hat = 0
Rv = lambda uu_: uu_ ** 2 / (a0v - uu_)
f_pe = sp.lambdify((x, y, z), (gP - Kv * Pt) - Rv(Kv * sp.sqrt(Pt.dot(Pt))) * Pt / sp.sqrt(Pt.dot(Pt)), "numpy")
res_pe = max(float(np.max(np.abs(np.array(f_pe(*p), dtype=float)))) for p in pts)
k1a = phi_ok and p_ok and k_R == 0 and k_wfull == 0 and k_balance == 0 and k_mu == 0 and res3d < 1e-10 and res_pe < 1e-10
say("\n[Part 1] Euler-Lagrange equations of the action (gamma = 0, static, O(eps))")
say(f"  K dW_full/du - a0 u/(a0-u) = {k_wfull};  R = K dW_rem/du = {R_u}  (R - u^2/(a0-u) = {k_R})")
say(f"  Phi-eq == div(grad Phi - K P) - K rho : {phi_ok};  P-eq == (grad Phi - K P) - R(u) P_hat : {p_ok}")
say(f"  balance g - u - R(u) at u = a0 g/(a0+g): {k_balance};  mu = 1 - u/g - x/(1+x): {k_mu}")
say(f"  general 3-D field: |div(grad Phi - K P) - div(mu grad Phi)| = {res3d:.1e}; P-eq residual {res_pe:.1e}")
check("K1a", k1a, f"symbolic 0/0/0/0, 3-D residual {res3d:.1e}/{res_pe:.1e}", "exact / <1e-10",
      "PAPER49 action -> div[mu(|grad Phi|/a0) grad Phi] = K rho, mu = x/(1+x): AQUAL")
# K1b: A33 static weak-field form identical; D7d (L)/(P) at L*=0 equal these equations
pv = sp.symbols("p", positive=True)
d7d_P = sp.simplify(a0s * pv / (a0s - pv) - K * sp.diff(W_full_u, u).subs(u, pv))   # D7d (P) at L*=0 vs A33 dW_full
k1b = (k1b_same == 0) and d7d_P == 0
say(f"  L_PAPER49 - L_A33(static weak field) = {k1b_same};  D7d (P) at L*=0 minus A33 P-eq: {d7d_P}")
check("K1b", k1b, f"{k1b_same}/{d7d_P}", "0/0", "A33/DSF-21 form and D7d's (L),(P) at L*=0 give the same AQUAL equations")
RES["Part1"] = dict(R_u=str(R_u), KdWfull_minus=str(k_wfull), L49_minus_LA33=str(k1b_same), res3d=res3d, res_P=res_pe,
                    D7d_P_minus=str(d7d_P), statement="div[mu(|grad Phi|/a0) grad Phi] = 4 pi G rho, mu = x/(1+x) (AQUAL); "
                    "grad Phi curl-free; h = mu grad Phi = g_N + (divergence-free part), the latter NOT set to zero")

# ================================================================== Part 2: Route A (axisymmetric)
LAW = RA.law_canonical()


def y_of(law, foot, e):
    a0 = A0[foot]
    if e == "E0":
        return GNE_A60 / a0
    return float(law.newton_from_total(np.array([GE_KIN[e] / a0]))[0])


def q2_SI(law, y_e, a0, mode, **kw):
    kk = dict(RES_A); kk.update(kw)
    s = RA.AxiSolver(law, y_e, mode=mode, **kk)
    s.solve(maxit=800)
    unit = a0 ** 1.5 / math.sqrt(GM)
    q0, qs = s.q2(r_eval=R_SAT / math.sqrt(GM / a0))
    return q0 * unit, qs * unit, s


say("\n[Part 2, Route A] axisymmetric solver checks")
# K2: QUMOND vs D7b Route M
k2 = []
for foot in A0:
    for e in EL:
        yv = y_of(LAW, foot, e)
        qq, _, _ = q2_SI(LAW, yv, A0[foot], "QUMOND")
        ref = D7B["grid"][foot]["none"][e]["Q2_M"]
        k2.append((foot, e, qq, ref, qq / ref - 1))
mx = max(abs(t[4]) for t in k2)
check("K2", mx <= 0.02 and all(np.sign(t[2]) == np.sign(t[3]) for t in k2), f"max|A_QUMOND/D7b-1|={mx:.4f}", "<=0.02 same sign",
      "Route A in QUMOND mode vs D7b Route M, 4 E x 2 footings")
RES["K2"] = [dict(footing=f, E=e, Q2_routeA_QUMOND=a, Q2_D7b=b, rel=c) for f, e, a, b, c in k2]
# K3: BN11
Qbn, a0bn, gebn = BN11
ybn = float(LAW.newton_from_total(np.array([gebn / a0bn]))[0])
qa_bn, _, s_bn = q2_SI(LAW, ybn, a0bn, AQ)
qq_bn, _, _ = q2_SI(LAW, ybn, a0bn, "QUMOND")
r3 = qa_bn / Qbn
check("K3", abs(r3 - 1) <= 0.10 and abs(qq_bn / Qbn - 0.737) <= 0.02, f"AQUAL/BN11={r3:.4f} QUMOND/BN11={qq_bn / Qbn:.4f}",
      "|.-1|<=0.10, 0.737+-0.02", f"BN11 mu1 AQUAL 3.8e-26 at a0=1.2e-10, g_e=1.9e-10; ours {qa_bn:.3e} ({s_bn.iters} it)")
RES["K3"] = dict(Q2_AQUAL=qa_bn, Q2_QUMOND=qq_bn, BN11=Qbn, ratio_AQUAL=r3, ratio_QUMOND=qq_bn / Qbn)
# K4: isolated
s_iso = RA.AxiSolver(LAW, 0.0, mode=AQ, **RES_A)
s_iso.solve()
errs = []
for rp in (0.1, 1.0, 10.0):
    dr_, dt_ = s_iso.field_at(np.array([rp]), np.array([np.pi / 3]))
    Fr = 1.0 / rp ** 2 + dr_[0]
    errs.append(abs(Fr ** 2 / (Fr + 1.0) * rp ** 2 - 1.0))
cm = s_iso.legendre_modes()
ang = float(np.max(np.abs(cm[:, 1:])))
check("K4", max(errs) <= 1e-3 and ang < 1e-6, f"max rel err {max(errs):.2e}, l>=1 content {ang:.1e}", "<=1e-3, <1e-6",
      "isolated AQUAL = algebraic law at r = 0.1, 1, 10 r_M")
RES["K4"] = dict(rel_err=errs, angular=ang)
# K5: convergence + iteration (canonical E2, AQUAL)
y2 = y_of(LAW, "canonical", "E2")
base, _, sb = q2_SI(LAW, y2, A0["canonical"], AQ)
vT, _, _ = q2_SI(LAW, y2, A0["canonical"], AQ, Nt=2 * RES_A["Nt"])
vR, _, _ = q2_SI(LAW, y2, A0["canonical"], AQ, Nr_per_dec=int(1.5 * RES_A["Nr_per_dec"]))
vI, _, _ = q2_SI(LAW, y2, A0["canonical"], AQ, r_in=1e-6)
conv = max(abs(vT / base - 1), abs(vR / base - 1), abs(vI / base - 1))
# iteration: Q2 change in the last Anderson step (re-solve with one extra fixed-point application)
psi_next = sb.G(sb.psi)
sb2 = sb
old = sb.q2()
sb2.psi = psi_next
it_rel = abs(sb2.q2() / old - 1)
check("K5", conv < 0.02 and it_rel < 1e-6, f"grid {conv:.4f} iter {it_rel:.1e}", "<0.02, <1e-6",
      f"Ntheta x2 {vT:.4e}, Nr x1.5 {vR:.4e}, r_in/10 {vI:.4e} vs {base:.4e}")
RES["K5"] = dict(base=base, Nt2=vT, Nr15=vR, rin10=vI, max_rel=conv, iter_rel=it_rel)
# K1c: transverse part of h = mu grad Phi at r = r_M (AQUAL solution, canonical E2)
sK = RA.AxiSolver(LAW, y2, mode="AQUAL", **RES_A)
sK.solve()
tf, amag = sK.transverse_fraction(1.0)
check("K1c", tf >= 0.01, f"|mu F - F_N|/|F - F_N| at r_M = {tf:.4f}", ">=0.01",
      "the action leaves h's divergence-free part nonzero; QUMOND sets it to 0")
RES["K1c"] = dict(transverse_fraction=tf, anomalous_mag=amag)

# ================================================================== R1: D7b recomputed with AQUAL
say("\n[R1] Cassini Q2 of the canonical law with the action's equation (AQUAL), Route A; QUMOND on the same grid;"
    " 'anch' = (AQUAL/QUMOND) x D7b Route M")
R1 = {}
for foot in A0:
    for yt in YT_ROWS:
        law = LAW if yt is None else RA.law_canonical(yt)
        row = {}
        for e in EL:
            yv = y_of(law, foot, e)
            qa, qas, _ = q2_SI(law, yv, A0[foot], AQ)
            qq, _, _ = q2_SI(law, yv, A0[foot], "QUMOND")
            key = "none" if yt is None else ("%g" % yt)
            ref = D7B["grid"][foot][key][e]["Q2_M"] if key in D7B["grid"][foot] else None
            row[e] = dict(y_e=yv, Q2_AQUAL=qa, Q2_AQUAL_Saturn=qas, Q2_QUMOND_A=qq, ratio=qa / qq,
                          Q2_D7b=ref, Q2_AQUAL_anch=(qa / qq * ref if ref else None))
        vals = [row[e]["Q2_AQUAL"] for e in EL]
        anch = [row[e]["Q2_AQUAL_anch"] for e in EL]
        hees = "PASS" if all(H_LO <= v <= H_HI for v in vals) else ("FAIL" if all(not (H_LO <= v <= H_HI) for v in vals) else "E-DEPENDENT")
        hees_a = "PASS" if all(H_LO <= v <= H_HI for v in anch) else ("FAIL" if all(not (H_LO <= v <= H_HI) for v in anch) else "E-DEPENDENT")
        park = "PASS" if all(P_LO <= v <= P_HI for v in vals) else "FAIL"
        R1[f"{foot}|{'none' if yt is None else yt}"] = dict(cells=row, Hees=hees, Hees_anch=hees_a, Park=park,
                                                          over_Hees=[v / H_HI for v in vals])
        say(f"  R {foot:9s} y_t={str(yt):8s} Q2_AQUAL=" + " ".join(f"{v:.3e}" for v in vals)
            + f"  x[{min(vals) / H_HI:.2f},{max(vals) / H_HI:.2f}]  AQUAL/QUMOND=" + ",".join(f"{row[e]['ratio']:.3f}" for e in EL)
            + f"  anch x[{min(anch) / H_HI:.2f},{max(anch) / H_HI:.2f}]  Hees:{hees}/{hees_a}  Park:{park}")
RES["R1"] = R1
allfail = all(v["Hees"] == "FAIL" and v["Hees_anch"] == "FAIL" for v in R1.values())
anypass = any(v["Hees"] == "PASS" for v in R1.values())
ov = [o for v in R1.values() for o in v["over_Hees"]]
r1_out = "D7b's FAIL SURVIVES" if allfail else ("D7b's verdict REVERSES" if anypass else "D7b's verdict becomes E-DEPENDENT")
can = [o for k, v in R1.items() if k.startswith("canonical") for o in v["over_Hees"]]
alt = [o for k, v in R1.items() if k.startswith("alt") for o in v["over_Hees"]]
rat = [c["ratio"] for v in R1.values() for c in v["cells"].values()]
say(f"R1  AQUAL Q2 / Hees 2sigma: canonical {min(can):.2f}-{max(can):.2f}x, alt {min(alt):.2f}-{max(alt):.2f}x; "
    f"AQUAL/QUMOND {min(rat):.3f}-{max(rat):.3f} -> {r1_out}")
RES["R1_outcome"] = dict(outcome=r1_out, canonical_range=[min(can), max(can)], alt_range=[min(alt), max(alt)],
                         ratio_range=[min(rat), max(rat)])

# ================================================================== R3: D7c family under AQUAL
say("\n[R3] D7c family under AQUAL (SPARC verdicts from D7c, unchanged: algebraic RAR fits)")
FAM = {"n=2": RA.Law(RA.w_cap(2.0), RA.omm_cap(2.0), "n=2"), "n=8": RA.Law(RA.w_cap(8.0), RA.omm_cap(8.0), "n=8"),
       "S": RA.Law(RA.w_standard, RA.omm_standard, "S")}
for b in (1.25, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0):
    FAM["beta=%g" % b] = RA.Law(RA.w_beta(b), None, "beta=%g" % b)
R3 = {}
for name, law in FAM.items():
    rec = {}
    for foot in A0:
        qs, rs = [], []
        for e in EL:
            yv = y_of(law, foot, e)
            qa, _, _ = q2_SI(law, yv, A0[foot], AQ)
            qq, _, _ = q2_SI(law, yv, A0[foot], "QUMOND")
            ref = D7C["Q2"][name][foot]["Q2"][e]
            qs.append(qa); rs.append(qa / qq)
            rec.setdefault(foot, {})[e] = dict(Q2_AQUAL=qa, Q2_QUMOND_A=qq, ratio=qa / qq, Q2_D7c=ref, Q2_anch=qa / qq * ref)
        anch = [rec[foot][e]["Q2_anch"] for e in EL]
        rec[foot]["pass"] = all(H_LO <= v <= H_HI for v in qs)
        rec[foot]["pass_anch"] = all(H_LO <= v <= H_HI for v in anch)
        rec[foot]["over_Hees"] = [v / H_HI for v in qs]
    sparc = D7C["joint"][name]["SPARC_both"]
    rec["SPARC_both_D7c"] = sparc
    rec["Q2_both_AQUAL"] = rec["canonical"]["pass"] and rec["alt"]["pass"]
    rec["Q2_both_AQUAL_anch"] = rec["canonical"]["pass_anch"] and rec["alt"]["pass_anch"]
    rec["both"] = sparc and (rec["Q2_both_AQUAL"] or rec["Q2_both_AQUAL_anch"])
    rec["Q2_both_QUMOND_D7c"] = D7C["joint"][name]["Q2_both"]
    R3[name] = rec
    say(f"  {name:9s} SPARC(D7c) {'PASS' if sparc else 'fail'} | AQUAL Q2/Hees canonical "
        + ",".join(f"{v:.2f}" for v in rec["canonical"]["over_Hees"]) + " alt "
        + ",".join(f"{v:.2f}" for v in rec["alt"]["over_Hees"])
        + f" | AQUAL/QUMOND {min(rec[f][e]['ratio'] for f in A0 for e in EL):.3f}-{max(rec[f][e]['ratio'] for f in A0 for e in EL):.3f}"
        + f" | Q2 both: QUMOND {rec['Q2_both_QUMOND_D7c']} -> AQUAL {rec['Q2_both_AQUAL']} | BOTH {rec['both']}")
RES["R3"] = R3
breakers = [k for k, v in R3.items() if v["both"]]
r3_out = "No-go SURVIVES" if not breakers else "No-go BREAKS: " + ",".join(breakers)
# least tension among SPARC passers: the smallest worst-cell over_Hees (both footings)
lt = min(((k, max(max(v["canonical"]["over_Hees"]), max(v["alt"]["over_Hees"]))) for k, v in R3.items() if v["SPARC_both_D7c"]),
         key=lambda t: t[1])
say(f"R3  {r3_out}; least-tense SPARC passer under AQUAL: {lt[0]} worst cell {lt[1]:.2f}x Hees 2sigma")
RES["R3_outcome"] = dict(outcome=r3_out, least_tense=lt)

# ================================================================== Part 2: Route B (3-D) checks + R2
del s_iso, sb, sb2, sK, s_bn
_ = None
gc.collect()
say("\n[Part 2, Route B] 3-D FFT solver checks")
# K6 linear AQUAL EFE
x18 = 1.8
r6 = RB.run_isolated("k6", dict(x=x18, N=192, m=8))
mu_e, L0 = r6["mu_e"], r6["L0"]
CHILD_RSS = [r6["rss"]]
k6 = []
for th, Bm, ana in ((0.0, r6["B"][0], 1.0 / mu_e), (math.pi / 2, r6["B"][1], 1.0 / (mu_e * math.sqrt(1 + L0)))):
    k6.append((th, Bm, ana, abs(Bm / ana - 1)))
m6x = max(t[3] for t in k6)
check("K6", m6x <= 0.02, f"{m6x:.4f}", "<=0.02",
      "FFT linear AQUAL EFE: B_par=%.4f (ana %.4f), B_perp=%.4f (ana %.4f)" % (k6[0][1], k6[0][2], k6[1][1], k6[1][2]))
RES["K6"] = [dict(theta=t, B=b, analytic=a, rel=r) for t, b, a, r in k6]
# K7 single mass, Route B vs Route A, canonical x_e = 1.9, r_M = 1
xe7 = 1.9
PTS = ((0.0, (0.0, 0.0, 1.5)), (math.pi, (0.0, 0.0, -0.5)), (math.pi / 2, (1.0, 0.0, 0.5)))
r7 = RB.run_isolated("k7", dict(N=192, m=8, x_e=xe7, mode=AQ, points=[p for _, p in PTS]))
CHILD_RSS.append(r7["rss"])
y7 = xe7 * xe7 / (1 + xe7)
sA = RA.AxiSolver(LAW, y7, mode=AQ, **RES_A)
sA.solve()
k7 = []
for (th, P), vb in zip(PTS, r7["vals"]):
    dr_, dt_ = sA.field_at(np.array([1.0]), np.array([th]))
    gr, gt = -dr_[0], -dt_[0]                       # physical anomalous field in (r_hat, theta_hat)
    rh = np.array([math.sin(th), 0.0, math.cos(th)])
    thh = np.array([math.cos(th), 0.0, -math.sin(th)])
    vA = gr * rh + gt * thh
    vB = np.array(vb)
    k7.append((th, vA.tolist(), vB.tolist(), float(np.linalg.norm(vB - vA) / np.linalg.norm(vA))))
del sA
gc.collect()
m7x = max(t[3] for t in k7)
check("K7", m7x <= 0.03, f"{m7x:.4f}", "<=0.03", "single mass, |dF_B - dF_A|/|dF_A| at r_M (axis both sides, equator); "
      f"Route B {r7['iters']} it")
RES["K7"] = [dict(theta=t, routeA=a, routeB=b, rel=r) for t, a, b, r in k7]


def ytot(s_kau, a0):
    return G * 2.0 * MSUN / ((s_kau * KAU) ** 2 * a0)


# K8 QUMOND reproduction + convergence
yt20 = ytot(20.0, A0["canonical"])
xq = GEXT["PREREG_primary"] / A0["canonical"]
rq = RB.run_isolated("arel", dict(y_tot=yt20, x_e=xq, theta=0.0, N=192, m=8, mode="QUMOND"))
gq0 = math.sqrt(rq["a"])
d2ref = D2["gamma_table"]["canonical|PREREG_primary|20"]["th0"]
iA = RB.run_isolated("arel", dict(y_tot=yt20, x_e=xq, theta=0.0, N=192, m=8, mode=AQ, extra=dict(tol=1e-9, maxit=300)))
iB = RB.run_isolated("arel", dict(y_tot=yt20, x_e=xq, theta=0.0, N=NB, m=MB, mode=AQ, extra=dict(tol=1e-9, maxit=300)))
aA, aB = iA["a"], iB["a"]
CHILD_RSS += [rq["rss"], iA["rss"], iB["rss"]]
dconv = abs(math.sqrt(aB) - math.sqrt(aA))
itr = max(iA["rel"], iB["rel"])
check("K8", abs(gq0 - d2ref) <= 0.002 and dconv <= 0.005 and itr < 1e-5,
      f"QUMOND {gq0:.4f} vs D2 {d2ref:.4f}; AQUAL 192/8 {math.sqrt(aA):.4f} vs {NB}/{MB} {math.sqrt(aB):.4f}; iter {itr:.1e}",
      "<=0.002, <=0.005, <1e-5", "theta = 0, 20 kAU, PREREG primary, canonical")
RES["K8"] = dict(gamma_QUMOND_192=gq0, D2_ref=d2ref, gamma_AQUAL_192=math.sqrt(aA), gamma_AQUAL_prod=math.sqrt(aB),
                 dconv=dconv, iter_rel=itr)

say("\n[R2] wide binaries, 1+1 Msun, 20 kAU, orientation-averaged (3-pt GL in cos theta), Route B on "
    f"N={NB}, m={MB}")
R2 = {}
D2REF = {(f, k): D2["gamma_table"][f"{f}|{k}|20"]["avg"] for f in A0 for k in GEXT}
for foot in A0:
    for gk, gv in GEXT.items():
        yt = ytot(20.0, A0[foot])
        xe = gv / A0[foot]
        gA, valsA, infA = RB.gamma_v_avg_isolated(yt, xe, NB, MB, AQ, extra=dict(tol=1e-9, maxit=300))
        gQ, valsQ, infQ = RB.gamma_v_avg_isolated(yt, xe, NB, MB, "QUMOND")
        CHILD_RSS += [i["rss"] for i in infA + infQ]
        dd = gA - gQ
        R2[f"{foot}|{gk}"] = dict(x_e=xe, y_tot=yt, gamma_AQUAL=gA, gamma_QUMOND_sameGrid=gQ, delta=dd,
                                  gamma_D2=D2REF[(foot, gk)], gamma_AQUAL_anch=D2REF[(foot, gk)] + dd,
                                  arel_AQUAL=valsA, arel_QUMOND=valsQ, iters=[i["iters"] for i in infA],
                                  iter_rel=max(i["rel"] for i in infA))
        say(f"  {foot:9s} {gk:15s} x_e={xe:.4f}  gamma_v AQUAL {gA:.4f}  QUMOND(same grid) {gQ:.4f}  "
            f"Delta {dd:+.4f}  D2 {D2REF[(foot, gk)]:.4f} -> {D2REF[(foot, gk)] + dd:.4f}  "
            f"(per-orientation a_rel A/Q: " + ",".join(f"{a:.4f}/{b:.4f}" for a, b in zip(valsA, valsQ)) + ")")
RES["R2"] = R2
mxd = max(abs(v["delta"]) for v in R2.values())
r2_out = "gamma_v CHANGES" if mxd > 0.005 else "gamma_v = 1.175/1.210 STANDS"
say(f"R2  max |gamma_AQUAL - gamma_QUMOND| = {mxd:.4f} (threshold 0.005; A24's claim <= 0.019) -> {r2_out}")
RES["R2_outcome"] = dict(outcome=r2_out, max_abs_delta=mxd)

# ================================================================== R4: D7d consistency
d7d_ok = k1b and abs(r3 - 1) <= 0.10
r4 = "D7d CONSISTENT" if d7d_ok else "D7d INCONSISTENT"
say(f"\nR4  D7d's (L),(P) at L*=0 reduce to the same AQUAL equation (K1b {k1b}); BN11 target reproduced by AQUAL "
    f"({r3:.3f}) -> {r4}.  L*->0 reference for D7d Route N (canonical / alt, E0..E3): "
    + "; ".join(f"{f}: " + ",".join(f"{R1[f + '|none']['cells'][e]['Q2_AQUAL']:.3e}" for e in EL) for f in A0))
RES["R4"] = dict(outcome=r4, reference_Q2_AQUAL_Lstar0={f: {e: R1[f + "|none"]["cells"][e]["Q2_AQUAL"] for e in EL} for f in A0})

# ------------------------------------------------------------------ wrap up
npass = sum(c["passed"] for c in CHECKS)
RES["checks"] = CHECKS
RES["checks_pass"], RES["checks_total"] = npass, len(CHECKS)
RES["runtime_s"] = time.time() - T0
RES["max_rss_MB_parent"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
RES["max_rss_MB_child"] = max(CHILD_RSS)
say(f"\nruntime {RES['runtime_s']:.0f} s, peak RSS parent {RES['max_rss_MB_parent']:.0f} MB, 3-D child {RES['max_rss_MB_child']:.0f} MB "
    "(sequential, one child at a time)")
say(f"E2_FIELD_EQUATION COMPLETE: {npass}/{len(CHECKS)} checks PASS.")
open(OUT_TXT, "w").write("\n".join(lines) + "\n")
json.dump(RES, open(OUT_JSON, "w"), indent=1, default=float)
sys.exit(0 if npass == len(CHECKS) else 1)
