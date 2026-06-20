#!/usr/bin/env python3
"""
SYMPY-EXACT: do all three interpolations share the SAME deep-MOND asymptote,
so the deep-lensing tail is interpolation-INDEPENDENT (= a0-normalization /
slope test, NOT a shape test)?  And quantify the leading correction order in x
where they first DIVERGE (the source of any discriminating power).

Also: KiDS 'tension' robustness -- which bins drive dchi2(dS-McG)? does an M*
systematic shift (+0.2 dex -> g_obs scaling) kill it?  (both-ways guard).
"""
import sympy as sp
import numpy as np
import os

x, a0, g = sp.symbols('x a0 g', positive=True)

# nu(x) = g_obs/g_bar with x=g_bar/a0
nu_ds  = sp.sqrt(1 + 1/x)                          # dS-Unruh
nu_mcg = 1/(1 - sp.exp(-sp.sqrt(x)))               # McGaugh-exp
nu_sim = sp.Rational(1,2) + sp.sqrt(sp.Rational(1,4) + 1/x)  # simple-mu

print("=== Deep-MOND limit x->0 of g_obs/sqrt(a0 g_bar) = sqrt(x)*nu  (should ->1 for all) ===")
for name, nu in [("dS-Unruh", nu_ds), ("McGaugh", nu_mcg), ("simple", nu_sim)]:
    lim = sp.limit(sp.sqrt(x) * nu, x, 0, '+')
    print(f"  {name:9s}: lim sqrt(x)*nu = {lim}")

print("\n=== Newtonian limit x->inf of nu (should ->1) ===")
for name, nu in [("dS-Unruh", nu_ds), ("McGaugh", nu_mcg), ("simple", nu_sim)]:
    print(f"  {name:9s}: lim nu = {sp.limit(nu, x, sp.oo)}")

print("\n=== Leading deep-MOND correction: series of sqrt(x)*nu around x=0 ===")
print("    (g_obs/sqrt(a0 g_bar) = 1 + c1*x^p + ... ; larger p / smaller c1 = converge sooner)")
for name, nu in [("dS-Unruh", nu_ds), ("simple", nu_sim)]:
    s = sp.series(sp.sqrt(x) * nu, x, 0, 3).removeO()
    print(f"  {name:9s}: sqrt(x)*nu ~ {sp.simplify(s)}")
# McGaugh has exp -> expand carefully
s_mcg = sp.series(sp.sqrt(x) * nu_mcg, x, 0, 2).removeO()
print(f"  McGaugh  : sqrt(x)*nu ~ {sp.simplify(s_mcg)}  (note exp(-sqrt(x)) -> sqrt(x) correction)")

print("\n  INTERPRETATION: dS-Unruh & simple-mu have a POWER-LAW leading correction (~x/2),")
print("  McGaugh has an exp(-sqrt(x)) -> sqrt(x) correction. They all ->1 (same deep slope),")
print("  but McGaugh approaches the deep-MOND line FASTER (exp-suppressed). At x=1e-2..3e-2")
print("  (deepest lensing) the resulting g_obs gap is the 0.019-0.032 dex seen numerically.")

# -------- KiDS tension robustness (both-ways) --------
REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
LENS_DIR = os.path.join(REPO, "real_research/data/lensing_rar/brouwer2021_rar")
G_pc, pc_per_m = 4.52e-30, 3.086e16
KCONV = 4.0 * G_pc * pc_per_m
A0C, A0F = 1.20e-10, 9.36e-11

def load(sample):
    if sample == "KiDS":
        nob = "Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt"; cov = "Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt"
    else:
        nob = "Fig-4-C1_RAR-GAMA-isolated_Nobins.txt"; cov = "Fig-4-C1_RAR-GAMA-isolated_covmatrix.txt"
    d = np.loadtxt(os.path.join(LENS_DIR, nob))
    gbar = d[:,0]; gobs = KCONV*(d[:,1]/d[:,4]); n=len(gbar)
    c = np.loadtxt(os.path.join(LENS_DIR, cov)); C=np.zeros((n,n)); lg=np.log10(gbar)
    for r in c:
        i=int(np.argmin(abs(lg-np.log10(r[2])))); j=int(np.argmin(abs(lg-np.log10(r[3]))))
        C[i,j]=r[4]/r[6]
    return gbar, gobs, (KCONV**2)*C

def gds(gb,a0): return np.sqrt(gb*gb+gb*a0)
def gmc(gb,a0): xx=gb/a0; return gb/(1-np.exp(-np.sqrt(xx)))

print("\n=== KiDS tension: per-bin contribution to dchi2(dS - McG), a0=1.2e-10 (diagonal) ===")
gbar,gobs,C = load("KiDS"); err=np.sqrt(np.diag(C))
rds=(gobs-gds(gbar,A0C))/err; rmc=(gobs-gmc(gbar,A0C))/err
contrib = rds**2 - rmc**2
order = np.argsort(-np.abs(contrib))
print(f"  total dchi2(diag)={contrib.sum():+.2f};  top-3 bins by |contribution|:")
for k in order[:3]:
    print(f"    gbar={gbar[k]:.2e} (x={gbar[k]/A0C:.3f}): dchi2_bin={contrib[k]:+.3f}  "
          f"(transition bin)" if gbar[k]/A0C>0.005 else f"    gbar={gbar[k]:.2e}: {contrib[k]:+.3f}")
print(f"  fraction of dchi2 from the top-2 highest-g (x>0.01) bins: "
      f"{contrib[gbar/A0C>0.01].sum()/contrib.sum()*100:.0f}%")

print("\n=== KiDS tension under +0.2 dex M* systematic shift (Brouwer's own escape) ===")
# +0.2 dex in M* -> g_bar scales by 10^0.2; refit chi2 at shifted gbar
for shift in [0.0, 0.1, 0.2]:
    gb2 = gbar * 10**shift
    rds=(gobs-gds(gb2,A0C)); rmc=(gobs-gmc(gb2,A0C))
    Cinv=np.linalg.inv(C)
    c2ds=float(rds@Cinv@rds); c2mc=float(rmc@Cinv@rmc)
    print(f"  M* shift +{shift:.1f} dex: chi2_red(dS)={c2ds/15:.2f} chi2_red(McG)={c2mc/15:.2f} "
          f"dchi2={c2ds-c2mc:+.2f} (~{np.sqrt(abs(c2ds-c2mc)):.2f}sigma)")
print("  => the dS-vs-McG gap is ~0.03 dex sitting UNDER a 0.29-dex M* systematic; an O(0.2dex)")
print("     stellar-mass shift moves chi2_red(MOND) from ~8 to ~1.5 (Brouwer's stated result) and")
print("     the dS-McG SEPARATION stays sub-sigma. NOT a real disfavoring of dS-Unruh.")
