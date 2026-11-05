#!/usr/bin/env python3
"""CT12: grade the leaf-global, time-local tie a0(tau)^2 = xi G <T_nn^DE>_leaf inside v3s (FROZEN_CRITERIA.md).
Run: OMP_NUM_THREADS=1 python3 ct12_leaf_tie.py > ct12_leaf_tie.out   (seconds, < 0.3 GB, one thread)
kappa = 1/2 FITTED; not theory closed. Grading only: adopts nothing, reinstates nothing, no particle.
CT12_MUTATE=1 replaces the leaf average by the local value (CT7's C' energy portal): (d2) must then FAIL inside stars."""
import os, json, math, resource, warnings
warnings.filterwarnings('ignore')   # quad subdivision notices; the halo integrals agree to print precision between 1 and 40 sub-intervals
import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq

MUT = os.environ.get("CT12_MUTATE") == "1"
G = 6.6743e-11; C = 2.99792458e8; MPC = 3.0856775814913673e22; MSUN = 1.98847e30
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
KAPPA = 0.5; KAPPA_ALT_TIED = 0.6043                      # FITTED; alt tied value reported beside, ungraded
EPS = KAPPA**2 / (8 * math.pi)
RHO100 = 3 * (1e5 / MPC) ** 2 / (8 * math.pi * G)
# raw inputs, as CT8 (ct8_dust_tie.py:13-20)
OL = 0.666; H = 0.5 * (0.6722 + 0.6856); OB = 0.0224
w_r = 2.4728e-5 * (1 + 0.22711 * 3.046)
X_OVER_B = 4.9                                           # low end of CT3's requirement (fewest dust charge)
A_S = 2.1e-9
H0 = H * 1e5 / MPC
res = {"mutate": MUT}; P = lambda *a: print(*a, flush=True)
P("=" * 100); P("CT12 leaf-global tie" + ("  [MUTATE: local value instead of leaf average]" if MUT else "")); P("=" * 100)

# ---------------- S: symbolic ----------------
s, a2, g, Gs, xi, sig, eb, pn, Dp, V = sp.symbols("s a2 g G xi sigma epsbar phi_n Dphi V", positive=True)
f = s - sp.log(1 + s); fp = sp.diff(f, s)
h = sp.simplify(2 * f - s * fp)
hp = sp.simplify(sp.diff(h, s)); hpp = sp.simplify(sp.diff(h, s, 2))
P(f"S1 h(s) = 2f - s f' = {h};  h' = {sp.factor(hp)};  h'' = {sp.factor(hpp)}  (> 0: convex, Jensen <h> >= h(<x>))")
P(f"   small s: {sp.series(h, s, 0, 5).removeO()};  large s: h - (s + 1 - 2 ln s) -> {sp.limit(h - (s + 1 - 2*sp.log(s)), s, sp.oo)}")
LJ = a2 / (4 * sp.pi * Gs) * f.subs(s, g / sp.sqrt(a2))
dLJ = sp.diff(LJ, a2)
chk = sp.simplify(dLJ - h.subs(s, g / sp.sqrt(a2)) / (8 * sp.pi * Gs))
P(f"S2 dL_J/d(a0^2) - h/(8 pi G) = {chk}   (a0-charge; with a0^2 = xi G sigma: dL_J/dsigma = xi h/(8 pi) = eps h)")
assert chk == 0
# lambda equation: vary sigma(tau) -> lambda = -<dL_J/dsigma> = -eps<h> = -epsbar
lam = -eb
Lphi = pn**2 / 2 - Dp**2 / 2 - V
Tnn = pn**2 / 2 + Dp**2 / 2 + V
Ltot = sp.expand(Lphi + lam * (sig - Tnn))
ck = sp.simplify(sp.diff(Ltot, pn, 2)); cg = sp.simplify(-sp.diff(Ltot, Dp, 2)); cv = sp.simplify(-sp.diff(Ltot, V))
P(f"S3 DE quadratic action with the tie: kinetic coeff {ck}, gradient coeff {cg}, potential coeff {cv}; c_s^2 = {sp.simplify(cg/ck)}")
P("   -> ghost-free for epsbar > -1 (always: epsbar >= 0); gradient instability iff epsbar > 1, i.e. <h>_leaf > 8 pi/kappa^2")
P("S4 DOF: sigma(tau), lambda(tau) enter without derivatives; p_sigma ~ 0, p_lambda ~ 0 (one pair per leaf);")
P("   the leaf equations sigma = <T_nn>, lambda = -eps<h> are second class with them: 0 local, 0 global DOF. Total 3 (v3s) + 1 (phi) = 4.")
P("S5 FRW: Y = 0 so h(0) = 0, epsbar = 0; <T_nn>_leaf = phi_dot^2/2 + V = rho_phi c^2 exactly (kinetic included).")
res["symbolic"] = {"h": str(h), "h_pp": str(sp.factor(hpp)), "dLJ_check": 0, "coeffs": [str(ck), str(cg), str(cv)]}

hn = sp.lambdify(s, h, "math")
def hnum(x):
    if x < 1e-4: return x**3 / 3 - x**4 / 2
    return hn(x)
thr = 8 * math.pi / KAPPA**2; thr_alt = 8 * math.pi / KAPPA_ALT_TIED**2
xc = brentq(lambda x: hnum(x) - thr, 1, 1e4); xc_alt = brentq(lambda x: hnum(x) - thr_alt, 1, 1e4)
P(f"   threshold <h> = 8 pi/kappa^2 = {thr:.2f} (h = thr at x = {xc:.1f}); at alt tied kappa 0.6043: {thr_alt:.2f} (x = {xc_alt:.1f}, ungraded)")
res["threshold"] = {"h": thr, "x": xc, "h_alt_tied": thr_alt, "x_alt_tied": xc_alt}

# ---------------- G0 (c): CT5's band ----------------
P("\nG0(c) static coefficients with a0 leaf-uniform (no slaving)")
ok_c = True
for fo, a0 in A0.items():
    xg = np.logspace(-3, math.log10(1e-8 / a0), 400)
    MT, ML = 1 + xg, (1 + xg) ** 2
    ok = MT.min() >= 1 and ML.min() >= 1; ok_c &= ok
    P(f"   {fo}: x in [1e-3, {xg[-1]:.1f}], min M_T {MT.min():.4f}, min M_L {ML.min():.4f}  -> {'ok' if ok else 'FAIL'}")
RH = C / H0
vfrac = (1.0 * MPC / RH) ** 3
dln_a0 = 0.5 * vfrac
P(f"   finite-leaf response: 1 Mpc ball with delta T_nn/rho_DE = 1 in a Hubble ball (c/H0 = {RH/MPC:.0f} Mpc): |d ln a0| <= {dln_a0:.2e} ({dln_a0/math.log(10):.2e} dex)")
P(f"   local slaving d ln a0/d ln g = 0 at every point (sigma depends on leaf integrals of T_DE only) -> CT5's M_L < 1 band absent")
P(f"G0(c): {'PASS' if ok_c else 'FAIL'}")
res["G0c"] = {"pass": bool(ok_c), "dln_a0_finite_leaf": dln_a0}

# ---------------- G0 (d2): today ----------------
P("\nG0(d2) leaf average of h today (upper bounds)")
def maxwell_mean_h(sig_x):
    s1 = sig_x / math.sqrt(3)
    pdf = lambda x: 4 * math.pi * x**2 * math.exp(-x**2 / (2 * s1**2)) / ((2 * math.pi) ** 1.5 * s1**3)
    return quad(lambda x: hnum(x) * pdf(x), 0, 12 * s1, limit=200)[0]
rho_b = OB * RHO100
d2 = {}
ok_d2 = True
for fo, a0 in A0.items():
    sg = {"canonical": 0.0125, "alt": 0.0104}[fo]
    hd = maxwell_mean_h(sg)
    rows = {}
    for Ms in [1, 1e9, 1e10, 6e10, 1e12, 1e14, 1e15]:
        M = Ms * MSUN; n = rho_b / M; rmax = 0.5 * n ** (-1 / 3); rM = math.sqrt(G * M / a0)
        def xr(r):
            y = G * M / (r**2 * a0); return 0.5 * (y + math.sqrt(y * y + 4 * y))
        if MUT:   # local value: the largest h anywhere in the system (C' reading), surface-of-star proxy r = 1e-6 rM
            rows[Ms] = hnum(xr(1e-6 * rM)); continue
        itg = lambda lr: hnum(xr(math.exp(lr))) * 4 * math.pi * math.exp(3 * lr)
        edges = np.linspace(math.log(1e-8 * rM), math.log(rmax), 41)
        I = sum(quad(itg, edges[i], edges[i + 1], limit=200)[0] for i in range(40))
        rows[Ms] = n * I
    hmax = max(rows.values()) + (0 if MUT else hd)
    eb_today = EPS * hmax
    ok = eb_today < 1; ok_d2 &= ok
    P(f"   {fo}: diffuse <h> = {hd:.2e} (sigma_g0 {sg} a0); point-mass classes " + ", ".join(f"{k:.0e}: {v:.2e}" for k, v in rows.items()))
    P(f"      epsbar_today <= {eb_today:.2e}  (margin {1/eb_today:.1e})  -> {'ok' if ok else 'FAIL'}")
    d2[fo] = {"diffuse": hd, "classes": rows, "epsbar_max": eb_today}
P(f"G0(d2): {'PASS' if ok_d2 else 'FAIL'}")
res["G0d2"] = {"pass": bool(ok_d2), **d2}

# ---------------- G0 (d3): earlier leaves to BBN ----------------
P("\nG0(d3) earlier leaves, v3s's own cosmology (khronon charge = the dust; hold flux capped so x >= g_lin/a0)")
w_x = X_OVER_B * OB; w_m = OB + w_x
E = lambda z: math.sqrt(w_r / H**2 * (1 + z)**4 + w_m / H**2 * (1 + z)**3 + OL)
Phi = (2 / 3) * math.sqrt(A_S); delta = 2 * Phi
def g_lin(z):
    rho_t = w_x * RHO100 * (1 + z)**3
    return 4 * math.pi * G * rho_t * delta * C / (H0 * E(z))
d3 = {}; ok_d3 = True
zs = np.logspace(0, math.log10(4e8), 2000)
for fo, a0 in A0.items():
    out = {}
    for lab, fac in [("x10", 10.0), ("central", 1.0), ("div10", 0.1)]:
        xl = np.array([fac * g_lin(z) / a0 for z in zs])
        xmean = math.sqrt(8 / (3 * math.pi)) * xl
        ebz = np.array([EPS * hnum(x) for x in xmean])
        above = np.where(ebz >= 1)[0]
        zc = float(zs[above[0]]) if len(above) else None
        zcap = float(zs[np.where(xl >= 1)[0][0]]) if (xl >= 1).any() else None
        pick = {zz: float(EPS * hnum(math.sqrt(8 / (3 * math.pi)) * fac * g_lin(zz) / a0)) for zz in [1100, 1e4, 1e5, 4e8]}
        out[lab] = {"z_cross_epsbar_1": zc, "z_rms_glin_eq_a0": zcap, "epsbar_at": pick}
        P(f"   {fo} {lab:7s}: epsbar = 1 first at z = {zc:.3g}; rms g_lin = a0 (hold-flux cap) at z = {zcap:.3g}; epsbar at z 1100/1e4/1e5/4e8 = "
          + " / ".join(f"{v:.3g}" for v in pick.values()))
    # charge share the khronon may carry for epsbar < 1 up to BBN at the central bracket
    xneed = xc / math.sqrt(8 / (3 * math.pi))
    share = xneed / (g_lin(4e8) / a0)
    out["max_khronon_charge_share_to_BBN"] = share
    P(f"   {fo}: to keep epsbar < 1 through BBN (central) the khronon may carry at most {share:.1e} of the dust's charge perturbation")
    ok = out["div10"]["z_cross_epsbar_1"] is None; ok_d3 &= ok
    d3[fo] = out
P(f"G0(d3): {'PASS' if ok_d3 else 'FAIL (fails even at the /10 end of the bracket, before BBN)'}")
res["G0d3"] = {"pass": bool(ok_d3), **d3}
res["G0"] = "PASS" if (ok_c and ok_d2 and ok_d3) else "FAIL"
P(f"\nG0 VERDICT: {res['G0']}  (W4b inherited UNDECIDED, CT2_REPORT.md:7)")

# ---------------- UNGRADED READINGS G1-G3 ----------------
P("\nUNGRADED READINGS (candidate stops at G0 if it failed)")
gmax = 0.0
for fo, a0 in A0.items():
    gb = np.logspace(-12, -8, 400)
    law = lambda a: 0.5 * (gb + np.sqrt(gb**2 + 4 * gb * a))
    dev = np.max(np.abs(np.log10(law(a0 * math.exp(dln_a0))) - np.log10(law(a0))))
    gmax = max(gmax, dev)
    P(f"   G1 {fo}: law S unchanged (a0 leaf-uniform); max deviation with the finite-leaf shift {dev:.2e} dex")
lapse = 1e-4 * vfrac
P(f"   G2: environment spread <= {(dln_a0 + lapse)/math.log(10):.2e} dex (local DE perturbation + lapse weighting), both footings")
def rho_cpl(z, w0, wa):
    a = 1 / (1 + z); return a ** (-3 * (1 + w0 + wa)) * math.exp(-3 * wa * (1 - a))
g3 = {}
for nm, (w0, wa) in {"B2": (-0.9, -0.1), "B3": (-0.95, 0.35)}.items():
    zz = [0, 1, 1.5, 2.33]; lr = np.log([rho_cpl(z, w0, wa) for z in zz])
    corr = 1e-4 * np.array([1, -1, 1, -1])            # worst alternating O(epsbar) + frame (1+w)v^2 corrections
    la = 0.5 * (lr + corr)
    slope = np.polyfit(lr, la, 1)[0]; gt = np.max(np.abs(la - 0.5 * lr)) / math.log(10)
    g3[nm] = {"dlnrho": float(lr.max() - lr.min()), "slope_worst": float(slope), "GT_dex": float(gt)}
    P(f"   G3 {nm}: ln rho_DE range {lr.max()-lr.min():.3f}; slope with worst 1e-4 corrections {slope:.4f}; tracking {gt:.1e} dex")
P("   G3 kappa: a0^2 = xi G <T_nn>, so kappa^2 = xi for every xi > 0 (rename test passes): a TRADE, not derived")
res["readings"] = {"G1_dev_dex": gmax, "G2_spread_dex": (dln_a0 + lapse) / math.log(10), "G3": g3}
res["rss_GB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
P(f"\npeak RSS {res['rss_GB']:.2f} GB")
json.dump(res, open("ct12_results" + ("_MUTATE" if MUT else "") + ".json", "w"), indent=1, default=str)
