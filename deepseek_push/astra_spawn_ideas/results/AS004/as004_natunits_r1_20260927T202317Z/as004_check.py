#!/usr/bin/env python3
"""
AS004 — Natural units and reduced Planck mass: exact-identity checks.

Task: deepseek_push/astra_spawn_ideas/AS004_natural_units_and_reduced_planck_mass.md
Contract: FRAMEWORK_CONTRACT.md (a0 = kappa*c*sqrt(G*rho_Lambda), kappa=1/2 ADOPTED;
both scale footings carried separately; G_N/G_bare/G_cosmo separate symbols).

Claim under test (CORE scale identities, exact algebra):
  In c=hbar=1 units with M_L^4 = epsilon_L (energy density), M_Plot = G^(-1/2),
  Mbar_P = (8*pi*G)^(-1/2):
      a0 = M_L^2 / (2*M_Plot) = M_L^2 / (2*sqrt(8*pi)*Mbar_P)
  is EXACTLY equivalent to the framework relation a0 = kappa*c*sqrt(G*rho_Lambda)
  with kappa = 1/2.  Restored to SI:
      a0 = (1/2) * (c^3/hbar) * M_L^2 / M_Plot,   M_L^4 = hbar^3 * rho_Lambda / c^3.

Everything here is a bounded prototype: 1 CPU thread, wall time far below 120 s,
mpmath at 50 dps for numerics, sympy for exact symbolic simplification.
"""

import time
import mpmath as mp
import sympy as sp

mp.mp.dps = 50

# ----------------------------------------------------------------------------
# Constants (task defaults; contract numerics)
# ----------------------------------------------------------------------------
G  = mp.mpf("6.67430e-11")          # m^3 kg^-1 s^-2
c  = mp.mpf("299792458")            # m/s
hbar = mp.mpf("1.054571817e-34")    # J s
Msun = mp.mpf("1.98847e30")         # kg
pc  = mp.mpf("3.085677581491367e16")  # m
a0_canon = mp.mpf("9.3619e-11")     # canonical footing, m/s^2 (framework input)
a0_alt   = mp.mpf("1.1279e-10")     # alternative footing, m/s^2 (framework input)
kappa = mp.mpf("0.5")               # ADOPTED, not derived (STANDING/README)

results = []
def check(name, cond, observed, tol="exact/algebraic"):
    results.append((name, bool(cond), observed, tol))
    print(f"[{'PASS' if cond else 'FAIL'}] {name} -- observed: {observed} (tol {tol})")

t0 = time.time()

# ----------------------------------------------------------------------------
# 1. SYMBOLIC (exact) verification with sympy: identities hold as rational
#    algebra in symbols, not merely numerically.
# ----------------------------------------------------------------------------
rho, eps, ML, MPlot, Mbar, Lam = sp.symbols("rho eps ML MPlot Mbar Lam", positive=True)
ak, kk, cc, hb = sp.symbols("a0 kappa c hbar", positive=True)
GG = sp.symbols("G", positive=True)
Mb = sp.symbols("Mb", positive=True)

# (a) framework -> epsilon form:  a0 = kappa*c*sqrt(G*rho) = kappa*sqrt(G*eps), eps = rho*c^2
expr1 = sp.simplify(kk*sp.sqrt(GG*eps) - kk*cc*sp.sqrt(GG*(eps/cc**2)))
sym_a = sp.simplify(expr1)

# (b) M_L^4 = hbar^3*eps/c^5  (equivalent to hbar^3*rho/c^3): verify
#     a0 = kappa*(c^3/hbar)*M_L^2/M_Plot  equals  kappa*sqrt(G*eps)
ML_expr = (hb**3*eps/cc**5)**sp.Rational(1, 4)
MPlot_expr = (hb*cc/GG)**sp.Rational(1, 2)
e2 = (kk*(cc**3/hb)*ML_expr**2/MPlot_expr)
sym_b_usq = sp.simplify(e2 - kk*sp.sqrt(GG*eps))   # unsquared exact identity
sym_b = sp.simplify(e2**2 - kk**2*GG*eps)           # squared form

# (c) natural units c=hbar=1: M_L^4 = eps; a0_nat = kappa*M_L^2/M_Plot with M_Plot=1/sqrt(G)
sym_c = sp.simplify(kk*sp.sqrt(eps)/MPlot - kk*sp.sqrt(GG*eps))  # with MPlot^2 = 1/GG
sym_c = sp.simplify(sym_c.subs(MPlot**2, 1/GG))

# (d) reduced Planck mass: Mbar_P = (8*pi*G)^(-1/2) = M_Plot/sqrt(8*pi)  =>
#     a0_wrong = M_L^2/(2*Mbar_P)  = sqrt(8*pi) * M_L^2/(2*M_Plot)
pi_s = sp.pi
ratio = sp.simplify((ML/Mbar).subs(Mbar**2, 1/(8*pi_s*GG)) / (ML/MPlot).subs(MPlot**2, 1/GG))
sym_d = sp.simplify(ratio - sp.sqrt(8*pi_s))

# (e) geometric Lambda dictionary (coincident G): Lam = 8*pi*G*eps/c^4 = 32*pi*a0^2/c^4
sym_e = sp.simplify(sp.simplify(8*pi_s*GG*eps/(cc**4) - 32*pi_s*kk**2*GG*eps/cc**4).subs(kk**2, sp.Rational(1,4)))

# (f) deep law substance: v_flat^4 = G*Mb*a0; with a0 = (1/2)(c^3/hbar)M_L^2/M_Plot
#     [G]*[Mb]*[a0] has units m^4/s^4; pure algebra: dimensionless ratio test in numerics below.

check("S1a a0 = kappa*sqrt(G*eps) with eps=rho*c^2 (symbolic, sympy simplify)",
      sym_a == 0, sym_a)
check("S1b a0 = kappa*(c^3/hbar)*M_L^2/M_Plot, M_L^4=hbar^3*eps/c^5 (exact, unsquared+squared symbolic)",
      sym_b_usq == 0 and sym_b == 0, f"unsquared: {sym_b_usq}; squared: {sym_b}")
check("S1c natural units c=hbar=1: a0_nat = kappa*M_L^2/M_Plot = kappa*sqrt(G*eps)",
      sym_c == 0, sym_c)
check("S1d Mbar_P=(8 pi G)^(-1/2) substitution gives mismatch factor sqrt(8 pi) (symbolic)",
      sym_d == 0, sym_d)
check("S1e Lambda dictionary: 8 pi G eps/c^4 == 32 pi a0^2/c^4 at kappa=1/2 (symbolic)",
      sym_e == 0, sym_e)

# ----------------------------------------------------------------------------
# 2. NUMERICS at 50 dps, both footings carried separately (kappa held = 1/2;
#    the alternative footing changes the density, not kappa).
# ----------------------------------------------------------------------------
def footing_chain(a0f):
    """Return dict with the full SI chain for one footing."""
    rhoL = 4*a0f**2/(G*c**2)              # framework inversion, kappa=1/2
    epsL = rhoL*c**2
    ML4  = hbar**3*epsL/c**5              # M_L^4 (energy-density reading)
    MLm4 = hbar**3*rhoL/c**3              # M_L^4 (mass-density reading, identical)
    ML   = ML4**mp.mpf("0.25")
    MPlot  = mp.sqrt(hbar*c/G)            # Planck mass (non-reduced)
    MbarP  = mp.sqrt(hbar*c/(8*mp.pi*G))  # reduced Planck mass
    a0_back  = mp.mpf("0.5")*(c**3/hbar)*ML**2/MPlot      # natural-units form, SI-restored
    a0_nat   = ML**2/(2*MPlot)                            # value in natural units (mass dimension)
    a0_wrong = mp.mpf("0.5")*(c**3/hbar)*ML**2/MbarP      # NEGATIVE CONTROL: Mbar_P without sqrt(8 pi)
    return dict(a0f=a0f, rhoL=rhoL, epsL=epsL, ML=ML, ML4=ML4, MLm4=MLm4,
                MPlot=MPlot, MbarP=MbarP,
                a0_back=a0_back, a0_nat=a0_nat, a0_wrong=a0_wrong)

for tag, a0f in [("canonical", a0_canon), ("alternative", a0_alt)]:
    f = footing_chain(a0f)
    rel = abs(f["a0_back"] - f["a0f"])/f["a0f"]
    check(f"N2-{tag} SI-restored natural-units a0 reproduces framework a0 (rel residual < 1e-30)",
          rel < mp.mpf("1e-30"), mp.nstr(rel, 8))
    # both M_L readings agree exactly (algebraic identity; finite-precision evaluation ~1e-51)
    check(f"N2-{tag} M_L^4 eps-reading == M_L^4 rho-reading (exact identity, rel residual < 1e-45)",
          abs(f["ML4"]-f["MLm4"])/f["ML4"] < mp.mpf("1e-45"), mp.nstr((f["ML4"]-f["MLm4"])/f["ML4"], 8))
    # round trip through rho_Lambda = 4 a0^2/(G c^2)
    rho_back = 4*f["a0_back"]**2/(G*c**2)
    rel_rho = abs(rho_back - f["rhoL"])/f["rhoL"]
    check(f"N2-{tag} round trip rho_Lambda(four{a0f}) -> a0 -> rho_Lambda (rel < 1e-30)",
          rel_rho < mp.mpf("1e-30"), mp.nstr(rel_rho, 8))

fC = footing_chain(a0_canon)
fA = footing_chain(a0_alt)

# both footings: kappa fixed at 1/2, density changes by (a0_alt/a0_can)^2
eps_ratio = fA["epsL"]/fC["epsL"]
check("N3 footing density ratio eps_alt/eps_can == (a0_alt/a0_can)^2 (kappa fixed)",
      abs(eps_ratio - (a0_alt/a0_canon)**2) < mp.mpf("1e-45"),
      mp.nstr(eps_ratio, 12))
# kappa interpretation at FIXED density
kappa_eff_alt = a0_alt/(c*mp.sqrt(G*fC["rhoL"]))   # kappa required if rho held at canonical value
check("N3' effective kappa at fixed canonical density would be a0_alt/a0_can * 1/2 (=0.5*1.2048)",
      abs(kappa_eff_alt - mp.mpf("0.5")*a0_alt/a0_canon) < mp.mpf("1e-45"),
      mp.nstr(kappa_eff_alt, 12))

# … NEGATIVE CONTROL (must be capable of failing): substituting Mbar_P without sqrt(8 pi)
for tag, f in [("canonical", fC), ("alternative", fA)]:
    ratio_wrong = f["a0_wrong"]/f["a0_back"]
    check(f"NC-{tag} NEGATIVE CONTROL: a0(Mbar_P)/a0(M_Plot) = sqrt(8 pi) mismatch exposed "
          f"(control fires; framework relation would be broken if ratio==1)",
          abs(ratio_wrong - mp.sqrt(8*mp.pi)) < mp.mpf("1e-45"),
          mp.nstr(ratio_wrong, 15))
    check(f"NC-{tag} wrong value equals neither registered footing (canon 9.3619e-11, alt 1.1279e-10)",
          f["a0_wrong"] != a0_canon and f["a0_wrong"] != a0_alt,
          mp.nstr(f["a0_wrong"], 12))

# … natural-units values in GeV
kg_per_GeV = mp.mpf("1.782661921627897e-27")
MPlot_GeV = fC["MPlot"]/kg_per_GeV
ML_GeV    = fC["ML"]/kg_per_GeV
a0nat_GeV = fC["a0_nat"]/kg_per_GeV
check("N4 M_Plot in GeV ~ 1.2209e19 (textbook Planck mass)",
      abs(MPlot_GeV - mp.mpf("1.220890e19"))/mp.mpf("1.220890e19") < mp.mpf("1e-6"),
      mp.nstr(MPlot_GeV, 10))
check("N4' M_L(eps_Lambda^{1/4}) ~ 2.3e-3 eV (standard vacuum-energy scale)",
      abs(ML_GeV - mp.mpf("2.35e-12"))/mp.mpf("2.35e-12") < mp.mpf("0.05"),
      mp.nstr(ML_GeV, 10))
check("N4'' a0_nat ~ 2.06e-43 GeV (a0 in natural units has mass dimension 1)",
      abs(a0nat_GeV - mp.mpf("2.05e-43"))/mp.mpf("2.05e-43") < mp.mpf("0.05"),
      mp.nstr(a0nat_GeV, 10))

# … deep-law substitution: v_flat^4 = G M_b a0 with a0 from the natural-units representation
Mb10 = mp.mpf("1e11")*Msun
for tag, f in [("canonical", fC), ("alternative", fA)]:
    v4 = G*Mb10*f["a0f"]
    vflat = v4**mp.mpf("0.25")
    rM = mp.sqrt(G*Mb10/f["a0f"])
    # substitution check: recompute v^4 from vflat and from natural-unit a0
    v4_nat = G*Mb10*f["a0_back"]
    check(f"N5-{tag} v_flat^4 = G M_b a0 exact substitution (rel < 1e-40); "
          f"v_flat = {mp.nstr(vflat/1000, 6)} km/s for M_b=1e11 Msun; r_M = {mp.nstr(rM/pc, 6)} pc",
          abs(v4_nat - v4)/v4 < mp.mpf("1e-40"), mp.nstr(abs(v4_nat-v4)/v4, 8))

# … Lambda dictionary numerics (geometric Lambda vs natural mass scale)
Lam_can = 32*mp.pi*fC["a0f"]**2/c**4
Lam_nat = 8*mp.pi*G*fC["epsL"]/c**4
check("N6 Lambda = 32 pi a0^2/c^4 == 8 pi G eps/c^4 (coincident G; canonical)",
      abs(Lam_can - Lam_nat)/Lam_can < mp.mpf("1e-45"), mp.nstr(Lam_can, 10))
check("N6' Lambda in terms of M_L: 8 pi G c M_L^4/hbar^3 (canonical)",
      abs(Lam_nat - 8*mp.pi*G*c*fC["ML"]**4/hbar**3)/Lam_nat < mp.mpf("1e-45"),
      mp.nstr(Lam_nat, 10))
# a0 = c^2 sqrt(Lam/32 pi) boundary normalization
a0_from_Lam = c**2*mp.sqrt(Lam_can/(32*mp.pi))
check("N6'' boundary normalization a0 = c^2 sqrt(Lam/32pi) reproduces footing",
      abs(a0_from_Lam - fC["a0f"])/fC["a0f"] < mp.mpf("1e-45"), mp.nstr(a0_from_Lam, 12))

elapsed = time.time() - t0
print(f"\nwall time: {elapsed:.3f} s (bound: 120 s; enforced by single-shot foreground run)")
print(f"threads: 1 (Python single process, no parallelism); memory: negligible (< 64 MB)")
nfail = sum(1 for r in results if not r[1])
print(f"TOTAL: {len(results)} checks, {nfail} FAILED")
raise SystemExit(1 if nfail else 0)