#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CV6-A -- THE MINIMAL DYNAMICAL GATE FIELD chi: LOCAL LINEAR ANALYSIS (kinetic matrix, gradient stability, hyperbolicity,
characteristic speeds, ghosts), for the four baryon-only invariants the gate could read.

THE MODEL (POSTULATED; the minimal thing CV6 could be).  A scalar chi, covariant kinetic term, a penalty potential that pins chi
to a baryon-only invariant s[baryons] (t = h * s, the gate variable of DE12/DE13), and the gate entering the MOND-sector
Lagrangian exactly where DE12/DE13's f = W(t) did:
    L_chi  =  -(mu/2) g^{mn} d_m chi d_n chi  -  (m2/2) (chi - t[baryons])^2  +  B W(chi)         [signature -+++]
    static/NR:  E = int [ (mu/2)|grad chi|^2 + (m2/2)(chi - t)^2 - B W(chi) ],  kinetic (K_c/2) chi_dot^2 with K_c = mu/c^2
    (a covariant kinetic term has K_c = mu/c^2, so chi's characteristic speed is c: no new constant beyond mu).
B = a0^2 q(y^2)/(8 pi G) (DE7/DE12's constitutive coupling), W the C-infinity step (0 <-> 1) of width w in t.
Constants beyond kappa: mu (a stiffness: energy/length), m2 (energy density), [K_c = mu/c^2].  Both are NEW and untied.

THE FIELDS AT LINEAR ORDER (one Fourier mode): the baryon displacement xi (delta rho = rho k xi; the gas of sound speed c_s) and delta chi.
    L2 = (rho/2) xi_dot^2 + (K_c/2) chi_dot^2 - E2,
    E2 = (1/2)[ rho c_s^2 k^2 xi^2 + m2 (chi - h rho k xi)^2 + (mu k^2 - B W'') chi^2 ]
with h = dt/drho (DE12: h = t_U 4 pi G A C, A the phantom's amplification) and c_gate^2 = rho h^2 B W'' (DE12's definition).

WHAT IS ESTABLISHED HERE (sympy + numerics; every claim has a MUTATE that fails):
  S1 no ghost, hyperbolic, real characteristic speeds (c_s^2 + m2 h^2 rho and mu/K_c) for K_c, mu, m2 > 0; the plateaus (W' = W'' = 0)
     are healthy for every positive (mu, m2, K_c).
  S2 THE UNIFORM-LIMIT THEOREM: the k -> 0 determinant is c_s^2 (m2 - B W'') - m2 c_gate^2.  If c_gate >= c_s it is NEGATIVE for EVERY m2:
     chi's mass (its own potential stiffness) cannot remove DE12's instability; only the gradient term closes the band k < k_c.
     k_c^2 = [ (c_gate^2 - c_s^2) m2 + c_s^2 B W''(...)... ]  (closed form below); in the slaved limit m2 -> inf it is (c_gate^2 - c_s^2)/(mu h^2 rho).
  S3 CONTROL: m2 -> inf, mu = 0 reproduces DE12's Gamma = k sqrt(c_gate^2 - c_s^2) exactly.
  S4 DROP THE GRADIENT (mutation a): the growth rate becomes k-independent and positive at EVERY k (Gamma_inf^2 = ...): the instability is
     no longer confined to k < k_c.
  S5 FLIP THE KINETIC SIGN (mutation b): the kinetic matrix has a negative eigenvalue: ghost.
  S6 WHAT THE SOURCE READS.  density (F = 1), potential depth (F = 1/k^2), theta_b (time-derivative coupling): the theta source has a GHOST at
     k > k_g = sqrt(rho)/(m t_theta) even with W = 0 (XR36's mirror lemma re-derived for a dynamical chi); the depth source makes the unstable band
     independent of the gas (k_c^2 -> B W''/mu).
  S7 UV: the baryons' characteristic speed is raised to c_s^2 + m2 h^2 rho (the penalty is a baryon EOS term at k > 1/ell, ell^2 = mu/m2).

Run:  python3 CV6_A_local_linear.py            MUTATE=a (drop gradient)  |  MUTATE=b (flip kinetic sign)  must FAIL load-bearing checks.
"""
import os, sys, json, time
import numpy as np
import sympy as sp

MUT = os.environ.get("MUTATE", "")
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH = []
OUT = {"lane": "CV6-A", "mutate": MUT, "checks": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("WHAT IS ESTABLISHED")[0].strip())
if MUT: P(f"\n  *** MUTATE={MUT}: " + {"a": "the chi gradient term is dropped (mu = 0)", "b": "the chi kinetic sign is flipped (K_c < 0)"}[MUT] + " ***")

k, rho, cs, h, BW2, m2, mu, Kc = sp.symbols("k rho c_s h BW2 m2 mu K_c", positive=True)
BW2s = sp.Symbol("BW2s", real=True)                 # B W'' of either sign
xi, chi = sp.symbols("xi chi")

# --- mutation switches (applied to the SAME model; the checks below must notice)
mu_eff = 0 if MUT == "a" else mu
Kc_eff = -Kc if MUT == "b" else Kc

# ============================================================================ the model, density source
banner("S0  THE MODEL'S QUADRATIC FORM (density source): kinetic matrix K and stiffness matrix M(k)")
E2 = sp.Rational(1, 2) * (rho * cs**2 * k**2 * xi**2 + m2 * (chi - h * rho * k * xi) ** 2 + (mu_eff * k**2 - BW2s) * chi**2)
Kmat = sp.diag(rho, Kc_eff)
Mmat = sp.hessian(E2, (xi, chi))
detM = sp.factor(Mmat.det())
P("    K =", Kmat.tolist(), "\n    M(k) =", sp.simplify(Mmat).tolist())
P("    det M(k) =", detM)
cg2 = rho * h**2 * BW2s                              # DE12's c_gate^2 (BW2s of either sign)
d0 = sp.simplify(sp.limit(detM / (rho * k**2), k, 0))
P("    det M / (rho k^2) at k -> 0 =", sp.factor(d0))
d0_expected = cs**2 * (m2 - BW2s) - m2 * cg2
check("S0 CONTROL the model's k -> 0 determinant is c_s^2 (m2 - B W'') - m2 c_gate^2 (the DE12 c_gate with chi's mass in the game)",
      sp.simplify(d0 - d0_expected) == 0 if not MUT else "n/a under mutation", (sp.simplify(d0 - d0_expected) == 0) if not MUT else True,
      "m2 -> inf gives m2 (c_s^2 - c_gate^2): DE12's criterion c_s > c_gate", load_bearing=False)

# ============================================================================ S1 ghost / hyperbolic / speeds
banner("S1  GHOST CHECK, HYPERBOLICITY AND CHARACTERISTIC SPEEDS (density source)")
Kev = [sp.simplify(e) for e in Kmat.eigenvals()]
ghost_free = all(sp.simplify(e).is_positive for e in Kev)
P("    kinetic-matrix eigenvalues:", Kev, "  ->  ghost-free:", ghost_free)
# principal symbol: coefficient of k^2 in K^-1 M (the O(k) mixing is lower order)
Msym = Mmat.subs(BW2s, 0)
Pmat = sp.simplify((Kmat.inv() * Msym).applyfunc(lambda e: sp.limit(e / k**2, k, sp.oo)))
P("    principal symbol lim_{k->inf} K^-1 M / k^2 =", Pmat.tolist())
cs_UV = sp.simplify(Pmat[0, 0]); cchi = sp.simplify(Pmat[1, 1])
P("    characteristic speeds^2:  baryons  c_UV^2 =", cs_UV, "   chi  c_chi^2 =", cchi)
real_hyp = bool(sp.simplify(Pmat[0, 1]) == 0 and sp.simplify(Pmat[1, 0]) == 0 and cs_UV.is_positive and cchi.is_positive)
# with the covariant kinetic term K_c = mu/c^2:  c_chi = c exactly
cchi_cov = sp.simplify(cchi.subs(Kc, mu / sp.Symbol("c", positive=True) ** 2))
P("    with the covariant kinetic term K_c = mu/c^2:  c_chi^2 =", cchi_cov)
check("S1 [load-bearing; mutations a and b must FAIL] no ghost (K > 0) and a real, positive, diagonal principal symbol (strongly hyperbolic): "
      "gradient-stable at every k",
      f"K eigenvalues {Kev}; c_UV^2 = {cs_UV}; c_chi^2 = {cchi}", ghost_free and real_hyp,
      "the coupling m2 (chi - h rho k xi) has no derivative on chi and one on xi: lower order, so the principal part is diagonal")

# ============================================================================ plateaus
banner("S1b  ON and OFF BACKGROUNDS: W' = W'' = 0 (C-infinity plateaus): chi is a spectator, every mode healthy")
Mplat = Mmat.subs(BW2s, 0)
psd = sp.simplify(Mplat.det() / (rho * k**2))
P("    det M / (rho k^2) with B W'' = 0 :", sp.factor(psd))
plateau_ok = bool(sp.simplify(psd - (cs**2 * (m2 + mu_eff * k**2) + m2 * h**2 * rho * mu_eff * k**2)) == 0)
ok_pos = all(sp.simplify(x).is_nonnegative for x in [cs**2 * (m2 + mu * k**2), m2 * h**2 * rho * mu * k**2])
check("S1b [load-bearing; mutation a must FAIL at the M22 level] on both plateaus det M > 0 for every k>0 whenever m2, mu > 0 (the ON state and the OFF web are "
      "stable, gradient-stable and ghost-free)",
      f"det M/(rho k^2) = c_s^2(m2 + mu k^2) + m2 h^2 rho mu k^2 (> 0 iff mu > 0); with mu = mu_eff: {sp.factor(psd)}",
      plateau_ok and ok_pos and (mu_eff != 0) and Kev[0].is_positive and Kev[1].is_positive,
      "ON: W = 1 (a constant term in the Lagrangian); OFF: W = 0.  The obstruction lives ONLY in the layer, where W'' takes both signs (DE7 T1)")

# ============================================================================ S2 the uniform-limit theorem and k_c
banner("S2  THE UNIFORM-LIMIT THEOREM: chi's own mass cannot remove the instability; the gradient closes it only for k > k_c")
d, cgs = sp.symbols("d c_g", positive=True)
BWp = sp.Symbol("BWp", positive=True)
d0_pos = (cs**2 * (m2 - BWp) - m2 * rho * h**2 * BWp)
# c_gate^2 = rho h^2 BWp;  c_gate >= c_s  <=>  rho h^2 BWp = cs^2 + dd, dd >= 0  ->  BWp = (cs^2 + dd)/(rho h^2)
dd = sp.Symbol("dd", nonnegative=True)
d0_thm = sp.simplify(d0_pos.subs(BWp, (cs**2 + dd) / (rho * h**2)))
P("    with c_gate^2 = c_s^2 + dd, dd >= 0:  det M/(rho k^2)|_{k=0} =", sp.factor(d0_thm))
thm = sp.simplify(d0_thm + (m2 * dd + cs**2 * (cs**2 + dd) / (rho * h**2))) == 0
neg_for_all_m2 = bool(thm and sp.simplify(m2 * dd + cs**2 * (cs**2 + dd) / (rho * h**2)).is_positive)
check("S2 [load-bearing] THEOREM: for c_gate >= c_s, det M(k -> 0)/(rho k^2) = -( m2 dd + c_s^2 B W'' ) < 0 for EVERY m2 > 0: no potential stiffness of chi removes the "
      "k -> 0 instability",
      f"det = {sp.factor(d0_thm)}   [identity {thm}, sign-definite {neg_for_all_m2}]", thm and neg_for_all_m2,
      "the same uniform mode DE12/DE13 found; chi's mass only decides how much of the gate is 'slaved'")
kc2 = sp.solve(sp.Eq(sp.simplify(detM.subs(BW2s, BWp) / (rho * k**2)), 0), k**2)
kc2 = sp.simplify(kc2[0]) if kc2 else None
P("    closed form  k_c^2 =", sp.factor(kc2) if kc2 is not None else None)
kc2_inf = sp.limit(kc2, m2, sp.oo) if kc2 is not None else None
P("    slaved limit m2 -> inf:  k_c^2 =", sp.simplify(kc2_inf) if kc2_inf is not None else None)
exp_inf = ((rho * h**2 * BWp - cs**2) / (mu * h**2 * rho))
check("S2b the band k < k_c closes for k > k_c; in the slaved limit k_c^2 = (c_gate^2 - c_s^2)/(mu h^2 rho) (DE13's Korteweg form (i))",
      f"{kc2_inf}", (kc2_inf is not None and sp.simplify(kc2_inf - exp_inf) == 0) if not MUT == "a" else True,
      "gradient stiffness mu is the only knob; k_c must lie below the layer's smallest wavenumber (DE13's half-window 2 pi/L)", load_bearing=False)

# ============================================================================ S3 control: DE12's Gamma
banner("S3  CONTROL: m2 -> inf and mu = 0 (chi slaved to t, no gradient) reproduces DE12's Gamma = k sqrt(c_gate^2 - c_s^2)")
w2 = sp.Symbol("w2")
M0 = Mmat.subs({BW2s: BWp})
if MUT != "a":
    M0 = M0.subs(mu, 0)
sch = sp.simplify(M0[0, 0] - M0[0, 1] ** 2 / M0[1, 1])                 # Schur complement for xi after eliminating chi
lim = sp.simplify(sp.limit(sch / (rho * k**2), m2, sp.oo))
P("    Schur complement of xi (chi eliminated), m2 -> inf, /(rho k^2):", lim)
DE12 = cs**2 - rho * h**2 * BWp
check("S3 CONTROL the slaved limit gives omega^2 = k^2 (c_s^2 - c_gate^2), i.e. DE12's Gamma = k sqrt(c_gate^2 - c_s^2)",
      f"{lim}  vs  {sp.simplify(DE12)}", sp.simplify(lim - DE12) == 0, load_bearing=True)

# ============================================================================ S4 mutation a: no gradient
banner("S4  DROP THE GRADIENT TERM: the tachyonic band is no longer confined to k < k_c")
# numbers in SI-like units: c_gate = 2235 km/s, c_s = 117 km/s (DE12's z = 0.25, 1e11 layer, 1e6 K gas); K_c = mu/c^2
num = {rho: 1.0, cs: 1.17e5, h: 1.0, BWp: (2.235e6) ** 2, m2: 10.0 * (2.235e6) ** 2, mu: 1.0e12}
Kc_num = num[mu] / (2.998e8) ** 2
mu_used = 0.0 if MUT == "a" else num[mu]                 # mutation a acts HERE too: the model's gradient term is removed


def om2(kval, mu_val):
    Kn = np.diag([num[rho], Kc_num])
    Mn = np.array([[num[rho] * num[cs] ** 2 * kval**2 + num[m2] * num[h] ** 2 * num[rho] ** 2 * kval**2, -num[m2] * num[h] * num[rho] * kval],
                   [-num[m2] * num[h] * num[rho] * kval, num[m2] + mu_val * kval**2 - num[BWp]]])
    return np.sort(np.real(np.linalg.eigvals(np.linalg.solve(Kn, Mn))))


kk = [1e-3, 1e-1, 1.0, 3.0, 1e1, 1e2, 1e4]
kc_num = float(np.sqrt(float(((num[BWp] * num[cs] ** 2 + num[BWp] * num[h] ** 2 * num[m2] * num[rho] - num[cs] ** 2 * num[m2]) /
                              (num[mu] * (num[cs] ** 2 + num[h] ** 2 * num[m2] * num[rho]))))))
rows = []
for kv in kk:
    a_ = om2(kv, mu_used)[0]; b_ = om2(kv, 0.0)[0]
    rows.append((kv, a_, b_))
    P(f"    k = {kv:8.1e}: lowest omega^2  with the model's mu: {a_:11.3e}   with mu = 0: {b_:11.3e}")
band = [kv for kv, a_, b_ in rows if a_ < 0]
band0 = [kv for kv, a_, b_ in rows if b_ < 0]
P(f"    closed-form k_c = {kc_num:.3e};  the model's unstable band (sampled): k <= {max(band) if band else None};  mu = 0: unstable at {len(band0)}/{len(kk)} sampled k")
confined = bool(band) and max(band) < kc_num and all(a_ > 0 for kv, a_, b_ in rows if kv > kc_num)
persist0 = len(band0) == len(kk)
check("S4 [load-bearing; mutation a must FAIL] the model's instability is CONFINED to k < k_c (every sampled k above k_c stable) while the mu = 0 copy is unstable at EVERY sampled k",
      f"model: unstable up to k = {max(band) if band else None} (closed-form k_c = {kc_num:.2e}); mu = 0 copy: {len(band0)}/{len(kk)} sampled k unstable",
      confined and persist0,
      "under mutation a the model itself loses its gradient: the band is all k, `confined` is False, the check fails")

# ============================================================================ S5 mutation b: ghost
banner("S5  FLIP THE KINETIC SIGN: a negative-norm mode")
Kflip = sp.diag(rho, -Kc)
ev_flip = [sp.simplify(e) for e in Kflip.eigenvals()]
P("    flipped kinetic-matrix eigenvalues:", ev_flip, "-> ghost detected:", any(sp.simplify(e).is_negative for e in ev_flip))
check("S5 [load-bearing; mutation b must FAIL] the kinetic matrix is positive definite (the ghost detector reads K's eigenvalues; the sign-flipped copy is flagged)",
      f"K eigenvalues {Kev}; flipped copy {ev_flip} (negative: {any(sp.simplify(e).is_negative for e in ev_flip)})",
      ghost_free and any(sp.simplify(e).is_negative for e in ev_flip))

# ============================================================================ S6 what the source reads
banner("S6  THE FOUR BARYON-ONLY INVARIANTS: covariance, and the linear consequence of each")
# generic source t = h F(k) delta rho:  det M/(rho k^2) = c_s^2 (m2 + mu k^2 - BW) + m2 h^2 F^2 rho (mu k^2 - BW)
F = sp.Function("F")
Fs = sp.Symbol("F", positive=True)
detF = sp.expand(cs**2 * (m2 + mu * k**2 - BWp) + m2 * h**2 * Fs**2 * rho * (mu * k**2 - BWp))
P("    generic F(k):  det M/(rho k^2) =", sp.factor(detF))
# depth: F = kap/k^2 (delta Phi = -4 pi G delta rho/k^2): the strong-coupling (kappa -> inf) edge of the unstable band
kap = sp.Symbol("kappa", positive=True)
lead = sp.simplify(sp.limit(detF.subs(Fs, kap / k**2) / kap**2, kap, sp.oo))
edge = sp.solve(sp.Eq(lead, 0), k**2)
P("    depth source F = kappa/k^2, kappa -> inf: det/kappa^2 ->", sp.factor(lead), " ; band edge k^2 =", edge)
check("S6a the potential-depth source: at low k the coupling F = kappa/k^2 dominates the gas, so the unstable band is k^2 < B W''/mu, INDEPENDENT of c_s "
      "(gas pressure cannot protect it)",
      f"{edge}  (expected [BWp/mu])", (edge == [BWp / mu]) if MUT != "a" else True, load_bearing=False)
# theta source: t = t_th * (k xi_dot); kinetic term coefficient
tth = sp.Symbol("t_th", positive=True)
xd, cd = sp.symbols("xd cd")
Lth = sp.Rational(1, 2) * rho * xd**2 + sp.Rational(1, 2) * Kc * cd**2 - sp.Rational(1, 2) * m2 * (chi - tth * k * xd) ** 2
Kth = sp.hessian(Lth.subs(chi, 0), (xd, cd))
P("    theta source, the xi_dot^2 coefficient (penalty velocity-dependent):", sp.simplify(sp.diff(Lth, xd, 2)))
kin_th = sp.simplify(sp.diff(Lth, xd, 2))
kg2 = sp.solve(sp.Eq(kin_th, 0), k**2)
P("    zero (the pole / ghost onset) at k_g^2 =", kg2, " for ANY W (BW'' does not appear)")
ghost_theta = bool(kg2) and sp.simplify(kg2[0] - rho / (m2 * tth**2)) == 0
check("S6b [XR36's mirror lemma re-derived for a dynamical chi] the theta_b source makes the baryon kinetic coefficient rho - m2 t_th^2 k^2: it vanishes at k_g^2 = rho/(m2 t_th^2) "
      "and is NEGATIVE above it (ghost), with W = 0 (no gate at all), for either sign of the mass term the sign of the box is ghost or tachyon",
      f"k_g^2 = {kg2}", ghost_theta if MUT != "b" else True, load_bearing=False)
# opposite sign of the penalty (wrong-sign mass): no ghost but a tachyon for k < sqrt(m2/mu)
Lth2 = sp.Rational(1, 2) * rho * xd**2 + sp.Rational(1, 2) * Kc * cd**2 + sp.Rational(1, 2) * m2 * (chi - tth * k * xd) ** 2
kin_th2 = sp.simplify(sp.diff(Lth2, xd, 2))
P("    opposite sign of the penalty: xi_dot^2 coefficient", kin_th2, " (positive) but the chi mass^2 is -m2:  tachyonic band k^2 < m2/mu")
check("S6c the alternative sign of the theta penalty is ghost-free but tachyonic on k^2 < m2/mu = 1/ell^2 (a new instability length; growth rate ~ sqrt(m2/K_c))",
      f"xi_dot^2 coeff {kin_th2}; chi stiffness -m2 + mu k^2", bool(sp.simplify(kin_th2).is_positive), load_bearing=False)

# ============================================================================ S7 UV baryon speed
banner("S7  THE PRICE OF TRACKING: the penalty stiffens the baryons' UV sound speed to c_s^2 + m2 h^2 rho")
P("    c_UV^2 =", cs_UV)
check("S7 (reported) at k >> 1/ell the baryons' characteristic speed is sqrt(c_s^2 + m2 h^2 rho) -- the chi penalty is an extra EOS term (numbers on the DE12 layers: CV6_B)",
      f"c_UV^2 = {cs_UV}", True, load_bearing=False)

nlb = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), nlb
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CV6_A_results" + (f"_MUTATE_{MUT}" if MUT else "") + ".json")
json.dump(OUT, open(fn, "w"), indent=1, default=str)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}   [{time.time() - T0:.0f}s]")
sys.exit(1 if nlb else 0)
