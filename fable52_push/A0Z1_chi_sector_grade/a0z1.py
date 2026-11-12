#!/usr/bin/env python3
"""A0Z1: the chi sector and a0(chi) of DT1's action (FROZEN_CRITERIA.md, d9adb0feaa).
Q1 the chi EOM by certified variation (sympy, exact), term by term against ACTION.md section 3;
Q2 the sign of the bracket in the Solar System, in galaxies and in a cluster core, and what follows;
Q3 a0(z) for V = V0 exp(-lambda chi sqrt(K)) through FRZ2's own forest gate (Delta chi^2 <= 4 per footing,
   12 DESI P1D bins, reading L); Q4 screening by gamma_L F(Pi).
  A0Z1_SKIP_PIPE=1 skips the halo-model / forest subprocesses (local parts only).
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json, math, time, subprocess
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
import sympy as sp
from scipy.optimize import brentq
from scipy.integrate import solve_ivp

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
RES = dict(lane="A0Z1", criteria="d9adb0feaa", note="kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing",
           KA={}, MUTATE={}, Q={})
def dump():
    json.dump(RES, open(os.path.join(HERE, "a0z1.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "a0z1.out"), "w").write("\n".join(OUT) + "\n")

# ---------------------------------------------------------------- constants (the record's, frozen in the criteria)
KAPPA2 = 0.25                                                  # kappa^2, kappa = 1/2 FITTED
G_SI = 6.674e-11; MSUN = 1.989e30; CLIGHT = 299792458.0
PC = 3.0856775814913673e16; KPC = 1e3 * PC; MPC = 1e6 * PC
HBARC = 1.973269804e-16                                        # GeV m  (Compton wavelength conversion)
HBAR = 6.582119569e-25                                         # GeV s
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}              # CFG556 A0, m/s^2
LSTAR = {"canonical": 21.7 * PC, "alt": 22.9 * PC}             # QX17, m
FOOTS = ("canonical", "alt")
GM_SUN = 1.3271244e20; AU = 1.495979e11; G_EARTH = 9.80665; R_EARTH = 6.371e6
RHO_CRIT = 8.62e-27                                            # kg/m^3, h = 0.674 (r200c of the cluster)
ZB = [round(2.2 + 0.2 * i, 1) for i in range(12)]
F1A = os.path.join(REPO, "closure_2026_11_07", "F1A_primary_cmb_audit", "parts")
OMF = {}
for ft in FOOTS:
    pr = json.load(open(os.path.join(F1A, f"fit_B2_{ft}_cold.json")))["pars"]
    OMF[ft] = (pr["ob"] + pr["oc"]) / pr["h"] ** 2
OPHI0 = {ft: 1.0 - OMF[ft] for ft in FOOTS}
K_GEO = 4 * math.pi * G_SI / CLIGHT ** 2                        # K = 4 pi G/c^2, m/kg
P(f"A0Z1 constants: a0 {A0} m/s^2; Lstar { {k: round(v / PC, 1) for k, v in LSTAR.items()} } pc; "
  f"Om { {k: round(v, 5) for k, v in OMF.items()} }; kappa 1/2")

# ================================================================== Q1: the chi EOM by certified variation (sympy, exact)
P("\n==================== Q1: the chi equation of motion, certified variation (sympy, exact)")
u, a0, K, G, kap, p, A = sp.symbols("u a0 K G kappa p A", positive=True)
uu = A / a0
W = (a0 ** 2 / K) * (-p / a0 - sp.log(1 - p / a0))             # the record's W, p = K|P|
LP = (p / K) * A - W                                           # P.A - W with P along A
pstar = sp.simplify(sp.solve(sp.diff(LP, p), p)[0])
J_on = sp.simplify(LP.subs(p, pstar))                          # the on-shell law term
J_claim = (a0 ** 2 / K) * (uu - sp.log(1 + uu))
r_K0a = sp.simplify(pstar - a0 * uu / (1 + uu))
r_K0b = sp.simplify(J_on - J_claim)
S_u = 2 * (u - sp.log(1 + u)) - u ** 2 / (1 + u)               # ACTION.md's S(u)
dJda0 = sp.simplify(sp.diff(J_claim, a0))                       # at fixed |A|, so u = A/a0 depends on a0
r_S = sp.simplify(dJda0 - (a0 / K) * S_u.subs(u, A / a0))
P(f"  K0 Legendre: K|P| = {pstar};  claim a0 u/(1+u);  residual {r_K0a}")
P(f"  K0 Legendre: max_P[P.A - W] = {J_on};  claim (a0^2/K)(u - ln(1+u));  residual {r_K0b}")
P(f"  dJ/da0 at fixed |A| = {dJda0};  claim (a0/K) S(u) with S = 2(u-ln(1+u)) - u^2/(1+u);  residual {r_S}")

chi_s = sp.symbols("chi"); Vf = sp.Function("V")
a0_of_chi = kap * sp.sqrt(G * Vf(chi_s)); Vp_s = sp.Derivative(Vf(chi_s), chi_s)
da0dchi = sp.simplify(sp.diff(a0_of_chi, chi_s))
r_a0 = sp.simplify(da0dchi - kap ** 2 * G * Vp_s / (2 * a0_of_chi))
P(f"  da0/dchi from a0 = kappa sqrt(G V) = {da0dchi};  claim kappa^2 G V'/(2 a0);  residual {r_a0}")

# the certified variation: 1+1 is the smallest setting in which the sign of the d'Alembertian is visible
t, x = sp.symbols("t x")
chiF = sp.Function("chi")(t, x)
a0f = kap * sp.sqrt(G * Vf(chiF)); uf = A / a0f
Jf = (a0f ** 2 / K) * (uf - sp.log(1 + uf))
Ldens = sp.Rational(1, 2) * sp.Derivative(chiF, t) ** 2 - sp.Rational(1, 2) * sp.Derivative(chiF, x) ** 2 - Vf(chiF) + Jf
EL0 = sp.euler_equations(Ldens, chiF, (t, x))[0]
ELx = sp.expand(EL0.lhs - EL0.rhs)
box = -sp.Derivative(chiF, t, 2) + sp.Derivative(chiF, x, 2)
Vp = sp.diff(Vf(chiF), chiF)
dJdchi = sp.diff(Jf, chiF)
r_EL = sp.simplify(ELx - (box - Vp + dJdchi))
P(f"  Euler-Lagrange of L = -(1/2)(dchi)^2 - V + J: residual against (box chi - V' + dJ/dchi) = {r_EL}")
# the bracket: dJ/dchi against V' kappa^2 S(u)/(8 pi), using K = 4 pi G
S_of_chi = S_u.subs(u, A / a0f)
r_br = sp.simplify(sp.simplify(dJdchi.subs(K, 4 * sp.pi * G)) - Vp * kap ** 2 * S_of_chi / (8 * sp.pi))
P(f"  dJ/dchi - V' kappa^2 S(u)/(8 pi) with K = 4 pi G: residual {r_br}")
EOM_OK = all(sp.simplify(r) == 0 for r in (r_K0a, r_K0b, r_S, r_a0, r_EL, r_br))
RES["Q"]["Q1"] = dict(K0_p_res=str(r_K0a), K0_J_res=str(r_K0b), dJda0_res=str(r_S), da0dchi_res=str(r_a0),
                      EL_res=str(r_EL), bracket_res=str(r_br), EOM_certified=bool(EOM_OK))
P(f"  Q1 verdict: ACTION.md's hand EOM  box chi = V'(chi) [1 - S(u) kappa^2/(8 pi)]  -> "
  f"{'CERTIFIED (every residual exactly 0)' if EOM_OK else 'REFUTED'}")

L_ka1 = sp.Rational(1, 2) * sp.Derivative(chiF, t) ** 2 - sp.Rational(1, 2) * sp.Derivative(chiF, x) ** 2 - Vf(chiF)
e1 = sp.euler_equations(L_ka1, chiF, (t, x))[0]
ka1 = sp.simplify(sp.expand(e1.lhs - e1.rhs) - (box - Vp))
RES["KA"]["KA1"] = dict(res=str(ka1), pass_=bool(sp.simplify(ka1) == 0))
P(f"  KA1 (law sector removed, J == 0): residual against box chi = V' = {ka1} -> {'PASS' if RES['KA']['KA1']['pass_'] else 'FAIL'}")
L_mu1 = Ldens - 2 * Jf                                         # MU1: the on-shell law term given the wrong sign (-J)
mu1_br = sp.simplify(sp.simplify(sp.diff(-Jf, chiF).subs(K, 4 * sp.pi * G)) + Vp * kap ** 2 * S_of_chi / (8 * sp.pi))
RES["MUTATE"]["MU1"] = dict(res=str(mu1_br), bites=bool(sp.simplify(mu1_br) == 0 and EOM_OK))
P(f"  MU1 (on-shell law term given the wrong sign, -J): residual against 1 + kappa^2 S/(8 pi) = {mu1_br} "
  f"-> the bracket would be 1 + kappa^2 S/(8 pi), never negative -> {'bites' if RES['MUTATE']['MU1']['bites'] else 'DOES NOT BITE'}")

Snum = sp.lambdify(u, S_u, "math")
ser = sp.series(S_u, u, 0, 5)
u32 = brentq(lambda z: Snum(z) - 32 * math.pi, 1.0, 1e4, xtol=1e-12)
RES["KA"]["KA4"] = dict(series=str(ser.removeO()), S_at_3=float(Snum(3.0)), u_of_S_32pi=float(u32),
                        S_over_u_at_1e6=float(Snum(1e6) / 1e6),
                        pass_=bool(abs(Snum(3.0) - 1) < 0.05 and 90 < u32 < 130))
P(f"  KA4 S(u): series {ser.removeO()}; S(3) = {Snum(3.0):.4f} (ACTION.md: about 1 at u = 3); "
  f"S(u) = 32 pi at u = {u32:.2f} (ACTION.md: about u > 100); S(1e6)/1e6 = {Snum(1e6) / 1e6:.6f} "
  f"-> {'PASS' if RES['KA']['KA4']['pass_'] else 'FAIL'}")
Sfn = lambda z: float(Snum(min(max(z, 1e-300), 1e16)))

# ================================================================== Q2: where the bracket turns negative, and what follows
P("\n==================== Q2: u = |A|/a0, the sign of the bracket, and what follows")
def law_S(gN, a0v):                                            # the record's spherical static law: g^2 = g_N (g + a0)
    return 0.5 * (gN + math.sqrt(gN * gN + 4 * a0v * gN))
def bracket(u_):                                               # 1 - S(u) kappa^2/(8 pi), kappa = 1/2
    return 1.0 - Sfn(u_) * KAPPA2 / (8 * math.pi)
def A_profile(kind, r, Mb, c=3.5):                             # Newtonian g_N at radius r
    if kind == "point": return G_SI * Mb / r ** 2
    if kind == "nfw":                                          # M200c, r200c against rho_crit, concentration c
        r200 = (3 * Mb / (4 * math.pi * 200 * RHO_CRIT)) ** (1 / 3); rs = r200 / c; xx = r / rs
        mnc = math.log1p(c) - c / (1 + c)
        return G_SI * Mb * (math.log1p(xx) - xx / (1 + xx)) / (mnc * r ** 2)
    if kind == "hernquist": return G_SI * Mb / (r + 3.0 * KPC) ** 2   # reported only
    raise ValueError(kind)
ENVS = [("Solar System 1 AU",        "point", GM_SUN / G_SI, AU),
        ("Solar System 10 AU",       "point", GM_SUN / G_SI, 10 * AU),
        ("Sun surface",              "point", GM_SUN / G_SI, 6.957e8),
        ("galaxy logMb 10 @1 kpc",   "point", 1e10 * MSUN, 1 * KPC),
        ("galaxy logMb 10 @10 kpc",  "point", 1e10 * MSUN, 10 * KPC),
        ("galaxy logMb 10 @100 kpc", "point", 1e10 * MSUN, 100 * KPC),
        ("galaxy logMb 11 @1 kpc",   "point", 1e11 * MSUN, 1 * KPC),
        ("galaxy logMb 11 @10 kpc",  "point", 1e11 * MSUN, 10 * KPC),
        ("galaxy logMb 11 @100 kpc", "point", 1e11 * MSUN, 100 * KPC),
        ("cluster 1e15 @50 kpc",     "nfw",   1e15 * MSUN, 50 * KPC),
        ("cluster 1e15 @100 kpc",    "nfw",   1e15 * MSUN, 100 * KPC),
        ("cluster 1e15 @300 kpc",    "nfw",   1e15 * MSUN, 300 * KPC)]
P("  place                      footing     g_N [m/s^2]  A_law [m/s^2]     u = A/a0      S(u)     bracket")
Q2 = {}
for name, kind, Mb, r in ENVS:
    for ft in FOOTS:
        a0v = A0[ft]; gN = A_profile(kind, r, Mb); Alaw = law_S(gN, a0v); uu_ = Alaw / a0v
        Q2[(name, ft)] = dict(g_N=gN, A_law=Alaw, u=uu_, S=Sfn(uu_), bracket=bracket(uu_), r_m=r)
        P(f"  {name:26s} {ft:9s} {gN:11.3e} {Alaw:13.3e} {uu_:13.5g} {Sfn(uu_):10.4g} {bracket(uu_):11.4g}")
for ft in FOOTS:                                               # the Earth's surface: g given, not from a profile
    a0v = A0[ft]; uu_ = G_EARTH / a0v
    Q2[("Earth surface (given g)", ft)] = dict(g_N=G_EARTH, A_law=G_EARTH, u=uu_, S=Sfn(uu_), bracket=bracket(uu_),
                                               r_m=R_EARTH)
    P(f"  {'Earth surface (given g)':26s} {ft:9s} {G_EARTH:11.3e} {G_EARTH:13.3e} {uu_:13.5g} {Sfn(uu_):10.4g} "
      f"{bracket(uu_):11.4g}")
neg = sorted([(k, v) for k, v in Q2.items() if v["bracket"] < 0], key=lambda kv: kv[1]["bracket"])
P(f"  bracket negative in {len(neg)} of {len(Q2)} place/footing rows; most negative: "
  + "; ".join(f"{k[0]} [{k[1]}] {v['bracket']:.3g}" for k, v in neg[:5]))
BRACKET_NEG = bool(neg)
RES["Q"]["Q2_sign"] = dict(rows={f"{k[0]}|{k[1]}": {kk: float(vv) for kk, vv in v.items()} for k, v in Q2.items()},
                           negative_anywhere=BRACKET_NEG, n_negative=len(neg))
# reported, not graded: the same galaxies with the record's Hernquist softening, A(r) = G M_b/(r + a)^2
P("  reported (not graded): the same galaxies with the record's Hernquist softening, A(r) = G M_b/(r+a)^2:")
for lM, a in ((10, 1.5 * KPC), (11, 3.0 * KPC)):
    for ft in FOOTS:
        a0v = A0[ft]; row = []
        for r in (0.1 * KPC, 1 * KPC):
            uu_ = law_S(G_SI * 10 ** lM * MSUN / (r + a) ** 2, a0v) / a0v
            row.append(f"u({r / KPC:g} kpc) {uu_:7.3f} bracket {bracket(uu_):+.4f}")
        P(f"    log M_b {lM} (a = {a / KPC:.1f} kpc) {ft:9s}: " + "; ".join(row) +
          f";  centre u -> {law_S(G_SI * 10 ** lM * MSUN / a ** 2, a0v) / a0v:.2f}")

# --- the static response: (lap - m_eff^2) dchi = -V' kappa^2 S/(8 pi); da0/a0 = (V'/2V) dchi
#     with V = V0 exp(-lambda chi sqrt(K)): da0/a0 = (lambda^2 a_geo^2/4) Int S(u(r)) r dr, a_geo = a0/c^2
def da0_over_a0(kind, Mb, a0v, r_in, r_out, lam=1.0, Sfun=Sfn, n=6000):
    rr = np.geomspace(r_in, r_out, n)
    uu_ = np.array([law_S(A_profile(kind, r, Mb), a0v) / a0v for r in rr])
    ss = np.array([Sfun(z) for z in uu_])
    I = float(np.trapezoid(ss * rr, rr) if hasattr(np, "trapezoid") else np.trapz(ss * rr, rr))
    a_geo = a0v / CLIGHT ** 2
    return lam ** 2 * a_geo ** 2 / 4 * I, I
def m_eff_of(a0v, br, lam=1.0):
    """|m_eff| in GeV: m_eff^2 = lambda^2 K V |1 - kappa^2 S/(8 pi)| and K V = 16 pi a_geo^2 (kappa = 1/2, GV = 4 a0^2)."""
    a_geo_nat = a0v * HBAR / CLIGHT                            # a0/c^2 in 1/m, converted to GeV
    return lam * math.sqrt(16 * math.pi * a_geo_nat ** 2 * abs(br))
P("  static response and the runaway test (lambda = 1; da0/a0 scales as lambda^2):")
P("    place                                footing     da0/a0        closed form    |m_eff| L    1/|m_eff| [Mpc]  region")
Q2b = {}
for name, kind, Mb, r_in in [("Sun (surface to 100 r_1)", "point", GM_SUN / G_SI, 6.957e8),
                             ("galaxy logMb 11 (100 pc to 100 r_1)", "point", 1e11 * MSUN, 100 * PC),
                             ("galaxy logMb 10 (100 pc to 100 r_1)", "point", 1e10 * MSUN, 100 * PC),
                             ("cluster 1e15 (50 kpc to 100 r_1)", "nfw", 1e15 * MSUN, 50 * KPC)]:
    for ft in FOOTS:
        a0v = A0[ft]; r1 = math.sqrt(G_SI * Mb / a0v)
        val, I = da0_over_a0(kind, Mb, a0v, r_in, 100 * r1)
        uu_L = law_S(A_profile(kind, r_in, Mb), a0v) / a0v; brL = bracket(uu_L)
        m_eff = m_eff_of(a0v, brL)                             # GeV
        comp_m = HBARC / m_eff if m_eff > 0 else float("inf")  # m
        mL = r_in / comp_m if m_eff > 0 else 0.0
        cf = 0.25 * (a0v / CLIGHT ** 2) ** 2 * (G_SI * Mb / a0v) * math.log(r1 / r_in)   # KA6 closed form
        Q2b[(name, ft)] = dict(da0_over_a0=val, closed_form=cf, m_eff_L=mL, compton_Mpc=comp_m / MPC,
                               region_m=r_in, r_1=r1, u_at_r_in=uu_L, bracket_at_r_in=brL,
                               growth_time_s=HBAR / m_eff if m_eff > 0 else None)
        P(f"    {name:36s} {ft:9s} {val:.3e}  {cf:.3e}  {mL:.3e}  {comp_m / MPC:12.4g}  {r_in / KPC:.4g} kpc")
RES["Q"]["Q2_response"] = {f"{k[0]}|{k[1]}": {kk: (float(vv) if isinstance(vv, (int, float)) else vv)
                                             for kk, vv in v.items()} for k, v in Q2b.items()}
ka6_rows = {k: v for k, v in Q2b.items() if "cluster" not in k[0]}   # the closed form is for a point mass
ka6_ok = all(abs(v["da0_over_a0"] / v["closed_form"] - 1) <= 0.20 for v in ka6_rows.values())
RES["KA"]["KA6"] = dict(pass_=bool(ka6_ok),
                        worst=float(max(abs(v["da0_over_a0"] / v["closed_form"] - 1) for v in ka6_rows.values())),
                        cluster_pointmass_closed_form_vs_integral=[float(Q2b[("cluster 1e15 (50 kpc to 100 r_1)", "canonical")]["da0_over_a0"]),
                                                                   float(Q2b[("cluster 1e15 (50 kpc to 100 r_1)", "canonical")]["closed_form"])])
P(f"  KA6 (point-mass closed form vs the numerical Poisson integral, 20 %): worst {RES['KA']['KA6']['worst']:.3f} -> "
  f"{'PASS' if ka6_ok else 'FAIL'}; the NFW cluster row is excluded, the closed form is a point mass's: "
  f"integral {RES['KA']['KA6']['cluster_pointmass_closed_form_vs_integral'][0]:.3e} vs point-mass closed form "
  f"{RES['KA']['KA6']['cluster_pointmass_closed_form_vs_integral'][1]:.3e} (reported)")
max_ml = max(v["m_eff_L"] for v in Q2b.values()); max_da0 = max(abs(v["da0_over_a0"]) for v in Q2b.values())
K3 = bool(max_ml >= math.pi); K4 = bool(max_da0 > 1e-2)
P(f"  K3 runaway (|m_eff| L >= pi anywhere observed): max |m_eff| L = {max_ml:.3e} -> {'FIRES' if K3 else 'does not fire'}")
P(f"  K4 a0 varies (|da0/a0| > 1e-2 anywhere observed): max {max_da0:.3e} -> {'FIRES' if K4 else 'does not fire'}")
P("  response time where the bracket is negative: the light-crossing time of the region "
  f"(100 pc: {100 * PC / CLIGHT / 3.156e7:.2e} yr; 1 AU: {AU / CLIGHT / 60:.1f} min)")

Smu = lambda z: min(z, 1e12) ** 3 / 3                          # MU2: S(u) replaced by its small-u expansion
mu2 = {}
for name, kind, Mb, r_in in [("Sun", "point", GM_SUN / G_SI, 6.957e8), ("galaxy logMb 11", "point", 1e11 * MSUN, 100 * PC)]:
    for ft in FOOTS:
        a0v = A0[ft]; r1 = math.sqrt(G_SI * Mb / a0v)
        v0, _ = da0_over_a0(kind, Mb, a0v, r_in, 100 * r1)
        v1, _ = da0_over_a0(kind, Mb, a0v, r_in, 100 * r1, Sfun=Smu)
        mu2[(name, ft)] = [float(v0), float(v1)]
        P(f"  MU2 (S = u^3/3 everywhere) {name:16s} {ft:9s} da0/a0 {v0:.3e} -> {v1:.3e} ({v1 / v0:.3g}x)")
RES["MUTATE"]["MU2"] = dict(rows={f"{k[0]}|{k[1]}": v for k, v in mu2.items()},
                            bites=bool(all(v[1] / v[0] > 10 for v in mu2.values())))
P(f"  MU2 -> {'bites' if RES['MUTATE']['MU2']['bites'] else 'DOES NOT BITE'}")

# ================================================================== Q4: screening by gamma_L F(Pi)
P("\n==================== Q4: is the chi coupling screened by gamma_L F(Pi)?  (QX17 (E2), the record's diagnostic)")
P("  (1 + gamma_L Pi_+) A + gamma_L D Pi_+ = K W' Phat; the two additions to A are sized on the unscreened")
P("  on-shell P (K|P| = a0 u/(1+u), the K0 Legendre map), spherical symmetry.")
def pi_profile(kind, Mb, a0v, r0, n=6000, spread=3.0):
    rr = np.geomspace(r0 / spread, r0 * spread, n)
    a_geo = a0v / CLIGHT ** 2
    uu_ = np.array([law_S(A_profile(kind, r, Mb), a0v) / a0v for r in rr])
    pp = a_geo * uu_ / (1 + uu_)                               # p = K|P|, geometric [1/m]
    Pi = np.gradient(rr ** 2 * pp, rr) / (K_GEO * rr ** 2)
    dPi = np.gradient(Pi, rr)
    i = int(np.argmin(abs(rr - r0)))
    return rr[i], Pi[i], dPi[i], uu_[i]
P("  place                      footing      Pi_+ [kg/m^3]  gamma_L Pi_+   gamma_L|gradPi|/|A|   screened?")
Q4 = {}
for name, kind, Mb, r in [("Solar System 1 AU", "point", GM_SUN / G_SI, AU),
                          ("Earth surface", "point", 5.972e24, R_EARTH),
                          ("galaxy logMb 10 @1 kpc", "point", 1e10 * MSUN, 1 * KPC),
                          ("galaxy logMb 11 @1 kpc", "point", 1e11 * MSUN, 1 * KPC),
                          ("galaxy logMb 11 @10 kpc", "point", 1e11 * MSUN, 10 * KPC),
                          ("galaxy logMb 11 @100 kpc", "point", 1e11 * MSUN, 100 * KPC),
                          ("cluster 1e15 @100 kpc", "nfw", 1e15 * MSUN, 100 * KPC)]:
    for ft in FOOTS:
        a0v = A0[ft]; gL = K_GEO * LSTAR[ft] ** 2 / 2
        rr, Pi, dPi, uu_ = pi_profile(kind, Mb, a0v, r)
        A_geo = law_S(A_profile(kind, rr, Mb), a0v) / CLIGHT ** 2
        d_Pi = gL * max(Pi, 0.0); d_gr = gL * abs(dPi) / A_geo
        Q4[(name, ft)] = dict(Pi=Pi, gamma_L_Pi=d_Pi, gamma_L_gradPi_over_A=d_gr, screened=bool(max(d_Pi, d_gr) >= 1.0))
        P(f"  {name:26s} {ft:9s} {Pi:12.3e} {d_Pi:13.3e} {d_gr:20.3e}    {'YES' if Q4[(name, ft)]['screened'] else 'no'}")
RES["Q"]["Q4"] = {f"{k[0]}|{k[1]}": {kk: float(vv) for kk, vv in v.items() if kk != "screened"} |
                  {"screened": v["screened"]} for k, v in Q4.items()}
gal_screened = any(v["screened"] for (n, ft), v in Q4.items() if "galaxy" in n)
K5 = bool(not gal_screened)
P(f"  Q4: in a galaxy the stiffness is {'screened' if gal_screened else 'NOT screened'}; in the Solar System it is "
  f"{'screened' if Q4[('Solar System 1 AU', 'canonical')]['screened'] else 'not screened'}; in a cluster core "
  f"{'screened' if Q4[('cluster 1e15 @100 kpc', 'canonical')]['screened'] else 'not screened'}. "
  f"K5 (not screened in a galaxy) -> {'FIRES' if K5 else 'does not fire'}")

# ================================================================== Q3: a0(z) of this action through FRZ2's gate
P("\n==================== Q3: a0(z) of this action through FRZ2's forest gate")
# the action's own FRW scalar: V = V0 exp(-lambda chi sqrt(K)); in 8 pi G = 1 units sqrt(K) = 1/sqrt(2), so the
# exponent is -lambda_std chi with lambda_std = lambda/sqrt(2).  Thawing from rest at z_i = 100, Omega_phi0 = 1 - Om.
def bg_solve(lam_std, Om, z_i=100.0):
    def rhs(N, y):
        xx, yy = y
        q = 1 + xx * xx - yy * yy
        return [-3 * xx + lam_std * math.sqrt(1.5) * yy * yy + 1.5 * xx * q,
                -lam_std * math.sqrt(1.5) * xx * yy + 1.5 * yy * q]
    def run(y0):
        s = solve_ivp(rhs, [math.log(1 / (1 + z_i)), 0.0], [0.0, y0], rtol=1e-9, atol=1e-12, method="LSODA",
                      dense_output=True)
        return s, s.y[0, -1], s.y[1, -1]
    y0 = brentq(lambda y0: (lambda r: r[1] ** 2 + r[2] ** 2 - (1 - Om))(run(y0)), 1e-9, 0.35, xtol=1e-12)
    s, xx, yy = run(y0)
    return s, (xx * xx - yy * yy) / (xx * xx + yy * yy), xx * xx + yy * yy
def f_of_z(s, Om, zz):
    y0 = s.sol(0.0)[1]; out = []
    for z in zz:
        xx, yy = s.sol(-math.log(1 + z))
        E = math.sqrt(Om * (1 + z) ** 3 / max(1 - (xx * xx + yy * yy), 1e-30))
        out.append(yy * E / y0)
    return out
CPL_W0 = {"Pan": (-0.838, -0.62), "DES5": (-0.752, -0.86), "Uni": (-0.667, -1.09)}
ZG = list(np.linspace(0.0, 6.0, 601))
CASES = {"P0": {ft: [1.0] * len(ZG) for ft in FOOTS}}           # KA5: FRZ2's P0
for ft in FOOTS:                                                # KA5: FRZ2's own D-Pan f(z) = sqrt(F)
    w0_, wa_ = CPL_W0["Pan"]
    CASES.setdefault("D-Pan", {})[ft] = [math.sqrt((1 + z) ** (3 * (1 + w0_ + wa_)) * math.exp(-3 * wa_ * z / (1 + z)))
                                         for z in ZG]
LAMBDA_FIT = {}
for nm, (w0t, wa_t) in CPL_W0.items():
    for ft in FOOTS:
        lam = brentq(lambda l: bg_solve(l, OMF[ft])[1] - w0t, 0.02, 2.0, xtol=1e-6)
        s, w0m, Ophi = bg_solve(lam, OMF[ft])
        fz = f_of_z(s, OMF[ft], ZG)
        LAMBDA_FIT[(nm, ft)] = dict(lambda_std=lam, lambda_action=lam * math.sqrt(2), w0_model=w0m, w0_target=w0t,
                                    Ophi0=Ophi, f_z3=float(np.interp(3.0, ZG, fz)), f_z44=float(np.interp(4.4, ZG, fz)))
        CASES.setdefault(f"X-{nm}", {})[ft] = fz
        CASES.setdefault(f"MU3-{nm}", {})[ft] = [v * v for v in fz]
        P(f"  X-{nm:5s} {ft:9s} lambda_std {lam:.5f} (action's lambda {lam * math.sqrt(2):.5f}) w0 {w0m:+.4f} "
          f"(target {w0t:+.3f}) Omega_phi0 {Ophi:.4f} f(z=3) {np.interp(3.0, ZG, fz):.4f} f(z=4.4) {np.interp(4.4, ZG, fz):.4f}")
for nm, (w0_, wa_) in CPL_W0.items():
    zc = brentq(lambda z: w0_ + wa_ * z / (1 + z) + 1.0, 0.01, 50.0)
    P(f"  reported: the observed CPL {nm} (w0 {w0_}, wa {wa_}) crosses w = -1 at z = {zc:.2f}; a canonical scalar has "
      f"w >= -1 at every z, so this action cannot reproduce that CPL at any lambda (a0(z) is then fixed by the fit to w0)")
json.dump(dict(z=ZG, cases=CASES), open(os.path.join(HERE, "a0z1_fz.json"), "w"))
RES["Q"]["Q3_fits"] = {f"{k[0]}|{k[1]}": {kk: float(vv) for kk, vv in v.items()} for k, v in LAMBDA_FIT.items()}

CASES_RUN = ["P0", "D-Pan", "X-Pan", "X-DES5", "X-Uni", "MU3-Pan"]
if os.environ.get("A0Z1_SKIP_PIPE", "0") != "1":
    P(f"  running this lane's copy of FRZ2's halo model on {len(CASES_RUN)} cases x 2 footings, then the forest "
      f"(FRZ2's gate: Delta chi^2 <= 4 per footing over the 12 DESI P1D bins, reading L)")
    procs = []
    for c, ft in [(c, ft) for c in CASES_RUN for ft in FOOTS]:
        env = dict(os.environ, A0Z1_CASE=c, A0Z1_FOOT=ft)
        lg = open(os.path.join(HERE, "logs", f"hm_{c}_{ft}.log"), "w")
        procs.append((c, ft, subprocess.Popen([sys.executable, "a0z1_hm.py"], cwd=HERE, env=env, stdout=lg,
                                              stderr=subprocess.STDOUT)))
        while sum(1 for _, _, q in procs if q.poll() is None) >= 4:
            time.sleep(1.0)
    for c, ft, q in procs:
        q.wait(); P(f"    hm {c:8s} {ft:9s} exit {q.returncode}  [{time.time() - T0:.0f} s]")
    fps = []
    for ft in FOOTS:
        env = dict(os.environ, HLF1_FOOT=ft); env.pop("HLF1_MUTATE", None)
        lg = open(os.path.join(HERE, "logs", f"forest_{ft}.log"), "w")
        fps.append((ft, subprocess.Popen([sys.executable, "a0z1_forest.py"], cwd=HERE, env=env, stdout=lg,
                                         stderr=subprocess.STDOUT)))
    for ft, q in fps:
        q.wait(); P(f"    forest {ft:9s} exit {q.returncode}  [{time.time() - T0:.0f} s]")

RES["Q"]["Q3_forest"] = {}
if all(os.path.exists(os.path.join(HERE, f"a0z1_forest_{ft}.json")) for ft in FOOTS):
    FO = {ft: json.load(open(os.path.join(HERE, f"a0z1_forest_{ft}.json"))) for ft in FOOTS}
    for ft in FOOTS:
        RES["KA"][f"KA2_{ft}"] = dict(dchi2=FO[ft]["KA"]["KA2"]["dchi2"], pass_=bool(FO[ft]["KA"]["KA2"]["pass_"]))
        RES["KA"][f"KA3_{ft}"] = dict(dchi2=FO[ft]["KA"]["KA3"]["dchi2"], hlf1=FO[ft]["KA"]["KA3"]["hlf1"],
                                      pass_=bool(FO[ft]["KA"]["KA3"]["pass_"]))
        P(f"  inherited: KA2 (R = 1 -> 0) {FO[ft]['KA']['KA2']['dchi2']:.1e} -> "
          f"{'PASS' if FO[ft]['KA']['KA2']['pass_'] else 'FAIL'}; KA3 (CO1 z = 0 held) {FO[ft]['KA']['KA3']['dchi2']:.2f} "
          f"against HLF1 {FO[ft]['KA']['KA3']['hlf1']} -> {'PASS' if FO[ft]['KA']['KA3']['pass_'] else 'FAIL'}")
    P("  case     footing     Delta chi^2   gate <= 4   f(z=3)  R_cold(z3,k3/k5)")
    for nm in CASES_RUN:
        row = {}
        for ft in FOOTS:
            d = FO[ft]["cases"].get(nm)
            if d is None: continue
            row[ft] = d
            P(f"  {nm:8s} {ft:9s} {d['dchi2']:12.3f}   {d['label']:8s}  {d['f_z3']:.4f}  "
              f"{d['R_cold_z3_k135'][1]:.4f}/{d['R_cold_z3_k135'][2]:.4f}")
        RES["Q"]["Q3_forest"][nm] = {ft: dict(dchi2=v["dchi2"], label=v["label"], f_z3=v["f_z3"],
                                              R_cold_z3_k135=v["R_cold_z3_k135"]) for ft, v in row.items()}
    ka5 = {}
    for nm, want in (("P0", {"canonical": 9916.2, "alt": 9008.7}), ("D-Pan", {"canonical": 13657.7, "alt": 13418.1})):
        for ft in FOOTS:
            d = FO[ft]["cases"].get(nm)
            ka5[(nm, ft)] = bool(d and abs(d["dchi2"] - want[ft]) <= 0.1)
    RES["KA"]["KA5"] = dict(rows={f"{k[0]}|{k[1]}": v for k, v in ka5.items()}, pass_=all(ka5.values()))
    P("  KA5 (this lane's copy of FRZ2's pipeline against FRZ2's own printed numbers, 0.1): " +
      "; ".join(f"{k[0]} {k[1]} {'PASS' if v else 'FAIL'}" for k, v in ka5.items()))
    xs = [nm for nm in CASES_RUN if nm.startswith("X-")]
    all_fail = all(FO[ft]["cases"][nm]["label"] == "FAILS" for ft in FOOTS for nm in xs)
    any_pass = any(all(FO[ft]["cases"][nm]["label"] == "PASSES" for nm in xs) for ft in FOOTS)
    K2 = bool(all_fail and not any_pass)
    MU3_bite = all(abs(FO[ft]["cases"]["MU3-Pan"]["dchi2"] - FO[ft]["cases"]["X-Pan"]["dchi2"]) > 0.5 for ft in FOOTS)
    RES["MUTATE"]["MU3"] = dict(dchi2={ft: float(FO[ft]["cases"]["MU3-Pan"]["dchi2"]) for ft in FOOTS}, bites=bool(MU3_bite))
    P(f"  MU3 (f = V/V0, the square root of a0 = kappa sqrt(GV) dropped): Delta chi^2 "
      f"{FO['canonical']['cases']['MU3-Pan']['dchi2']:.1f} / {FO['alt']['cases']['MU3-Pan']['dchi2']:.1f} against X-Pan "
      f"{FO['canonical']['cases']['X-Pan']['dchi2']:.1f} / {FO['alt']['cases']['X-Pan']['dchi2']:.1f} -> "
      f"{'bites' if MU3_bite else 'DOES NOT BITE'}")
    RES["Q"]["Q3_label"] = dict(all_fail=bool(all_fail), any_pass_on_both=bool(any_pass), K2_fires=bool(K2))
    P(f"  K2 (every X case fails on both footings): {'FIRES' if K2 else 'does not fire'}")
else:
    P("  pipeline outputs missing (A0Z1_SKIP_PIPE=1 or a job failed): Q3 is NOT graded")
    K2 = False; RES["Q"]["Q3_label"] = dict(all_fail=None, any_pass_on_both=None, K2_fires=None)
    RES["MUTATE"]["MU3"] = dict(dchi2=None, bites=False)

# ================================================================== labels
P("\n==================== labels, kill conditions, mutations")
ok_KA = all(v.get("pass_", True) for v in RES["KA"].values())
ok_MU = all(v.get("bites", False) for v in RES["MUTATE"].values())
P(f"  known answers: " + "; ".join(f"{k} {'PASS' if v.get('pass_') else 'FAIL'}" for k, v in RES["KA"].items()))
P(f"  mutations: " + "; ".join(f"{k} {'bites' if v.get('bites') else 'DOES NOT BITE'}" for k, v in RES["MUTATE"].items()))
verdict = "NO VERDICT" if not (ok_KA and ok_MU and EOM_OK) else ("a0(chi) FAILS" if K2 else "a0(chi) PASSES")
LABEL = f"EOM {'CERTIFIED' if EOM_OK else 'REFUTED'}; {verdict} / {verdict}"
P(f"  Q1 EOM {'CERTIFIED' if EOM_OK else 'REFUTED'};  Q2 bracket negative anywhere: {'YES' if BRACKET_NEG else 'NO'};  "
  f"K3 runaway {'FIRES' if K3 else 'no'};  K4 a0 varies {'FIRES' if K4 else 'no'};  "
  f"K5 not screened in a galaxy {'FIRES' if K5 else 'no'};  K2 forest {'FIRES' if K2 else 'no'}")
P(f"  LABEL: {LABEL}")
RES["label"] = LABEL
RES["kills"] = dict(K1_EOM_refuted=bool(not EOM_OK), K2_forest=bool(K2), K3_runaway=bool(K3), K4_a0_varies=bool(K4),
                    K5_not_screened_in_galaxy=bool(K5))
RES["bracket_negative_anywhere"] = ("YES - the Solar System (u 6.3e7 at 1 AU, 1.0e11 at the Earth's surface, 2.9e12 at "
                                    "the solar surface) and, under the frozen point-mass bound, the core of a "
                                    "log M_b 11 galaxy (u 1.2e2-1.5e2 at 1 kpc); NOT in cluster cores (u 2-3, "
                                    "bracket +0.99) or at 10-100 kpc in a galaxy (u 0.3-1.5, bracket ~ +1)"
                                    if BRACKET_NEG else "NO")
_k = []
if K2: _k.append("K2 (a0(chi) fails FRZ2's forest gate, Delta chi^2 <= 4, on both footings)")
if K5: _k.append("K5 (gamma_L F(Pi) does not screen in a galaxy)")
if K3: _k.append("K3 (runaway)")
if K4: _k.append("K4 (a0 varies)")
if not EOM_OK: _k.append("K1 (EOM refuted)")
RES["kill_that_fired"] = "; ".join(_k) if _k else "none"
RES["elapsed_s"] = time.time() - T0
P(f"[{time.time() - T0:.0f} s]")
dump()
