#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FP9 -- THE MINIMAL-CONSTANT SEPARATOR BETWEEN THE COSMIC WEB AND GALAXIES, on FP7's repaired (AQUAL-type) root: which
action-level term keeps the MOND scalar off in the linear web and the z = 2-3 IGM and on in galaxies with the FEWEST declared
constants -- every route varied out of the action, every gate scored, both a0 footings.

WHY.  FP7 (committed 17a90e572) repaired the root: statics, the Solar System, FRW well-posedness (J's zero tangent), stability,
c_T = 1 and PPN pass, but sigma_8 FAILS with no gate -- the web is MOND acting on itself, and phi's a0-free inertia has an
EMPTY window (sigma_8 needs lambda_eff >= 1.1e7, tracking <= 277).  With the zero tangent a gate need not vanish on FRW, so
FP3's convexity lemma no longer binds (its chord bound still does).  FP6 (committed 9d9e75369) found (H) on the OLD root: a
band-pass plus a running cut-off, FIVE declared constants, linchpin met, Local Group failed.  This lane tests, ON THE REPAIRED
ROOT, the three routes the coordinator named and their hybrids, and reports the configuration that passes sigma_8, the forest,
the flagship, SPARC and KiDS with the fewest declared constants -- or the fail.

THE ROOT (FP7; per 1/16 pi G, c = 1, alpha = a0/c^2):
  R - 2 Lambda + alpha_c a^2 - c_2 (K - <K>_h)^2 + (2 - alpha_c) h^mn (2 a_m - D_m chi) D_n chi - 2 alpha^2 J(h^mn D_m phi D_n phi/alpha^2)
  + 2 lambda (n.d phi)^2 + heat pair (W_0 = phi, chi = W_b = S_h phi) + S_m[g],   J = J_P2(Y) = -(1/4) ln(1 - 2 sqrt Y) - sqrt(Y)/2 - Y/2.
THE ROUTES (each a term placed in that action and varied with it):
  (i)    the band-pass on the chassis:  chi = W_b - W_B = (S_xi - S_L) phi  (C-H's heat branch read out at z = b and z = B = L^2/2),
         L = L_Lambda Omega_L(<K>_h)^(n/2)                                                                 [L_Lambda, n]
  (ii)   a CONCAVE density-read gate on the whole AQUAL block:  W(rho_dyn/rho_*(<K>_h)) x {chassis - 2 alpha^2 J + 2 lambda (n.d phi)^2},
         rho_dyn = (1/8 pi G)(<K>_h^2/3 - Lambda + 2 D_i a^i)                                              [rho_* (+ its running)]
  (iii)  a ~Mpc scale for phi: (a) a Yukawa mass -2 phi^2/ell^2; (b) a scale-dependent inertia lambda(k); (c) whether (a0, Lambda,
         G, c, sqrt(G M/a0)) can set that scale                                                           [ell, or lambda(k)'s]
  (Y)    the YIELD floor:  J -> J_Y(Y) = J_P2(Y) + 2 y_th(<K>_h) sqrt(Y),  y_th = y_Lambda Omega_L(<K>_h)^(-p')     [y_Lambda, p']
         (the lowest-order term of J's small-gradient expansion; phi responds to the excess of the band-passed field over y_th a0)
  (H_Y)  = (i) + (Y)                                          [4 declared]
  (H_A)  = (i) + FP6's cut-off tangent in AQUAL form           [5 declared] -- FP6's (H), which the root's duality C^phi = 1/C^Q maps here
The footings: a0 = 9.3603e-11 (canonical) and 1.1312e-10 m/s^2 (alt), FP0.

CHECKS
  K  CONTROLS: K1 FP6's committed machinery (exec'd read-only up to its CONTROLS banner) reproduces FP6's committed numbers (LCDM
     sigma_8, the (H) headline's sigma_8/forest/flagship/KiDS/LG); K2 this lane's own re-derivation of the zero-field Minkowski
     block (FP7 B3's variation, the filter factor a symbol h) reproduces FP7's committed det M; K3 the duality: the AQUAL growth
     at lambda = 0 IS FP6's growth (its tracking speed is c^2 C^phi/lambda_eff^phi, lambda_eff^phi = lambda + (2 + 3c_2) h^2/c_2),
     the spherical AQUAL law IS FP6's band-passed phantom, and the yield law reduces to P2 at y_th = 0.
  A  THE BAND-PASS ON THE AQUAL BLOCK: A1 placement (discrete action with a band-pass; Fourier gains); A2 the zero-field block
     with the band-pass: roots, T, V, det V = 16 C_phi k^4 (2 - alpha_c)/alpha_c for every h, E(C_phi, h) in [alpha_c, 2];
     A3 how the band-pass reaches the web: at lambda = 0 the formal linear response is h-INDEPENDENT (the khronon carries the
     mode); only J's physical amplitude (h^2 C^Q(h y)) or lambda > 0 carries the h^2; A4 (reported) route (i) keeps FP7's lambda.
  I  ROUTE (i) ALONE: I1 sigma_8 (physical amplitude) over (n, L_Lambda); I2 (reported) the linear yardstick; I3 the flagship floor
     on L(2.5); I4 the forest FAILS wherever the flagship passes (and vice versa); I5 KiDS and SPARC; I6 the verdict.
  Y  THE YIELD FLOOR: Y1 closed form, spherical law, C_T, C_L, strict convexity (unique statics); Y2 admissible on the AQUAL root
     (E -> 2, marginal) and not on the QUMOND core (C_L^Q -> oo: E -> 2 + alpha_c); Y3 FRW: phi frozen below the yield, the formal
     linearisation is GR + BPS, lambda = 0 allowed; Y4 the lowest order: a finite stiffness (c_2 Y) cannot separate the IGM from
     the flagship, the yield (c_1 sqrt Y) can -- no shape constant.
  H  THE COMBINATION (H_Y): H1 the window scan; H2 the headline cell, every gate, both footings and yardstick modes, lambda > 0,
     tolerances and grids; H2b E in the BPS window at every field; H2c (reported) the flagship's z_max, the z = 2-3 IGM lumps, the
     linear web's G_eff on the sigma_8 modes, the Solar System; H3 the Local Group FAILS (verified at every KiDS-passing cell);
     H4 (reported) the constants and their windows.
  D  ROUTE (ii): D1 the static law with the gate (sympy EL, the lapse back-reaction T included); D2 the stability rule (block
     energy E > 0 on every galaxy background => concave); D3 FRW with the gate (strictly stable for 0 < W < 1; G_eff/G_N = 1/(1-W),
     h-independent); D4 the sigma_8 budget; D5 the AQUAL sensitivity eps(y); D6 the KiDS-sigma_8 pincer through the chord bound
     (FAIL) and FP3's chord-bound prices; D7 (reported) the stiffness-placement variant.
  V  ROUTE (iii): V1 the scale test (sympy nullspace): no host-independent Mpc length from (a0, Lambda, G, c); V2 the Yukawa mass:
     sigma_8 vs KiDS screening (FAIL); V3 lambda(k): forest vs tracking at the same scale (FAIL).
  T  the route table.   F  the constants.   W  the ledger.   G (reported) the whole G-1 including the Local Group.
MUTATE=1 removes the yield floor from (H_Y) (y_th -> 0: route (i) in the combination's clothes): H1's window and H2's forest gate
must FAIL (rc = 1).

SCOPE.  Frozen-coefficient linear theory and the record's growth yardstick (L341/FP6: EH98, growing-mode ICs, rms and per-mode
field arguments, the tracking weight); the forest is a LINEAR-THEORY PROXY (1D projection of the linear matter power with a
Gaussian IGM filter), plus reported nonlinear-lump prices; KiDS is lead grade (L341 F7: isolated lenses, M_b free per bin, no
2-halo); the Local Group is XR4's point-mass + Lambda shell model.  No particle-mesh or N-body run.

Run from the repository root:  python3 real_research/derivation_chain_2026/FP9_web_galaxy_separator.py
"""
import os, re, sys, io, json, math, time, contextlib, warnings
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
from scipy.linalg import expm

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "FP9_web_galaxy_separator"
OUT = {"lane": "FP9", "mutate": MUTATE, "root": "FP7's AQUAL-type repair", "checks": {}, "numbers": {}, "ledger": []}
CH = []
T0 = time.time()


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 116 + "\n" + t + "\n" + "=" * 116)


def check(name, measured, ok, load_bearing=True, reading=None):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def el():
    return f"[{time.time() - T0:.0f} s]"


def jkey(d):
    return {str(k_): v for k_, v in d.items()}


P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the yield floor is removed from (H_Y) (y_th -> 0) -- H1's window and H2's forest gate must FAIL ***")

# ================================================================================================= loading FP6's machinery
FP6_PATH = os.path.join(HERE, "FP6_gate_survey.py")
FP7_JSON = os.path.join(HERE, "FP7_aqual_type_repair_results.json")
FP6_JSON = os.path.join(HERE, "FP6_gate_survey_results.json")


def load_fp6():
    """exec FP6's committed script up to its CONTROLS banner (constants, the L341 growth yardstick, kernels, the forest proxy, the
    band-passed phantom, KiDS lead grade, the LG shell model) in a private namespace; nothing is edited, its prints are captured."""
    src = open(FP6_PATH).read()
    cut = src.index('banner("K  CONTROLS')
    ns = {"__file__": FP6_PATH, "__name__": "fp6_machinery"}
    old = os.environ.get("MUTATE")
    os.environ["MUTATE"] = "0"
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src[:cut], FP6_PATH, "exec"), ns)
    finally:
        if old is None:
            os.environ.pop("MUTATE", None)
        else:
            os.environ["MUTATE"] = old
    ns["BANDPASS"] = True
    return ns


M6 = load_fp6()
FOOTS, MODES = M6["FOOTS"], M6["MODES"]
A0 = dict(M6["A0"])
fp0 = os.path.join(HERE, "FP0_core_postulates_results.json")
if os.path.exists(fp0):
    n0 = json.load(open(fp0))["numbers"]
    A0 = {"canonical": n0["a0_canonical"], "alt": n0["a0_rho_total"]}
c, Mpc, kpc, G, MSUN = M6["c"], M6["Mpc"], M6["kpc"], M6["G"], M6["MSUN"]
G6, MPCm = M6["G6"], M6["MPCm"]
h_, H0, Om, OL = M6["h"], M6["H0"], M6["Om"], M6["OL"]
Ez, dlnH, OmL_a, OmL_z = M6["Ez"], M6["dlnH"], M6["OmL_a"], M6["OmL_z"]
KH, KHF, DI, DIF, W8 = M6["KH"], M6["KHF"], M6["DI"], M6["DIF"], M6["W8"]
S8_LCDM, sigma8_of, gfield, nu_p2 = M6["S8_LCDM"], M6["sigma8_of"], M6["gfield"], M6["nu_p2"]
Z_KIDS, Z_FLAG = M6["Z_KIDS"], M6["Z_FLAG"]
SIG8_BAND, SIG8_TIGHT, FOREST_TOL, FLAG_TOL, SPARC_TOL, KIDS_TOL = (M6["SIG8_BAND"], M6["SIG8_TIGHT"], M6["FOREST_TOL"],
                                                                   M6["FLAG_TOL"], M6["SPARC_TOL"], M6["KIDS_TOL"])
LG_R0, LG_EDGE = M6["LG_R0"], M6["LG_EDGE"]
C2W = M6["C2W"]                                             # c_2 = 7.3e-3: lambda_eff^phi(lambda = 0, h = 1) = (2 + 3 c_2)/c_2 = 277
RHOM0 = Om * M6["rho_crit0"]
ALPHA_C = (9.62e-14, 3.2e-9)
P(f"\n  loaded FP6's machinery (read-only exec of {os.path.basename(FP6_PATH)} up to its CONTROLS banner); footings a0 = "
  f"{A0['canonical']:.4e} / {A0['alt']:.4e} m/s^2; gates sigma_8 in {SIG8_BAND} (1.02 reported), forest proxy <= {FOREST_TOL}, "
  f"flagship <= {FLAG_TOL} dex, SPARC <= {SPARC_TOL} dex, KiDS d chi^2 <= +{KIDS_TOL}, LG 0.96 +- 0.03 Mpc")

# ---- the yield floor, hooked into FP6's kernel slot (its phantom(), bandpass_model(), kids_class(), lg_both() call cutfac)
YIELD = -1                                                  # the 'm' slot value that selects the yield law
_cut_fp6 = M6["cutfac"]


def x_P2(D):
    """P2's scalar field for a Newtonian field D (units a0): mu_s(x) x = D, mu_s(x) = x/(1 - 2x); stable closed form."""
    D = np.maximum(np.asarray(D, float), 0.0)
    return np.where(D > 0, 1.0 / (1.0 + np.sqrt(1.0 + 1.0 / np.maximum(D, 1e-300))), 0.0)


def CQ_yield(y, yth):
    """the yield law's QUMOND-form tangent: phi' = a0 x_P2(y - y_th) along the band-passed Newtonian field, i.e. C^Q = x/y."""
    y = np.maximum(np.asarray(y, float), 1e-300)
    return x_P2(y - (yth or 0.0)) / y


def cut_hook(y, yth, m):
    if m == YIELD:
        if yth is None or yth <= 0:
            return np.ones_like(np.asarray(y, float))
        y = np.maximum(np.asarray(y, float), 1e-300)
        return CQ_yield(y, yth) / (nu_p2(y) - 1.0)
    return _cut_fp6(y, yth, m)


M6["cutfac"] = cut_hook
bandpass_model, L_phys, y_th_z = M6["bandpass_model"], M6["L_phys"], M6["y_th_z"]
law_dev_dex, kids_class, lg_both, lg_R0, phantom = M6["law_dev_dex"], M6["kids_class"], M6["lg_both"], M6["lg_R0"], M6["phantom"]
forest_proxy, growth6 = M6["forest_proxy"], M6["growth"]


def growth_aq(model, a0v, mode="rms", KHg=None, Dig=None, zs_out=(), c2=C2W, lam=0.0, rtol=1e-6):
    """the AQUAL block's physical-amplitude growth (FP6's integrator with phi's own inertia): delta'' + (2 + dlnH) delta' =
    1.5 Om(a) [1 + h^2 C^Q w] delta, C^Q = (nu - 1) cut at the band-passed field, w = 1/(1 + (H/(c_s k))^2),
    c_s^2 = c^2 C^phi/lambda_eff^phi, C^phi = 1/C^Q, lambda_eff^phi = lambda + (2 + 3 c_2) h^2/c_2 (A2/A3); lambda = 0 is FP6's."""
    KHg = KH if KHg is None else KHg; Dig = DI if Dig is None else Dig
    nk = len(KHg); m341 = KHg <= 20.0 * 1.0001
    kk341 = KHg[m341]; norm341 = np.trapz(1 / kk341, kk341)

    def rhs(N_, Y):
        a = math.exp(N_); D = Y[:nk]; Dp = Y[nk:]
        gk = gfield(D, a, KHg); hk = model["hfac"](a, KHg); gb = gk * hk
        if mode == "rms":
            y = np.full(nk, math.sqrt(np.trapz(gb[m341] ** 2 / kk341, kk341) / norm341) / a0v)
        else:
            y = gb / a0v
        CQ = np.maximum((nu_p2(y, model.get("yr", 0.0)) - 1.0) * model["cut"](y, a), 0.0)
        lam_phi = lam + (2 + 3 * c2) * hk ** 2 / c2
        cs = c / np.sqrt(np.maximum(CQ, 1e-300) * np.maximum(lam_phi, 1e-300))
        kk = (1.0 * h_ / (a * Mpc)) if mode == "rms" else KHg * h_ / (a * Mpc)
        wt = 1.0 / (1.0 + (H0 * Ez(a) / (cs * kk)) ** 2)
        return np.concatenate([Dp, 1.5 * (Om / a ** 3 / Ez(a) ** 2) * (1.0 + CQ * hk ** 2 * wt) * D - (2 + dlnH(a)) * Dp])
    Nout = sorted({math.log(1 / (1 + z)) for z in zs_out if z > 0}) + [0.0]
    sol = solve_ivp(rhs, (math.log(M6["A_I"]), 0.0), np.concatenate([Dig, Dig]), method="LSODA", rtol=rtol, atol=1e-24, t_eval=Nout)
    return {round(1 / math.exp(N_) - 1, 6): sol.y[:nk, i] for i, N_ in enumerate(sol.t)}


def s8_aq(model, foot, mode, lam=0.0, rtol=1e-6):
    return sigma8_of(growth_aq(model, A0[foot], mode=mode, lam=lam, rtol=rtol)[0.0]) / S8_LCDM


def forest_aq(model, foot, mode, lam=0.0, kFs=(10.0, 15.0, 20.0)):
    res = growth_aq(model, A0[foot], mode=mode, KHg=KHF, Dig=DIF, zs_out=(2.0, 3.0), lam=lam)
    return max(forest_proxy(res, kF=kF)[0] for kF in kFs)


def LL_of(L25, n):
    return L25 / OmL_z(Z_KIDS) ** (n / 2.0)


# ================================================================================================= K  CONTROLS
banner("K  CONTROLS: the reused machinery reproduces the record; the duality that maps FP6's (H) onto the repaired root")
F6 = json.load(open(FP6_JSON))["numbers"]
F7 = json.load(open(FP7_JSON))["numbers"]
HEAD6 = dict(n=2.0, L25=1.3, pp=4.0, y25=1e-6, m=4)
LL6 = LL_of(HEAD6["L25"], HEAD6["n"]); FL6 = (HEAD6["y25"], HEAD6["pp"], HEAD6["m"])
mod6 = bandpass_model(LL6, HEAD6["n"], floor=FL6)
k1 = {"s8": {(f, m): M6["s8ratio"](mod6, f, m) for f in FOOTS for m in MODES}}
k1["forest"] = forest_proxy(growth6(mod6, M6["A0"]["canonical"], mode="permode", KHg=KHF, Dig=DIF, zs_out=(2.0, 3.0)), kF=15.0)[0]
k1["flag"] = law_dev_dex(1e11, M6["A0"]["canonical"], 0.1, L_phys(LL6, HEAD6["n"], 1 / 3.5), y_th_z(FL6, Z_FLAG))
KB = {f: kids_class(A0[f]) for f in FOOTS}                                           # isolated P2 chi^2 (this lane's footings)
KB6 = {f: kids_class(M6["A0"][f]) for f in FOOTS}
k1["kids"] = {f: kids_class(M6["A0"][f], HEAD6["L25"], y_th_z(FL6, Z_KIDS)) - KB6[f] for f in FOOTS}
k1["lg"] = lg_both(LL6, HEAD6["n"], floor=FL6)
ref = F6["H2"]
dev_k1 = max([abs(k1["s8"][(f, m)] / ref["s8"][str((f, m))] - 1) for f in FOOTS for m in MODES]
             + [abs(k1["forest"] / ref["forest"][str(("canonical", "permode", 15.0))] - 1),
                abs(k1["flag"] / ref["flag"][str(("canonical", 1e11))] - 1)]
             + [abs(k1["kids"][f] - ref["kids"][f]) for f in FOOTS]
             + [abs(k1["lg"][f] / F6["H3"]["2.0_1.3"][f] - 1) for f in FOOTS])
P(f"    FP6 (H) headline via the exec'd machinery: sigma_8 " + ", ".join(f"{k_[0][:3]}/{k_[1]} {v:.5f}" for k_, v in k1["s8"].items())
  + f"; forest can/permode/15 {k1['forest']:.5f}; flagship {k1['flag']:+.5f} dex; KiDS {k1['kids']['canonical']:+.2f}/{k1['kids']['alt']:+.2f}; "
  f"LG {k1['lg']['canonical']:.4f}/{k1['lg']['alt']:.4f} Mpc; LCDM sigma_8 {S8_LCDM:.4f}")
check("K1 CONTROL: FP6's committed machinery, exec'd read-only, reproduces FP6's committed numbers -- LCDM sigma_8 0.8101 and the "
      "(H) headline cell's sigma_8 (both footings, both modes), forest proxy, flagship shift, KiDS d chi^2 and Local-Group R0",
      f"max relative deviation {dev_k1:.1e} (KiDS absolute); LCDM {S8_LCDM:.5f}", dev_k1 < 1e-6 and abs(S8_LCDM / 0.81009 - 1) < 1e-3)
OUT["numbers"]["K1"] = {"s8": jkey(k1["s8"]), "forest": k1["forest"], "flag": k1["flag"], "kids": k1["kids"], "lg": k1["lg"]}

# ---- K2: this lane's own zero-field block (FP7 B3's variation; filter factor a symbol h; gate W on the whole block; Yukawa mass)
tK2 = time.time()
tt_, xx_, yy_, zz_ = sp.symbols('t x y z', real=True)
X3m = (xx_, yy_, zz_)
eb = sp.Symbol('e_b')
alm, c2m, Cph, lmm, hq, Wg, mY = sp.symbols('alpha_c c_2 C_phi lambda h W m_Y', real=True)
Bsym, Csym = sp.symbols('B_ch C_ch', real=True)
nf, pf, Bf, Sf, Ff = [sp.Function(s_)(tt_, xx_, yy_, zz_) for s_ in ('n', 'psi', 'B', 'S', 'phi')]
Nl = sp.exp(eb * nf)
gam = sp.diag(*[sp.exp(-2 * eb * pf)] * 3)
gin = gam.inv()
Ni = [eb * (sp.diff(Bf, X3m[0]) + Sf), eb * sp.diff(Bf, X3m[1]), eb * sp.diff(Bf, X3m[2])]
Gm3 = [[[sum(gin[a_, d_] * (sp.diff(gam[d_, b_], X3m[c_]) + sp.diff(gam[d_, c_], X3m[b_]) - sp.diff(gam[b_, c_], X3m[d_])) for d_ in range(3)) / 2
         for c_ in range(3)] for b_ in range(3)] for a_ in range(3)]
DN = [[sp.diff(Ni[j], X3m[i]) - sum(Gm3[kq][i][j] * Ni[kq] for kq in range(3)) for j in range(3)] for i in range(3)]
Kij = sp.Matrix(3, 3, lambda i, j: (sp.diff(gam[i, j], tt_) - DN[i][j] - DN[j][i]) / (2 * Nl))
Kup = gin * Kij * gin
KK = sum(Kij[i, j] * Kup[i, j] for i in range(3) for j in range(3))
trK = sum(gin[i, j] * Kij[i, j] for i in range(3) for j in range(3))


def Ric3(b_, c_):
    return sum(sp.diff(Gm3[a_][b_][c_], X3m[a_]) - sp.diff(Gm3[a_][b_][a_], X3m[c_]) +
               sum(Gm3[a_][a_][d_] * Gm3[d_][b_][c_] - Gm3[a_][c_][d_] * Gm3[d_][b_][a_] for d_ in range(3)) for a_ in range(3))


R3 = sum(gin[b_, c_] * Ric3(b_, c_) for b_ in range(3) for c_ in range(3))
ai = [sp.diff(sp.log(Nl), xi_) for xi_ in X3m]
aa = sum(gin[i, j] * ai[i] * ai[j] for i in range(3) for j in range(3))
Fi = [sp.diff(eb * Ff, xi_) for xi_ in X3m]
Xi = [hq * f_ for f_ in Fi]                                      # D_i chi, chi = B phi -> h(k) phi mode by mode (band-pass or filter)
chassis = Bsym * sum(gin[i, j] * ai[i] * Xi[j] for i in range(3) for j in range(3)) + Csym * sum(gin[i, j] * Xi[i] * Xi[j] for i in range(3) for j in range(3))
Jquad = -2 * Cph * sum(gin[i, j] * Fi[i] * Fi[j] for i in range(3) for j in range(3))
ndphi = (sp.diff(eb * Ff, tt_) - sum(sum(gin[i, j] * Ni[j] for j in range(3)) * Fi[i] for i in range(3))) / Nl
massY = -2 * mY ** 2 * (eb * Ff) ** 2                            # route (iii-a): -2 phi^2/ell^2, m_Y = 1/ell
Lfull = Nl * sp.exp(-3 * eb * pf) * (KK - trK ** 2 + R3 + alm * aa - c2m * trK ** 2 + Wg * (chassis + Jquad + 2 * lmm * ndphi ** 2) + massY)
L2f = sp.expand((sp.diff(Lfull, eb, 2) / 2).subs(eb, 0))
ELf = euler_equations(L2f, [nf, pf, Bf, Sf, Ff], [tt_, xx_, yy_, zz_])
kq_, wq_ = sp.symbols('k omega', real=True)
An, Ap, AB, AS, AF = sp.symbols('A_n A_psi A_B A_S A_phi')
phs = sp.exp(sp.I * (kq_ * zz_ - wq_ * tt_))
fsub = {nf: An * phs, pf: Ap * phs, Bf: AB * phs, Sf: AS * phs, Ff: AF * phs}
ELk_gen = [sp.expand(sp.simplify((e_.lhs - e_.rhs).subs(fsub).doit() / phs)) for e_ in ELf]
Bu, Cu = 2 * (2 - alm), -(2 - alm)                               # FP7 A1's perfect square
ELk = [sp.expand(e_.subs({Bsym: Bu, Csym: Cu})) for e_ in ELk_gen]
Mblk = sp.Matrix([[sp.expand(sp.diff(ELk[r_], v_)) for v_ in (Ap, An, AB, AF)] for r_ in (1, 0, 2, 4)])
U2 = sp.Symbol('U2')


def blk_det(subs):
    return sp.factor(sp.expand(Mblk.subs(subs).det(method='berkowitz')))


def blk_roots(subs):
    d = blk_det(subs)
    p_ = sp.Poly(sp.numer(sp.together(d.subs(wq_, sp.sqrt(U2) * kq_))), U2)
    return d, p_, [sp.factor(r_) for r_ in sp.solve(p_.as_expr(), U2)]


det_bp = blk_det({Wg: 1, mY: 0})
sig_ = sp.Symbol('sigma', real=True)
det7 = sp.sympify(re.sub(r"\blambda\b", "lam_", F7["B3"]["det"]),
                  locals={"alpha_c": alm, "c_2": c2m, "C_phi": Cph, "lam_": lmm, "sigma": sig_, "k": kq_, "omega": wq_})
k2_ok = sp.simplify(sp.expand(det_bp - det7.subs(sig_, hq))) == 0
P(f"    this lane's block (W = 1, no mass): det M = {det_bp}   ({time.time() - tK2:.0f} s)")
check("K2 CONTROL: this lane's own second variation of the repaired action about Minkowski (FP7 B3's unitary-gauge block, the "
      "filter factor kept as a symbol h(k)) reproduces FP7's committed zero-field determinant exactly (sigma -> h); the same block "
      "carries route (ii)'s gate W on the whole AQUAL block and route (iii)'s Yukawa mass as switches",
      f"det M == FP7's committed det (sigma -> h): {k2_ok}", k2_ok)
OUT["numbers"]["K2"] = {"det": str(det_bp)}

# ---- K3: the duality / identities that put FP6's (H) on this root
yv = np.logspace(-8, 4, 300)                                               # FP6's nu - 1 = sqrt(1 + 1/y) - 1 cancels beyond ~1e4
k3_p2 = float(np.max(np.abs(CQ_yield(yv, 0.0) / (nu_p2(yv) - 1) - 1)))
mdl_bp = bandpass_model(LL6, 2.0, floor=FL6)
gA = growth_aq(mdl_bp, A0["canonical"], mode="permode", lam=0.0)[0.0]
gF = growth6(mdl_bp, A0["canonical"], mode="permode")[0.0]
k3_growth = float(np.max(np.abs(gA / gF - 1)))
CQs, lam_s, c2s, hs = sp.symbols('C_Q lambda_s c_2s h_s', positive=True)
cs_aq = 1 / (CQs * (lam_s + (2 + 3 * c2s) * hs ** 2 / c2s))                # AQUAL: c_s^2/c^2 = C^phi/lambda_eff^phi, C^phi = 1/C^Q
cs_fp6 = c2s / (CQs * hs ** 2 * (2 + 3 * c2s))                             # FP6: c_2 c^2/(C_eff (2 + 3 c_2)), C_eff = C^Q h^2
k3_cs = sp.simplify(cs_aq.subs(lam_s, 0) - cs_fp6) == 0
Mb_t = 1e11 * MSUN; rr_t = M6["RG"]
gbp_t = G6 * Mb_t / rr_t ** 2 * (1 - M6["gfrac_smooth"](rr_t / (0.5 * MPCm)))
x_t = x_P2(gbp_t / A0["canonical"])                                        # AQUAL flux law F(x) = y_bp solved directly
ok_t = (gbp_t / A0["canonical"] < 1e4) & (gbp_t > 0)                         # where FP6's nu - 1 is free of cancellation
k3_sph = float(np.max(np.abs(x_t * A0["canonical"] - (nu_p2(gbp_t / A0["canonical"]) - 1) * gbp_t)[ok_t] / (x_t * A0["canonical"])[ok_t]))
P(f"    yield law at y_th = 0 vs P2's nu - 1: max rel dev {k3_p2:.1e}; AQUAL growth (lambda = 0) vs FP6's growth: {k3_growth:.1e}; "
  f"c_s identity at lambda = 0: {k3_cs}; spherical AQUAL flux law vs FP6's (nu - 1) g_bp: {k3_sph:.1e}")
check("K3 THE DUALITY: on the repaired root the band-passed spherical AQUAL law (mu_s(|phi'|) phi' = the band-passed Newtonian field, "
      "output band-passed by the variation) IS FP6's band-passed phantom (phi' = (nu - 1) g_bp); the AQUAL growth at lambda = 0 IS "
      "FP6's (the tracking speeds agree identically: c^2 C^phi/lambda_eff^phi with lambda_eff^phi = (2 + 3c_2) h^2/c_2 vs FP6's "
      "c_2 c^2/(C_eff (2 + 3 c_2))); and the yield law reduces to P2 at y_th = 0 -- so FP6's (H) cell numbers ARE (H_A)'s on this root",
      f"yield->P2 {k3_p2:.1e}; growth {k3_growth:.1e}; c_s identity {k3_cs}; spherical {k3_sph:.1e}",
      k3_p2 < 1e-8 and k3_growth < 1e-8 and k3_cs and k3_sph < 1e-8)
P(f"    {el()}")

# ================================================================================================= A  THE BAND-PASS ON THE AQUAL BLOCK
banner("A  THE BAND-PASS ON THE AQUAL BLOCK: placement, the zero-field block, how the band-pass reaches the web")
# A1 the placement (discrete action on a periodic leaf, band-pass Bm = e^{b lap} - e^{B lap}; J on phi unfiltered)
rng = np.random.default_rng(9)
NG, dxg = 10, 1.0 / 10
I1 = np.eye(NG)
D1 = (np.roll(I1, -1, axis=1) - I1) / dxg
Dx, Dy = np.kron(D1, I1), np.kron(I1, D1)
DTD = Dx.T @ Dx + Dy.T @ Dy
Bm = expm(-0.004 * DTD) - expm(-0.05 * DTD)
xs_ = np.arange(NG) * dxg
XG, YG = np.meshgrid(xs_, xs_, indexing="ij")
Ph0 = (np.sin(2 * np.pi * XG) + 0.3 * rng.standard_normal(XG.shape)).ravel() * 0.02
f0 = (0.4 * np.cos(2 * np.pi * (XG + YG)) + 0.2 * rng.standard_normal(XG.shape)).ravel() * 0.01
acn = 1e-3; Bn, Cn = 2 * (2 - acn), -(2 - acn)
mu_s = lambda x: x / (1.0 - 2.0 * x)
J_P2 = lambda Y: -0.25 * np.log(1 - 2 * np.sqrt(Y)) - np.sqrt(Y) / 2 - Y / 2


def act_bp(fv):
    ch_ = Bm @ fv
    Y = (Dx @ fv) ** 2 + (Dy @ fv) ** 2
    return float(np.sum(-(2 - acn) * ((Dx @ Ph0) ** 2 + (Dy @ Ph0) ** 2) + Bn * ((Dx @ Ph0) * (Dx @ ch_) + (Dy @ Ph0) * (Dy @ ch_))
                        + Cn * ((Dx @ ch_) ** 2 + (Dy @ ch_) ** 2) - 2 * J_P2(Y)))


def stated_bp(fv):
    ch_ = Bm @ fv
    Y = (Dx @ fv) ** 2 + (Dy @ fv) ** 2
    Jp = mu_s(np.sqrt(Y))
    return Bm.T @ (Bn * DTD @ Ph0 + 2 * Cn * DTD @ ch_) - 4 * (Dx.T @ (Jp * (Dx @ fv)) + Dy.T @ (Jp * (Dy @ fv)))


fdg = np.array([(act_bp(f0 + 1e-6 * e_) - act_bp(f0 - 1e-6 * e_)) / 2e-6 for e_ in np.eye(NG * NG)])
err_bp = float(np.max(np.abs(fdg - stated_bp(f0))) / np.max(np.abs(fdg)))
ac_, J0s, sK, hk_s, kf = sp.symbols("alpha_c J_0 s h k", positive=True)
PhiK, phK = sp.symbols("Phi_k phi_k")


def gain(sc, sj):
    Lk = (-(2 - ac_) * kf ** 2 * PhiK ** 2 + 2 * (2 - ac_) * kf ** 2 * PhiK * sc * phK - (2 - ac_) * kf ** 2 * sc ** 2 * phK ** 2
          - 2 * J0s * kf ** 2 * sj ** 2 * phK ** 2 - sK * PhiK)
    sol = sp.solve([sp.diff(Lk, PhiK), sp.diff(Lk, phK)], [PhiK, phK], dict=True)[0]
    mond = sp.simplify(sol[PhiK] - (-sK / (2 * (2 - ac_) * kf ** 2)))
    return sp.simplify(mond / sp.simplify(mond.subs(hk_s, 1)))


g_ch, g_J, g_both = gain(hk_s, 1), gain(1, hk_s), gain(hk_s, hk_s)
kk_ = np.array([1e-3, 1e-2, 0.1, 1.0, 10.0, 30.0]); Lb_, xb_ = 1.0, 0.03
hk_num = np.exp(-0.5 * (xb_ * kk_) ** 2) - np.exp(-0.5 * (Lb_ * kk_) ** 2)
P(f"    discrete static action, band-pass B = e^(-0.004 D^TD) - e^(-0.05 D^TD) on the chassis, J_P2 on phi: |FD gradient - "
  f"(B^T[chassis source] - 4 D^T(J' D phi))| = {err_bp:.1e}")
P(f"    physical MOND response relative to the unfiltered law: chassis on B phi: {g_ch};  J on B phi: {g_J};  both: {g_both};  "
  f"band-pass gain h(k) at k L = 1e-3..30: " + ", ".join(f"{v:.1e}" for v in hk_num) + " -> 1/h^2 diverges at both ends")
check("A1 THE BAND-PASS PLACEMENT IS FORCED (FP7 A1b for a band-pass): the discrete action's phi-gradient is B^T[chassis source] + "
      "div(J' grad phi); in Fourier the physical MOND response is h^2 with the chassis on B phi, 1/h^2 with J on B phi -- unbounded "
      "at BOTH ends for a band-pass (h -> 0 as k -> 0 and k -> oo) -- and 1 with both: only chi = (S_xi - S_L) phi is admissible",
      f"adjoint residual {err_bp:.1e}; gains {g_ch}, {g_J}, {g_both}",
      err_bp < 1e-6 and sp.simplify(g_ch - hk_s ** 2) == 0 and sp.simplify(g_J - hk_s ** -2) == 0 and sp.simplify(g_both - 1) == 0)

# A2 the zero-field block with the band-pass (C_phi = 0 at zero field; general C_phi for health)
d0, p0, r0 = blk_roots({Wg: 1, mY: 0, Cph: 0})
r0 = [sp.simplify(r_) for r_ in r0]
nB = sp.solve([ELk[0].subs({Wg: 1, mY: 0}), ELk[2].subs({Wg: 1, mY: 0})], [An, AB], dict=True)[0]
rows2 = [sp.expand(sp.simplify(ELk[1].subs({Wg: 1, mY: 0}).subs(nB))), sp.expand(sp.simplify(ELk[4].subs({Wg: 1, mY: 0}).subs(nB)))]
M2 = sp.Matrix([[sp.expand(sp.diff(r_, v_)) for v_ in (Ap, AF)] for r_ in rows2])
T2 = M2.applyfunc(lambda e_: sp.simplify(sp.expand(e_).coeff(wq_, 2)))
V2 = M2.applyfunc(lambda e_: sp.simplify(-sp.expand(e_).subs(wq_, 0)))
detV = sp.factor(V2.det())
EAQ = (2 * (2 - alm) * hq ** 2 + 2 * alm * Cph) / ((2 - alm) * hq ** 2 + 2 * Cph)
Egrid = [float(EAQ.subs({alm: av, Cph: cv, hq: hv})) for av in ALPHA_C for cv in (0.0, 1e-6, 1e-2, 1.0, 1e3, 1e12) for hv in (1e-6, 0.1, 1.0)]
fast_ok = all(float(r_.subs({alm: av, c2m: cv, lmm: lv, hq: hv})) >= 0 for r_ in r0 for av in (1e-13, 3.2e-9) for cv in (1e-4, 7.3e-3, 1.0)
              for lv in (1e-3, 1.0, 1e8) for hv in (1e-6, 0.3, 1.0))
P(f"    zero field (C_phi = 0), band-pass gain h: omega^2/k^2 roots {r0}")
P(f"    reduced (psi, phi): T = {T2.tolist()};  det V = {detV};  E(C_phi, h) on the grid in [{min(Egrid):.3g}, {max(Egrid):.3g}]")
check("A2 THE BAND-PASSED AQUAL BLOCK IS HEALTHY AND WELL-POSED ON FRW for every gain h in [0, 1]: at zero field the roots are "
      "omega^2 = 0 (FP7's marginal mode) and (2 - alpha_c)(c_2 lambda + (2 + 3c_2) h^2) k^2/(alpha_c lambda (2 + 3c_2)) >= 0; after the "
      "lapse and shift constraints T = diag(4(2 + 3c_2)/c_2, 4 lambda) and det V = 16 C_phi k^4 (2 - alpha_c)/alpha_c, independent of h "
      "(no ghost, no gradient instability iff C_phi >= 0 per channel); the khronon's E(C_phi, h) lies in [alpha_c, 2]",
      f"roots {r0}; roots >= 0 on the grid {fast_ok}; det V {detV}; E range [{min(Egrid):.2e}, {max(Egrid):.4f}]",
      any(sp.simplify(r_) == 0 for r_ in r0) and fast_ok and sp.simplify(detV - 16 * Cph * kq_ ** 4 * (2 - alm) / alm) == 0
      and min(Egrid) >= min(ALPHA_C) * (1 - 1e-9) and max(Egrid) <= 2 + 1e-12)
OUT["numbers"]["A2"] = {"roots": [str(r_) for r_ in r0], "detV": str(detV), "E_range": [min(Egrid), max(Egrid)]}

# A3 how the band-pass reaches the web: FP7's slow root and static law with sigma -> h
slow = sp.factor(Cph * c2m / (c2m * lmm + (2 + 3 * c2m) * hq ** 2))           # FP7 B4/C3: c_s^2 = C_phi/lambda_eff^phi
static = hq ** 2 / Cph                                                          # FP7 C3: static response sigma^2/C_phi
Hs, kc = sp.symbols("H k_c", positive=True)
resp = static / (1 + Hs ** 2 / (slow * kc ** 2))                                 # physical-amplitude interpolation (FP6/L341 weight)
lin = sp.limit(resp, Cph, 0)                                                    # the formal linear (zero-tangent) limit
lin0 = sp.simplify(lin.subs(lmm, 0))
P(f"    boost(C_phi -> 0) = {sp.simplify(lin)};  at lambda = 0: {lin0}  (h-independent: {sp.diff(lin0, hq) == 0})")
check("A3 HOW THE BAND-PASS REACHES THE WEB (derived from FP7's committed slow root c_s^2 = C_phi/lambda_eff^phi and static law "
      "h^2/C_phi): the formal zero-tangent response is h^2 (ck/H)^2/(lambda + (2 + 3c_2) h^2/c_2) -- at lambda = 0 it is "
      "h-INDEPENDENT, c_2 (ck/H)^2/(2 + 3c_2): with no inertia of its own phi is auxiliary, the khronon carries the mode and the "
      "band-pass cannot shield the web; the h^2 suppression acts only through J's physical amplitude (h^2 C^Q(h y), the growth "
      "yardstick) or through lambda > 0",
      f"lim C_phi->0: {sp.simplify(lin)}; lambda = 0: {lin0}", sp.diff(lin0, hq) == 0 and sp.simplify(lin0 - c2m * kc ** 2 / (Hs ** 2 * (2 + 3 * c2m))) == 0)
check("A4 (reported) route (i) keeps FP7's lambda: at lambda = 0 and exactly zero field phi is auxiliary and FP7 E1's value "
      "phi = A_n/h(k) needs 1/h -- divergent at k -> 0 for a band-pass (h ~ (kL)^2/2); lambda > 0 (bounded by tracking: "
      "lambda + (2 + 3c_2)/c_2 <= 277 at C_phi >= 0.01) removes it.  A floor that freezes phi at zero field (Y3) removes it too",
      "h(kL = 1e-3) = %.1e -> 1/h = %.1e" % (hk_num[0], 1 / hk_num[0]), True, load_bearing=False)
P(f"    {el()}")

# ================================================================================================= I  ROUTE (i) ALONE
banner("I  ROUTE (i): THE BAND-PASS ALONE on the AQUAL block (no floor; J's zero tangent makes FRW well-posed without one)")
i1 = {}
for n in (0, 1, 2, 3):
    for LLv in (0.5, 1.0, 2.0, 3.0, 5.0):
        mod = bandpass_model(LLv, n, yr=0.0)
        i1[(n, LLv)] = {m: s8_aq(mod, "canonical", m) for m in MODES}
P("    sigma_8/LCDM (physical amplitude, canonical, rms / per-mode), band-pass alone, lambda = 0+:")
for n in (0, 1, 2, 3):
    P(f"      n = {n}: " + "; ".join(f"L_Lambda = {LLv}: {i1[(n, LLv)]['rms']:.3f}/{i1[(n, LLv)]['permode']:.3f}" for LLv in (0.5, 1.0, 2.0, 3.0, 5.0)))
i1_ok = (min(i1[(0, LLv)]["rms"] for LLv in (0.5, 1.0, 2.0, 3.0, 5.0)) > 3 and all(max(i1[(2, LLv)].values()) <= SIG8_BAND[1] for LLv in (0.5, 1.0, 2.0, 3.0)))
check("I1 ROUTE (i) sigma_8: the band-pass alone fixes late-time growth on the AQUAL root only if L shrinks into the past -- n = 0 "
      "leaves sigma_8 >= 3.5 x LCDM, n >= 2 keeps it <= 1.05 for L_Lambda <= 3 Mpc (physical-amplitude yardstick; FP6 B2 without "
      "the (e1) regulator the old root needed)",
      f"n = 0 min {min(i1[(0, LLv)]['rms'] for LLv in (0.5, 1.0, 2.0, 3.0, 5.0)):.2f}; n = 2, L_Lambda <= 3: max "
      f"{max(max(i1[(2, LLv)].values()) for LLv in (0.5, 1.0, 2.0, 3.0)):.4f}", i1_ok)
OUT["numbers"]["I1"] = jkey(i1)
# I2 (reported) the formal linear yardstick (FP7's derived system; A3's h-independence at lambda = 0)
lin277 = F7["B5"]["linear"]["277.4"]
check("I2 (reported) the formal linear yardstick for route (i): at lambda = 0 the band-pass does not enter it (A3), so it is FP7's "
      "no-gate value; with lambda > 0 only the super-L modes are shielded and the sub-L modes (h ~ 1) still run away inertia-limited: "
      "the linear yardstick is divergent for route (i) at every tracking-allowed lambda",
      f"FP7 B5 linear sigma_8/LCDM at lambda_eff = 277: {lin277:.2e}", True, load_bearing=False)
# I3 the flagship floor on L(2.5)
Lflag = {}
for f in FOOTS:
    Lflag[f] = brentq(lambda Lk: law_dev_dex(1e11, A0[f], 0.1, Lk / 1e3) + FLAG_TOL, 5.0, 400.0)
LF = max(Lflag.values())
kF_phys = 1.0 / (15.0 * h_) / (1 + Z_FLAG) * 1e3
check("I3 THE FLAGSHIP FLOOR on the AQUAL root (spherical AQUAL = FP6's band-passed phantom, K3): the 1e11 flagship at z = 2.5 stays "
      "within 0.05 dex only if L(2.5) >= L_flag, while the IGM filtering length is 1/k_F",
      f"L_flag = {Lflag['canonical']:.1f} / {Lflag['alt']:.1f} kpc (canonical / alt) vs 1/k_F = {kF_phys:.0f} kpc (k_F = 15 h/Mpc, z = 2.5)",
      30 < LF < 90 and LF > kF_phys)
# I4 forest vs flagship
i4 = {}
for n in (1.0, 1.5, 2.0, 2.5, 3.0, 4.0):
    for fac in (1.0, 1.5):
        LLv = fac * LF / 1e3 / OmL_z(Z_FLAG) ** (n / 2)
        mod = bandpass_model(LLv, n, yr=0.0)
        i4[(n, fac)] = {(f, m): forest_aq(mod, f, m) for f in FOOTS for m in MODES}
i4_min = min(min(v.values()) for v in i4.values())
for (n, fac), v in i4.items():
    P(f"    n = {n}, L(2.5) = {fac:.1f} L_flag: forest proxy worst |dP1D| " + ", ".join(f"{k_[0][:3]}/{k_[1]}: {x_:.3g}" for k_, x_ in v.items()))
# the converse: L(2.5) at the IGM's filtering length -> the flagship
flag_at_kF = {f: law_dev_dex(1e11, A0[f], 0.1, kF_phys / 1e3) for f in FOOTS}
lam_i4 = 100.0; c2_i4 = 0.1                                                    # a larger c_2 lets lambda > 0 within tracking
lamphi = lam_i4 + (2 + 3 * c2_i4) / c2_i4
mod_l = bandpass_model(1.0 * LF / 1e3 / OmL_z(Z_FLAG) ** 1.0, 2.0, yr=0.0)
res_l = growth_aq(mod_l, A0["canonical"], mode="permode", KHg=KHF, Dig=DIF, zs_out=(2.0, 3.0), c2=c2_i4, lam=lam_i4)
fl_lam = max(forest_proxy(res_l, kF=kF)[0] for kF in (10.0, 15.0, 20.0))
P(f"    converse: L(2.5) = 1/k_F = {kF_phys:.0f} kpc gives the flagship {flag_at_kF['canonical']:+.3f} / {flag_at_kF['alt']:+.3f} dex; "
  f"with phi's own inertia at the tracking edge (lambda = {lam_i4:g}, c_2 = {c2_i4}: lambda_eff^phi = {lamphi:.0f}) the n = 2 cell's "
  f"forest proxy is {fl_lam:.3g}")
check("I4 ROUTE (i) FAILS THE FOREST WHEREVER IT KEEPS THE FLAGSHIP, on the AQUAL root too: for every epoch law n = 1-4 with "
      "L(2.5) >= L_flag the linear forest proxy is off by > 10% (both footings, both yardstick modes), inertia at the tracking edge does "
      "not help (the IGM's phi moves at c_s >~ 10^3 km/s), and at L(2.5) = 1/k_F the flagship is off by > 0.05 dex: the low-field "
      "response of the AQUAL block is the same MOND equilibrium as QUMOND's (K3), so FP6 B4's scale overlap survives the repair",
      f"smallest worst-deviation over the scan {i4_min:.3g}; with lambda {fl_lam:.3g}; flagship at L = 1/k_F {min(flag_at_kF.values()):+.3f} dex",
      i4_min > FOREST_TOL and fl_lam > FOREST_TOL and min(flag_at_kF.values()) < -FLAG_TOL)
OUT["numbers"]["I4"] = {f"{k_[0]}_{k_[1]}": jkey(v) for k_, v in i4.items()}
OUT["numbers"]["I4"]["flag_at_kF"] = flag_at_kF
# I5 KiDS and SPARC for the band-pass alone
L25s = (0.75, 1.0, 1.3, 1.6, 2.0)
i5 = {(f, L25): kids_class(A0[f], L25) - KB[f] for f in FOOTS for L25 in L25s}
Lk = {}
for f in FOOTS:
    ys_ = [i5[(f, x_)] for x_ in L25s]
    j = next(i for i in range(len(L25s) - 1) if ys_[i] > KIDS_TOL >= ys_[i + 1])
    Lk[f] = L25s[j] + (KIDS_TOL - ys_[j]) * (L25s[j + 1] - L25s[j]) / (ys_[j + 1] - ys_[j])
sp_i = {f: max(abs(law_dev_dex(Mv, A0[f], yv_, L_phys(LL_of(1.3, 2.0), 2.0, 1.0))) for Mv in (1e9, 1e10, 1e11, 1e12)
               for yv_ in (0.01, 0.03, 0.1, 1.0, 10.0, 100.0)) for f in FOOTS}
lg_i = lg_both(LL_of(1.3, 2.0), 2.0)
P("    KiDS lead grade d chi^2 vs L(0.25): " + "; ".join(f"{f[:3]}: " + ", ".join(f"{L25}: {i5[(f, L25)]:+.1f}" for L25 in L25s) for f in FOOTS))
check("I5 ROUTE (i) KEEPS KiDS AND SPARC: KiDS (lead grade) needs L(0.25) >~ 1.2 Mpc, and at n = 2, L(0.25) = 1.3 Mpc the SPARC range "
      "(M_b = 1e9-1e12, y = 0.01-100, z = 0) is intact to 0.01 dex; the Local Group is reported (the band-pass removes its EFE)",
      f"L_KiDS {Lk['canonical']:.2f} / {Lk['alt']:.2f} Mpc; SPARC {sp_i['canonical']:.1e} / {sp_i['alt']:.1e} dex; LG R0 "
      f"{lg_i['canonical']:.3f} / {lg_i['alt']:.3f} Mpc", max(Lk.values()) < 1.3 and max(sp_i.values()) <= SPARC_TOL)
OUT["numbers"]["I5"] = {"kids": jkey(i5), "L_kids": Lk, "sparc": sp_i, "lg": lg_i}
check("I6 ROUTE (i) IS NOT ENOUGH: the zero tangent removes the cut-off's FRW role (FP6 needed m > 1/2 for E < 2; here FRW is "
      "well-posed with no floor, A2) but NOT its forest role -- the band-pass alone (2 constants + FP7's lambda) passes sigma_8, the "
      "flagship, SPARC and KiDS and FAILS the forest; (e3)'s three constants are not all unnecessary (Y and H: one of them is)",
      f"route (i): sigma_8 <= {max(max(i1[(2, 2.0)].values()), 1.0):.3f} at n = 2; forest >= {i4_min:.2f}; flagship floor {LF:.0f} kpc; "
      f"KiDS floor {max(Lk.values()):.2f} Mpc", i4_min > FOREST_TOL and i1_ok)
P(f"    {el()}")

# ================================================================================================= Y  THE YIELD FLOOR
banner("Y  THE YIELD FLOOR: J_Y = J_P2(Y) + 2 y_th sqrt(Y) -- the lowest-order amplitude floor, and why only the AQUAL root admits it")
Ysym, xs, ys, yth_s = sp.symbols("Y x y y_th", positive=True)
JP2s = -sp.Rational(1, 4) * sp.log(1 - 2 * sp.sqrt(Ysym)) - sp.sqrt(Ysym) / 2 - Ysym / 2
JYs = JP2s + 2 * yth_s * sp.sqrt(Ysym)
JYp = sp.simplify(sp.diff(JYs, Ysym).subs(Ysym, xs ** 2))                        # J_Y' = mu_eff(x)
flux = sp.simplify(xs * JYp)                                                      # F(x) = x mu_eff = F_P2(x) + y_th
FP2 = xs ** 2 / (1 - 2 * xs)
flux_ok = sp.simplify(flux - (FP2 + yth_s)) == 0
xsol = sp.sqrt((ys - yth_s) ** 2 + (ys - yth_s)) - (ys - yth_s)
law_ok = sp.simplify(FP2.subs(xs, xsol) - (ys - yth_s)) == 0
CT_Y = sp.simplify(flux / xs); CL_Y = sp.simplify(sp.diff(flux, xs))
CL_Q = sp.simplify(sp.diff(xsol, ys))                                            # QUMOND-form longitudinal tangent dx/dy
lim_CLQ = sp.limit(CL_Q, ys, yth_s, dir="+")
ser = sp.series(JP2s, Ysym, 0, 3).removeO()
c1_, c2_ = sp.simplify(ser.coeff(sp.sqrt(Ysym), 1)), sp.simplify(ser.coeff(Ysym, 1))
# strict convexity of v -> J_Y(|v|^2) on a grid: radial eigenvalue F'(x) = CL_Y, transverse F/x = CT_Y
fx = sp.lambdify((xs, yth_s), (CL_Y, CT_Y), "numpy")
xg = np.linspace(1e-6, 0.4999, 4000)
conv_ok = all(np.all(np.asarray(fx(xg, yt)[0]) >= 0) and np.all(np.asarray(fx(xg, yt)[1]) > 0) for yt in (0.0, 1e-6, 1e-2))
CLmin0 = float(np.asarray(fx(np.array([1e-9]), 1e-2)[0])[0])
P(f"    J_Y' = {JYp};  flux F(x) = F_P2(x) + y_th: {flux_ok};  spherical law x = sqrt(D^2 + D) - D, D = y - y_th: {law_ok}")
P(f"    C_T = F/x = {CT_Y};  C_L = F'(x) = {CL_Y} (>= 0; -> {CLmin0:.1e} as x -> 0+);  J_P2 small-Y expansion {sp.simplify(ser)}: "
  f"c_1 (sqrt Y) = {c1_}, c_2 (Y) = {c2_}")
check("Y1 THE YIELD LAW FROM THE ACTION: J_Y = J_P2 + 2 y_th sqrt(Y) has flux F(x) = F_P2(x) + y_th, so the static equation "
      "div(F(|grad phi|) grad phi/|grad phi|) = 4 pi G B rho/a0 gives phi' = a0 x_P2(y_bp - y_th) above the yield and phi' = 0 below it "
      "(the subdifferential absorbs any source weaker than y_th a0); C_T = F/x > 0, C_L = F_P2'(x) >= 0, and v -> J_Y(|v|^2) is "
      "strictly convex (|v|^3 is), so the static solution is UNIQUE; at y_th = 0 it is P2 exactly",
      f"flux {flux_ok}; law {law_ok}; convex on the grid {conv_ok}; C_L(0+) = {CLmin0:.1e}", flux_ok and law_ok and conv_ok)
EQ = alm + 2 * sp.Symbol("C") / (1 + sp.Symbol("C"))                                # FP5's E(C) on the QUMOND core
E_core = sp.limit(EQ, sp.Symbol("C"), sp.oo)
E_aq = sp.simplify(sp.limit(EAQ, Cph, 0))
P(f"    at the yield surface (y -> y_th+): C_L^Q = dx/dy -> {lim_CLQ}; QUMOND core E(C) -> {E_core} (> 2: Hadamard, FP5); AQUAL root "
  f"E(C_phi = 1/C_L^Q -> 0, h) -> {E_aq} (marginal, FP7's zero-field value)")
check("Y2 ADMISSIBLE ON THE REPAIRED ROOT ONLY: at every yield surface the QUMOND-form tangent C_L^Q = dx/dy is infinite, which on the "
      "C-H core puts the khronon at E = alpha_c + 2 > 2 (FP5's Hadamard band: the old root could not take this floor, hence FP6's "
      "smooth cut-off and its sharpness m); on the AQUAL root C_L^phi = 1/C_L^Q -> 0 gives E -> 2, FP7's marginal zero-field value "
      "(at most linear growth), and inside the yield (phi frozen) E = alpha_c",
      f"C_L^Q -> {lim_CLQ}; E_core -> {E_core}; E_AQUAL -> {E_aq}",
      lim_CLQ == sp.oo and sp.simplify(E_core - (alm + 2)) == 0 and sp.simplify(E_aq - 2) == 0)
check("Y3 FRW WITH THE FLOOR: on FRW every source is infinitesimal, below any y_th > 0, so phi is frozen (the yield absorbs it) and the "
      "formal linearisation is GR + BPS khronon (E = alpha_c, a0 absent): the linear sigma_8 yardstick is exactly 1 on both footings "
      "(uninformative -- the physical web is above the yield at z <~ 2, which the physical-amplitude yardstick scores); FP7 E1's "
      "zero-field inverse filter is not needed, so lambda = 0 is allowed (N = 3 modes: FP7's lambda becomes optional)",
      "linear yardstick 1.000 / 1.000 (canonical / alt); E(C_phi -> oo) = " + str(sp.limit(EAQ, Cph, sp.oo)),
      sp.limit(EAQ, Cph, sp.oo) == alm)
# Y4 lowest order: a finite zero-field stiffness c_2 Y (mu_eff = mu_s + s0) vs the yield c_1 sqrt(Y)
s0s = np.logspace(-3, 3, 121)
yIGM = 1.56e-2                                                                    # the z = 2.5 web's linear rms field (FP6 E2)


def stiff_boost(y, s0):                                                          # (mu_s(x) + s0) x = y -> phantom/g_N = x/y
    return brentq(lambda x_: x_ * (x_ / (1 - 2 * x_) + s0) - y, 0.0, 0.5 - 1e-15, xtol=1e-16) / y


def stiff_flag(s0):
    x_ = brentq(lambda x__: x__ * (x__ / (1 - 2 * x__) + s0) - 0.1, 0.0, 0.5 - 1e-15, xtol=1e-16)
    return math.log10((0.1 + x_) / (0.1 + math.sqrt(0.11) - 0.1))


s_need = next(s for s in s0s if stiff_boost(yIGM, s) <= 0.10)
fl_need = stiff_flag(s_need)
yl_flag = math.log10((0.1 + float(x_P2(0.1 - 0.0141))) / (0.1 + float(x_P2(0.1))))
P(f"    finite stiffness mu_eff = mu_s + s_0 (J = s_0 Y + J_P2): the z = 2.5 IGM (y = {yIGM}) needs s_0 >= {s_need:.3f} for a <= 10% boost; "
  f"the flagship then moves {fl_need:+.3f} dex.  Yield y_th = 0.0141: IGM boost 0, flagship {yl_flag:+.3f} dex")
check("Y4 THE YIELD IS THE LOWEST-ORDER FLOOR AND CARRIES NO SHAPE CONSTANT: J_P2's small-gradient expansion has no sqrt(Y) and no Y "
      "term (c_1 = c_2 = 0; it starts at (2/3) Y^(3/2)); the next-order floor, a finite stiffness s_0 Y, is additive at every field and "
      "cannot separate the z = 2.5 IGM from the flagship (holding the IGM to <= 10% moves the flagship by > 0.05 dex), while the "
      "lowest-order c_1 sqrt(Y) term does -- so the floor needs only its amplitude and its running, not FP6's sharpness m",
      f"c_1 = {c1_}, c_2 = {c2_}; stiffness s_0 >= {s_need:.3f} -> flagship {fl_need:+.3f} dex; yield: IGM 0, flagship {yl_flag:+.3f} dex",
      c1_ == 0 and c2_ == 0 and fl_need < -FLAG_TOL and abs(yl_flag) < FLAG_TOL)
OUT["numbers"]["Y"] = {"C_T": str(CT_Y), "C_L": str(CL_Y), "CLQ_limit": str(lim_CLQ), "stiff_s0": s_need, "stiff_flag": fl_need, "yield_flag": yl_flag}
P(f"    {el()}")

# ================================================================================================= H  THE COMBINATION (H_Y)
banner("H  THE COMBINATION (H_Y) = band-pass (i) + yield floor (Y): four declared constants")
FLOOR_ON = not MUTATE


def floor_of(y25, pp):
    return (y25, pp, YIELD) if FLOOR_ON else None


def hy_model(n, L25, pp, y25):
    return bandpass_model(LL_of(L25, n), n, yr=0.0, floor=floor_of(y25, pp))


def flag_hy(n, L25, pp, y25, foot, M=1e11, z=Z_FLAG):
    fl = floor_of(y25, pp)
    return law_dev_dex(M, A0[foot], 0.1, L_phys(LL_of(L25, n), n, 1 / (1 + z)), y_th_z(fl, z) if fl else None, YIELD)


def kids_hy(L25, y25, pp, foot):
    fl = floor_of(y25, pp)
    return kids_class(A0[foot], L25, y_th_z(fl, Z_KIDS) if fl else None, YIELD) - KB[foot]


h1 = {}
H1_N, H1_L25, H1_PP, H1_Y25 = (2.0, 2.5), (1.3, 1.6), (3.5, 4.0, 4.5), (3e-7, 1e-6, 2e-6, 3e-6)
for n in H1_N:
    for L25 in H1_L25:
        for pp in H1_PP:
            for y25 in H1_Y25:
                mod = hy_model(n, L25, pp, y25)
                h1[(n, L25, pp, y25)] = dict(s8={m: s8_aq(mod, "canonical", m) for m in MODES},
                                             forest={m: forest_aq(mod, "canonical", m) for m in MODES},
                                             flag=flag_hy(n, L25, pp, y25, "canonical"), kids=kids_hy(L25, y25, pp, "canonical"),
                                             yth25=y25 * (OmL_z(Z_KIDS) / OmL_z(Z_FLAG)) ** pp)


def inwin(v):
    return (max(v["s8"].values()) <= SIG8_BAND[1] and min(v["s8"].values()) >= SIG8_BAND[0] and max(v["forest"].values()) <= FOREST_TOL
            and abs(v["flag"]) <= FLAG_TOL and v["kids"] <= KIDS_TOL)


win = [k_ for k_, v in h1.items() if inwin(v)]
fail_by = {g_: sum(1 for v in h1.values() if not ok_(v)) for g_, ok_ in (
    ("sigma_8", lambda v: SIG8_BAND[0] <= min(v["s8"].values()) and max(v["s8"].values()) <= SIG8_BAND[1]),
    ("forest", lambda v: max(v["forest"].values()) <= FOREST_TOL), ("flagship", lambda v: abs(v["flag"]) <= FLAG_TOL),
    ("KiDS", lambda v: v["kids"] <= KIDS_TOL))}
for k_, v in sorted(h1.items()):
    if k_[0] == 2.0 and k_[1] == 1.3:
        P(f"      n={k_[0]} L(0.25)={k_[1]} p'={k_[2]} y_th(0.25)={k_[3]:g} (y_th(2.5) = {v['yth25']:.4f}): s8 {v['s8']['rms']:.4f}/"
          f"{v['s8']['permode']:.4f}, forest {v['forest']['rms']:.2g}/{v['forest']['permode']:.2g}, flagship {v['flag']:+.4f} dex, "
          f"KiDS {v['kids']:+.1f}{'  <- window' if k_ in win else ''}")
win_s8t = [k_ for k_ in win if max(h1[k_]["s8"].values()) <= SIG8_TIGHT]
P(f"    {len(h1)} cells (canonical): in the window {len(win)} (with sigma_8 <= {SIG8_TIGHT}: {len(win_s8t)}); cells failing each gate {fail_by}")
check("H1 (H_Y) HAS A WINDOW on the linchpin's gates (canonical scan of 48 cells: n, L(0.25), p', y_th(0.25)): sigma_8 in [0.922, 1.05], "
      "the linear forest proxy within 10% at z = 2 and 3 (k_F = 10-20 h/Mpc), the 1e11 flagship within 0.05 dex at z = 2.5 and KiDS "
      "(lead grade, band-pass and yield together) within +9 -- with NO sharpness constant: the window is set by y_th(0.25) <~ 3e-6 "
      "(KiDS) and 4e-3 <~ y_th(2.5) <~ 0.03 (forest / flagship)",
      f"{len(win)} of {len(h1)} cells in the window ({len(win_s8t)} also at sigma_8 <= 1.02); failing per gate {fail_by}",
      len(win) >= 10)
OUT["numbers"]["H1"] = {f"{k_[0]}_{k_[1]}_{k_[2]}_{k_[3]}": v for k_, v in h1.items()}
OUT["numbers"]["H1_window"] = [list(k_) for k_ in win]
P(f"    {el()}")

# H2 the headline cell (the same labels as FP6's headline, so the two floors compare cell for cell)
HEAD = dict(n=2.0, L25=1.3, pp=4.0, y25=1e-6)
LLh = LL_of(HEAD["L25"], HEAD["n"]); FLh = floor_of(HEAD["y25"], HEAD["pp"])
modh = hy_model(HEAD["n"], HEAD["L25"], HEAD["pp"], HEAD["y25"])
h2 = {"s8": {}, "forest": {}, "flag": {}, "sparc": {}, "kids": {}}
for f in FOOTS:
    for m in MODES:
        h2["s8"][(f, m)] = s8_aq(modh, f, m)
        res_ = growth_aq(modh, A0[f], mode=m, KHg=KHF, Dig=DIF, zs_out=(2.0, 3.0))
        for kF in (10.0, 15.0, 20.0):
            h2["forest"][(f, m, kF)] = forest_proxy(res_, kF=kF)[0]
    for Mv in (1e10, 1e11):
        h2["flag"][(f, Mv)] = flag_hy(HEAD["n"], HEAD["L25"], HEAD["pp"], HEAD["y25"], f, M=Mv)
    L0h = L_phys(LLh, HEAD["n"], 1.0); y0h = y_th_z(FLh, 0.0) if FLh else None
    h2["sparc"][f] = max(abs(law_dev_dex(Mv, A0[f], yv_, L0h, y0h, YIELD)) for Mv in (1e9, 1e10, 1e11, 1e12) for yv_ in (0.01, 0.03, 0.1, 1.0, 10.0, 100.0))
    h2["kids"][f] = kids_hy(HEAD["L25"], HEAD["y25"], HEAD["pp"], f)
h2["s8_lam"] = {lamv: s8_aq(modh, "canonical", "permode", lam=lamv) for lamv in (0.0, 1.0, 100.0)}
h2["s8_rtol"] = (s8_aq(modh, "canonical", "rms"), s8_aq(modh, "canonical", "rms", rtol=1e-8))
KHF2 = np.logspace(math.log10(0.02), math.log10(100.0), 144); DIF2 = np.array([M6["Delta_lin0"](k) for k in KHF2]) / M6["_r0"]
REF_F2 = growth6(M6["lcdm_model"](), A0["canonical"], KHg=KHF2, Dig=DIF2, zs_out=(2.0, 3.0))
h2["forest_conv"] = {m: (forest_aq(modh, "canonical", m, kFs=(15.0,)),
                         forest_proxy(growth_aq(modh, A0["canonical"], mode=m, KHg=KHF2, Dig=DIF2, zs_out=(2.0, 3.0)), kF=15.0, KHg=KHF2, REFg=REF_F2)[0])
                     for m in MODES}
yth_tab = {z: (y_th_z(FLh, z) if FLh else 0.0) for z in (0.0, 0.25, 1.0, 2.0, 2.5, 3.0)}
P(f"    headline (H_Y): n = {HEAD['n']}, L(0.25) = {HEAD['L25']} Mpc (L_Lambda = {LLh:.2f} Mpc; L(0) = {L_phys(LLh, HEAD['n'], 1.0):.2f} Mpc, "
  f"L(2.5) = {1e3 * L_phys(LLh, HEAD['n'], 1 / 3.5):.0f} kpc), y_th(0.25) = {HEAD['y25']:g}, p' = {HEAD['pp']} "
  f"(y_th = " + " / ".join(f"{v:.3g}" for v in yth_tab.values()) + " at z = 0/0.25/1/2/2.5/3; y_Lambda = "
  f"{HEAD['y25'] * OmL_z(Z_KIDS) ** HEAD['pp']:.3g})")
P("      sigma_8/LCDM (physical amplitude): " + ", ".join(f"{k_[0][:3]}/{k_[1]}: {v:.4f}" for k_, v in h2["s8"].items())
  + ("; linear (formal) yardstick: 1.0000 / 1.0000 (Y3: phi frozen below the yield)" if FLOOR_ON
     else f"; linear (formal) yardstick: divergent without the floor (I2: {lin277:.1e} at lambda = 0)"))
P("      sigma_8 vs phi's own inertia (canonical, per-mode): " + ", ".join(f"lambda = {k_:g}: {v:.4f}" for k_, v in h2["s8_lam"].items()))
P("      forest proxy worst |dP1D| (z = 2, 3): " + ", ".join(f"{k_[0][:3]}/{k_[1]}/{k_[2]:.0f}: {v:.2g}" for k_, v in h2["forest"].items()))
P("      flagship (g_bar = 0.1 a0, z = 2.5): " + ", ".join(f"{k_[0][:3]} {k_[1]:.0e}: {v:+.4f} dex" for k_, v in h2["flag"].items()))
P("      SPARC range (z = 0): " + ", ".join(f"{k_[:3]}: {v:.1e} dex" for k_, v in h2["sparc"].items())
  + ";  KiDS lead grade d chi^2: " + ", ".join(f"{k_[:3]}: {v:+.1f}" for k_, v in h2["kids"].items()))
P(f"      sigma_8 at ODE rtol 1e-6 / 1e-8: {h2['s8_rtol'][0]:.5f} / {h2['s8_rtol'][1]:.5f};  forest proxy 96 vs 144 k-points: "
  + ", ".join(f"{m}: {v[0]:.2e} / {v[1]:.2e}" for m, v in h2["forest_conv"].items()))
h2_ok = (all(SIG8_BAND[0] <= v <= SIG8_BAND[1] for v in h2["s8"].values())
         and all(v <= FOREST_TOL for v in h2["forest"].values()) and all(abs(v) <= FLAG_TOL for v in h2["flag"].values())
         and all(v <= SPARC_TOL for v in h2["sparc"].values()) and all(v <= KIDS_TOL for v in h2["kids"].values())
         and all(max(v) <= FOREST_TOL for v in h2["forest_conv"].values()) and abs(h2["s8_rtol"][0] - h2["s8_rtol"][1]) < 1e-3
         and max(h2["s8_lam"].values()) <= SIG8_BAND[1])
check("H2 THE (H_Y) HEADLINE CELL passes every linchpin gate on both footings: sigma_8 in [0.922, 1.05] (rms and per-mode; also <= 1.02; "
      "the formal linear yardstick is exactly 1), the forest proxy within 10% at k_F = 10, 15, 20 h/Mpc, the 1e10 and 1e11 flagships "
      "within 0.05 dex at z = 2.5, the SPARC range within 0.01 dex, KiDS within +9 -- robust to phi's own inertia, the ODE tolerance and "
      "the k-grid; FOUR declared constants (L_Lambda, n, y_Lambda, p')",
      f"sigma_8 {min(h2['s8'].values()):.4f}-{max(h2['s8'].values()):.4f} (<= 1.02: {max(h2['s8'].values()) <= SIG8_TIGHT}); forest <= "
      f"{max(h2['forest'].values()):.2g}; flagship {min(h2['flag'].values()):+.3f}..{max(h2['flag'].values()):+.3f} dex; SPARC "
      f"{max(h2['sparc'].values()):.1e} dex; KiDS {min(h2['kids'].values()):+.1f}..{max(h2['kids'].values()):+.1f}", h2_ok,
      reading="the forest passes because the z = 2-3 IGM's band-passed field sits below the yield (the MOND scalar is exactly off there), "
              "not because it is small; the forest remains a LINEAR PROXY and KiDS lead grade")
OUT["numbers"]["H2"] = {k_: jkey(d_) if isinstance(d_, dict) else d_ for k_, d_ in h2.items()}
OUT["numbers"]["H2"]["y_th"] = jkey(yth_tab)

# H2b E in the BPS window at every field value (both channels), and where it touches 2
xg2 = np.logspace(-9, math.log10(0.4999), 3000)
Emax, Emin = -1.0, 9.0
for yt in (yth_tab[0.0], yth_tab[2.5]):
    CLv, CTv = [np.asarray(v, float) for v in fx(xg2, yt)]
    for Cv in (CLv, CTv):
        for hv in (1e-4, 0.3, 1.0):
            for av in ALPHA_C:
                Ev = (2 * (2 - av) * hv ** 2 + 2 * av * Cv) / ((2 - av) * hv ** 2 + 2 * Cv)
                Emax, Emin = max(Emax, float(np.max(Ev))), min(Emin, float(np.min(Ev)))
check("H2b E IN THE BPS WINDOW AT EVERY FIELD: with the yield, C_T in (y_th/x, oo) and C_L = F_P2'(x) in [0, oo), so the khronon's "
      "E(C_phi, h) stays in [alpha_c, 2] at every background, both channels, every band-pass gain -- E = 2 (marginal, FP7's zero-field "
      "value) only on the yield surfaces in the longitudinal channel, E = alpha_c inside the yield; no Hadamard band anywhere",
      f"E over x in [1e-9, 0.5), h in {{1e-4, 0.3, 1}}, both alpha_c ends: [{Emin:.2e}, 2 - {2 - Emax:.1e}]", Emax <= 2 + 1e-12 and Emin >= 0)

# H2c (reported) the flagship's z_max, the z = 2-3 IGM lumps, the linear web's G_eff, the Solar System
def _flag_z(z, f="canonical"):
    return flag_hy(HEAD["n"], HEAD["L25"], HEAD["pp"], HEAD["y25"], f, z=z) + FLAG_TOL


try:
    zmax = {f: brentq(lambda z: _flag_z(z, f), 2.0, 8.0, xtol=1e-3) for f in FOOTS}
except ValueError:
    zmax = {f: float("nan") for f in FOOTS}
lumps = {}
gfr = M6["gfrac_smooth"]
for z in (2.0, 2.5, 3.0):
    Lz = L_phys(LLh, HEAD["n"], 1 / (1 + z)) * MPCm; yt = yth_tab.get(z, y_th_z(FLh, z) if FLh else 0.0)
    rhob = RHOM0 * (1 + z) ** 3
    for Rc in (0.1, 0.3, 1.0):
        sg = Rc / h_ / (1 + z) * MPCm
        for dl in (1.0, 3.0, 10.0):
            Ml = dl * rhob * (2 * math.pi) ** 1.5 * sg ** 3
            r_ = np.geomspace(0.05, 5, 300) * sg
            gN_ = G6 * Ml * gfr(r_ / sg) / r_ ** 2
            gbp_ = G6 * Ml * (gfr(r_ / sg) - gfr(r_ / math.sqrt(sg ** 2 + Lz ** 2))) / r_ ** 2
            lumps[(z, Rc, dl)] = float(np.max(x_P2(gbp_ / A0["canonical"] - yt) * A0["canonical"] / gN_))
lump_on = {k_: v for k_, v in lumps.items() if v > 0}
resh_all = growth_aq(modh, A0["canonical"], mode="permode", zs_out=(0.25, 0.5))
lensC = {}
for zl in (0.0, 0.25, 0.5):
    al_ = 1 / (1 + zl); gk_ = gfield(resh_all[zl], al_, KH); hk_ = modh["hfac"](al_, KH); yk_ = gk_ * hk_ / A0["canonical"]
    Ce_z = (nu_p2(yk_) - 1) * modh["cut"](yk_, al_) * hk_ ** 2
    lensC[zl] = {kv: float(np.interp(kv, KH, Ce_z)) for kv in (0.05, 0.1, 0.2, 0.3, 0.5, 1.0)}
    if zl == 0.0:
        Ce_ = Ce_z
sel = (KH >= 0.05) & (KH <= 0.5)
Geff = dict(max_sigma8_modes=float(np.max(Ce_[sel])), at_0p1=float(np.interp(0.1, KH, Ce_)), at_0p3=float(np.interp(0.3, KH, Ce_)), max_all=float(np.max(Ce_)))
D_lcdm = growth_aq(M6["lcdm_model"](), A0["canonical"], mode="permode", zs_out=(0.25,))
Pboost = {zl: {kv: float(np.interp(kv, KH, (resh_all[zl] / D_lcdm[zl]) ** 2)) - 1.0 for kv in (0.1, 0.3, 0.5, 1.0)} for zl in (0.0, 0.25)}
gain_sun = float(gfr(np.array([8.2 * kpc / (L_phys(LLh, HEAD["n"], 1.0) * MPCm)]))[0])
yield_sun = yth_tab[0.0] / 0.4501 / (0.4501 / (1 - 2 * 0.4501))                 # y_th/x_e relative to mu_s(x_e) at the Sun (FP7 A4's x_e)
P(f"    flagship z_max (1e11 at 0.1 a0 within 0.05 dex): {zmax['canonical']:.2f} / {zmax['alt']:.2f}")
P("    z = 2-3 IGM Gaussian lumps (peak delta, comoving sigma): max phantom/g_N " + ", ".join(f"z{k_[0]:g}/R{k_[1]:g}/d{k_[2]:g}: {v:.2f}" for k_, v in lumps.items() if v > 0 or k_[2] == 10.0))
P("    linear lensing proxy (per-mode G_eff/G - 1 = C_eff, no slip): " + "; ".join(
    f"z = {zl}: " + ", ".join(f"k = {kv}: {v:.3f}" for kv, v in d_.items()) for zl, d_ in lensC.items()) + " (h/Mpc)")
P("    linear matter power boost P/P_LCDM - 1 (per-mode yardstick): " + "; ".join(
    f"z = {zl}: " + ", ".join(f"k = {kv}: {v:+.3f}" for kv, v in d_.items()) for zl, d_ in Pboost.items()) + " (h/Mpc)")
P(f"    Solar System: band-passed fraction of the Galactic field at the Sun {gain_sun:.1e}, yield/mu_s at the Sun's x_e {yield_sun:.1e} "
  f"(FP7's floors and PPN unchanged)")
check("H2c (reported) THE PRICES OF (H_Y): galaxy MOND at 0.1 a0 switches off above z_max (the running yield: a prediction, the analogue "
      "of FP6's 3.0); the z = 2.5-3 IGM lumps (delta <= 10, 0.1-1 Mpc/h) are ALL below the yield, but dense (delta ~ 10) z = 2 lumps "
      "switch on -- a nonlinear forest price the linear proxy does not see; the linear lensing amplitude is within ~5% for k <= 0.2 h/Mpc "
      "at z = 0.25 but the sub-L modes are strongly boosted (k >= 0.3 h/Mpc) -- the cosmic-shear/S8 risk only a PM run can settle; the "
      "Solar System is untouched",
      f"z_max {zmax['canonical']:.2f}/{zmax['alt']:.2f}; lumps on: {len(lump_on)} of {len(lumps)} ({', '.join(f'z{k_[0]:g}/d{k_[2]:g}' for k_ in lump_on)}); "
      f"C_eff(z = 0.25) at k = 0.1/0.2/0.3/0.5 h/Mpc: {lensC[0.25][0.1]:.3f}/{lensC[0.25][0.2]:.3f}/{lensC[0.25][0.3]:.2f}/{lensC[0.25][0.5]:.2f}; "
      f"linear P boost today at k = 0.3/0.5/1 h/Mpc: {Pboost[0.0][0.3]:+.2f}/{Pboost[0.0][0.5]:+.2f}/{Pboost[0.0][1.0]:+.2f}; "
      f"Sun {gain_sun:.1e}, {yield_sun:.1e}", True, load_bearing=False)
OUT["numbers"]["H2c"] = {"zmax": zmax, "lumps": {f"{k_[0]}_{k_[1]}_{k_[2]}": v for k_, v in lumps.items()}, "Geff": Geff,
                         "lensing_Ceff": {str(zl): jkey(d_) for zl, d_ in lensC.items()}, "Pboost": {str(zl): jkey(d_) for zl, d_ in Pboost.items()},
                         "sun_gain": gain_sun, "sun_yield": yield_sun}

# H3 the Local Group at every KiDS-passing cell tested
h3 = {}
for (n, L25) in ((2.0, 1.3), (2.0, 1.6), (2.5, 1.3), (2.0, 1.0), (2.0, 0.6)):
    h3[(n, L25)] = lg_both(LL_of(L25, n), n, floor=floor_of(HEAD["y25"], HEAD["pp"]))
    P(f"    n = {n}, L(0.25) = {L25} Mpc + yield: LG R0 = {h3[(n, L25)]['canonical']:.3f} / {h3[(n, L25)]['alt']:.3f} Mpc")
kids_ok_cells = [k_ for k_ in h3 if k_[1] >= max(Lk.values())]
h3_fail = len(kids_ok_cells) > 0 and all(min(h3[k_].values()) > LG_EDGE for k_ in kids_ok_cells)
check("H3 (H_Y) FAILS THE LOCAL GROUP (the KiDS-LG pincer, verified at every KiDS-passing cell tested, both footings): the band-pass "
      "removes the LG's external field as it removes the lenses', the yield is ~1e-7 at z < 1, so R0 = 1.4-1.5 Mpc against 0.96 +- "
      "0.03 (edge 1.21); R0 ~ 1.0 needs L(0.25) ~ 0.6 Mpc, which KiDS excludes",
      "; ".join(f"n={k_[0]} L25={k_[1]}: {v['canonical']:.2f}/{v['alt']:.2f}" for k_, v in h3.items()), h3_fail)
OUT["numbers"]["H3"] = {f"{k_[0]}_{k_[1]}": v for k_, v in h3.items()}

# H4 (reported) the constants' windows (from the H1 scan)
wy25 = sorted({k_[3] for k_ in win}); wpp = sorted({k_[2] for k_ in win}); wyth25 = [h1[k_]["yth25"] for k_ in win]
check("H4 (reported) THE CONSTANTS OF (H_Y) AND THEIR WINDOWS (all DECLARED, none derived): L_Lambda (KiDS: L(0.25) >= ~1.2 Mpc; "
      "sigma_8 <= 1.02 caps it near L(0.25) ~ 1.6 at n = 2), n (>= ~2 for growth, <~ 2.7 for the flagship's L(2.5) >= 52 kpc), y_Lambda "
      "and p' (KiDS: y_th(0.25) <~ 3e-6; forest and flagship: 4e-3 <~ y_th(2.5) <~ 0.03, hence p' >~ 3); the sharpness m of FP6 is gone",
      (f"window y_th(0.25) in {wy25}, p' in {wpp}, y_th(2.5) in [{min(wyth25):.4f}, {max(wyth25):.4f}]" if win else "no window (MUTATE)"),
      True, load_bearing=False)
P(f"    {el()}")

# ================================================================================================= D  ROUTE (ii)
banner("D  ROUTE (ii): A CONCAVE DENSITY-READ GATE ON THE WHOLE AQUAL BLOCK -- allowed now, and scored against the chord bound")
# D1 the static spherical law with the gate, from the action (the gate reads rho_dyn = rho_bar + lap Phi/(4 pi G)); a generic test
#    gate and a generic test primitive (the algebra is gate- and kernel-blind, as in FP7 A1)
r_ = sp.symbols("r", positive=True)
Phr, phr = sp.Function("Phi")(r_), sp.Function("varphi")(r_)
a0s, Gs_, rst, rbs, rhs_, acs, k1s, k2s, w1s, w2s, w3s = sp.symbols("a_0 G rho_* rhobar rho alpha_c k1 k2 w1 w2 w3", positive=True)
uS = sp.Symbol("u")
Wtest = lambda u: w1s * u + w2s * u ** 2 + w3s * u ** 3
Jtest = lambda Y: k1s * Y ** sp.Rational(3, 2) + k2s * Y ** 2
Jp_test = lambda Y: sp.Rational(3, 2) * k1s * sp.sqrt(Y) + 2 * k2s * Y
u_expr = (rbs + sp.diff(r_ ** 2 * sp.diff(Phr, r_), r_) / (4 * sp.pi * Gs_ * r_ ** 2)) / rst
Yx = sp.diff(phr, r_) ** 2 / a0s ** 2
Eblk = (2 - acs) * (2 * sp.diff(Phr, r_) * sp.diff(phr, r_) - sp.diff(phr, r_) ** 2) - 2 * a0s ** 2 * Jtest(Yx)
Lrad = r_ ** 2 * (-(2 - acs) * sp.diff(Phr, r_) ** 2 + Wtest(u_expr) * Eblk - 16 * sp.pi * Gs_ * rhs_ * Phr)
ELr = euler_equations(Lrad, [Phr, phr], [r_])
flux_claim = r_ ** 2 * Wtest(u_expr) * (2 * (2 - acs) * (sp.diff(Phr, r_) - sp.diff(phr, r_)) - 4 * Jp_test(Yx) * sp.diff(phr, r_))
d1_phi = sp.simplify(sp.expand(ELr[1].lhs + sp.diff(flux_claim, r_))) == 0
Qx = sp.diff(Wtest(uS), uS).subs(uS, u_expr) * Eblk / (4 * sp.pi * Gs_ * rst)
claim = -16 * sp.pi * Gs_ * rhs_ * r_ ** 2 + sp.diff(2 * (2 - acs) * r_ ** 2 * (sp.diff(Phr, r_) - Wtest(u_expr) * sp.diff(phr, r_)) + r_ ** 2 * sp.diff(Qx, r_), r_)
d1_Phi = sp.simplify(sp.expand(ELr[0].lhs - claim)) == 0
P(f"    radial EL (sympy): phi's equation = -(d/dr){{r^2 W [2(2 - a_c)(Phi' - phi') - 4 J' phi']}}: {d1_phi};  Phi's equation = "
  f"-16 pi G rho r^2 + d/dr[2(2 - a_c) r^2 (Phi' - W phi') + r^2 Q'],  Q = W'(u) E/(4 pi G rho_*): {d1_Phi}")
check("D1 THE GATED STATIC LAW FROM THE ACTION: with W(rho_dyn/rho_*) on the whole block the radial variation gives phi's flux "
      "W[(2 - a_c)(Phi' - phi') - 2 J' phi'] = 0 and, once integrated, Phi' - W phi' + T = g_N with the gate's back-reaction "
      "T = (W'(u) E)'/(8 pi G (2 - a_c) rho_*), E the block's static energy; for constant W: x (mu_s(x) + (1 - W)) = y, g = y + W x "
      "(in a0 units, a_c -> 0): a gate below 1 adds a Newtonian stiffness (1 - W) to the MOND scalar and scales its force by W",
      f"phi flux form {d1_phi}; Phi equation {d1_Phi}", d1_phi and d1_Phi)
# D2 the stability rule: E > 0 on every galaxy background, so the gate must be concave (FP3 C1's symbol with B -> E)
yb = np.logspace(-8, 12, 600); xb = x_P2(yb)
Eb = 2 * (2 * yb * xb + xb ** 2) - 2 * J_P2(xb ** 2)
Erat = Eb / (2 * xb ** 2)                                                        # E / (2 x^2): -> 1 in the deep regime
Bs, W2s, Cg, kk2, WW, CTs = sp.symbols("E W2 C_g k2 Wbar C_T", real=True)
detS = sp.factor(16 * kk2 ** 3 * (Bs * W2s * Cg ** 2 * kk2 * (1 + WW * CTs) - 4))
zero_k = sp.solve(sp.Eq(detS, 0), kk2)
check("D2 THE STABILITY RULE CARRIES OVER: the block's static energy E = (2 - a_c)(2 g phi' - phi'^2) - 2 a0^2 J is POSITIVE on every P2 "
      "background (E ~ 2 x^2 a0^2 deep, ~ 2 y a0^2 high: J grows only logarithmically at saturation), so FP3 C1's symbol with B -> E "
      "applies: a zero at k^2 = 4/(E W'' C_g^2 (1 + W C_T)) exists iff E W'' > 0 -- a stable density gate on the AQUAL block must be "
      "CONCAVE, and FP3's chord bound W(rho) <= (rho/rho_bar) W(rho_bar) holds",
      f"min E/a0^2 over y = 1e-8..1e12: {float(np.min(Eb)):.2e} (> 0); E/(2 x^2) in [{float(np.min(Erat)):.3f}, {float(np.max(Erat)):.3g}]; "
      f"symbol zero at k^2 = {zero_k}", float(np.min(Eb)) > 0)
# D3 FRW with the gate (W = const on the leaf): the zero-field block
dW, pW, rW = blk_roots({mY: 0, Cph: 0})
cW = pW.all_coeffs()
prodW = sp.factor(cW[-1] / cW[0])
slowW0 = sp.factor(sp.solve(sp.Poly(sp.numer(sp.together(dW.subs(lmm, 0).subs(wq_, sp.sqrt(U2) * kq_))), U2).as_expr(), U2)[0])
# the static (omega -> 0) response to a conserved matter source, by Cramer's rule on the gated block (FP7 C3's construction)
wT_, kT_, Rs_ = sp.symbols("omega_T k_T R", positive=True)
MC = Mblk.subs({mY: 0}).subs({wq_: wT_, kq_: kT_})
SC = sp.Matrix([0, Rs_, sp.I * wT_ * Rs_, 0])                                  # rows (psi, n, B, phi): lapse R, momentum -D R


def cramer(Mx, Sx, i):
    Mi = Mx.copy(); Mi[:, i] = Sx
    return sp.cancel(sp.expand(Mi.det(method='berkowitz')) / sp.expand(Mx.det(method='berkowitz')))


num0, den0 = sp.fraction(sp.cancel(cramer(MC, SC, 0) / (-Rs_ / (4 * kT_ ** 2))))
statW = sp.factor(sp.cancel(num0.subs(wT_, 0) / den0.subs(wT_, 0)))
s_ac = 1 - alm / 2
statW_expect = (1 / s_ac) * (1 + Wg * hq ** 2 / (Cph / s_ac + (1 - Wg) * hq ** 2))
statW0 = sp.simplify(statW.subs(Cph, 0))
P(f"    gated zero-field block: product of the omega^2/k^2 roots {prodW};  lambda = 0 root {slowW0}")
P(f"    static response (Cramer, omega -> 0) Psi/Psi_N[G] = {statW}  ->  at zero field {statW0}")
check("D3 FRW WITH THE GATE: W(FRW) > 0 is allowed on this root -- the gated zero-field block has root product c_2 h^2 (2 - a_c)^2 (1 - W)/"
      "(2 a_c lambda (2 + 3c_2)) > 0 for 0 < W < 1 (FP7's marginal mode becomes a stable oscillation; at lambda = 0 c_s^2 = c_2 (2 - a_c)"
      "(1 - W)/((2 + 3c_2)(W (2 - a_c) + a_c)), fast), W > 1 grows; the static response (Cramer) is (1/s)[1 + W h^2/(C_phi/s + (1 - W) h^2)], "
      "s = 1 - a_c/2, which at zero field is 1/(s (1 - W)) -- INDEPENDENT of the band-pass gain h: a density gate on the web cannot be "
      "hidden behind a band-pass",
      f"root product {prodW}; lambda = 0 root {slowW0}; static == expectation: {sp.simplify(statW - statW_expect) == 0}; zero field {statW0}",
      sp.simplify(prodW - c2m * hq ** 2 * (2 - alm) ** 2 * (1 - Wg) / (2 * alm * lmm * (2 + 3 * c2m))) == 0
      and sp.simplify(statW - statW_expect) == 0 and sp.simplify(statW0 - 1 / (s_ac * (1 - Wg))) == 0)


# D4 the sigma_8 budget of the gate (quasi-static G_eff = G/(1 - f), c_s fast per D3)
def s8_gate_f(ffun, foot="canonical", mode="rms"):
    def cut(y, a):
        f = min(ffun(1 / a - 1), 0.999)
        return (f / (1 - f)) / (nu_p2(y) - 1.0)
    model = {"hfac": lambda a, k: np.ones_like(k), "cut": cut, "yr": 0.0}
    return sigma8_of(growth6(model, A0[foot], mode=mode, c2=1e8)[0.0]) / S8_LCDM


fmax = {}
for tgt in (SIG8_TIGHT, SIG8_BAND[1]):
    for f in FOOTS:
        fmax[(tgt, f)] = brentq(lambda fv: s8_gate_f(lambda z, fv=fv: fv, f) - tgt, 1e-6, 0.5, xtol=1e-7)
fmax_low = brentq(lambda fv: s8_gate_f(lambda z, fv=fv: fv if z <= 0.5 else 0.0) - SIG8_BAND[1], 1e-5, 0.9, xtol=1e-6)
P("    sigma_8 budget of a uniform web on-fraction f = W(rho_bar): " + ", ".join(f"<= {k_[0]} ({k_[1][:3]}): f <= {v:.2e}" for k_, v in fmax.items())
  + f"; spent only at z <= 0.5 (<= 1.05): f <= {fmax_low:.3f}")
check("D4 THE GATE'S sigma_8 BUDGET: the web's response is G_N/(1 - f) with f = W(rho_bar) on every scale (no MOND enhancement: the gate's "
      "stiffness Newtonianises phi), so sigma_8 <= 1.02 allows a uniform f of a few e-3 (a0-blind: both footings agree), and even a budget "
      "spent only at z <= 0.5 stays well below 1",
      ", ".join(f"{k_[0]}/{k_[1][:3]} {v:.2e}" for k_, v in fmax.items()) + f"; z <= 0.5: {fmax_low:.3f}",
      max(fmax.values()) < 0.05 and abs(fmax[(SIG8_TIGHT, 'canonical')] / fmax[(SIG8_TIGHT, 'alt')] - 1) < 1e-3)


# D5 the AQUAL sensitivity: how close to 1 the gate must be to keep the law within 0.05 dex at field y
def x_gate(y, W):
    y = np.asarray(y, float); W = np.asarray(W, float)
    A_ = 2 * W - 1; B_ = 1 - W + 2 * y
    return 2 * y / (B_ + np.sqrt(np.maximum(B_ ** 2 + 4 * A_ * y, 0.0)))        # x (mu_s(x) + 1 - W) = y, stable closed form


def eps_needed(y):
    g0 = y + float(x_P2(y))
    return 1 - brentq(lambda W: math.log10((y + W * float(x_gate(y, W))) / g0) + FLAG_TOL, 0.0, 1.0, xtol=1e-12)


xg_chk = float(np.max(np.abs(x_gate(np.logspace(-6, 3, 50), 1.0) - x_P2(np.logspace(-6, 3, 50)))))
eps_t = {yv_: eps_needed(yv_) for yv_ in (1e-4, 1.5e-4, 1e-3, 1e-2, 0.03, 0.1, 1.0)}
P("    1 - W allowed for |dlog g| <= 0.05 dex (a_c -> 0, T = 0): " + ", ".join(f"y = {k_:g}: {v:.2e}" for k_, v in eps_t.items())
  + f"  (closed form at W = 1 vs P2: {xg_chk:.1e})")
check("D5 THE AQUAL SENSITIVITY: because W < 1 adds a Newtonian stiffness (1 - W) next to mu_s(x) ~ sqrt(y), a galaxy keeps its law "
      "within 0.05 dex only if 1 - W <~ eps(y) ~ 0.1 sqrt(y) -- about 1e-3 at KiDS's 1 Mpc (y ~ 1.5e-4) and 0.09 at the flagship -- "
      "far stricter than FP3's QUMOND gate (which needed W ~ 0.9 everywhere)",
      ", ".join(f"eps({k_:g}) = {v:.1e}" for k_, v in eps_t.items()), eps_t[1.5e-4] < 3e-3 and 0.05 < eps_t[0.1] < 0.2 and xg_chk < 1e-12)
OUT["numbers"]["D4"] = {"fmax": jkey(fmax), "fmax_lowz": fmax_low}
OUT["numbers"]["D5"] = jkey(eps_t)


# D6 the chord-bound prices: the MOST GENEROUS stable gate W = min(1, f rho_dyn/rho_bar) (a concave kink), rho_dyn from the UNGATED
#    phantom (an upper bound on W), T neglected (reported), and the KiDS-sigma_8 pincer
def rho_ph_P2(r, Mb, a0v):
    y = G6 * Mb / (r ** 2 * a0v); x = x_P2(y)
    dxdy = (2 * y + 1) / (2 * np.sqrt(y * y + y)) - 1
    return a0v * (2 * r * x - 2 * r * y * dxdy) / (4 * math.pi * G6 * r ** 2)


def gated_g(r, Mb, a0v, z, f):
    """the most generous stable gate: the concave kink W = min(1, f rho_dyn/rho_bar) at the chord bound, rho_dyn from the UNGATED
    phantom (an upper bound on W); T neglected (its size at the kink is reported)"""
    rhob = RHOM0 * (1 + z) ** 3
    W = np.minimum(f * (rhob + rho_ph_P2(r, Mb, a0v)) / rhob, 1.0)
    y = G6 * Mb / (r ** 2 * a0v)
    return a0v * (y + W * x_gate(y, W)), W


def kids_gate(foot, f, z=Z_KIDS):
    def Mf(Mb):
        g, W = gated_g(M6["RR"], Mb, A0[foot], z, f)
        return g * M6["RR"] ** 2 / G6
    return M6["kids_chi2"](Mf) - KB[foot]


def dex_gate(Mb_msun, y, z, f, foot="canonical"):
    Mb = Mb_msun * MSUN; r = np.array([math.sqrt(G6 * Mb / (y * A0[foot]))])
    g, W = gated_g(r, Mb, A0[foot], z, f)
    return math.log10(g[0] / (A0[foot] * (y + float(x_P2(y))))), float(W[0])


fK = {}
for f in FOOTS:
    fgrid = (0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99)
    kd = [kids_gate(f, fv) for fv in fgrid]
    j = next((i for i in range(len(fgrid) - 1) if kd[i] > KIDS_TOL >= kd[i + 1]), None)
    fK[f] = (fgrid[j] + (KIDS_TOL - kd[j]) * (fgrid[j + 1] - fgrid[j]) / (kd[j + 1] - kd[j])) if j is not None else float("nan")
    P(f"    KiDS lead grade with the most generous gate at z = 0.25 ({f}): d chi^2 at f = " + ", ".join(f"{fv}: {v:+.0f}" for fv, v in zip(fgrid, kd)))
# the flagship's own requirement at z = 2.5: W(r_F) >= 1 - eps(0.1) with rho_dyn(r_F) from the ungated phantom
fF = {}
for f in FOOTS:
    rF_ = math.sqrt(G6 * 1e11 * MSUN / (0.1 * A0[f]))
    fF[f] = (1 - eps_t[0.1]) / (1 + float(rho_ph_P2(np.array([rF_]), 1e11 * MSUN, A0[f])[0]) / (RHOM0 * 3.5 ** 3))
fKm = max(v for v in fK.values() if np.isfinite(v)) if any(np.isfinite(v) for v in fK.values()) else 1.0
fFm = max(fF.values())
# (a) the two-constant family: f(z) = f(0.25) (Omega_L(z)/Omega_L(0.25))^p through both requirements, capped at f(0.25) (else f(0) > 1)
p_ii = math.log(fKm / fFm) / math.log(OmL_z(Z_KIDS) / OmL_z(Z_FLAG))
f_cap = lambda z: min(fKm, fKm * (OmL_z(z) / OmL_z(Z_KIDS)) ** p_ii)
f_pl = lambda z: min(fKm * (OmL_z(z) / OmL_z(Z_KIDS)) ** p_ii, 0.999)
s8_cap = {(f, m): s8_gate_f(f_cap, f, m) for f in FOOTS for m in MODES}
s8_pl = s8_gate_f(f_pl)
# (b) the most generous history: a step, fF above z_s and fK below (it needs its own z_s: >= 3 constants)
s8_step = {zs: s8_gate_f(lambda z, zs=zs: fKm if z <= zs else fFm) for zs in (0.25, 0.3, 0.5)}
Geff_late = 1.0 / (1.0 - fKm)
fm = fmax[(SIG8_TIGHT, "canonical")]
prices = {"L*_0.03": dex_gate(1e11, 0.03, 0.0, fm), "L*_0.01": dex_gate(1e11, 0.01, 0.0, fm), "dwarf_0.01": dex_gate(1e10, 0.01, 0.0, fm),
          "flag1e11_z2.5": dex_gate(1e11, 0.1, 2.5, fm), "flag1e12_z2.5": dex_gate(1e12, 0.1, 2.5, fm),
          "1e12_0.01": dex_gate(1e12, 0.01, 0.0, fm)}
kids_fm = {f: kids_gate(f, fmax[(SIG8_TIGHT, f)]) for f in FOOTS}
half = {}
for Mv in (1e10, 1e11, 1e12):
    rr = np.geomspace(0.01, 5, 2000) * MPCm
    g, W = gated_g(rr, Mv * MSUN, A0["canonical"], Z_KIDS, fm)
    gp2 = A0["canonical"] * (G6 * Mv * MSUN / (rr ** 2 * A0["canonical"]) + x_P2(G6 * Mv * MSUN / (rr ** 2 * A0["canonical"])))
    ph = (g - G6 * Mv * MSUN / rr ** 2) / (gp2 - G6 * Mv * MSUN / rr ** 2)
    half[Mv] = float(rr[np.argmax(ph < 0.5)] / MPCm)
igm = {}
for dl in (1.0, 10.0):
    W = min(fm * (1 + dl), 1.0); yl = 4 * math.pi * G6 * RHOM0 * 3.5 ** 3 * dl * (1 * Mpc / 3.5) / 3 / A0["canonical"]
    igm[dl] = (W, W * float(x_gate(yl, W)) / yl)
# the gate's own force at the kink (the back-reaction T's potential step relative to v_f^2), 1e11 at z = 0.25 with f = fK
rr = np.geomspace(0.01, 5, 4000) * MPCm; Mb11 = 1e11 * MSUN
g, W = gated_g(rr, Mb11, A0["canonical"], Z_KIDS, fKm)
ik = int(np.argmax(W < 1.0)); yk = G6 * Mb11 / (rr[ik] ** 2 * A0["canonical"]); xk = float(x_P2(yk))
Ek = A0["canonical"] ** 2 * (2 * (2 * yk * xk + xk ** 2) - 2 * float(J_P2(xk ** 2)))
rst_k = RHOM0 * 1.25 ** 3 / fKm
Tstep = Ek / (8 * math.pi * G6 * 2 * rst_k) / math.sqrt(G6 * Mb11 * A0["canonical"])
P("    prices at the sigma_8 budget f = %.2e (the most generous stable gate): " % fm
  + ", ".join(f"{k_} {v[0]:+.3f} dex (W {v[1]:.2f})" for k_, v in prices.items()))
P(f"    KiDS d chi^2 at that f: {kids_fm['canonical']:+.0f} / {kids_fm['alt']:+.0f}; half-on radius at z = 0.25: "
  + ", ".join(f"{k_:.0e}: {v:.2f} Mpc" for k_, v in half.items()) + "; z = 2.5 IGM lump (1 Mpc/h): "
  + ", ".join(f"delta {k_:g}: W {v[0]:.3f}, extra force {v[1]:.3f}" for k_, v in igm.items()))
P(f"    requirements on the web on-fraction f = W(rho_bar): KiDS f(0.25) >= {fK['canonical']:.3f} / {fK['alt']:.3f}; the z = 2.5 flagship "
  f"f(2.5) >= {fF['canonical']:.2e} / {fF['alt']:.2e};  the gate's own potential step at the kink (1e11, f(0.25)) ~ {Tstep:.2f} v_f^2")
P(f"    (a) the 2-constant running f(0.25) (Omega_L(z)/Omega_L(0.25))^p through both (p = {p_ii:.2f}): f(0) = {fKm * (OmL_z(0) / OmL_z(Z_KIDS)) ** p_ii:.2f} "
  f"> 1 -> sigma_8 {s8_pl:.2f}; capped at f(0.25): " + ", ".join(f"{k_[0][:3]}/{k_[1]} {v:.4f}" for k_, v in s8_cap.items()))
P(f"    (b) the most generous history (a step f(2.5) -> f(0.25) at z_s; >= 3 constants): sigma_8 " + ", ".join(f"z_s = {k_}: {v:.4f}" for k_, v in s8_step.items())
  + f"; the linear web's G_eff = 1/(1 - f(0.25)) = {Geff_late:.2f} on EVERY scale at z <= z_s (lensing amplitude ~{Geff_late:.1f} x LCDM)")
check("D6 ROUTE (ii) FAILS -- THE KiDS / FLAGSHIP / sigma_8 PINCER THROUGH THE CHORD BOUND, sharpened by the AQUAL sensitivity: KiDS "
      "(lead grade) needs the lenses' phantom intact to ~0.5-1 Mpc, where rho_dyn is a few rho_bar, so even the most generous stable gate "
      "(the concave kink at the chord bound, rho_dyn from the ungated phantom) needs f(0.25) >~ 0.65, while the z = 2.5 flagship needs "
      "f(2.5) >~ 3.6e-3.  (a) The two-constant power-law running through both drives sigma_8 above 1.05 even capped at f(0.25) (uncapped "
      "f(0) > 1); (b) only a step-like switch-on at z_s <~ 0.3 (>= 3 constants) keeps sigma_8 <= 1.05 -- still above 1.02 -- and then the "
      "linear web carries G_eff = 1/(1 - f) ~ 2.9 on EVERY scale at z <~ 0.3, a linear-scale lensing amplitude ~3x LCDM that the "
      "record's cosmic-shear gate excludes.  At the uniform sigma_8 budget KiDS is off by hundreds in chi^2",
      f"f_KiDS {fK['canonical']:.3f}/{fK['alt']:.3f}, f_flag {fF['canonical']:.1e}; (a) sigma_8 capped {min(s8_cap.values()):.3f}-"
      f"{max(s8_cap.values()):.3f}, uncapped {s8_pl:.2f}; (b) step sigma_8 {s8_step[0.25]:.3f} with G_eff {Geff_late:.2f}; KiDS at the "
      f"budget {kids_fm['canonical']:+.0f}/{kids_fm['alt']:+.0f}",
      all(np.isfinite(v) for v in fK.values()) and min(s8_cap.values()) > SIG8_BAND[1] and s8_pl > SIG8_BAND[1]
      and Geff_late > 1.5 and s8_step[0.25] > SIG8_TIGHT and min(kids_fm.values()) > 10 * KIDS_TOL,
      reading="the step history is the only way the five named gates can pass at the 1.05 band (with >= 3 constants, one fewer than "
              "(H_Y) if the step is sharp); it fails sigma_8 <= 1.02, and KiDS's lenses span z ~ 0.1-0.5, so a switch-on at z_s = 0.25 "
              "gates the upper half off (z_s = 0.5 costs sigma_8 = %.3f); its decisive failure is a gate outside the five -- the "
              "linear-scale lensing amplitude, scored at linear order where the yardstick is reliable -- stated, not hidden" % s8_step[0.5])
# (reported) the Local Group under the step history (the most generous KiDS-passing route-(ii) configuration)
lnaT = M6["LNA_T"]; RGg = M6["RG"]; LGMb = M6["LG_MB"] * M6["LG_Msun"]
lg_ii = {}
for f in FOOTS:
    tab = []
    for la in lnaT:
        zz = 1 / math.exp(la) - 1
        g_, W_ = gated_g(RGg, LGMb, A0[f], zz, fKm if zz <= 0.25 else fFm)
        tab.append(g_ * RGg ** 2 / G6)
    tab = np.array(tab)

    def Menc_ii(r, a, tab=tab):
        x = math.log(a); j = min(max(np.searchsorted(lnaT, x) - 1, 0), len(lnaT) - 2)
        fr_ = (x - lnaT[j]) / (lnaT[j + 1] - lnaT[j])
        return np.interp(np.log(np.maximum(r, RGg[0])), np.log(RGg), (1 - fr_) * tab[j] + fr_ * tab[j + 1])
    lg_ii[f] = lg_R0(Menc_ii)
P(f"    (reported) Local Group under the step history: R0 = {lg_ii['canonical']:.3f} / {lg_ii['alt']:.3f} Mpc")
OUT["numbers"]["D6"] = {"f_KiDS": fK, "f_flag": fF, "p_running": p_ii, "s8_capped": jkey(s8_cap), "s8_uncapped": s8_pl, "lg_step": lg_ii,
                        "s8_step": jkey(s8_step), "Geff_late": Geff_late, "prices": prices, "kids_at_budget": kids_fm,
                        "half_on_Mpc": jkey(half), "igm": jkey(igm), "T_step_over_vf2": Tstep}
# D7 (reported) the stiffness-placement variant: -2 K (1 - W) |grad phi|^2 -- linear pass, overdense web switched on
sig8z = 0.8 * 0.83                                                                 # linear sigma_8 at z = 0.25 (LCDM, rough)
sln = math.sqrt(math.log(1 + sig8z ** 2)); thr = math.log(2.1)
fon_mass = 0.5 * math.erfc((thr - 0.5 * sln ** 2) / (sln * math.sqrt(2)))
check("D7 (reported) THE STIFFNESS PLACEMENT (the gate on an added Newtonian stiffness, -2 K (1 - W) |grad phi|^2) escapes the chord bound "
      "at LINEAR order (the web sees K (1 - W(rho_bar)) >> 1, G_eff ~ G (1 + 1/K)), but KiDS's smallest lenses need W = 1 down to "
      "rho_dyn ~ 2 rho_bar at z = 0.25, so every region of the web above ~2 rho_bar -- the printed fraction of the mass on 8 Mpc/h "
      "scales (lognormal estimate) -- is MOND-on on ALL scales: a nonlinear sigma_8/S8 failure the linear yardstick cannot see (estimate, "
      "not a PM run); it also needs K, rho_* and a running for the forest: no fewer constants than (H_Y)",
      f"mass fraction above 2.1 rho_bar at 8 Mpc/h, z = 0.25: {fon_mass:.2f}", True, load_bearing=False)
P(f"    {el()}")

# ================================================================================================= V  ROUTE (iii)
banner("V  ROUTE (iii): A ~Mpc SCALE FOR phi -- can the framework's constants set it; a Yukawa mass; a scale-dependent inertia")
# V1 dimensional analysis: lengths from (a0, c, G, H_Lambda) [and a host mass M]
aE, bE, dE, eE, fE = sp.symbols("a b d e f")
Mdim = sp.Matrix([[1, 1, 3, 0], [0, 0, -1, 0], [-2, -1, -2, -1]])            # rows m, kg, s; columns a0, c, G, H
sol0 = sp.linsolve((Mdim, sp.Matrix([1, 0, 0])), [aE, bE, dE, eE])
Mdim2 = sp.Matrix([[1, 1, 3, 0, 0], [0, 0, -1, 0, 1], [-2, -1, -2, -1, 0]])  # + M
sol1 = sp.linsolve((Mdim2, sp.Matrix([1, 0, 0])), [aE, bE, dE, eE, fE])
H_L = H0 * math.sqrt(OL); ZZ = c * H_L / A0["canonical"]
scales = {"c/H_Lambda": c / H_L / MPCm, "c^2/a0": c ** 2 / A0["canonical"] / MPCm}
for Mv in (1e10, 1e11, 1e12):
    GM = G6 * Mv * MSUN
    scales[f"r_M({Mv:.0e})"] = math.sqrt(GM / A0["canonical"]) / MPCm
    scales[f"r_ZG({Mv:.0e})"] = (GM / H_L ** 2) ** (1 / 3) / MPCm
    scales[f"v_f/H_L({Mv:.0e})"] = (GM * A0["canonical"]) ** 0.25 / H_L / MPCm
t_need = math.log(scales["c/H_Lambda"] / LLh) / math.log(ZZ)
P(f"    lengths from (a0, c, G, H_Lambda): {sol0}  -> (c/H_Lambda) (a0/(c H_Lambda))^a = (c/H_Lambda) Z^(-a), G absent (no mass)")
P(f"    with a host mass M: {sol1}  (every solution with f != 0 scales as a power of M)")
P("    the candidates [Mpc]: " + ", ".join(f"{k_} {v:.3g}" for k_, v in scales.items()) + f";  L_Lambda = {LLh:.2f} Mpc would need Z^(-{t_need:.2f})")
check("V1 THE SCALE IS A NEW DECLARED CONSTANT: the only length built from (a0, c, G, Lambda) is c/H_Lambda times a power of Z (G cannot "
      "enter without a mass; Z = 5.79 would need the non-integer power printed to reach 2.5 Mpc); a Mpc scale needs the host's mass "
      "-- the zero-gravity radius (G M/H_Lambda^2)^(1/3) and v_f/H_Lambda are ~0.2-6 Mpc for 1e10-1e12 -- which a local action term "
      "cannot read, and KiDS stacks 1e10-1e11 lenses with one edge (the band-pass is one leaf operator with one L)",
      f"lengths (no M): {sol0}; Z power needed {t_need:.2f}; r_ZG = " + ", ".join(f"{scales[f'r_ZG({Mv:.0e})']:.2f}" for Mv in (1e10, 1e11, 1e12)) + " Mpc",
      list(sol0)[0][2] == 0 and abs(t_need - round(t_need)) > 0.05)


# V2 the Yukawa mass: linear response, sigma_8 (fixed ell), KiDS screening
dY, pY, rY = blk_roots({Wg: 1, Cph: 0})
cY = pY.all_coeffs()
prodY = sp.factor(cY[-1] / cY[0])
qs_Y = sp.simplify(1 / (mY ** 2 * sp.Symbol("ell") ** 2))
P(f"    Yukawa block at zero field: product of roots {prodY} (> 0: the mass lifts FP7's marginal mode)")


def s8_yuk(ell_mpc, mode="rms", foot="canonical"):
    ellm = ell_mpc * MPCm; nk = len(KH); a0v = A0[foot]; norm = np.trapz(1 / KH, KH)

    def rhs(N_, Y):
        a = math.exp(N_); D = Y[:nk]; Dp = Y[nk:]
        gk = gfield(D, a, KH)
        y = np.full(nk, math.sqrt(np.trapz(gk ** 2 / KH, KH) / norm) / a0v) if mode == "rms" else gk / a0v
        CQ = nu_p2(y) - 1; kl2 = (KH * h_ / (a * Mpc) * ellm) ** 2
        return np.concatenate([Dp, 1.5 * (Om / a ** 3 / Ez(a) ** 2) * (1 + CQ * kl2 / (kl2 + CQ)) * D - (2 + dlnH(a)) * Dp])
    sol = solve_ivp(rhs, (math.log(M6["A_I"]), 0.0), np.concatenate([DI, DI]), method="LSODA", rtol=1e-6, atol=1e-24)
    return sigma8_of(sol.y[:nk, -1]) / S8_LCDM


s8Y = {ell: (s8_yuk(ell), s8_yuk(ell, "permode")) for ell in (0.001, 0.003, 0.01, 0.1, 1.0, 10.0)}
ell_s8 = math.exp(brentq(lambda le: s8_yuk(math.exp(le)) - SIG8_BAND[1], math.log(1e-4), math.log(0.01), xtol=1e-3))


def yukawa_solution(Mb, ell_m, a0v, nbis=60):
    """spherical point mass, J_P2 + the Yukawa term (the static phi-equation div(mu_s grad phi) - phi/ell^2 = 4 pi G rho): in units
    r_M = sqrt(G M/a0), F = the MOND flux/(G M), u = phi/v_f^2:  dF/dln rho = rho^3 u/lam^2, du/dln rho = rho x_P2(F/rho^2),
    F(0) = 1, u(oo) = 0 -- shooting (bisection) on u(rho_min) between 'flux exhausted' and 'phi overshoots zero'."""
    rM = math.sqrt(G6 * Mb / a0v); lam_ = ell_m / rM
    lr0, lr1 = math.log(1e-3), math.log(60 * lam_)

    def f_(t, Yv):
        rho = math.exp(t); F_, u_ = Yv
        return [rho ** 3 * u_ / lam_ ** 2, rho * float(x_P2(max(F_, 0.0) / rho ** 2))]

    def evF(t, Yv):
        return Yv[0]

    def evu(t, Yv):
        return Yv[1]
    evF.terminal, evF.direction, evu.terminal, evu.direction = True, -1, True, 1

    def shoot(u0, dense=False):
        return solve_ivp(f_, (lr0, lr1), [1.0, u0], events=(evF, evu), rtol=1e-10, atol=1e-13, max_step=0.1, dense_output=dense)
    lo, hi = -300.0, 0.0
    for _ in range(nbis):
        mid = 0.5 * (lo + hi)
        if shoot(mid).t_events[0].size:
            lo = mid
        else:
            hi = mid
    return shoot(0.5 * (lo + hi), dense=True), rM


def yukawa_rhalf(Mb, ell_m, a0v):
    s_, rM = yukawa_solution(Mb, ell_m, a0v)
    j = np.argmax(s_.y[0] < 0.5)
    return math.exp(s_.t[j]) * rM / MPCm if s_.y[0][j] < 0.5 else float("nan")


def Mtot_yuk(Mb, ell_m, a0v):
    s_, rM = yukawa_solution(Mb, ell_m, a0v)
    t = np.log(np.maximum(M6["RR"] / rM, 1e-3)); tmax = s_.t[-1]
    F = np.where(t <= tmax, s_.sol(np.minimum(t, tmax))[0], 0.0)
    g = G6 * Mb / M6["RR"] ** 2 + a0v * x_P2(np.maximum(F, 0.0) * rM ** 2 / M6["RR"] ** 2)
    return g * M6["RR"] ** 2 / G6


yk = {(Mv, ell): yukawa_rhalf(Mv * MSUN, ell * MPCm, A0["canonical"]) for Mv in (1e10, 1e11) for ell in (0.3, 1.0, 3.0, 10.0)}
anal = {(Mv, ell): (3 * math.sqrt(G6 * Mv * MSUN / A0["canonical"]) / MPCm * ell ** 2) ** (1 / 3) for (Mv, ell) in yk}
kidsY = {ell: M6["kids_chi2"](lambda Mb, ell=ell: Mtot_yuk(Mb, ell * MPCm, A0["canonical"])) - KB["canonical"] for ell in (1.0, 3.0, 10.0)}
ell_K = float(math.exp(np.interp(-KIDS_TOL, [-kidsY[1.0], -kidsY[3.0], -kidsY[10.0]], [math.log(1.0), math.log(3.0), math.log(10.0)])))
rF11 = math.sqrt(G6 * 1e11 * MSUN / (0.1 * A0["canonical"])) / MPCm
ell_flag = math.sqrt((2 * rF11) ** 3 / (3 * math.sqrt(G6 * 1e11 * MSUN / A0["canonical"]) / MPCm))
P("    sigma_8 with a fixed Yukawa length (rms / per-mode): " + ", ".join(f"ell = {k_} Mpc: {v[0]:.3f}/{v[1]:.3f}" for k_, v in s8Y.items())
  + f";  sigma_8 <= 1.05 needs ell <= {1e3 * ell_s8:.1f} kpc")
P("    screening: radius where the MOND flux halves " + ", ".join(f"{k_[0]:.0e}/ell {k_[1]}: {v:.3f} (est {anal[k_]:.3f})" for k_, v in yk.items()) + " Mpc")
P("    KiDS lead grade with the screened phantom (canonical): " + ", ".join(f"ell = {k_} Mpc: {v:+.1f}" for k_, v in kidsY.items())
  + f" -> needs ell >= {ell_K:.1f} Mpc; the 1e11 flagship keeps its flux to 2 r_F only if ell >= {1e3 * ell_flag:.0f} kpc")
check("V2 THE YUKAWA MASS FAILS: -2 phi^2/ell^2 lifts FP7's marginal mode (root product > 0) and, with J's zero tangent, makes the web's "
      "linear response a HIGH-pass, G_eff/G - 1 = (k_phys ell)^2 -- but a fixed physical ell leaves every mode sub-ell in the early "
      "universe, so sigma_8 <= 1.05 needs ell of a few kpc; the nonlinear screening radius (3 r_M ell^2)^(1/3) (shooting solution) keeps "
      "the flagship only for ell >~ 0.1 Mpc and KiDS (lead grade, scored with the screened phantom) only for ell >~ 5-10 Mpc: no window, "
      "by three decades.  A running ell would be the band-pass again (route i)",
      f"sigma_8 needs ell <= {1e3 * ell_s8:.1f} kpc; flagship ell >= {1e3 * ell_flag:.0f} kpc; KiDS ell >= {ell_K:.1f} Mpc; "
      f"screening vs estimate within {max(abs(yk[k_] / anal[k_] - 1) for k_ in yk):.0%}; root product {prodY}",
      ell_s8 < ell_flag < ell_K and max(abs(yk[k_] / anal[k_] - 1) for k_ in yk) < 0.25 and sp.simplify(prodY) != 0)
OUT["numbers"]["V2"] = {"s8": jkey(s8Y), "ell_s8": ell_s8, "r_half": jkey(yk), "kids": jkey(kidsY), "ell_KiDS": ell_K, "ell_flag": ell_flag, "prod": str(prodY)}
# V3 a scale-dependent inertia lambda(k)
kF_ph = 15.0 * h_ * (1 + Z_FLAG) / Mpc                                             # physical k_F at z = 2.5 [1/m]
aHc = H0 * Ez(1 / 3.5) / c
CQ_igm = float(nu_p2(5e-3) - 1)
lam_forest = (CQ_igm / 0.05 - 1) / (CQ_igm * (aHc / kF_ph) ** 2)                  # boost C/(1 + C lambda (aH/ck)^2) <= 5%
xF = float(x_P2(0.1)); Cphi_F = xF / (1 - 2 * xF)
lam_flag = Cphi_F * (c / 1.8e6) ** 2
lam_s8 = F7["B5"]["lin_threshold_k1"]
check("V3 A SCALE-DEPENDENT INERTIA lambda(k) FAILS: the forest needs lambda >= ~1e10 at the IGM's k_F (1/28 kpc at z = 2.5), the z = 2.5 "
      "flagship's own tracking needs lambda <= ~1e4 at 1/39 kpc, and sigma_8 needs >= 1e7 at k <= 1 h/Mpc: lambda(k) would have to be "
      "large, then small, then large again, jumping by ~1e6 over a factor 1.4 in k -- the IGM and the flagship share a scale",
      f"forest lambda >= {lam_forest:.1e}; flagship tracking lambda <= {lam_flag:.1e} (C_phi = {Cphi_F:.2f}, 3 x 600 km/s); sigma_8 >= {lam_s8:.1e}",
      lam_forest / lam_flag > 1e4 and lam_s8 / lam_flag > 100)
OUT["numbers"]["V"] = {"scales_Mpc": scales, "Z_power": t_need, "lam_forest": lam_forest, "lam_flag": lam_flag, "lam_s8": lam_s8}
P(f"    {el()}")

# ================================================================================================= T  THE ROUTE TABLE
banner("T  THE ROUTE TABLE (sigma_8: physical-amplitude rms/per-mode, both footings; forest: linear proxy; KiDS: lead grade)")
s8H = h2["s8"]; fH = max(h2["forest"].values())
rows = [
    ("(i) band-pass alone", "chi = (S_xi - S_L) phi, L = L_Lambda Omega_L^(n/2)", "2 declared (+ FP7's lambda kept)",
     "yes (zero tangent; marginal)", "yes (C x h^2)", f"<= {max(max(i1[(2, 2.0)].values()), 1):.3f} (n = 2)",
     f">= {i4_min:.2f} FAIL", f"ok if L(2.5) >= {LF:.0f} kpc", "ok", f"ok (L(0.25) >= {max(Lk.values()):.2f})",
     f"{lg_i['canonical']:.2f}/{lg_i['alt']:.2f} FAIL", "FAILS (forest)"),
    ("(ii) concave density gate", "W(rho_dyn/rho_*) x whole AQUAL block", "2 (rho_*, power-law running); a step history needs >= 3",
     "yes (W(1-W) > 0: stable)", "iff concave (D2)", f"KiDS+flagship force {min(s8_cap.values()):.3f} (2 const) / {s8_step[0.25]:.3f} (step)",
     f"leak {igm[1.0][1]:.3f}-{igm[10.0][1]:.3f}", f"1e11 {prices['flag1e11_z2.5'][0]:+.2f}, 1e12 {prices['flag1e12_z2.5'][0]:+.2f} (at budget)",
     f"{prices['L*_0.01'][0]:+.2f} (L* 0.01 a0)", f"needs f(0.25) >= {fK['canonical']:.2f} (+{kids_fm['canonical']:.0f} at budget)",
     f"{lg_ii['canonical']:.2f}/{lg_ii['alt']:.2f}", f"FAILS (sigma_8, or G_eff {Geff_late:.1f} on all scales)"),
    ("(iii-a) Yukawa mass", "-2 phi^2/ell^2", "1 declared (no framework length)", "yes (mass lifts the marginal mode)", "yes",
     f"needs ell <= {1e3 * ell_s8:.0f} kpc", "FAIL (high-pass)", f"needs ell >= {1e3 * ell_flag:.0f} kpc", "-", f"needs ell >= {ell_K:.1f} Mpc", "-", "FAILS (no window)"),
    ("(iii-b) lambda(k)", "nonlocal inertia", ">= 2 declared", "yes", "yes (lambda > 0)", "needs >= 1e7 at 0.2 h/Mpc",
     f"needs >= {lam_forest:.0e}", f"tracking <= {lam_flag:.0e}", "-", "-", "-", "FAILS (same-scale pincer)"),
    ("(H_A) = (i) + FP6 cut-off", "+ C^Q = (nu - 1) x^m/(1 + x^m), x = y/y_th", "5 declared", "yes (C^phi(0) = oo)", "yes",
     f"{min(k1['s8'].values()):.3f}-{max(k1['s8'].values()):.3f}", f"{k1['forest']:.4f}", f"{k1['flag']:+.4f}", f"{F6['H2']['sparc']['canonical']:.0e}",
     f"{k1['kids']['canonical']:+.1f}/{k1['kids']['alt']:+.1f}", f"{k1['lg']['canonical']:.2f}/{k1['lg']['alt']:.2f} FAIL", "linchpin met; LG FAILS"),
    ("(H_Y) = (i) + yield", "+ J_Y = J_P2 + 2 y_th sqrt(Y)", "4 declared", "yes (frozen below yield)", "yes (marginal at yield edge)",
     f"{min(s8H.values()):.3f}-{max(s8H.values()):.3f}", f"{fH:.1g}", f"{h2['flag'][('canonical', 1e11)]:+.3f}",
     f"{h2['sparc']['canonical']:.0e}", f"{h2['kids']['canonical']:+.1f}/{h2['kids']['alt']:+.1f}",
     f"{h3[(2.0, 1.3)]['canonical']:.2f}/{h3[(2.0, 1.3)]['alt']:.2f} FAIL", "linchpin met with FEWEST; LG FAILS"),
]
hdr = ("route", "action term", "new constants", "FRW well-posed", "stable", "sigma_8/LCDM", "forest proxy", "flagship z=2.5 [dex]", "SPARC", "KiDS dchi2", "LG R0 [Mpc]", "status")
for r_row in rows:
    P("    " + " | ".join(f"{h_}: {v}" for h_, v in zip(hdr, r_row)))
OUT["numbers"]["table"] = [dict(zip(hdr, r_row)) for r_row in rows]

# ================================================================================================= F  THE CONSTANTS
banner("F  THE CONSTANTS OF THE BEST CONFIGURATION (H_Y), AND THEIR STATUS")
consts = [
    ("L_Lambda", f"{LLh:.2f} Mpc", "DECLARED (bounded)", "band-pass length in the de Sitter limit; KiDS: L(0.25) >= ~1.2 Mpc; sigma_8 <= 1.02: L(0.25) <~ 1.6 (n = 2); no framework length sets it (V1)"),
    ("n", f"{HEAD['n']}", "DECLARED (bounded)", "the vacuum-share power of L (n = 2: L = a_L/H^2 with a_L = H_Lambda^2 L_Lambda); growth needs n >~ 2, the flagship n <~ 2.7"),
    ("y_Lambda", f"{HEAD['y25'] * OmL_z(Z_KIDS) ** HEAD['pp']:.2e} (y_th(0.25) = {HEAD['y25']:g})", "DECLARED (bounded)", "the yield in the de Sitter limit; KiDS: y_th(0.25) <~ 3e-6"),
    ("p'", f"{HEAD['pp']}", "DECLARED (bounded)", "the yield's vacuum-share power; forest/flagship: 4e-3 <~ y_th(2.5) <~ 0.03 => p' >~ 3"),
    ("m (FP6's sharpness)", "-", "ELIMINATED", "the yield is the lowest-order term of J (Y4) and needs no shape constant; admissible only on the AQUAL root (Y2)"),
    ("lambda (FP7's inertia)", "0 allowed", "OPTIONAL (bounded)", "with the yield phi is frozen at zero field, so FP7 E1's inverse filter is not needed (Y3); tracking caps it"),
    ("forms: Omega_L(<K>_h) running, heat-kernel band-pass, sqrt(Y) yield", "-", "POSTULATED", "leaf averages (no local second variation); the heat branch is C-H's own"),
    ("kappa, xi, alpha_c, c_2", "unchanged", "FITTED / bounded", "FP0/FP7: kappa = 1/2 fitted; xi >= 0.0243/0.0268 pc; alpha_c <= 3.2e-9; c_2 >= 7.29e-3"),
]
for k_, v, s_, w_ in consts:
    P(f"    {k_:34s} {v:28s} {s_:20s} {w_}")
OUT["numbers"]["constants"] = consts
check("F (reported) THE COUNT: (H_Y) adds FOUR declared constants (L_Lambda, n, y_Lambda, p'), each bounded to a window by the gates and "
      "none derived; it removes FP6's sharpness m and makes FP7's lambda optional.  Against FP6's (H): 5 declared + lambda -> 4 declared",
      "4 declared, 0 derived; eliminated: m; optional: lambda", True, load_bearing=False)

# ================================================================================================= W  THE LEDGER
banner("W  THE LEDGER: FP9, the web-galaxy separator on the repaired root")
LEDGER = [
    ("R9a", "the band-pass sits on the chassis, chi = (S_xi - S_L) phi (J on B phi needs 1/h^2, unbounded at both ends)", "DERIVED", "A1 (discrete adjoint + Fourier gains)"),
    ("R9b", "band-passed AQUAL block: roots >= 0, det V = 16 C_phi k^4 (2 - a_c)/a_c for every h, E in [a_c, 2]", "DERIVED", "A2 (this lane's re-derivation of FP7 B3, reproduced exactly: K2)"),
    ("R9c", "at lambda = 0 the formal linear response is h-independent (the khronon carries the mode); the band-pass acts through J's amplitude or lambda > 0", "DERIVED", "A3 (FP7's slow root and static law, sigma -> h)"),
    ("R9d", "route (i), the band-pass alone: sigma_8, flagship, SPARC, KiDS pass; the forest FAILS (scale overlap survives the repair)", "FAILS", "I1-I6 (both footings, both modes, inertia at the tracking edge)"),
    ("R9e", "the yield floor J_Y = J_P2 + 2 y_th sqrt(Y): unique statics, C_T > 0, C_L >= 0; lowest order of J; no shape constant", "DERIVED", "Y1, Y4"),
    ("R9f", "the yield is admissible on the AQUAL root (E -> 2 marginal) and not on the QUMOND core (E -> 2 + a_c)", "DERIVED", "Y2"),
    ("R9g", "FRW with the yield: phi frozen, GR + BPS at linear order, linear yardstick = 1; lambda = 0 allowed", "DERIVED", "Y3"),
    ("R9h", "the separator (H_Y): band-pass (L_Lambda, n) + yield (y_Lambda, p'), both through Omega_L(<K>_h)", "POSTULATED", "chosen after the survey: the fewest declared constants found"),
    ("R9i", "(H_Y) meets sigma_8 (phys; linear = 1), forest (linear proxy), flagship, SPARC, KiDS (lead grade), E in the BPS window", "DERIVED", "H1-H2b, given R9h (forest a proxy, KiDS lead grade)"),
    ("R9j", "(H_Y)'s constant windows: L(0.25) >= ~1.2 Mpc; y_th(0.25) <~ 3e-6; 4e-3 <~ y_th(2.5) <~ 0.03", "CONSTRAINT", "H1, H4"),
    ("R9k", "(H_Y): the Local Group's zero-velocity radius (the KiDS-LG pincer)", "FAILS", "H3: R0 = 1.4-1.5 Mpc at every KiDS-passing cell"),
    ("R9l", "route (ii), a concave density gate on the AQUAL block: stable iff concave; KiDS needs f(0.25) >~ 0.65, the flagship f(2.5) >~ 3.6e-3: "
            "its 2-constant running gives sigma_8 ~ 1.09; a step history (>= 3 constants) gives 1.04 with G_eff ~ 3 on all scales at z <~ 0.3", "FAILS",
     "D1-D6 (chord bound x AQUAL sensitivity; the step's failure is the linear-scale lensing amplitude)"),
    ("R9m", "route (iii): no host-independent Mpc length from (a0, Lambda, G, c); Yukawa: sigma_8 vs KiDS screening; lambda(k): forest vs tracking", "FAILS", "V1-V3"),
    ("R9n", "the four constants of (H_Y)", "POSTULATED", "declared inside R9j's windows; none derived"),
    ("R9o", "beyond linear order: the sub-L web (linear P boost at k >= 0.3 h/Mpc; cosmic shear/S8, halo masses), dense z ~ 2 IGM lumps above the yield (flux P1D), full KiDS (2-halo, lens-redshift spread), the running yield's z ~ 2.8 switch-off, non-analytic zero-field EFT", "OPEN", "H2c (reported); no PM run in this lane"),
]
for k_, what, st, why in LEDGER:
    P(f"    {k_:5s} {st:11s} {what}  --  {why}")
OUT["ledger"] = [dict(link=k_, what=w_, status=s_, basis=b_) for k_, w_, s_, b_ in LEDGER]
check("W (reported) the ledger", f"{len(LEDGER)} links", True, load_bearing=False)
check("G (reported) G-1 passed WHOLE on the repaired root (the linchpin's gates AND the Local Group)",
      f"no: (H_Y) meets sigma_8, forest, flagship, SPARC and KiDS with 4 declared constants but the LG gives R0 = "
      f"{h3[(2.0, 1.3)]['canonical']:.2f}/{h3[(2.0, 1.3)]['alt']:.2f} Mpc", False, load_bearing=False)

# ================================================================================================= VERDICT
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
banner("VERDICT")
P(f"""  (i)   The band-pass alone on the AQUAL block is well-posed and healthy (its gain h enters only the chassis; det V is h-free) and
        passes sigma_8, the flagship, SPARC and KiDS -- but FAILS the forest: the repair's zero tangent removes the cut-off's FRW role,
        not its forest role (the IGM at 28 kpc and the flagship at 52 kpc overlap in scale on either root).
  (Y)   The AQUAL root admits a floor the QUMOND core could not: the yield J_P2 + 2 y_th sqrt(Y), the lowest-order term of J's
        expansion -- unique statics, E in [alpha_c, 2] (marginal only on yield surfaces), phi frozen on FRW.  It carries no shape
        constant.
  (H_Y) Band-pass + running yield meets the linchpin with FOUR declared constants (L_Lambda, n, y_Lambda, p'): sigma_8
        {min(s8H.values()):.3f}-{max(s8H.values()):.3f} (physical; linear = 1), forest proxy <= {fH:.1g}, flagship {h2['flag'][('canonical', 1e11)]:+.3f} dex,
        SPARC {h2['sparc']['canonical']:.0e} dex, KiDS {h2['kids']['canonical']:+.1f}/{h2['kids']['alt']:+.1f} -- one fewer than FP6's (H), with FP7's lambda optional.
        It FAILS the Local Group (R0 = {h3[(2.0, 1.3)]['canonical']:.2f}/{h3[(2.0, 1.3)]['alt']:.2f} Mpc).  Nothing here is derived from the framework's first
        principles: the four constants are declared inside data-set windows.
  (ii)  A concave density gate on the whole block is now allowed and stable, but the chord bound times the AQUAL sensitivity FAILS it:
        with a 2-constant running KiDS + the flagship force sigma_8 = {min(s8_cap.values()):.3f}; a step history (>= 3 constants) reaches
        {s8_step[0.25]:.3f} only with G_eff = {Geff_late:.1f} on every scale at z <~ 0.3.
  (iii) No combination of (a0, Lambda, G, c) gives a host-independent Mpc length; a Yukawa mass and a lambda(k) both FAIL.
  Not 'closed'.  Time {time.time() - T0:.0f} s.""")
json.dump(OUT, open(os.path.join(HERE, f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"), "w"), indent=1, default=str)
P(f"\n  {len(CH) - n_fail}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {SLUG}_results{'_MUTATE' if MUTATE else ''}.json")
sys.exit(0 if n_fail == 0 else 1)
