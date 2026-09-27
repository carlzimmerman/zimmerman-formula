#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
MS5 -- THE REGION CAP AS AN ACTION TERM: WHICH LOCAL INVARIANT REPRODUCES MS3's CAP, AND DOES THE CAPPED GATE KEEP
RECIPROCITY?

WHY.  MS3 (2a5def6d9) passed cosmic shear on L363's resolution-free halo model with every MOND region stopped at
r_cap = 1.75 Mpc (z = 0.5), a velocity scale v_cap = r_cap H sqrt(x) = 325 km/s, and L388's retention.  That cap was a
hard radius cut.  To put it in the action the gate must read a local scalar of the MOND-sector field Phi_X = Phi - v.
This lane's README (step 4) proposed v_loc^2 = |grad Phi|^2 / lap Phi, and L395 implements the cap in that form
(XR6: the switch is on where 4 pi G rho_ms >= max(x_c H^2, sqrt(x_c) H |g| / v_cap)).  In deep MOND

    lap Phi_X / |grad Phi_X| = (1 + beta_b/2) / r,     beta_b = dln M_b(<r) / dln r,

which is 1/r only where the baryons have stopped rising.  Wherever the baryons still rise at the cap (clusters, whose gas
keeps tracing the host past r200), that form puts the edge (1 + beta_b/2) further out than MS3 scored.  The mean
curvature of the MOND field's equipotentials,

    kappa_X = (1/2) div( grad Phi_X / |grad Phi_X| ) = (lap Phi_X - n.(grad grad Phi_X).n) / (2 |grad Phi_X|),

is exactly 1/r for EVERY spherical profile, so the gate U_cap = C min(lap Phi_X, v_cap^2 kappa_X^2) stops every spherical
region at exactly l_cap(z) = v_cap / (H(z) sqrt(x_c(z))): MS3's hard cap, for any baryon profile.

CHECKS
  A1 [sympy, MS1's chassis = CV1's Lagrangian, loaded unedited] the gate varied on a GENERIC reading
     U = C F(Phi_X', Phi_X'') (any function of the MOND-sector field's first and second derivatives, which covers both cap
     forms and the uncapped door): the gate's term enters the Phi and v equations with opposite signs (zero residual), the
     u, lam, w, Psi equations are CV1's, and the dark component's potential is exactly Newtonian, V_d - u_N = 0.
  A2 [sympy, 3-D] for an arbitrary spherical potential phi(r) with phi' > 0, kappa = 1/r identically; for deep MOND with
     phi' = sqrt(G a0 M(r))/r, lap Phi / |grad Phi| = (1 + r M'/(2M))/r.
  N1 (numbers, both footings) the cap edge in L395's form (lap Phi_X / |grad Phi_X| >= 1/l_cap) on spherical hosts at
     z = 0.5, for three baryon readings -- MS3's point mass (GP0's observed bound baryons), the same mass tracing the
     host's NFW and truncated at r200, and tracing it past r200 (the infall region) -- as a ratio to l_cap.  Also the
     XR6 comparison: l_cap(z) and the L395-form edge of a Coma-like host at z = 0.023.
  S1 PRE-DECLARED (written before the run): on MS3's machinery (L363's halo model, door convention, L388's retention,
     both footings) (i) the kappa form reproduces MS3's K1 row at 1.75 Mpc exactly and passes (worst R <= 1.2); (ii) the
     L395 form on baryons that keep tracing the NFW past r200 FAILS (worst R > 1.2 on at least one footing).  Only the
     edge moves; the phantom transform is MS3's (the point-mass phantom), so (ii) understates that reading's phantom.
  P1 [sympy] the fourth-order part of the gate's linearisation, Q(k) = d^2/dt^2 [W(U) B] along grad grad Phi -> + t k k:
       uncapped door            Q = C^2 W'' B k^4
       kappa form (capped)      Q = (C v_cap^2 k_perp^4 / |g|^2) B [W'' U + W'/2]     (k_perp: k across grad Phi_X)
       L395 form (capped)       Q = (4 C v_cap^2 k^4 / |g|^2) B [W'' U + W'/2]
     and (numbers) where in DE9's smooth gate the bracket changes sign (w = 0.25, 0.5).
MUTATE=1 (i) adds the carrier's density to the generic reading (A1 must FAIL) and (ii) scores L395's form on extended
baryons in place of the kappa form (S1 must FAIL); rc = 1.

SCOPE.  A1 is the one-dimensional reduction MS1 uses (the identity it checks, dF[Phi - v]/dPhi = -dF[Phi - v]/dv, holds
in any dimension).  N1/S1 are spherical and use MS3's halo model; the kappa form's pass is MS3's, with MS3's caveats (the
halo model over-counts phantoms in crowded places).  P1 is the non-relativistic principal symbol only: whether either
bracket is admissible is DE7's reduced operator's call (its repair term), not this lane's.  v_cap stays a declared
constant.

Run from the repository root:  python3 real_research/mond_sector_gate_2026/MS5_cap_as_action_term.py
"""
import os, sys, json, math, time, io, contextlib
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "MS5_cap_as_action_term"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "MS5", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the carrier's density enters the reading, and L395's form replaces kappa; A1 and S1 must FAIL ***")

# ---------------------------------------------------------------------------------- MS1's chassis, loaded unedited
p1 = os.path.join(HERE, "MS1_gate_variation_reciprocity.py")
M1 = {"__name__": "ms1", "__file__": p1}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(p1).read().split("# ============================================================================================ A1 control")[0]
         .replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), M1)
x, C, G_, m2 = M1["x"], M1["C"], M1["G_"], M1["m2"]
Phi, u, v, lam, w, Psi, rb, rd = (M1[k_] for k_ in ("Phi", "u", "v", "lam", "w", "Psi", "rb", "rd"))
W, d_, EPG, lagrangian, EL_of = M1["W"], M1["d_"], M1["EPG"], M1["lagrangian"], M1["EL_of"]

# ============================================================================================ A1 reciprocity, generic reading
banner("A1  THE GATE VARIED ON A GENERIC MOND-SECTOR READING U = C F(Phi_X', Phi_X''): reciprocity")
F = sp.Function("F")
PX = Phi - v
U = C * F(d_(PX), d_(PX, 2)) + (C * rd if MUTATE else 0)
f = W(U)
L = lagrangian(f, m2 * (1 - f))
EL = EL_of(L)
gate_Phi = sp.expand(EL["Phi"] - (2 * d_(u, 2) - EPG * (rb + rd)))              # the gate's term in the Phi equation
res_v = sp.simplify(sp.expand(EL["v"] - (d_(lam, 2) + d_(f * Psi, 2)) + gate_Phi))   # v's gate term must be -gate_Phi
res_rest = {
    "u": sp.simplify(sp.expand(EL["u"] - (2 * d_(Phi, 2) - 2 * d_(u, 2) - d_(f * Psi, 2)))),
    "lam": sp.simplify(sp.expand(EL["lam"] - (d_(v, 2) - 4 * sp.pi * G_ * (rd - M1["rdbar"])))),
    "Psi": sp.simplify(sp.expand(EL["Psi"] - (d_(w, 2) - m2 * (1 - f) * w - f * (d_(u, 2) - d_(v, 2))))),
    "w": sp.simplify(sp.expand(EL["w"] - (d_(Psi, 2) - m2 * (1 - f) * Psi - 2 * d_(f * M1["qcp"](M1["s_w"]) * M1["wp"])
                                          - 2 * M1["sig"] * m2 * (1 - f) * w))),
}
P(f"    gate term in the Phi equation is non-zero: {gate_Phi != 0};  v equation's gate term + Phi's = {res_v}")
P("    other equations against CV1's: " + ", ".join(f"{k_} {v_}" for k_, v_ in res_rest.items()))
# the integrated solution (MS1 A3's convention): Gam'' = gate_Phi, so u = u_N - Gam/2, lam = -f Psi + Gam, Phi = u + f Psi/2
uN, Gam = sp.Function("u_N")(x), sp.Function("Gamma")(x)
Wps, fsym, rds = sp.symbols("Wp fval rds")
Vd = -sp.diff(L.subs(rd, rds), rds)
Vd = Vd.replace(lambda e: isinstance(e, sp.Subs), lambda e: Wps)
Vd = Vd.replace(lambda e: isinstance(e, sp.Function) and e.func == W, lambda e: fsym)
Vd = sp.expand(Vd.subs(rds, rd).subs({Phi: uN - Gam / 2 + fsym * Psi / 2, lam: -fsym * Psi + Gam}))
A1_leak = sp.simplify(Vd - uN)
P(f"    V_d - u_N = {A1_leak}")
OUT["numbers"]["A1"] = dict(v_residual=str(res_v), others={k_: str(v_) for k_, v_ in res_rest.items()}, leak=str(A1_leak))
check("A1 RECIPROCITY FOR ANY MOND-SECTOR READING: with U = C F(Phi_X', Phi_X'') varied, the gate's term enters the Phi "
      "and v equations with opposite signs, the other four equations are CV1's, and V_d = u_N exactly",
      f"v + Phi gate terms {res_v}; others {list(res_rest.values())}; V_d - u_N = {A1_leak}",
      res_v == 0 and all(v_ == 0 for v_ in res_rest.values()) and A1_leak == 0,
      "any cap built from the MOND-sector field alone (either form below) keeps the carrier exactly Newtonian")

# ============================================================================================ A2 the two invariants, spherical
banner("A2  THE TWO LOCAL INVARIANTS ON AN ARBITRARY SPHERICAL PROFILE [sympy, 3-D]")
X, Y, Z = sp.symbols("X Y Z", real=True)
rr = sp.sqrt(X ** 2 + Y ** 2 + Z ** 2)
rs_ = sp.Symbol("r", positive=True)
phi = sp.Function("phi")
Phs = phi(rr)
grad = [sp.diff(Phs, q) for q in (X, Y, Z)]
norm = sp.sqrt(sum(gq ** 2 for gq in grad))
kap = sp.Rational(1, 2) * sum(sp.diff(gq / norm, q) for gq, q in zip(grad, (X, Y, Z)))
at_pt = {X: rs_, Y: 0, Z: 0}                                              # spherical: evaluate on the x axis
dphi = sp.Symbol("dphi", positive=True)
kap_r = sp.simplify(kap.subs(at_pt).doit().subs(sp.Subs(sp.Derivative(phi(X), X), X, rs_), dphi)
                    .replace(lambda e: isinstance(e, sp.Abs), lambda e: e.args[0]))
kap_r = sp.simplify(sp.powsimp(sp.powdenest(kap_r, force=True), force=True))
P(f"    kappa = (1/2) div(grad Phi/|grad Phi|) at radius r, phi arbitrary with phi' > 0:  {kap_r}")
Mf = sp.Function("M")
Ga = sp.Symbol("G a0", positive=True)
g_dm = sp.sqrt(Ga * Mf(rs_)) / rs_                                        # deep MOND, spherical: |g| = sqrt(G a0 M(<r))/r
ratio = sp.simplify(sp.diff(rs_ ** 2 * g_dm, rs_) / rs_ ** 2 / g_dm)
target = (1 + rs_ * sp.diff(Mf(rs_), rs_) / (2 * Mf(rs_))) / rs_
P(f"    deep MOND: lap Phi/|grad Phi| = {ratio}   (target (1 + beta/2)/r: difference {sp.simplify(ratio - target)})")
OUT["numbers"]["A2"] = dict(kappa=str(kap_r), l395_ratio=str(ratio))
check("A2 the mean curvature of the equipotentials is 1/r for every spherical profile; lap Phi/|grad Phi| is "
      "(1 + beta_b/2)/r in deep MOND, 1/r only where the enclosed baryons have stopped rising",
      f"kappa = {kap_r}; lap/|grad| - (1 + beta/2)/r = {sp.simplify(ratio - target)}",
      sp.simplify(kap_r - 1 / rs_) == 0 and sp.simplify(ratio - target) == 0)

# ---------------------------------------------------------------------------------- MS3's machinery, loaded unedited
p3 = os.path.join(HERE, "MS3_cosmic_shear_bound_mond_sector.py")
M3 = {"__name__": "ms3", "__file__": p3}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(p3).read().split('banner("C1  CONTROL')[0].replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), M3)
MS3R = json.load(open(os.path.join(HERE, "MS3_cosmic_shear_bound_mond_sector_results.json")))["numbers"]
GP0, KC, RHO, PNL, PLIN, h, ZS, aS = (M3[k_] for k_ in ("GP0", "KC", "RHO", "PNL", "PLIN", "h", "ZS", "aS"))
G, MS, MPC, nu_mono, E2, I1, nfw_uk = (M3[k_] for k_ in ("G", "MS", "MPC", "nu_mono", "E2", "I1", "nfw_uk"))
FB, dn, bh, LMH, dlnM, XLIN, A0, KG = (M3[k_] for k_ in ("FB", "dn", "bh", "LMH", "dlnM", "XLIN", "A0", "KG"))
H05, ret_L388, transform = M3["H05"], M3["ret_L388"], M3["transform"]
RCAP = 1.75
VCAP = RCAP * H05 * math.sqrt(XLIN)                                       # MS3's v_cap (km/s)
P(f"\n  MS3 loaded: v_cap = {VCAP:.1f} km/s (r_cap {RCAP} Mpc at z = 0.5); (v_cap/c)^2 = {(VCAP / 2.99792458e5) ** 2:.3e}   [{time.time() - T0:.0f}s]")


def Ez2(z): return GP0.Om * (1 + z) ** 3 + GP0.OL
def l_cap(z): return VCAP / (H05 * math.sqrt(Ez2(z) / E2) * math.sqrt(2.5 * Ez2(z)))


def edge_L395(M, Mb, a0, z, reading):
    """outermost radius (physical Mpc) where lap Phi_X / |grad Phi_X| >= 1/l_cap(z), baryons in the given reading."""
    c = 10 ** (0.905 - 0.101 * math.log10(M / (1e12 / h))) * (1 + z) ** -0.5
    r200 = (3 * M / (4 * math.pi * 200 * GP0.RHO_CRIT0 * Ez2(z))) ** (1 / 3); rs = r200 / c
    mn = lambda s: np.log(1 + s) - s / (1 + s)
    r = np.geomspace(1e-2 * r200, 40.0, 6000)
    if reading == "point":
        Mr = np.full_like(r, Mb)
    elif reading == "nfw_trunc":
        Mr = Mb * np.minimum(mn(r / rs) / mn(c), 1.0)
    else:                                                                 # "nfw_ext": keeps tracing the NFW past r200
        Mr = Mb * mn(r / rs) / mn(c)
    gN = G * Mr * MS / (r * MPC) ** 2
    g = nu_mono(gN / a0) * gN
    q = np.gradient(r ** 2 * g, r) / r ** 2 / g                           # lap Phi_X / |grad Phi_X|, 1/Mpc
    on = np.where(q >= 1 / l_cap(z))[0]
    return float(r[on.max()]) if on.size else float(r[0]), r200


# ============================================================================================ N1 where L395's form puts the edge
banner("N1  L395's FORM ON SPHERICAL HOSTS: its edge as a ratio to l_cap (the kappa form's edge, 1.75 Mpc at z = 0.5)")
N1 = {}
for foot, a0 in A0.items():
    for lm in (13.5, 14.0, 14.5, 15.0):
        M = 10 ** lm; Mb = float(GP0.M_bound(M, ZS, "observed"))
        row = {rd_: edge_L395(M, Mb, a0, ZS, rd_)[0] / RCAP for rd_ in ("point", "nfw_trunc", "nfw_ext")}
        N1[f"{foot}/{lm}"] = row
        P(f"    {foot:9s} M = 1e{lm}: edge/l_cap  point mass {row['point']:.3f}, NFW to r200 {row['nfw_trunc']:.3f}, "
          f"NFW past r200 {row['nfw_ext']:.3f}")
zc, Mcoma = 0.023, 1.0e15
lc = {z_: l_cap(z_) for z_ in (0.02, 0.023, 0.04, 0.06, 0.25, 0.5)}
Mbc = float(GP0.M_bound(Mcoma, zc, "observed"))
coma = {rd_: edge_L395(Mcoma, Mbc, A0["canonical"], zc, rd_)[0] for rd_ in ("point", "nfw_trunc", "nfw_ext")}
P("    l_cap(z) [kappa form, every host above v_cap]: " + ", ".join(f"z={k_}: {v_:.2f}" for k_, v_ in lc.items()) + " Mpc")
P(f"    Coma-like host (1e15, z = 0.023, canonical): L395-form edge {coma['point']:.2f} (point) / {coma['nfw_trunc']:.2f} "
  f"(NFW to r200) / {coma['nfw_ext']:.2f} Mpc (NFW past r200); XR6 reports 3.5-3.7 Mpc for its hosts at z = 0.02-0.06")
OUT["numbers"]["N1"] = dict(edge_over_lcap=N1, l_cap=lc, coma_L395=coma)
check("N1 L395's form stays at l_cap on MS3's point-mass baryons but moves out wherever the baryons still rise at the cap",
      f"z = 0.5, 1e14.5 canonical: point {N1['canonical/14.5']['point']:.3f}, past r200 {N1['canonical/14.5']['nfw_ext']:.3f}",
      N1["canonical/14.5"]["point"] <= 1.02 and N1["canonical/14.5"]["nfw_ext"] >= 1.1, load_bearing=False)

# ============================================================================================ S1 cosmic shear with each form
banner("S1  COSMIC SHEAR ON MS3's MACHINERY WITH EACH LOCAL FORM (door convention, L388's retention, both footings)")


def R_capfun(a0, capfun):
    P1 = np.zeros_like(KC); X1 = np.zeros_like(KC); B = np.zeros_like(KC); rm = np.zeros_like(KC)
    for lm in LMH:
        M = 10 ** lm; n = float(np.interp(lm, GP0.LM, dn)); b = float(np.interp(lm, GP0.LM, bh))
        Mb = float(GP0.M_bound(M, ZS, "observed"))
        tr, _ = transform(M, Mb, XLIN, a0, capfun(M, Mb, a0), "door"); uk = nfw_uk(M, KC)
        P1 += n * tr ** 2 * dlnM / RHO ** 2; B += n * b * tr * dlnM / RHO
        fr = ret_L388(M); mass_1h = (FB + (1 - FB) * fr) * M
        rm += n * ((M * uk) ** 2 - (mass_1h * uk) ** 2) * dlnM / RHO ** 2
        X1 += n * mass_1h * uk * tr * dlnM / RHO ** 2
    R = (PNL - rm + 2 * (X1 + I1 * B * PLIN) + P1 + B ** 2 * PLIN) / PNL
    return max(float(np.interp(math.log(q * h), np.log(KC), R)) for q in KG)


FORMS = {
    "kappa": lambda M, Mb, a0: RCAP,                                      # A2: kappa = 1/r, so the edge is l_cap exactly
    "L395/point": lambda M, Mb, a0: edge_L395(M, Mb, a0, ZS, "point")[0],
    "L395/nfw_trunc": lambda M, Mb, a0: edge_L395(M, Mb, a0, ZS, "nfw_trunc")[0],
    "L395/nfw_ext": lambda M, Mb, a0: edge_L395(M, Mb, a0, ZS, "nfw_ext")[0],
}
if MUTATE: FORMS["kappa"] = FORMS["L395/nfw_ext"]
S1 = {k_: {foot: R_capfun(a0, fn) for foot, a0 in A0.items()} for k_, fn in FORMS.items()}
for k_, v_ in S1.items():
    P(f"    {k_:15s}: worst R canonical {v_['canonical']:.3f}, alt {v_['alt']:.3f}")
k1 = MS3R["K1"]["1.75"]
dctl = max(abs(S1["kappa"][f] - k1[f]["worst"]) for f in A0)
P(f"    MS3's committed K1 at 1.75 Mpc: {k1['canonical']['worst']:.3f}/{k1['alt']['worst']:.3f}; kappa form differs by {dctl:.1e}   [{time.time() - T0:.0f}s]")
OUT["numbers"]["S1"] = S1
check("S1 PRE-DECLARED: the kappa form reproduces MS3's K1 at 1.75 Mpc and passes; L395's form on baryons that keep "
      "tracing the host past r200 fails",
      f"kappa {S1['kappa']['canonical']:.3f}/{S1['kappa']['alt']:.3f} (MS3 diff {dctl:.1e}); L395 past r200 "
      f"{S1['L395/nfw_ext']['canonical']:.3f}/{S1['L395/nfw_ext']['alt']:.3f}",
      dctl < 1e-6 and all(S1["kappa"][f] <= 1.2 for f in A0) and max(S1["L395/nfw_ext"].values()) > 1.2,
      "the cap must read the equipotentials' curvature, not lap/|grad|: the latter lets cluster regions grow with their gas")

# ============================================================================================ P1 the principal symbol
banner("P1  THE GATE'S FOURTH-ORDER TERM [sympy] and where its bracket changes sign in DE9's smooth gate")
Hm = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"H{min(i, j)}{max(i, j)}", real=True))
gs, vc, Cc, tt = sp.symbols("g v_cap C t", positive=True)
k = sp.symbols("k1 k2 k3", real=True)
Wp_, Wpp_, Bb = sp.symbols("Wp Wpp B", real=True)
shift = {Hm[i, j]: Hm[i, j] + tt * k[i] * k[j] for i in range(3) for j in range(i, 3)}
kap_H = (Hm.trace() - Hm[2, 2]) / (2 * gs)                                # grad Phi_X = g e_z: n.H.n = H_zz
READ = {"uncapped": Cc * Hm.trace(), "kappa": Cc * vc ** 2 * kap_H ** 2, "L395": Cc * vc ** 2 * Hm.trace() ** 2 / gs ** 2}
k2, kp2 = sum(q ** 2 for q in k), k[0] ** 2 + k[1] ** 2
TGT = {"uncapped": Cc ** 2 * k2 ** 2 * Wpp_ * Bb,
       "kappa": Cc * vc ** 2 * kp2 ** 2 / gs ** 2 * Bb * (Wpp_ * READ["kappa"] + Wp_ / 2),
       "L395": 4 * Cc * vc ** 2 * k2 ** 2 / gs ** 2 * Bb * (Wpp_ * READ["L395"] + Wp_ / 2)}
P1res = {}
for k_, Ur in READ.items():
    Ut = Ur.subs(shift, simultaneous=True)
    dU, d2U = sp.diff(Ut, tt).subs(tt, 0), sp.diff(Ut, tt, 2).subs(tt, 0)
    Q = Wpp_ * Bb * dU ** 2 + Wp_ * Bb * d2U
    P1res[k_] = sp.simplify(sp.expand(Q - TGT[k_]))
    P(f"    {k_:8s}: Q - target = {P1res[k_]}")
# the bracket W''U + W'/2 in DE9's smooth gate W(t), t = (U/x_c - 1)/(2w) + 1/2: times (2 w x_c), it is
#   W_tt(t) (1 + 2w(t - 1/2))/(2w) + W_t(t)/2
ts = np.linspace(1e-3, 1 - 1e-3, 20001)
Wg = lambda s: np.exp(-1 / s) / (np.exp(-1 / s) + np.exp(-1 / (1 - s)))
Wt = np.gradient(Wg(ts), ts); Wtt = np.gradient(Wt, ts)
flip = {}
for wd in (0.25, 0.5):
    br = Wtt * (1 + 2 * wd * (ts - 0.5)) / (2 * wd) + Wt / 2
    neg = ts[br < 0]
    flip[wd] = dict(capped_t_flip=float(neg.min()) if neg.size else None, uncapped_t_flip=float(ts[Wtt < 0].min()))
    P(f"    w = {wd}: the capped bracket is negative for t > {flip[wd]['capped_t_flip']:.3f} (uncapped W'': t > "
      f"{flip[wd]['uncapped_t_flip']:.3f}) -- both change sign inside the layer")
OUT["numbers"]["P1"] = dict(residuals={k_: str(v_) for k_, v_ in P1res.items()}, flip=flip)
check("P1 the capped gate's fourth-order term has the stated closed form (zero residual): the kappa form's is transverse "
      "(k_perp^4) and carries a new definite-sign W'B/2 term; its bracket still changes sign inside the layer, as the "
      "uncapped door's W'' does",
      {k_: str(v_) for k_, v_ in P1res.items()}, all(v_ == 0 for v_ in P1res.values()), load_bearing=False)

# ============================================================================================ summary
banner("SUMMARY")
P(f"""  A cap built from the MOND-sector field alone keeps the carrier exactly Newtonian with the gate varied (A1).  The cap
  must read the mean curvature of the MOND field's equipotentials, kappa_X = (1/2) div(grad Phi_X/|grad Phi_X|), which is
  1/r for every spherical profile (A2): U_cap = C min(lap Phi_X, v_cap^2 kappa_X^2) ends every spherical region at
  l_cap(z) = v_cap/(H sqrt(x_c)) = {lc[0.5]:.2f} Mpc at z = 0.5 and {lc[0.023]:.2f} Mpc at z = 0.023, and reproduces MS3's pass
  ({S1['kappa']['canonical']:.3f}/{S1['kappa']['alt']:.3f}).  L395's form, lap Phi_X/|grad Phi_X|, is (1 + beta_b/2)/r: on baryons that keep
  tracing a cluster past r200 its edge sits {N1['canonical/14.5']['nfw_ext']:.2f}x further out at 1e14.5 and cosmic shear fails
  ({S1['L395/nfw_ext']['canonical']:.3f}/{S1['L395/nfw_ext']['alt']:.3f}).  The fourth-order term of the capped gate keeps a sign change inside
  the transition layer (P1): DE7's repair is still needed.  v_cap = {VCAP:.0f} km/s stays a declared constant.""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["summary"] = dict(load_bearing_failed=n_fail, runtime_s=round(time.time() - T0, 1))
suffix = "_MUTATE" if MUTATE else ""
json.dump(OUT, open(os.path.join(HERE, f"{SLUG}_results{suffix}.json"), "w"), indent=1, default=str)
P(f"\n  checks: {sum(ok for _, ok, _ in CH)}/{len(CH)} pass; load-bearing failures: {n_fail}   [{time.time() - T0:.0f}s]")
sys.exit(1 if n_fail else 0)
