"""VR1: vacuum-response identities for kappa (criteria FROZEN_CRITERIA.md, committed alone first).

Run:  python3 vr1.py            -> vr1.json / vr1.out
      MUTATE=1 python3 vr1.py   -> vr1_MUTATE.json / vr1_MUTATE.out  (each candidate's declared mutation)
sympy for the algebra; mpmath only for transcendental roots. Adopts nothing.
kappa = 1/2 FITTED; not theory closed.
"""
import json, os, sys
import sympy as sp
import mpmath as mp

MUT = os.environ.get("MUTATE", "0") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
TAG = "vr1_MUTATE" if MUT else "vr1"
out_lines = []


def say(*a):
    s = " ".join(str(x) for x in a)
    out_lines.append(s)
    print(s)


G, c, rho, a0, kap, xi, H, Lam = sp.symbols("G c rho a0 kappa xi H Lambda", positive=True)
pi = sp.pi
tie = sp.Eq(a0, kap * c * sp.sqrt(G * rho))           # Framework.tie (positive root)
H_L = sp.sqrt(8 * pi * G * rho / 3)                     # Framework.friedmann
Lam_v = 8 * pi * G * rho / c**2                         # Framework.einstein
a0_of_k = kap * c * sp.sqrt(G * rho)
ell = c / sp.sqrt(G * rho)                              # KF1 length


def kappa_from(eq_in_a0):
    """substitute the tie and solve for kappa > 0"""
    e = sp.simplify(eq_in_a0.subs(a0, a0_of_k))
    sols = [s for s in sp.solve(e, kap) if s.is_positive]
    return [sp.nsimplify(sp.simplify(s)) for s in sols]


def in_window(k):
    k2 = float(k) ** 2
    return (0.2280**2 <= k2 <= 0.6064**2) and (0.1886**2 <= k2 * 137 / 200 <= 0.5018**2)


res = {"mutate": MUT}

# ---------------- section 4: kinematic input (R) ----------------
t, x, y, z = sp.symbols("t x y z", real=True)
N = sp.Function("N", positive=True)(x, y, z)
s2 = sp.symbols("s2", positive=True)
coords = [t, x, y, z]
g = sp.diag(-N**2 * c**2, 1, 1, 1)
ginv = g.inv()
Gam = [[[sp.simplify(sum(ginv[m, l] * (sp.diff(g[l, n], coords[r]) + sp.diff(g[l, r], coords[n])
                                         - sp.diff(g[n, r], coords[l])) for l in range(4)) / 2)
         for r in range(4)] for n in range(4)] for m in range(4)]
u_up = [1 / N, 0, 0, 0]                                   # static khronon observer, u.u = -c^2
acc = [sp.simplify(sum(Gam[m][n][r] * u_up[n] * u_up[r] for n in range(4) for r in range(4))) for m in range(4)]
X = s2 / (2 * N**2)                                       # AC2q unitary gauge
fac = 1 if MUT else 2   # mutation of V1: a scalar with X ~ N^-1 (factor 1)
X_used = s2 / (2 * N**fac)
R_resid = [sp.simplify(sp.diff(sp.log(X_used), coords[i]) + fac * acc[i] / c**2) for i in (1, 2, 3)]
R_true = [sp.simplify(sp.diff(sp.log(X), coords[i]) + 2 * acc[i] / c**2) for i in (1, 2, 3)]
say("== (R) kinematics: A^i =", acc[1:], "; residual of grad ln X + 2A/c^2 =", R_true)
res["R_acc_x"] = str(acc[1])
res["R_residual_zero"] = all(r == 0 for r in R_true)
say("   response length L_v(A) = c^2/(%d |A|)" % fac)

# J-sector static energy density from (c^3/16 pi G) sqrt(-g)[-2 J]; per volume (divide the c^3 by c dt -> c^4)
u_ = sp.symbols("u", positive=True)
a_geo = a0 / c**2
J = Lam - 2 * a_geo**2 * (u_ - sp.log(1 + u_))
eps_J = sp.simplify(c**4 / (16 * pi * G) * 2 * (Lam - J))   # = |.|, since u - ln(1+u) >= 0 for u >= 0
h = lambda uu: uu - sp.log(1 + uu)
say("== |eps_J(u)| =", eps_J, " (expected a0^2 (u - ln(1+u))/(4 pi G))")
res["eps_J_check"] = sp.simplify(eps_J - a0**2 * h(u_) / (4 * pi * G)) == 0

# ---------------- KA controls ----------------
say("\n== KA controls (must read RESTATEMENT)")
ka1 = kappa_from(sp.Eq(a0, c**2 / (2 * xi * ell)))
say("KA-1 a0 = c^2/(2 xi l):  kappa =", ka1, "; at xi = 1 ->", [k.subs(xi, 1) for k in ka1])
res["KA1"] = {"kappa": str(ka1), "label": "RESTATEMENT" if [k.subs(xi, 1) for k in ka1] == [sp.Rational(1, 2)] else "BROKEN"}
# KA-2: SIS hydrostatics in Phi = v_f^2 ln r: sigma^2 dln rho/dln r = -v_f^2, rho ~ r^-2
sig2, vf2, r, M = sp.symbols("sigma2 vf2 r M", positive=True)
ratio = sp.solve(sp.Eq(sig2 * (-2), -vf2), sig2)[0] / vf2
ka2 = {}
for kv in (sp.Rational(1, 2), sp.Rational(1, 3)):
    a0v = kv * c * sp.sqrt(G * rho)
    ka2[str(kv)] = str(ratio.subs(vf2, sp.sqrt(G * M * a0v)))
say("KA-2 SIS sigma^2/v_f^2 at kappa 1/2, 1/3:", ka2)
res["KA2"] = {"ratio": ka2, "label": "RESTATEMENT" if len(set(ka2.values())) == 1 else "BROKEN"}
ka3 = kappa_from(sp.Eq(Lam_v * pi * (c**2 / a0)**2, 32 * pi**2))
say("KA-3 p32: kappa =", ka3)
res["KA3"] = {"kappa": str(ka3), "label": "RESTATEMENT" if ka3 == [sp.Rational(1, 2)] else "BROKEN"}
ka_ok = all(res[k]["label"] == "RESTATEMENT" for k in ("KA1", "KA2", "KA3"))
say("KA all RESTATEMENT:", ka_ok)

# ---------------- V1 response-length identity ----------------
say("\n== V1: c^2/(%d a0) = l_v" % fac)
opts = {
    "a_deSitter_c_over_H": c / H_L,
    "b_Poisson_c_over_sqrt4piGrho": c / sp.sqrt(4 * pi * G * rho),
    "c_c_tff": c * sp.sqrt(3 * pi / (32 * G * rho)),
    "d_Jeans_c_sqrt_pi_over_Grho": c * sp.sqrt(pi / (G * rho)),
    "e_inv_sqrt_Lambda": 1 / sp.sqrt(Lam_v),
    "f_2pi_c_over_H": 2 * pi * c / H_L,
}
V1 = {}
for k, lv in opts.items():
    ks = kappa_from(sp.Eq(c**2 / (fac * a0), lv))
    kv = ks[0]
    V1[k] = {"kappa": str(kv), "kappa2": str(sp.nsimplify(kv**2)), "float": float(kv),
             "is_half": sp.simplify(kv - sp.Rational(1, 2)) == 0, "in_window": in_window(kv)}
    say("  %-32s kappa = %-28s = %.4f  half=%s window=%s" % (k, kv, float(kv), V1[k]["is_half"], V1[k]["in_window"]))
res["V1"] = V1
res["V1_xi_map"] = str(sp.simplify((c**2 / (2 * a0)).subs(a0, a0_of_k) / ell))  # = xi
say("  xi = L_v(a0)/l =", res["V1_xi_map"], " -> kappa = 1/2 iff l_v = c/sqrt(G rho) (KA-1's posit)")

# ---------------- V2 vacuum cancellation ----------------
say("\n== V2: J(Y*) = 0, u* = A*/a0")
f_opts = {"a_cH": 1, "b_cH_over_2pi": 1 / (2 * mp.pi), "c_2cH": 2}
if MUT:
    f_opts = {"a_cH_x2": 2, "b_x2": 2 / (2 * mp.pi), "c_x2": 4}
V2 = {}
for k, f in f_opts.items():
    # Lambda = 2 a_geo^2 h(u*) -> 8 pi = 2 kappa^2 h(u*),  u* = f sqrt(8pi/3)/kappa
    F = lambda K: K**2 * (f * mp.sqrt(8 * mp.pi / 3) / K - mp.log(1 + f * mp.sqrt(8 * mp.pi / 3) / K)) - 4 * mp.pi
    grid = [10 ** (e / 50) for e in range(-200, 401)]
    vals = [F(K) for K in grid]
    roots = []
    for i in range(len(grid) - 1):
        if vals[i] * vals[i + 1] < 0:
            roots.append(float(mp.findroot(F, (grid[i], grid[i + 1]), solver="bisect")))
    sup = float(4 * mp.pi * f**2 / 3)
    V2[k] = {"f": float(f), "roots": roots, "sup_bound_kappa2h": sup, "four_pi": float(4 * mp.pi),
             "max_on_grid_plus_4pi": float(max(vals) + 4 * mp.pi)}
    say("  %-14s f=%.4f roots=%s  analytic sup kappa^2 h = 4 pi f^2/3 = %.3f vs 4 pi = %.3f" % (k, float(f), roots, sup, 4 * mp.pi))
res["V2"] = V2

# ---------------- V3 switch equipartition ----------------
u_eval = 2 if MUT else 1
say("\n== V3: |eps_J(u=%d)| = r rho_DE c^2" % u_eval)
V3 = {}
for rv in (sp.Rational(1, 2), sp.Integer(1)):
    ks = kappa_from(sp.Eq(a0**2 * h(sp.Integer(u_eval)) / (4 * pi * G), rv * rho * c**2))
    kv = ks[0]
    V3[str(rv)] = {"kappa": str(kv), "float": float(kv), "is_half": False if sp.simplify(kv - sp.Rational(1, 2)) != 0 else True,
                   "in_window": in_window(kv)}
    say("  r=%s kappa = %s = %.4f window=%s" % (rv, kv, float(kv), in_window(kv)))
res["V3"] = V3

# ---------------- V4 blend switch ----------------
gfac = sp.Rational(1, 4) if MUT else 1
say("\n== V4: rho_ph(g_N = %s a0) = rho_DE (point mass, law S)" % gfac)
gN = G * M / r**2
gS = (gN + sp.sqrt(gN**2 + 4 * gN * a0)) / 2
rho_ph = sp.diff(r**2 * (gS - gN), r) / (4 * pi * G * r**2)
rM = sp.sqrt(G * M / (gfac * a0))
rho_ph_M = sp.simplify(rho_ph.subs(r, rM))
k2_V4 = sp.simplify(a0**2 / (G * c**2 * rho_ph_M))     # rho_DE = a0^2/(kappa^2 G c^2) by the tie
dM = sp.simplify(sp.diff(k2_V4, M))
say("  rho_ph at transition =", rho_ph_M)
say("  kappa^2 =", k2_V4, " ; d kappa^2/dM =", dM)
res["V4"] = {"rho_ph": str(rho_ph_M), "kappa2": str(k2_V4), "M_dependent": dM != 0}

# ---------------- labels ----------------
lab = {}
lab["V1"] = "RESTATEMENT/DERIVES OTHER" if not any(v["is_half"] for v in V1.values()) else "CONDITIONAL"
lab["V2"] = "NO IDENTITY" if not V2[list(V2)[0]]["roots"] else "DERIVES OTHER"
lab["V3"] = "DERIVES OTHER" if not any(v["is_half"] for v in V3.values()) else "CONDITIONAL"
lab["V4"] = "NO IDENTITY" if res["V4"]["M_dependent"] else "?"
res["labels_raw"] = lab
say("\nraw labels:", lab)

# ---------------- cold component readout (section 6), V1's response ----------------
# (R) integrated: X ~ N^-2 ~ 1 - 2 Phi/c^2; clock bound X <= rho_DE c^2; active density of a kinetic fluid rho+3p = 4X
OmL = 0.685
cases = {"disc": (1e-6, None), "XCOP_cluster_r500": (1e-5, 500.0), "recombination": (1e-5, None)}
resp_cluster = 4 * OmL * 1e-5                       # in units of rho_crit,0
need_cluster = 500.0 * 4.0 / 5.0                    # f ~ 4 of baryons, dominant share of 500 rho_crit inside r500
need_cosmic_ratio_z1100 = 5.41                      # in units of rho_b(z)
resp_cosmic = 4 * OmL / (0.049 * 1101**3) * 1e-5    # rho_DE response / rho_b at z 1100
cold = {"cluster_response_over_need": resp_cluster / need_cluster,
        "cosmic_response_over_need": resp_cosmic / need_cosmic_ratio_z1100,
        "disc_response_rho_crit": 4 * OmL * 1e-6, "host_tracking": True,
        "verdict": "SAYS NOTHING"}
say("cold: cluster response/need = %.2e ; cosmic = %.2e ; host-tracking (prop. to Phi)" %
    (cold["cluster_response_over_need"], cold["cosmic_response_over_need"]))
res["cold"] = cold
res["footer"] = "kappa = 1/2 FITTED; not theory closed."
say(res["footer"])

with open(os.path.join(HERE, TAG + ".json"), "w") as fh:
    json.dump(res, fh, indent=1, default=str)
with open(os.path.join(HERE, TAG + ".out"), "w") as fh:
    fh.write("\n".join(out_lines) + "\n")
