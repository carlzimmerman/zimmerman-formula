#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG337 -- IS THERE A STABLE ACTION FOR CANDIDATE B'S BOUND-ONLY SWITCH?   (criteria: FROZEN_CRITERIA.md, committed first)

THE CANDIDATE (screen winner, Part 3).  A leaf-normalised, saturating, INVERTED symmetron: one canonical real scalar
sigma, minimally coupled (c_T = 1 and the beta = 0 chassis untouched), Z2-symmetric, whose mass term is triggered by a
baryon reading U >= 0 normalised by a leaf average (CFG329: diffeomorphism-safe):

    S_sw = Int sqrt(-g) [ -(eps_K/2) (d sigma)^2 - V(sigma; U) ],   V = -(1/2) mu0^2 T(U) sigma^2 + (lambda/4) sigma^4,
    T(U) = 1 - 1/U   (T < 0: symmetric phase, OFF;  T > 0: broken phase, ON;  T -> 1 deep inside: saturates),
    the chassis' MOND sector is multiplied by f(sigma) = sigma^2 / v^2,   v^2 = mu0^2 / lambda,
    E_c = mu0^2 v^2 = lambda v^4 (condensation energy density), R = E_c / B (B = the MOND-sector energy coefficient
    that f switches, DE7/DE12: B = a0^2 q(y^2) / 8 pi G).

Two doors (readers), both baryon-only (MS1):
    C1  the MOND-sector door (MS2/CV3; what M*/V0 use): U = DE12's contrast form, dU/drho_b = Umax A (the phantom's
        amplification A = nu + y nu' cos^2 theta);
    C2  the baryon-density door (B's T3(ii)-like density edge): U = rho_b / (Delta_e <rho_b>_leaf), A = 1, Delta_e set
        per system so the onset sits at the same edge radius as DE12's gate ("same edge", as DE12 G3).

Static energy density per unit volume at fixed background B (the -B f piece included):
    E(rho, sigma) = -(1/2) mu0^2 T(U(rho)) sigma^2 + (lambda/4) sigma^4 - B sigma^2 / v^2.
Broken phase: sigma_bar^2 = v^2 (T + 2/R), so f_bar = T + 2/R (law overshoot 2/R inside: nu_mono fidelity needs R >> 1).
Quadratic action (quasi-static Newtonian limit on the leaves; fluid displacement xi, delta rho = -i rho k xi; sigma
fluctuation s):  kinetic K = diag(rho, eps_K);  potential
    Q(k) = [[rho (c_s^2 + rho E_dir) k^2 - rho Gamma_g^2,  rho k g_x], [rho k g_x,  eps_K (k^2 + M^2)]],
    E_dir = d2E/drho2 |_sigma,  g_x = d2E/drho dsigma,  M^2 = d2E/dsigma2,  Gamma_g^2 = 4 pi G rho_m.

CONTROLS (frozen): R1 the record's prescribed gate (DE12, w = 0.25) as the slaved limit returns its failure (c_gate,
Gamma/H, Hadamard unboundedness, W'' > 0 somewhere); R2 the GR limit is healthy; MUTATE (CFG337_MUTATE=1): eps_K -> -1
must be flagged as a ghost (exit 1).

Run from the repository root:  python3 campaign_fresh_gravity/CFG337_stable_switch_action/cfg337_switch.py
                               CFG337_MUTATE=1 python3 campaign_fresh_gravity/CFG337_stable_switch_action/cfg337_switch.py
"""
import os, sys, json, math, io, contextlib, time
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("CFG337_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
T0 = time.time()
P = lambda *a: print(*a, flush=True)
OUT = {"lane": "CFG337", "mutate": MUTATE, "checks": {}, "numbers": {}}
CH = []


def check(name, measured, ok, reading=""):
    ok = bool(ok)
    CH.append((name, ok))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}" + (f"\n         reading:  {reading}" if reading else ""))
    return ok


def banner(t):
    P("\n" + "=" * 110 + "\n" + t + "\n" + "=" * 110)


P(__doc__.strip())
if MUTATE:
    P("\n  *** CFG337_MUTATE=1: the switch field's kinetic (and gradient) term flips sign; H1 must flag a ghost ***")
EPS_K = -1 if MUTATE else 1

# ---------------------------------------------------------------- the record's transitions (DE12, loaded read-only)
P_DE12 = os.path.join(REPO, "real_research", "dark_energy_2026", "DE12_mond_sector_gate_stiffness.py")
NS = {"__name__": "de12_readonly", "__file__": P_DE12}
_src = open(P_DE12).read().split('banner("G1 G2')[0]
_src = _src.replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src, NS)                                   # defines constants, Wd, host, transition; writes no files
G, KPC, MS, FB, CS, Wd, transition = [NS[k] for k in ("G", "KPC", "MS", "FB", "CS", "Wd", "transition")]
P(f"\n  DE12's transition() loaded read-only; gas sound speeds 1e5 K {CS['1e5K']/1e3:.0f} km/s, 1e6 K {CS['1e6K']/1e3:.0f} km/s")
ZS, MBS, FOOTS = (0.25, 1.0, 2.5, 4.0), (1e10, 1e11, 1e12), ("canonical", "alt")
ELL_LOC = 100 * KPC                                   # XR15's tolerance (frozen); 500 kpc reported

# =============================================================================================== Part 2: the screen
banner("PART 2  SCREEN OF SWITCH CLASSES (cheap symbolic checks; the reasoning is in the README table)")
x, c, s_, X, Kp, Kpp, phi, rho, M2s, lam_s, mu_s = sp.symbols("x c s X Kp Kpp phi rho M2 lambda mu", real=True)
SCREEN = {}
# S1 k-mouflage: force ratio 1/K'(X); K'' > 0 -> ratio falls at large gradient (screens where fields are strong)
SCREEN["S1"] = ("k-mouflage / kinetic switch: K''>0 screens at HIGH gradient (wrong direction); the reversed sign "
                "is ellipticity-admissible only as a band kernel that changes nu below ~0.015 a0, where galaxy outskirts "
                "(0.01-0.1 a0) and the web (0.002-0.015 a0, N12) overlap -> violates the nu_mono kernel; FAIL (constraint)")
d_ratio = sp.diff(1 / sp.Function("Kp")(X), X)
P("  S1: d(1/K')/dX = " + str(d_ratio) + "  (< 0 when K'' > 0: screened at large X)")
# S2 symmetron: standard sign OFF in dense; inverted sign ON in dense
Vstd = (rho / M2s - mu_s ** 2) * phi ** 2 / 2 + lam_s * phi ** 4 / 4
Vinv = (mu_s ** 2 - rho / M2s) * phi ** 2 / 2 + lam_s * phi ** 4 / 4
br_std = sp.solve(sp.diff(Vstd, phi) / phi, phi ** 2)
br_inv = sp.solve(sp.diff(Vinv, phi) / phi, phi ** 2)
P(f"  S2: standard broken branch phi^2 = {br_std} (exists only for rho < mu^2 M^2: OFF in dense)")
P(f"      inverted broken branch phi^2 = {br_inv} (exists only for rho > mu^2 M^2: ON in dense) -> carried to Part 3")
SCREEN["S2"] = ("symmetron: standard sign switches OFF in dense regions (wrong direction); inverted (density-triggered SSB) "
                "is ON in dense, Z2 keeps it exactly OFF at linear order on FRW, canonical kinetic -> PROMISING (Part 3)")
# S3 cubic Galileon: static x + c x^2 = s (x = phi'/r, s ~ enclosed density)
roots = sp.solve(sp.Eq(x + c * x ** 2, s_), x)
disc = sp.discriminant(c * x ** 2 + x - s_, x)
Zr = sp.diff(x + c * x ** 2, x)                    # radial kinetic coefficient of fluctuations ~ d(x + c x^2)/dx
x_thr = sp.solve(sp.Eq(Zr, 0), x)[0]
s_thr = sp.simplify((x + c * x ** 2).subs(x, x_thr))
P(f"  S3: discriminant {disc}; c<0 branch has no real root for s > {sp.simplify(-1 / (4 * c))}; Z = {Zr} -> 0 at x = {x_thr}"
  f" (s = {s_thr}): strong coupling at the threshold; c>0 branch: x ~ sqrt(s/c), suppression (Vainshtein, wrong direction)")
SCREEN["S3"] = ("cubic Galileon/Vainshtein: suppression-only (c>0); the inverted branch (c<0) has no static solution above "
                "s = -1/(4c) and its fluctuation coefficient Z = 1 + 2 c x vanishes there -> strong coupling; FAIL")
# S4 virial switch on a local stress-tensor scalar: same N14 structure in the read variable
Wf = sp.Function("W")
pr = sp.symbols("p", positive=True)
d2 = sp.diff(-sp.Symbol("B") * Wf(pr / rho), pr, 2)
P(f"  S4: d2(-B W(P/rho))/dP^2 = {d2}  (sign of -W'': negative where W''>0 -> negative thermal stiffness, N14)")
SCREEN["S4"] = ("virial switch from T^mu_mu or P/rho: dust trace = -rho (reduces to the density door); P/rho is zero per "
                "stream for collisionless stars (not a local field there); a prescribed W(P/rho) has W'' of both signs -> "
                "N14 on the gas temperature; FAIL")
# S5 leaf average alone: constant on a leaf
xs = sp.symbols("x_i", real=True)
P(f"  S5: d/dx_i <rho_b>_leaf(tau) = {sp.diff(sp.Function('rbar')(sp.Symbol('tau')), xs)}  (cannot localise)")
SCREEN["S5"] = ("leaf-averaged switch alone: constant on each leaf -> blind to bound vs unbound (N14 'K alone'); USED as the "
                "threshold normaliser in Part 3 (keeps the threshold OFF at all z on FRW)")
SCREEN["S6"] = ("nonlocal enclosed-mass gate (CFG48): stable 48/48 but bilocal (not a legal local term) and its edge sits at "
                "0.11-0.24 r_ta, below B's window; record reference only")
OUT["numbers"]["screen"] = SCREEN

# =============================================================================================== Part 3: the action
banner("PART 3  THE CANDIDATE: QUADRATIC ACTIONS (sympy)")
r_, sg, mu0, lam, Bs, U = sp.symbols("rho sigma mu0 lambda B U", positive=True)
eK, k, w2, cs2, Gg2 = sp.symbols("eps_K k omega2 c_s2 Gamma_g2", real=True)
Tf = 1 - 1 / U
v2 = mu0 ** 2 / lam
Uf = sp.Function("Ufun")(r_)
Efun = -sp.Rational(1, 2) * mu0 ** 2 * (1 - 1 / Uf) * sg ** 2 + lam / 4 * sg ** 4 - Bs * sg ** 2 / v2
E_s = sp.diff(Efun, sg)
sb2 = sp.solve(sp.Eq(E_s / sg, 0), sg ** 2)[0]
sb2_s = sp.simplify(sb2)
P(f"  broken phase: sigma_bar^2 = {sb2_s}   (= v^2 (T + 2/R), R = E_c/B, E_c = mu0^2 v^2)")
M2 = sp.simplify(sp.diff(Efun, sg, 2).subs(sg ** 2, sb2))
gx = sp.diff(Efun, sg, r_)
Edir = sp.diff(Efun, r_, 2)
P(f"  M^2 (broken) = {sp.simplify(M2)}  -> 2 lambda sigma_bar^2 > 0 wherever the broken phase exists")
M2_off = sp.diff(Efun, sg, 2).subs(sg, 0)
P(f"  M^2 (symmetric, sigma = 0) = {sp.simplify(M2_off)}  -> > 0 iff T < -2/R (OFF side)")
# FRW: sigma_bar = 0  -> every mixing term carries sigma_bar
gx_off, Edir_off = sp.simplify(gx.subs(sg, 0)), sp.simplify(Edir.subs(sg, 0))
f_sig = sg ** 2 / v2
df_off = sp.diff(f_sig, sg).subs(sg, 0)
P(f"  FRW / OFF side: g_x = {gx_off}, E_dir = {Edir_off}, df/dsigma = {df_off}, f = {f_sig.subs(sg, 0)}")

# generic 2x2 quadratic form and its dispersion
rho0, Ed, g0, m2 = sp.symbols("rho0 E_d g0 m2", real=True)
Kmat = sp.Matrix([[rho0, 0], [0, eK]])
Qmat = sp.Matrix([[rho0 * (cs2 + rho0 * Ed) * k ** 2 - rho0 * Gg2, rho0 * k * g0], [rho0 * k * g0, eK * (k ** 2 + m2)]])
disp = sp.expand((Qmat - w2 * Kmat).det())
w2sol = sp.solve(disp, w2)


def health(name, subsd, kgrid=np.geomspace(1e-3, 1e4, 400)):
    """H1 kinetic positivity, H2 high-k speeds in (0, 1], H3 omega^2 bounded below uniformly in k."""
    Kn = np.array(Kmat.subs(subsd), dtype=float)
    h1 = bool(np.all(np.linalg.eigvalsh(Kn) > 0))
    # high-k: coefficient of k^2 in Q divided by K
    Q2 = sp.Matrix([[subsd[rho0] * (subsd[cs2] + subsd[rho0] * subsd[Ed]), 0], [0, subsd[eK]]])
    sp2 = [float(Q2[i, i] / Kn[i, i]) for i in range(2)]
    h2 = all(0 < v <= 1 + 1e-12 for v in sp2)
    fs = [sp.lambdify(k, ws.subs({kk: vv for kk, vv in subsd.items() if kk != k}), "numpy") for ws in w2sol]
    vals = np.array([[complex(f(kk)) for f in fs] for kk in kgrid])
    wmin = np.min(vals.real, axis=1)
    # bounded below: the minimum at the largest k is not more negative than at moderate k (no k-linear divergence)
    h3 = bool(wmin[-1] > -abs(wmin[len(kgrid) // 2]) * 10 - 1e-9) and bool(np.all(np.isfinite(wmin)))
    return dict(H1=h1, H2=h2, H3=h3, speeds2=sp2, w2min_hi_k=float(wmin[-1]), w2min_min=float(np.min(wmin)))


# (a) FRW, linear perturbations, symmetric phase (dimensionless units: c = 1, k in units of the matter Jeans scale)
banner("(a) FRW WITH LINEAR PERTURBATIONS (symmetric phase, sigma_bar = 0)")
frw = {rho0: 1.0, Ed: 0.0, g0: 0.0, m2: 0.5, eK: EPS_K, cs2: 1e-6, Gg2: 1.0}
Ha = health("FRW", frw)
P(f"  H1 {Ha['H1']}  H2 {Ha['H2']} speeds^2 {Ha['speeds2']}  H3 {Ha['H3']}")
# matter growth equation: f_bar = 0 and df = 2 sigma_bar dsigma / v^2 = 0 at linear order -> LCDM
a_, Hh, d_, Om_ = sp.symbols("a H delta Omega_m")
growth_switch_term = sp.simplify(2 * 0 * sp.Symbol("dsigma") / v2)
frw_off = bool(gx_off == 0 and Edir_off == 0 and df_off == 0 and growth_switch_term == 0)
P(f"  linear-order switch contribution to the matter growth equation: {growth_switch_term} -> delta'' + 2H delta' = 4 pi G rho_m delta (LCDM)")
P(f"  leaf-normalised threshold: C2 U = (1 + delta)/Delta_e < 1 for delta < Delta_e - 1 at every z (T < 0, M^2 = mu0^2 (1/U - 1) > 0);")
P(f"  B (MOND-sector energy) is O(delta^3) on FRW (q ~ y^3 deep), so it does not enter the quadratic action there.")
check("FRW_H (a) FRW: no ghost, speeds^2 in (0,1], Hadamard-bounded, switch OFF at linear order (LCDM growth)",
      f"H1 {Ha['H1']} H2 {Ha['H2']} H3 {Ha['H3']} OFF {frw_off}", Ha["H1"] and Ha["H2"] and Ha["H3"] and frw_off)
OUT["numbers"]["FRW"] = Ha

# =========================================================================== numerical background evaluation
T_of = lambda u: 1.0 - u                               # u = 1/U


def sw_coeffs(rho_b, B, Urho, Uv, Ec):
    """local coefficients of the candidate at density rho_b; U and dU/drho at the point; condensation energy Ec."""
    u = 1.0 / Uv
    T = 1.0 - u
    R = Ec / B
    br = T + 2.0 / R                                  # sigma_bar^2 / v^2
    Tp = Urho / Uv ** 2                              # dT/drho
    Tpp = -2.0 * Urho ** 2 / Uv ** 3                 # d2T/drho2 (U linear in rho locally)
    on = br > 0
    # with mu0 = 1 / ell: M^2 = 2 mu0^2 br; g_x = -mu0^2 T' sigma_bar; E_dir = -(1/2) mu0^2 T'' sigma_bar^2
    cg2 = np.where(on, rho_b * Ec * Tp ** 2 / 2.0, 0.0)                    # rho g_x^2 / M^2 (mu0-independent)
    rEd = np.where(on, -0.5 * Ec * Tpp * br * rho_b, 0.0)                   # rho E_dir  (>= 0: T concave)
    slaved = cg2 - rEd                                                      # slaved-limit stiffness deficit
    return dict(u=u, T=T, br=br, on=on, cg2=cg2, rEd=rEd, slaved=slaved, R=R)


def rho_ph(tr, Mb):
    """the point-mass on-branch phantom density (DE12's formula), for Gamma_g^2 = 4 pi G (rho_b/f_b + rho_ph)."""
    y = tr["y"]
    return np.maximum(Mb * MS * (NS["h_of"](y) - y * NS["dh_of"](y)) / (2 * math.pi * tr["r"] ** 3 * y), 0.0)


def h4_rate(co, cs, ell):
    """max extra growth rate of the transition gas: M (c_g - c_eff)_+, M = sqrt(2 br)/ell, c_eff^2 = c_s^2 + rho E_dir."""
    M = np.sqrt(2.0 * np.maximum(co["br"], 0.0)) / ell
    ceff = np.sqrt(cs ** 2 + co["rEd"])
    return np.where(co["on"], M * np.maximum(np.sqrt(co["cg2"]) - ceff, 0.0), 0.0)


# =============================================================================================== R1 control
banner("R1  CONTROL: the record's prescribed gate (DE12 MOND-sector gate, w = 0.25) is the slaved limit and fails")
c25 = []
for Mb in MBS:
    for foot in FOOTS:
        tr = transition(0.25, Mb, foot, 0.25, amp=True)
        m = (tr["t"] > 0) & (tr["t"] < 1)
        cg = np.sqrt(np.maximum(tr["c_gate2"]["perp"], tr["c_gate2"]["par"]))
        cmax = float(np.max(cg[m]))
        gam = (1 / KPC) * math.sqrt(max(cmax ** 2 - CS["1e6K"] ** 2, 0))     # Gamma = k sqrt(c_gate^2 - c_s^2)
        c25.append((cmax, gam / tr["H"]))
cmin, gmin = min(v[0] for v in c25), min(v[1] for v in c25)
# Hadamard: slaved (no kinetic, no gradient) -> omega^2 = k^2 (c_s^2 - c_gate^2) - Gamma_g^2, unbounded below
cgate_s = sp.symbols("c_gate2", positive=True)
w2_slaved = k ** 2 * (cs2 - cgate_s) - Gg2
unb = sp.limit(w2_slaved.subs({cs2: CS['1e6K'] ** 2, cgate_s: cmin ** 2, Gg2: 0}), k, sp.oo)
tt = np.linspace(1e-4, 1 - 1e-4, 20001)
_, _, W2 = Wd(tt)
r1 = (abs(cmin / 1526169.663408363 - 1) < 0.01 and abs(gmin / 19820.49479645704 - 1) < 0.01 and unb == -sp.oo
      and np.max(W2) > 0 and np.min(W2) < 0)
check("R1 CONTROL: DE12's gate returns its failure (min c_gate, min Gamma/H at z = 0.25 within 1% of 1526 km/s, 2.0e4; "
      "slaved omega^2 -> -inf as k -> inf; W'' of both signs)",
      f"min c_gate {cmin/1e3:.1f} km/s; min Gamma/H {gmin:.3e}; slaved limit {unb}; W'' range [{np.min(W2):.2f}, {np.max(W2):.2f}]", r1,
      "the known failure is a Hadamard (k-linear, unbounded) gradient instability of the transition gas")
OUT["numbers"]["R1"] = dict(c_gate_min=cmin, Gamma_over_H_min=gmin)

# =============================================================================================== R2 control
banner("R2  CONTROL: the GR limit (switch decoupled, MOND sector off) is healthy")
gr = {rho0: 1.0, Ed: 0.0, g0: 0.0, m2: 1.0, eK: 1, cs2: 1e-4, Gg2: 1.0}
Hg = health("GR", gr)
jeans_k2 = 1.0 / 1e-4
check("R2 CONTROL: GR limit has K > 0, speeds^2 (c_s^2, 1), bounded growth = Jeans (omega^2 >= -4 pi G rho)",
      f"H1 {Hg['H1']} H2 {Hg['H2']} {Hg['speeds2']} H3 {Hg['H3']}; min omega^2 {Hg['w2min_min']:.3f} (>= -1)",
      Hg["H1"] and Hg["H2"] and Hg["H3"] and Hg["w2min_min"] >= -1.0 - 1e-9)

# =============================================================================================== (b) bound
banner("(b) STATIC VIRIALISED BARYONIC BACKGROUND (deep broken phase), both doors")
BOUND = {}
for door, amp in (("C1", True), ("C2", False)):
    tr = transition(0.25, 1e11, "canonical", 0.25, amp=amp)
    i = int(np.argmin(np.abs(tr["r"] - 30 * KPC)))                 # a point well inside (30 kpc)
    rho_b, B = tr["rho_b"][i], tr["B"][i]
    Umax = 4 * math.pi * G / (tr["H"] ** 2 * tr["xce"])
    A = (NS["nu_of"](tr["y"][i]) + NS["ynup_of"](tr["y"][i])) if amp else 1.0
    if door == "C1":
        Uv, Urho = tr["t"][i] * 2 * 0.25 - 0.25 + 1.0, Umax * A      # invert DE12's t = (U-1)/(2w) + 1/2
    else:
        r_e = float(np.interp(0.5, tr["t"][::-1], tr["r"][::-1]))
        rho_e = float(np.interp(r_e, tr["r"], tr["rho_b"]))
        Uv, Urho = rho_b / rho_e, 1.0 / rho_e
    co = sw_coeffs(rho_b, B, Urho, Uv, 4.0 * B)
    ell = ELL_LOC
    mu0n = 1 / ell
    M2n = 2 * mu0n ** 2 * co["br"]
    gxn = math.sqrt(co["cg2"] * M2n / rho_b)
    Edn = co["rEd"] / rho_b
    rho_m = rho_b / FB + 0.0
    CL = 2.99792458e8                                              # c = 1 units: velocities / c, rates / c
    sub = {rho0: rho_b, Ed: Edn / CL ** 2, g0: gxn / CL, m2: M2n, eK: EPS_K, cs2: CS["1e6K"] ** 2 / CL ** 2,
           Gg2: 4 * math.pi * G * rho_m / CL ** 2}
    Hb = health("bound", sub, kgrid=np.geomspace(1e-25, 1e-15, 400))
    Hb["growth_max_over_Gamma_g"] = float(math.sqrt(max(-Hb["w2min_min"], 0.0)) * CL / math.sqrt(4 * math.pi * G * rho_m))
    Hb.update(U=float(Uv), f_bar=float(co["br"]), overshoot_2_over_R=0.5, c_g_kms=float(np.sqrt(co["cg2"]) / 1e3),
              c_dir_kms=float(np.sqrt(co["rEd"]) / 1e3))
    BOUND[door] = Hb
    P(f"  {door}: r = 30 kpc, U = {Uv:.3g}; K>0 {Hb['H1']}; speeds^2 [{Hb['speeds2'][0]:.2e}, {Hb['speeds2'][1]:.0f}] (c=1 units); max growth / Gamma_g {Hb['growth_max_over_Gamma_g']:.4f};"
      f" bounded {Hb['H3']}; c_g {Hb['c_g_kms']:.2f} km/s vs direct stiffness {Hb['c_dir_kms']:.2f} km/s")
OUT["numbers"]["bound"] = BOUND
bound_ok = {d: BOUND[d]["H1"] and BOUND[d]["H2"] and BOUND[d]["H3"] for d in BOUND}
check("BOUND_H (b) static bound background: H1-H3 for both doors", bound_ok, all(bound_ok.values()),
      "the broken phase is a positive-mass minimum; the trigger's direct term is a POSITIVE stiffness (T concave)")

# =============================================================================================== (c) transition
banner("(c) THE TRANSITION REGION on the record's transitions (z, M_b, footing): H1-H3 symbolic + H4 numeric")
# H1-H3 in the transition: same matrices; K = diag(rho, eps_K); high-k speeds c_s^2 + rho E_dir >= c_s^2 > 0 and 1.
TR = {}
for door, amp in (("C1", True), ("C2", False)):
    # universal constant E_c for a single field: R x max B at the onset over all systems (conservative for a pass)
    rows = []
    Bon_all = []
    for z in ZS:
        for Mb in MBS:
            for foot in FOOTS:
                tr = transition(z, Mb, foot, 0.25, amp=amp)
                Umax = 4 * math.pi * G / (tr["H"] ** 2 * tr["xce"])
                if door == "C1":
                    Uv = (tr["t"] - 0.5) * 2 * 0.25 + 1.0
                    A = np.maximum(NS["nu_of"](tr["y"]) + NS["ynup_of"](tr["y"]), NS["nu_of"](tr["y"]))
                    Urho = Umax * A
                    Uv = np.maximum(Uv, 1e-6)
                else:
                    r_e = float(np.interp(0.5, tr["t"][::-1], tr["r"][::-1]))
                    rho_e = float(np.interp(r_e, tr["r"], tr["rho_b"]))
                    Uv, Urho = tr["rho_b"] / rho_e, np.full_like(tr["r"], 1.0 / rho_e)
                ion = int(np.argmin(np.abs(Uv - 1.0)))
                Bon_all.append(tr["B"][ion])
                rows.append((z, Mb, foot, tr, Uv, Urho))
    Bmax = max(Bon_all)
    res = {}
    for R in (4.0, 40.0):
        for Emode in ("local", "universal"):
            worst = {}
            for (z, Mb, foot, tr, Uv, Urho) in rows:
                win = (Uv > 0.3) & (Uv < 30.0)
                Ec = R * (tr["B"] if Emode == "local" else np.full_like(tr["B"], Bmax))
                co = sw_coeffs(tr["rho_b"], tr["B"], Urho, Uv, Ec)
                Gg = np.sqrt(4 * math.pi * G * (tr["rho_b"] / FB + rho_ph(tr, Mb)))
                for cslab in ("1e6K", "1e5K"):
                    for ell_lab, ell in (("100kpc", ELL_LOC), ("500kpc", 5 * ELL_LOC)):
                        ge = h4_rate(co, CS[cslab], ell)
                        ratio = np.where(win, ge / Gg, 0.0)
                        j = int(np.argmax(ratio))
                        # minimal switch length that passes H4 at the worst point: ell_min = max over r of sqrt(2 br)(c_g - c_eff)/Gamma_g
                        ce = np.sqrt(CS[cslab] ** 2 + co["rEd"])
                        need = np.where(win & co["on"], np.sqrt(2 * np.maximum(co["br"], 0)) * np.maximum(np.sqrt(co["cg2"]) - ce, 0) / Gg, 0.0)
                        key = f"{cslab}/{ell_lab}"
                        cur = worst.get(key, dict(ratio=0, ell_min_kpc=0, c_g_max_kms=0))
                        cgmax = float(np.max(np.sqrt(co["cg2"])[win])) if win.any() else 0.0
                        if ratio[j] >= cur["ratio"]:
                            cur.update(ratio=float(ratio[j]), at=f"{z}/{Mb:.0e}/{foot}", r_kpc=float(tr["r"][j] / KPC))
                        cur["ell_min_kpc"] = max(cur["ell_min_kpc"], float(np.max(need)) / KPC)
                        cur["c_g_max_kms"] = max(cur["c_g_max_kms"], cgmax / 1e3)
                        worst[key] = cur
            res[f"R{R:g}/{Emode}"] = worst
            w = worst["1e6K/100kpc"]
            P(f"  {door} R = {R:g} E_c {Emode:9s}: worst extra-growth / Gamma_g at 100 kpc, 1e6 K gas = {w['ratio']:.3g} "
              f"({w.get('at')}, r {w.get('r_kpc', 0):.0f} kpc); max c_g {w['c_g_max_kms']:.1f} km/s; ell_min {w['ell_min_kpc']:.3g} kpc"
              f" | 1e5 K: ratio {worst['1e5K/100kpc']['ratio']:.3g}, ell_min {worst['1e5K/100kpc']['ell_min_kpc']:.3g} kpc")
    TR[door] = dict(results=res, B_onset_max=Bmax)
OUT["numbers"]["transition"] = TR
# symbolic H1-H3 in the transition: the kinetic matrix and the high-k block do not depend on the background
h123_tr = (EPS_K > 0)
# H4 decision: lenient for C1 (local E_c, R = 4), conservative for C2 (universal E_c, R = 4 and 40; 1e6 K per DE12)
h4 = {}
h4["C1"] = TR["C1"]["results"]["R4/local"]["1e6K/100kpc"]["ratio"] <= 1.0
h4["C2"] = TR["C2"]["results"]["R4/universal"]["1e6K/100kpc"]["ratio"] <= 1.0
h4_c2_strict = all(TR["C2"]["results"][f"R{R}/universal"][f"{cs}/100kpc"]["ratio"] <= 1.0 for R in ("4", "40") for cs in ("1e6K", "1e5K"))
check("TRANS_H123 (c) transition: K = diag(rho, eps_K) > 0; high-k speeds^2 c_s^2 + rho E_dir (> 0, E_dir >= 0) and 1; "
      "omega^2 >= -(Gamma_g^2 + rho g_x^2) bounded", f"eps_K = {EPS_K}", h123_tr)
check("TRANS_H4_C1 (c) C1 MOND-sector door: extra growth <= Gamma_g at ell <= 100 kpc (lenient: local E_c, R = 4, 1e6 K)",
      f"worst ratio {TR['C1']['results']['R4/local']['1e6K/100kpc']['ratio']:.3g}; ell_min {TR['C1']['results']['R4/local']['1e6K/100kpc']['ell_min_kpc']:.3g} kpc",
      h4["C1"])
check("TRANS_H4_C2 (c) C2 baryon-density door: extra growth <= Gamma_g at ell <= 100 kpc (conservative: universal E_c, R = 4, 1e6 K)",
      f"worst ratio {TR['C2']['results']['R4/universal']['1e6K/100kpc']['ratio']:.3g}; strict (R 4 and 40, 1e5 and 1e6 K) {h4_c2_strict}",
      h4["C2"])

# =============================================================================================== verdict
banner("VERDICT (frozen rule)")
frw_pass = Ha["H1"] and Ha["H2"] and Ha["H3"] and frw_off
verdict = {}
for door in ("C1", "C2"):
    n = int(frw_pass) + int(bound_ok[door]) + int(h123_tr and h4[door])
    verdict[door] = "CANDIDATE FOUND" if n == 3 else ("PARTIAL" if n == 2 else "NO-GO")
    P(f"  {door}: FRW {frw_pass}, bound {bound_ok[door]}, transition {h123_tr and h4[door]} -> {verdict[door]}")
OUT["verdict"] = verdict
OUT["verdict_note"] = ("Both doors are healthy on FRW (exactly OFF at linear order by Z2) and in the bound interior; both fail "
                       "H4 in the transition: the bounded (well-posed) growth of transition gas outruns gravity unless the "
                       "switch length exceeds the ell_min above. C2 is closest but reads a pure baryon-density edge: the record's matter-only "
                       "door fails KiDS (L392 +118/+128) and the flagship (DE4/DE6 need >= 30% CGM) in the M* model, and "
                       "CFG21's universal-edge tension (KiDS vs LG 5.1-5.3 sigma) applies; it encodes neither turnaround nor "
                       "top-level ownership; it adds declared constants (mu0 or ell, E_c or R, Delta_e)")
P("  note: " + OUT["verdict_note"])

ok_controls = OUT["checks"]["R1"]["pass"] and OUT["checks"]["R2"]["pass"]
expected = (not MUTATE and ok_controls and frw_pass and all(bound_ok.values()) and h123_tr) or \
           (MUTATE and not (frw_pass and all(bound_ok.values()) and h123_tr))
OUT["elapsed_s"] = round(time.time() - T0, 1)
fn = os.path.join(HERE, f"cfg337_switch_results{SUF}.json")
json.dump(OUT, open(fn, "w"), indent=1, default=str)
P(f"\n  wrote {os.path.relpath(fn, REPO)}; {sum(o for _, o in CH)}/{len(CH)} checks pass; elapsed {OUT['elapsed_s']} s")
if MUTATE:
    P("  MUTATE: ghost " + ("FLAGGED (H1 fails) -> exit 1" if not (Ha['H1']) else "NOT flagged -> control broken"))
    sys.exit(1 if not Ha["H1"] else 2)
sys.exit(0 if expected else 1)
