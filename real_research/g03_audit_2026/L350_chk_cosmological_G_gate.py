#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L350 -- THE COSMOLOGICAL-G GATE FOR C-H/K: Planck-era cosmology bounds the khronon's lambda-term, and the bound sits
BELOW the floor that L340 set for phantom tracking.  What survives, and a construction that removes the conflict.

WHY THIS GATE.  L340 set C-H/K's lambda-channel window at c_2 in (7.3e-3, 0.067): the floor from phantom tracking
(c_s >= 3 x 600 km/s where C <= 100), the ceiling from BBN (|G_cos/G_N - 1| ~ 1.5 c_2 < 0.1).  The CMB and large-scale
structure constrain the same number far more tightly, and that constraint was never applied.  On the FRW background
C-H/K's MOND term vanishes identically (q(0) = 0, zero gradients), with or without L342's switch, so the Friedmann
equation is exactly that of low-energy Horava gravity with xi = 1 (c_T = 1), eta = alpha_c, lambda_H = 1 + c_2.
With L342's switch the linear web is that theory in full, perturbations included -- the setting of the published fits.

WHAT THIS LANE CHECKS
  G1 FROM THE ACTION (symbolic): the minisuperspace of C-H/K on flat FRW gives H^2 (1 + 3c_2/2) = 8 pi G rho/3 + Lambda/3,
     so G_cos = G/(1 + 3c_2/2); L340's own static block at C = 0 gives G_N = G/(1 - alpha_c/2).  Hence
     G_cos/G_N = (2 - alpha_c)/(2 + 3c_2), identical to Frusciante & Benetti 2020 eq. (9) at xi = 1, eta = alpha_c,
     lambda = 1 + c_2 (the convention bridge to the published constraints is checked, not assumed).
  G2 THE PUBLISHED BOUNDS (Frusciante & Benetti 2020, arXiv:2005.14705, PRD 101 104033, Table III; Planck 2018 +
     BICEP2/Keck 2015, + Planck lensing + DES-Y1 + Pantheon or JLA; flat log priors on lambda-1 and eta from 1e-13;
     xi = 1 imposed by GW170817): 95% upper limits |G_c/G_N - 1| < 1.9e-3 .. 4.4e-3 and log10(lambda - 1) < -3.2 .. -2.8.
     Mapped to c_2 they give ceilings 6.3e-4 .. 2.9e-3.  L340's floor 7.3e-3 is excluded by EVERY dataset combination,
     by factors 2.5 .. 12.  (Audren+2015, JCAP 03 016, Table I: the khronometric bound "(beta+lambda)/alpha < 91" is a
     prior-volume marginal; the physically constrained combination is G_N/G_cos - 1 = (alpha + beta + 3 lambda)/2,
     their eq. (24)/(32) -- the same quantity.)
  G3 AN INDEPENDENT PHYSICAL CROSS-CHECK: with the switch off, sub-horizon growth feels G_N while H(z) feels G_cos
     (Audren+2015 effect (i)).  L342's B2 growth machinery omitted this factor; at L340's floor it raises sigma_8 by
     several per cent, many times Planck's CMB-lensing precision -- the same order as the published exclusion.
  G4 WHAT SURVIVES: at the cosmological ceilings the phantom still tracks galaxy BODIES, but in the deep-MOND outskirts
     (y ~ 1e-4 .. 1e-3, the KiDS radii) KM2's exact law R = 1 + [C/(1+C)] v_par^2/(c_s^2 - v_par^2) gives angle-averaged
     amplifications of several to tens of per cent for galaxies moving at 300-620 km/s through the CMB frame, and at
     the tightest ceiling the Local Group's outskirts are LEFT BEHIND (v >= c_s).  T1 moves from 'below reach' (KM2) to
     'at KiDS precision'.
  G5 A CONSTRUCTION THAT REMOVES THE CONFLICT (symbolic): replace -c_2 K^2 by -c_2 (K - <K>_Sigma)^2, with <K>_Sigma the
     leaf average on C-H's closed leaves.  It vanishes identically on FRW (G_cos = G, so G_cos/G_N - 1 = -alpha_c/2 ~ 1e-9)
     and is identical to L340's term for every Fourier mode k != 0, so L340's tracking result H1 is unchanged.  It is a
     global (leaf-nonlocal) term, like C-H's own heat kernel: a construction, not a derivation.
  MUTATE=1 replaces the Planck-2018-era bounds by the WMAP7/SPT-era bound (Audren+2013: |G_N/G_c - 1| < 0.018): L340's
  floor is then allowed and the load-bearing G2 check must FAIL (rc = 1) -- the exclusion is the newer data's.

SCOPE.  G2 imports published MCMC limits (log-flat priors; massive-neutrino and dataset variants all reported); it
does not re-run a Boltzmann code.  G3 is a growth-only estimate (no transfer-function or CMB-peak change).  G4 uses
KM2's frozen-coefficient closed form, which L340/KM2 established at principal order.

Run from the repository root:  python3 real_research/g03_audit_2026/L350_chk_cosmological_G_gate.py
"""
import os, sys, json, math, time, warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L350_chk_cosmological_G_gate"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L350", "mutate": MUTATE, "checks": {}, "numbers": {}}
T0 = time.time()
_trap = getattr(np, "trapezoid", None) or np.trapz


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 104); P(t); P("=" * 104)


P(__doc__.split("WHAT THIS LANE CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the WMAP7/SPT-era bound (Audren+2013) replaces the Planck-2018-era bounds; G2 must FAIL ***")

# L340's window, as committed (real_research/g03_audit_2026/L340_filtered_khronon_completion.py, P1)
CKMS = 2.99792458e5
VTRK, CMAX = 3 * 600.0 / CKMS, 100.0
C2_FLOOR = 2 * CMAX * VTRK**2 / (1 - 3 * CMAX * VTRK**2)
C2_BBN = 0.1 / 1.5

# ============================================================================================ G1 from the action
banner("G1  FROM THE ACTION: C-H/K's Friedmann equation and local G (symbolic)")
Gs, c2, ac, Lam, rho0 = sp.symbols('G c_2 alpha_c Lambda rho_0', positive=True)
A_, Ad_, N_, Hs = sp.symbols('a adot N H', positive=True)           # scale factor, its time derivative, lapse
H_ = Ad_ / (N_ * A_)                                                 # expansion per unit proper time
KijKij, Ktr = 3 * H_**2, 3 * H_                                      # flat FRW: K_ij = H h_ij (a_i = D_i ln N = 0)
def minisuperspace(lam_term):
    # C-H/K bracket on FRW: R3 = 0, K_ij K^ij - K^2 (GR), the khronon terms alpha_c a^2 (= 0 here) - c_2 * lam_term,
    # -2 Lambda; the MOND term 2 alpha^2 q(0) = 0 and 2|DU - a|^2 = 0 (U = ln N + const).  Dust: -rho N a^3 = -rho_0 N.
    return (N_ * A_**3 * (KijKij - Ktr**2 - c2 * lam_term - 2 * Lam)) / (16 * sp.pi * Gs) - rho0 * N_
def friedmann(L_):
    fr_ = sp.simplify(sp.diff(L_, N_).subs(N_, 1).subs(Ad_, Hs * A_))   # vary the lapse, then N = 1
    H2_ = sp.simplify(sp.solve(sp.Eq(fr_, 0), Hs**2)[0])
    Gc_ = sp.simplify(sp.diff(H2_, rho0) * A_**3 * 3 / (8 * sp.pi))     # H^2 = (8 pi G_cos/3) rho + ...
    return fr_, H2_, Gc_
fried_H, H2, Gcos = friedmann(minisuperspace(Ktr**2))
# L340's static block at C = 0 gives the local Newton constant (psi = phi = psi_N / (1 - alpha_c/2))
k, Cc, w = sp.symbols('k C omega', real=True)
psi, phi, beta, U, R = sp.symbols('psi phi beta U R')
D = -sp.I * w
def block(C_, eps_, ac_):                                            # L340 H1 block, verbatim (a2 = a3 = g = 0)
    E = [4*k**2*psi - 4*k**2*phi - D*(-12*D*psi + 4*k**2*beta + 6*eps_*(3*D*psi - k**2*beta)),
         -4*k**2*psi - 4*k**2*(U - phi) + 2*ac_*k**2*phi - R,
         4*k**2*D*psi - 2*eps_*k**2*(3*D*psi - k**2*beta) + D*R,
         4*k**2*(U - phi) + 4*k**2*C_*U]
    X = [psi, phi, beta, U]
    M = sp.Matrix([[sp.diff(e_, x_) for x_ in X] for e_ in E]); S = sp.Matrix([-e_.subs({x_: 0 for x_ in X}) for e_ in E])
    return M, S
M0, S0 = block(0, -c2, ac)
det00 = sp.factor(M0.subs(w, 0).det())                               # non-zero for c_2 != 0 (L340 H1): solve at omega = 0
sol0 = M0.subs(w, 0).LUsolve(S0.subs(w, 0))
psiN = -R / (4 * k**2)
static_ratio = sp.simplify(sol0[0] / psiN)
GN = sp.simplify(Gs * static_ratio)
ratio = sp.simplify(Gcos / GN)
# Frusciante & Benetti 2020 eq. (9): G_c = (eta - 2 xi)/(1 - 3 lambda) G_N, with xi = 1, eta = alpha_c, lambda = 1 + c_2
FB = sp.simplify((ac - 2) / (1 - 3 * (1 + c2)))
P(f"    Friedmann (vary N, set N = 1): {fried_H} = 0")
P(f"    H^2 = {H2}")
P(f"    => G_cos = {Gcos};  L340 static block at C = 0 (det M(0) = {det00}): psi/psi_N = {static_ratio}  => G_N = {GN}")
P(f"    G_cos/G_N = {sp.factor(ratio)};   Frusciante & Benetti eq. (9) at xi = 1, eta = alpha_c, lambda = 1 + c_2: {sp.factor(FB)}")
g1_ok = sp.simplify(Gcos - Gs / (1 + sp.Rational(3, 2) * c2)) == 0 and sp.simplify(ratio - FB) == 0
OUT["numbers"]["G1"] = {"G_cos": str(Gcos), "G_N": str(GN), "ratio": str(sp.factor(ratio)), "FB_eq9": str(sp.factor(FB))}
check("G1 C-H/K's FRW Hamiltonian constraint gives G_cos = G/(1 + 3c_2/2); its static block gives G_N = G/(1 - alpha_c/2); "
      "G_cos/G_N = (2 - alpha_c)/(2 + 3c_2) is exactly the published Horava-gravity relation at xi = 1",
      f"G_cos/G_N = {sp.factor(ratio)}", g1_ok,
      "the published cosmological constraints on (lambda, eta) at xi = 1 apply to C-H/K's lambda-channel with lambda - 1 = c_2, eta = alpha_c")

# ============================================================================================ G2 published bounds
banner("G2  THE PUBLISHED BOUNDS (Frusciante & Benetti 2020, Table III, 95% CL) against L340's window")
# (dataset, massive neutrinos?, |G_c/G_N - 1| 95% upper limit, log10(lambda - 1) 95% upper limit or None)
FB_TABLE = [("BKP (Planck18 TT,TE,EE+lowE + BK15)",               False, 0.35e-2, None),
            ("BKP + Planck lensing + DES-Y1 + Pantheon",          False, 0.19e-2, -3.2),
            ("BKP + Planck lensing + DES-Y1 + JLA",               False, 0.27e-2, -3.1),
            ("BKP, massive nu",                                   True,  0.44e-2, None),
            ("BKP + lensing + DES-Y1 + Pantheon, massive nu",     True,  0.22e-2, -2.8),
            ("BKP + lensing + DES-Y1 + JLA, massive nu",          True,  0.28e-2, -2.8)]
if MUTATE:   # Audren, Blas, Lesgourgues & Sibiryakov 2013 (WMAP7 + SPT + WiggleZ): |G_N/G_c - 1| < 0.018 (95%)
    FB_TABLE = [("WMAP7 + SPT + WiggleZ (Audren+2013)", False, 0.018 / 1.018, None)]
AC_REF = 1e-9
def c2_ceiling_from_G(B, acv=AC_REF):
    # 1 - G_c/G_N = (alpha_c + 3c_2)/(2 + 3c_2) < B  <=>  c_2 < (2B - alpha_c)/(3(1 - B))
    return (2 * B - acv) / (3 * (1 - B))
rows = []
for name, nu, Gb, l10 in FB_TABLE:
    cG = c2_ceiling_from_G(Gb)
    cL = 10**l10 if l10 is not None else float("nan")
    ceil = min(cG, cL) if l10 is not None else cG
    dev_floor = (AC_REF + 3 * C2_FLOOR) / (2 + 3 * C2_FLOOR)
    zeq = dev_floor / (Gb / 1.645)                                   # Gaussian-equivalent, indicative only
    rows.append((name, nu, Gb, l10, cG, cL, ceil, C2_FLOOR / ceil, zeq))
    P(f"    {name:48s} |G_c/G_N-1| < {Gb:.2e} -> c_2 < {cG:.2e}" + (f";  log10(lambda-1) < {l10} -> c_2 < {cL:.1e}" if l10 else "") +
      f";  floor/ceiling = {C2_FLOOR / ceil:5.1f};  ~{zeq:.1f} sigma (Gaussian-equivalent)")
P(f"    L340 window: floor {C2_FLOOR:.2e} (tracking), ceiling {C2_BBN:.3f} (BBN) -- at the floor 1 - G_c/G_N = "
  f"{(AC_REF + 3 * C2_FLOOR) / (2 + 3 * C2_FLOOR):.4f}")
all_excl = all(r_[7] > 1.0 for r_ in rows)
loosest, tightest = max(r_[6] for r_ in rows), min(r_[6] for r_ in rows)
OUT["numbers"]["G2"] = {"floor": C2_FLOOR, "bbn_ceiling": C2_BBN,
                        "rows": [dict(zip(("dataset", "massive_nu", "Gc_bound", "log10_lam_bound", "c2_from_G", "c2_from_lam",
                                           "c2_ceiling", "floor_over_ceiling", "z_equiv"), r_)) for r_ in rows],
                        "ceiling_range": [tightest, loosest]}
check("G2 L340's lambda-channel window is EXCLUDED by Planck-era cosmology: every published dataset combination puts the "
      "95% ceiling on c_2 below the tracking floor 7.3e-3",
      f"ceilings {tightest:.1e} .. {loosest:.1e}; floor/ceiling {min(r_[7] for r_ in rows):.1f} .. {max(r_[7] for r_ in rows):.1f}",
      all_excl, "the BBN ceiling 0.067 quoted in L340 is superseded; the surviving range is c_2 <~ 0.6-2.9e-3")

# ============================================================================================ G3 growth cross-check
banner("G3  CROSS-CHECK: the growth mismatch G_N/G_cos that L342's B2 omitted (switch off in the web)")
c = 2.99792458e8; Mpc = 3.0856775814913673e22; Gn = 6.67430e-11
h = 0.6736; om_b, om_c = 0.02237, 0.1200; T_CMB = 2.7255; N_eff = 3.046; ns = 0.965
H0 = 100*h*1e3/Mpc; rho_crit0 = 3*H0**2/(8*math.pi*Gn)
Og = (4*5.670374419e-8*T_CMB**4/c**3)/rho_crit0; Or = Og*(1 + N_eff*(7/8)*(4/11)**(4/3))
Ob, Oc = om_b/h**2, om_c/h**2; Om = Ob + Oc; OL = 1 - Om - Or; SIG8 = 0.811
def T_EH98(kk):                                                      # L342's transfer function, unchanged
    th = T_CMB/2.7; s = 44.5*math.log(9.83/(Om*h*h))/math.sqrt(1 + 10*om_b**0.75)
    ag = 1 - 0.328*math.log(431*Om*h*h)*(Ob/Om) + 0.38*math.log(22.3*Om*h*h)*(Ob/Om)**2
    ge = Om*h*(ag + (1 - ag)/(1 + (0.43*kk*s/h)**4)); q = kk*th*th/ge
    L = math.log(2*math.e + 1.8*q); Cc_ = 14.2 + 731.0/(1 + 62.5*q); return L/(L + Cc_*q*q)
def Wth(x): return 3*(math.sin(x) - x*math.cos(x))/x**3
def growth_D(gratio, z_i=1000.0):
    # D'' + (2 + dlnH/dlnA) D' = (3/2) (G_N/G_cos) Omega_m(a) D  -- the Friedmann-normalised Omega_m(a) and H(a) are
    # those an observer infers; the mismatch enters only through the Poisson equation's G_N (Audren+2015 effect (i))
    Ez = lambda A: math.sqrt(Or/A**4 + Om/A**3 + OL); dlnH = lambda A: 0.5*(-4*Or/A**4 - 3*Om/A**3)/Ez(A)**2
    sol = solve_ivp(lambda Nn, Y: [Y[1], 1.5*gratio*(Om/math.exp(3*Nn)/Ez(math.exp(Nn))**2)*Y[0] - (2 + dlnH(math.exp(Nn)))*Y[1]],
                    (math.log(1/(1 + z_i)), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-10, atol=1e-14)
    return sol.y[0][-1]
D_lcdm = growth_D(1.0)
g3 = []
for c2v in (C2_FLOOR, 0.02, C2_BBN, 1.6e-3, 6.3e-4):
    gr = (2 + 3*c2v)/(2 - AC_REF)                                     # G_N/G_cos
    s8 = SIG8*growth_D(gr)/D_lcdm
    g3.append((c2v, gr, s8))
    P(f"    c_2 = {c2v:.2e}: G_N/G_cos = {gr:.5f}  -> sigma_8 = {s8:.4f}  ({(s8/SIG8 - 1)*100:+.2f}% vs the same primordial amplitude)")
s8_floor = g3[0][2]
PL_S8_ERR = 0.006                                                    # Planck 2018 TT,TE,EE+lowE+lensing: sigma_8 = 0.811 +/- 0.006
c2_b2 = brentq(lambda c2v: growth_D((2 + 3*c2v)/(2 - AC_REF))/D_lcdm - 1.02, 1e-5, 0.05)
P(f"    at L340's floor: sigma_8 shift {s8_floor - SIG8:+.4f} = {(s8_floor - SIG8)/PL_S8_ERR:.1f} x Planck's +/-{PL_S8_ERR}; "
  f"L342's own B2 criterion (sigma_8 within 2% of 0.811) fails for c_2 > {c2_b2:.1e}, i.e. across L340's whole window")
OUT["numbers"]["G3"] = {"rows": [dict(zip(("c2", "GN_over_Gcos", "sigma8"), r_)) for r_ in g3], "c2_B2_2pct": c2_b2}
check("G3 (cross-check) the G_N/G_cos growth mismatch at L340's floor shifts sigma_8 by several times Planck's precision -- "
      "the same order as the published exclusion; L342's B2 sigma_8 = 0.810 omitted it", f"sigma_8 = {s8_floor:.4f} at c_2 = {C2_FLOOR:.1e} "
      f"({(s8_floor - SIG8)/PL_S8_ERR:.1f} x 0.006)", (s8_floor - SIG8)/PL_S8_ERR > 3,
      "growth-only estimate; the MCMC of G2 is the load-bearing statement", load_bearing=False)

# ============================================================================================ G4 what survives
banner("G4  WHAT SURVIVES AT THE CEILINGS: phantom tracking in the deep-MOND outskirts (KM2's exact law)")
def h_rar(y): return y / np.expm1(np.sqrt(y))
def dh_rar(y, e=1e-6): return (h_rar(y*(1 + e)) - h_rar(y*(1 - e)))/(2*y*e)
Y_P = brentq(lambda y: dh_rar(y), 1.0, 5.0); H_P = h_rar(Y_P)
def nu_mono(y):                                                      # L340's A1 kernel (as in KM2)
    return 1.0 + h_rar(min(y, Y_P))/y if y <= Y_P else 1.0 + (H_P + 0.05*H_P*math.log((y + Y_P)/(2*Y_P)))/y
def CL(y, e=1e-5):
    f = lambda yy: yy*nu_mono(yy)
    return (f(y*(1 + e)) - f(y*(1 - e)))/(2*y*e) - 1.0
def R_avg(Cv, c2v, v_kms):
    cs = CKMS*math.sqrt(c2v/(Cv*(2 + 3*c2v)))
    if v_kms >= cs: return cs, float("nan")
    mu = np.linspace(0, 1, 20001); uu = v_kms*mu
    Rv = 1 + Cv/(1 + Cv)*uu**2/(cs**2 - uu**2)
    return cs, float(_trap(Rv, mu) - 1.0)
KIDS_PREC = 0.15                                                     # KM2's outer-bin precision
g4 = []
for c2v in (tightest, 1.6e-3, loosest, C2_FLOOR):
    for yv in (1e-4, 1e-3):
        for dirn, Cv in (("T", nu_mono(yv) - 1.0), ("L", CL(yv))):
            for vv in (300.0, 350.0, 620.0):
                cs, dR = R_avg(Cv, c2v, vv)
                g4.append((c2v, yv, dirn, Cv, cs, vv, dR))
for c2v in (tightest, loosest, C2_FLOOR):
    sel = [r_ for r_ in g4 if r_[0] == c2v and r_[2] == "T"]
    P(f"    c_2 = {c2v:.1e}:  " + ";  ".join(f"y={r_[1]:.0e} v={r_[5]:.0f}: c_s={r_[4]:.0f} "
                                            + ("LEFT BEHIND" if math.isnan(r_[6]) else f"<R-1>={r_[6]*100:.1f}%") for r_ in sel))
at_ceil = [r_ for r_ in g4 if r_[0] in (tightest, loosest)]
max_amp = max((r_[6] for r_ in at_ceil if not math.isnan(r_[6])), default=0.0)
n_left = sum(1 for r_ in at_ceil if math.isnan(r_[6]))
floor_amp = max(r_[6] for r_ in g4 if r_[0] == C2_FLOOR and not math.isnan(r_[6]))
typ = [r_[6] for r_ in g4 if r_[0] == tightest and r_[1] == 1e-4 and r_[2] == "T" and r_[5] == 350.0][0]
OUT["numbers"]["G4"] = {"rows": [dict(zip(("c2", "y", "dir", "C", "c_s", "v", "dR_avg"), r_)) for r_ in g4],
                        "max_amp_at_ceilings": max_amp, "n_left_behind_at_ceilings": n_left, "max_amp_at_old_floor": floor_amp}
check("G4 at the cosmological ceilings the phantom still tracks, but the deep-MOND outskirts are amplified by up to "
      "tens of per cent (above KiDS's ~15% outer-bin precision) and fast outskirts are left behind; at L340's old floor the "
      "same numbers were a few per cent", f"max <R-1> at ceilings {max_amp*100:.0f}%, left-behind cells {n_left}; typical galaxy "
      f"(350 km/s, y 1e-4, tightest ceiling) {typ*100:.0f}%; old floor max {floor_amp*100:.1f}%",
      max_amp > KIDS_PREC and floor_amp < KIDS_PREC,
      "KM2's T1 moves from below reach to at-or-above KiDS precision: a CMB-frame-velocity split of stacked lensing now "
      "tests the surviving range", load_bearing=False)

# ============================================================================================ G5 the construction
banner("G5  A LAMBDA-CHANNEL THAT VANISHES ON FRW: -c_2 (K - <K>_Sigma)^2 (symbolic)")
_, H2_sub, Gcos_sub = friedmann(minisuperspace(0))                  # on FRW K = <K>_Sigma on every leaf: the term is 0
ratio_sub = sp.simplify(Gcos_sub / GN)
# for a Fourier mode k != 0 the leaf average of delta K vanishes, so the quadratic term is L340's term exactly:
x_, L_ = sp.symbols('x L_box', positive=True); kk_ = 2*sp.pi*sp.Symbol('n', integer=True, positive=True)/L_
dK = sp.Symbol('A') * sp.cos(kk_ * x_)
avg = sp.simplify(sp.integrate(dK, (x_, 0, L_)) / L_)
P(f"    FRW with the subtracted term: H^2 = {H2_sub};  G_cos = {Gcos_sub};  G_cos/G_N = {sp.factor(ratio_sub)}")
P(f"    leaf average of a k = 2 pi n/L mode on the closed leaf: <delta K> = {avg}  -> the k != 0 block is L340's, verbatim")
P("    equivalently: -c_2 int N sqrt(h) K^2 + 2 c_2 <K>(t) dV/dt - c_2 <K>(t)^2 V_N(t): a global (sequestering-like) term,")
P("    leaf-nonlocal in the same sense as C-H's heat kernel; well defined on C-H's closed leaves (T^3)")
g5_ok = (sp.simplify(ratio_sub - (1 - ac / 2)) == 0) and avg == 0
OUT["numbers"]["G5"] = {"G_cos": str(Gcos_sub), "ratio": str(sp.factor(ratio_sub)), "leaf_average_kmode": str(avg)}
check("G5 the leaf-average-subtracted lambda-term leaves the Friedmann equation GR's (G_cos/G_N - 1 = -alpha_c/2 ~ 1e-9) "
      "and acts on every k != 0 mode exactly as L340's term, so L340's tracking (H1) is unchanged",
      f"G_cos/G_N = {sp.factor(ratio_sub)}; <delta K>_k = {avg}", g5_ok,
      "removes Audren+2015's effect (i) at its root; residual lambda-effects on horizon-scale perturbations (O(c_2 (aH/k)^2)) "
      "are not computed here -- a construction, not a derivation", load_bearing=False)

banner("VERDICT")
P(f"""  C-H/K's lambda-channel, at the strength L340 needs for phantom tracking (c_2 >= {C2_FLOOR:.1e}), is excluded by Planck-era
  cosmology: on FRW the candidate IS low-energy Horava gravity with lambda - 1 = c_2 (G1), and the published fits cap
  c_2 at {tightest:.1e} .. {loosest:.1e} (95%, every dataset combination; G2).  A growth-only cross-check lands at the same
  order (G3).  Inside the cosmological ceiling the phantom still tracks galaxy bodies, but deep-MOND outskirts are
  amplified by up to {max_amp*100:.0f}% and fast ones are left behind (G4): KM2's 'below reach' becomes 'at KiDS
  precision'.  The conflict disappears if the lambda-term acts only on the leaf-inhomogeneous part of K (G5) -- a
  global term on C-H's closed leaves, offered as a construction.  Time {time.time() - T0:.0f} s.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
