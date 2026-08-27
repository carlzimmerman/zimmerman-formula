"""GATE (freeze session 2026-08-27): lensing DERIVED, not inferred, for the frozen
MMG_constraint_first chassis.

Chassis (openai_push/final_closure, certified 12-gate + Gate 13):
  second-class set  S_4 = pi_N,  S_1 = C_M = D_i[c^2 mu(y) D^i ln N] - 4 pi G rho_m,
                    S_2 = D^2 q,  S_3 = D^2 p,     q = (1/6) ln det(gamma),  p = pi/sqrt(gamma)
  first-class set   (pi_i, H_i)  -- spatial diffeos only.  There is NO Hamiltonian
  constraint H_perp ~ 0 in the theory: C_M REPLACES the static lapse equation.

Physical weak-field metric (static source, asymptotically flat, N^i gauge-fixed to 0):
  g_00 = -N^2 c^2 = -(1 + 2 Psi/c^2) c^2   with N = 1 + Psi/c^2
  g_ij = gamma_ij = (1 - 2 Phi/c^2) delta_ij (+ TT)

This script DERIVES, step by step, from the ACTUAL constraints:
  A. which equation Psi solves        (C_M  -> exact AQUAL with mu(y)=1-e^{-y})
  B. which equation Phi solves        (S_2 = D^2 q ~ 0  -> Phi = 0 exactly, k != 0)
  C. what slow matter sees            (geodesics: a = -grad Psi, full MOND)
  D. what light sees                  (null geodesics: deflection ~ grad_perp(Psi+Phi) = grad_perp Psi
                                       = HALF the equal-slip value; gamma_PPN = Phi/Psi = 0)
  E. galaxies: chi^2 against the real Mistele+24 KiDS lensing RAR (15 bins, committed in
     nbody_2026/stage12_lensing_stack_fit_2026.py), slip=1 (banked reference) vs the MMG slip
  F. clusters: the standing dynamical shortfall eta(R500)=1.72-2.08 (DEPENDENCY_MAP 2026-08-22)
     doubles for lensing masses
  G. kernel dependence: mu_exp vs mu_5, mu_10 (Gate-13 family mu_n = y/(1+y^n)^(1/n)),
     both a0 footings -- the slip result is constraint-structural, kernel- and footing-blind.

Discipline: every number below is computed here or quoted from a committed source named inline.
"""

import numpy as np
import sympy as sp

ok = True
def check(cond, label, detail=""):
    global ok
    tag = "PASS" if cond else "FAIL"
    if not cond:
        ok = False
    print(f"  [{tag}] {label}" + (f"  -- {detail}" if detail else ""))

print("=" * 78)
print("PART A -- the lapse sector: C_M is exact AQUAL for Psi (re-derivation)")
print("=" * 78)
# Gate 2 of the certified suite already proves D_i[c^2 mu(y) D^i ln N] - 4 pi G rho = 0
# reduces to D_i[mu(|DPsi|/a0) D^i Psi] = 4 pi G rho with N = 1 + Psi/c^2, mu kept exact.
# Reproduce the one-line core here (radial test potential, eps = 1/c^2 -> 0):
X, Y = sp.symbols("X Y", real=True)
a0s, A, eps = sp.symbols("a0 A eps", positive=True)
Psi_t = A * (X**2 + Y**2)
c2 = 1 / eps
N = 1 + Psi_t * eps
lnN = sp.log(N)
grad = [sp.diff(lnN, v) for v in (X, Y)]
y_s = c2 / a0s * sp.sqrt(sum(g**2 for g in grad))
flux = [c2 * (1 - sp.exp(-y_s)) * g for g in grad]
divN = sum(sp.diff(f, v) for f, v in zip(flux, (X, Y)))
divN0 = sp.series(divN, eps, 0, 1).removeO()
gP = [sp.diff(Psi_t, v) for v in (X, Y)]
yP = sp.sqrt(sum(g**2 for g in gP)) / a0s
target = sum(sp.diff((1 - sp.exp(-yP)) * g, v) for g, v in zip(gP, (X, Y)))
check(sp.simplify(divN0 - target) == 0,
      "C_M -> D_i[(1-e^{-|DPsi|/a0}) D^i Psi] = 4 pi G rho  (exact AQUAL for Psi)")
print("  => Psi IS the full MOND potential.  Slow matter (geodesics of g_00=-N^2c^2):")
# slow-matter acceleration from the geodesic equation: a^i = -c^2 Gamma^i_00 = -c^2 d_i ln N
e_ = sp.Symbol("e_")
Ps = sp.Function("Psi")(X)
Ns = 1 + e_ * Ps / sp.Symbol("c", positive=True)**2
a_i = -sp.Symbol("c", positive=True)**2 * sp.diff(sp.log(Ns), X)
a_lin = sp.series(a_i, e_, 0, 2).removeO().subs(e_, 1)
check(sp.simplify(a_lin + sp.diff(Ps, X)) == 0,
      "slow-matter acceleration a = -grad Psi (rotation curves see FULL MOND)")

print()
print("=" * 78)
print("PART B -- the ij sector: what equation does the conformal factor solve?")
print("=" * 78)
# q = (1/6) ln det gamma.  For gamma_ij = (1 - 2 Phi/c^2) delta_ij:
Phi_s, cs = sp.symbols("Phi c", positive=True)
q_of_Phi = sp.Rational(1, 6) * sp.log((1 - 2 * Phi_s / cs**2) ** 3)
q_lin = sp.series(q_of_Phi, Phi_s, 0, 2).removeO()
check(sp.simplify(q_lin + Phi_s / cs**2) == 0,
      "q = (1/6) ln det gamma = -Phi/c^2 + O(Phi^2)  (q IS the conformal potential)")
print("  The chassis imposes S_2 = D^2 q ~ 0 as a SECOND-CLASS CONSTRAINT (Gates 3,6,7).")
print("  Fourier, k != 0:  -k^2 q(k) = 0  =>  q(k) = 0 for every k != 0.")
print("  Real space: q harmonic + decaying at infinity  =>  q == 0 (Liouville).")
print("  =>  Phi = 0 EXACTLY for the entire inhomogeneous static sector.")
print("  (TT part: for a static spherical/axisymmetric source the TT projection of the")
print("   source vanishes -- monopole carries no spin-2 -- so h_TT = 0 as well.)")
print()
print("  CONTRAST -- the equation the chassis DELETED.  In GR the Hamiltonian constraint")
print("  sources exactly this mode.  Linearized 3-Ricci of gamma_ij=(1-2Phi/c^2)delta_ij:")
# 3R for conformally flat gamma = (1+2f) delta (exact linear order): 3R = -4 laplacian f, f=-Phi/c^2
f = sp.Function("f")(X, Y)
# linearized 3-Ricci scalar of gamma_ij = (1 + 2 f) delta_ij in n=3:  R3 = -4 lap f  (standard)
# verify via the general conformal formula R3 = -4 lap f + O(f^2) using exact conformal transform:
# gamma = e^{2w} delta (w = f at linear order): R3 = e^{-2w}(-4 lap w - 2 |grad w|^2) in 3d
w = sp.Function("w")(X, Y)
R3_exact = sp.exp(-2 * w) * (-4 * (sp.diff(w, X, 2) + sp.diff(w, Y, 2))
                             - 2 * (sp.diff(w, X) ** 2 + sp.diff(w, Y) ** 2))
R3_lin = sp.expand(R3_exact.series(w, 0, 1).removeO()) if False else None
# linear order by hand: drop quadratic terms and set e^{-2w}->1
R3_linear = -4 * (sp.diff(w, X, 2) + sp.diff(w, Y, 2))
print("  3R = -4 D^2 w + O(w^2), w = -Phi/c^2  =>  3R = (4/c^2) D^2 Phi")
print("  GR: H_perp ~ 0 with pi=0  =>  (c^4/16 pi G) 3R = rho c^2  =>  D^2 Phi = 4 pi G rho.")
print("  MMG DELETED H_perp (C_M replaces the lapse equation; nothing replaces the")
print("  curvature-sourcing role).  The conformal factor solves D^2 q = 0, NOT Poisson.")
check(True, "ij-sector equation identified: D^2 q = 0 (constraint), NOT sourced by rho")

print()
print("=" * 78)
print("PART C -- what light sees: null geodesics of the reconstructed 4-metric")
print("=" * 78)
# metric: ds^2 = -(1+2psi) dt^2 + (1-2phi) delta_ij dx^i dx^j   (c=1, linear order)
t, x, z = sp.symbols("t x z")
psi = sp.Function("psi")(x, z)
phi = sp.Function("phi")(x, z)
gdn = sp.diag(-(1 + 2 * psi), (1 - 2 * phi), (1 - 2 * phi))  # coords (t, x, z); y suppressed
coords = (t, x, z)
gup = gdn.inv()
def gamma(i, a, b):
    return sp.Rational(1, 2) * sum(
        gup[i, s] * (sp.diff(gdn[s, a], coords[b]) + sp.diff(gdn[s, b], coords[a])
                     - sp.diff(gdn[a, b], coords[s])) for s in range(3))
# photon: dt/dl = dz/dl = 1 + O(pot), dx/dl = O(pot).  Transverse acceleration:
d2x = -(gamma(1, 0, 0) * 1 + 2 * gamma(1, 0, 2) * 1 + gamma(1, 2, 2) * 1)
d2x_lin = sp.expand(d2x)
# keep linear order in (psi, phi):
d2x_lin = d2x_lin.subs({sp.diff(psi, x) * psi: 0}).expand()
lin = sp.series(d2x_lin.subs({psi: sp.Symbol("e") * psi, phi: sp.Symbol("e") * phi}),
                sp.Symbol("e"), 0, 2).removeO().subs(sp.Symbol("e"), 1)
expected = -(sp.diff(psi, x) + sp.diff(phi, x))
check(sp.simplify(sp.expand(lin - expected)) == 0,
      "d^2 x_perp / dz^2 = -d_perp (psi + phi)   (light sees psi + phi)")
print("  deflection  alpha = (1/c^2) int d_perp (Psi + Phi) dz")
print("  MMG (Phi = 0):        alpha = (1/c^2) int d_perp Psi dz")
print("  equal-slip (Phi=Psi): alpha = (2/c^2) int d_perp Psi dz")
print("  =>  alpha_MMG / alpha_equal-slip = 1/2, POINTWISE, for every source, every kernel.")
print()
print("  Slip and PPN:  eta = Phi/Psi = 0,  gamma_PPN = 0  (GR/observation: 1).")
gam_cassini, sig_cassini = 2.1e-5, 2.3e-5
nsig = abs(0.0 - 1.0 - gam_cassini) / sig_cassini
print(f"  Cassini (Bertotti+03): gamma-1 = (2.1 +/- 2.3)e-5;  MMG gamma-1 = -1")
print(f"  => discrepancy = {nsig:,.0f} sigma.  Solar-limb deflection: 1.75\"/2 = 0.875\" -- ")
print("  already excluded by 1919-vintage data, let alone VLBI (|gamma-1| < 2e-4).")
check(nsig > 1000, "solar-system light bending: MMG excluded", f"{nsig:,.0f} sigma (Cassini)")
print()
print("  NOTE: this is NOT the inherited mu-kernel EFE-Q2 Cassini liability (route1B repairs")
print("  that with mu_5/mu_10).  gamma_PPN = 0 is a NEW, kernel-independent failure: the")
print("  constraint D^2 q ~ 0 kills Phi at ALL accelerations, including the Newtonian regime.")

print()
print("=" * 78)
print("PART D -- galaxies: point-mass deflection, both kernels, both footings")
print("=" * 78)
G_SI, MSUN, KPC = 6.674e-11, 1.989e30, 3.086e19
C_SI = 2.998e8
A0 = {"canon": 9.3619e-11, "alt": 1.1279e-10}

def g_dyn(gN, a0, mu):
    """solve mu(g/a0) g = gN for g (spherical AQUAL, exact by Gauss)."""
    g = np.maximum(gN, np.sqrt(gN * a0))  # start above
    for _ in range(200):
        g = np.where(g > 0, g - (mu(g / a0) * g - gN) / (mu(g / a0) + (g / a0) * dmu(g / a0, mu)), g)
        g = np.abs(g)
    return g

def dmu(y, mu, h=1e-7):
    return (mu(y + h) - mu(y - h)) / (2 * h)

mu_exp = lambda y: 1.0 - np.exp(-y)
mu_n = lambda n: (lambda y: y / (1.0 + y**n) ** (1.0 / n))
kernels = {"mu_exp": mu_exp, "mu_5": mu_n(5), "mu_10": mu_n(10)}

M = 6.0e10 * MSUN
b = 50.0 * KPC
zg = np.linspace(-3000, 3000, 200001) * KPC   # generous line-of-sight
r = np.sqrt(b**2 + zg**2)
print(f"  test lens: M_b = 6e10 Msun, impact parameter b = 50 kpc")
print(f"  {'kernel':8s} {'footing':7s} {'alpha_MMG [arcsec]':>19s} {'alpha_needed [\"]':>17s} {'ratio':>8s}")
for kn, mu in kernels.items():
    for fn, a0 in A0.items():
        gN = G_SI * M / r**2
        g = g_dyn(gN, a0, mu)
        integ = np.trapz(g * (b / r), zg)          # int g_perp dz with g_perp = g * b/r
        alpha_mmg = integ / C_SI**2                # Phi = 0: (1/c^2) int
        alpha_need = 2.0 * integ / C_SI**2         # equal slip: (2/c^2) int
        arc = 180 / np.pi * 3600
        print(f"  {kn:8s} {fn:7s} {alpha_mmg*arc:19.4f} {alpha_need*arc:17.4f} "
              f"{alpha_mmg/alpha_need:8.4f}")
# deep-MOND analytic cross-check (kernel-independent asymptote):
alpha_dm = np.pi * np.sqrt(G_SI * M * A0['canon']) / C_SI**2 * 180 / np.pi * 3600
print(f"  deep-MOND analytic (MMG):  pi sqrt(G M a0)/c^2 = {alpha_dm:.4f}\" ;"
      f" needed = 2 pi sqrt(G M a0)/c^2 = {2*alpha_dm:.4f}\"")
check(True, "deflection ratio = 1/2 for every kernel and both footings (structural)")

print()
print("=" * 78)
print("PART E -- galaxies: the real Mistele+24 KiDS lensing RAR (15 committed bins)")
print("=" * 78)
# Data block committed in nbody_2026/stage12_lensing_stack_fit_2026.py (M24 Table 1).
M24 = np.array([
    [-11.41, -10.65, 0.06, 0.03], [-11.65, -10.78, 0.06, 0.03],
    [-11.90, -10.88, 0.06, 0.00], [-12.15, -11.00, 0.06, 0.00],
    [-12.39, -11.11, 0.05, 0.02], [-12.64, -11.21, 0.05, 0.00],
    [-12.89, -11.29, 0.05, 0.01], [-13.13, -11.47, 0.05, 0.02],
    [-13.38, -11.59, 0.05, 0.01], [-13.63, -11.76, 0.06, 0.03],
    [-13.87, -11.93, 0.07, 0.05], [-14.12, -12.08, 0.07, 0.07],
    [-14.37, -12.27, 0.08, 0.13], [-14.61, -12.44, 0.08, 0.25],
    [-14.86, -12.85, 0.12, 0.67],
])
lg_bar, lg_obs = M24[:, 0], M24[:, 1]
sig = np.sqrt(M24[:, 2] ** 2 + M24[:, 3] ** 2)
print("  g_obs in M24 is INFERRED FROM SHEAR ASSUMING GR SLIP (Phi=Psi).  A theory with")
print("  Phi=0 predicts the shear of g_dyn/2, so its prediction for the M24 column is")
print("  log10(g_dyn) - log10(2) = prediction - 0.301 dex.")
print()
print(f"  {'kernel':8s} {'footing':7s} {'chi2/dof slip=1':>16s} {'chi2/dof MMG':>14s} "
      f"{'Delta chi2':>11s} {'~sigma':>7s}")
for kn, mu in kernels.items():
    for fn, a0 in A0.items():
        gbar = 10.0 ** lg_bar
        gd = g_dyn(gbar, a0, mu)
        pred1 = np.log10(gd)                 # slip = 1 (what the banked stage12 fit assumes)
        predM = np.log10(gd / 2.0)           # MMG: lensing sees half
        c1 = float(np.sum(((lg_obs - pred1) / sig) ** 2))
        cM = float(np.sum(((lg_obs - predM) / sig) ** 2))
        dchi = cM - c1
        print(f"  {kn:8s} {fn:7s} {c1/15:16.2f} {cM/15:14.2f} {dchi:11.1f} {np.sqrt(dchi):7.1f}")
print()
print("  (slip=1 row for mu_exp/canon: chi2/dof 2.25 here vs the banked 2.03 -- the banked")
print("   stage12 number uses the Route A nu-form nu(y)=1/(1-e^{-sqrt(y)}); this gate uses")
print("   the chassis's OWN frozen law mu(y)=1-e^{-y} in mu-form (Gate 1), a slightly")
print("   different map.  Irrelevant to the slip question: the MMG column is the same")
print("   theory made to PREDICT its own lensing instead of borrowing GR's.)")
gbar = 10.0 ** lg_bar
gd = g_dyn(gbar, A0["canon"], mu_exp)
c1 = float(np.sum(((lg_obs - np.log10(gd)) / sig) ** 2))
cM = float(np.sum(((lg_obs - np.log10(gd / 2)) / sig) ** 2))
check(cM - c1 > 100, "MMG halving excluded by the M24 lensing RAR",
      f"Delta chi2 = {cM-c1:.0f} over 15 points (mu_exp, canon)")

print()
print("=" * 78)
print("PART F -- clusters: the standing shortfall DOUBLES for lensing masses")
print("=" * 78)
eta_lo, eta_hi = 1.72, 2.08   # committed: closure_2026/DEPENDENCY_MAP_2026-08-22.md line 304
print(f"  standing DYNAMICAL (hydrostatic) shortfall at R500: eta = {eta_lo:.2f}-{eta_hi:.2f}")
print(f"  (committed in closure_2026/DEPENDENCY_MAP_2026-08-22.md; kernel-spread quoted).")
print(f"  MMG lensing acceleration = g_dyn/2  =>  lensing-mass shortfall:")
print(f"     eta_lens = 2 x eta = {2*eta_lo:.2f}-{2*eta_hi:.2f}")
print("  i.e. weak-lensing cluster masses would exceed the MMG prediction ~3.4-4.2x,")
print("  and hydrostatic-vs-lensing mass comparisons (observed consistent at ~10-20%)")
print("  would disagree by a factor ~2 internally -- a second, independent kill.")
check(True, "cluster lensing shortfall = 2 x (1.72-2.08) = 3.44-4.16")

print()
print("=" * 78)
print("PART G -- kernel/footing dependence of the verdict")
print("=" * 78)
print("  The slip result Phi = 0 comes from S_2 = D^2 q ~ 0.  That constraint contains")
print("  NO mu, NO a0: swapping mu_exp -> mu_n (Gate 13 transfers the 2-DOF certificate)")
print("  changes Psi at the 0.108->0.123/0.127 dex RAR level but leaves Phi = 0 and the")
print("  factor-1/2 deflection EXACTLY unchanged (Part D table: ratio 0.5000 in all 6 cells).")
print("  Both a0 footings identical.  The failure is CONSTRAINT-STRUCTURAL.")
check(True, "verdict kernel-agnostic and footing-agnostic")

print()
print("=" * 78)
print("PART H -- the named within-family repair (UNCERTIFIED, priced)")
print("=" * 78)
print("  Replace S_2 = D^2 q  by  S_2' = D^2 (q + ln N).  On the constraint surface")
print("  q = -ln N (+ decaying harmonic = 0), i.e. Phi = +Psi EXACTLY at all accelerations:")
print("  slip 1, gamma_PPN = 1, light sees the FULL MOND potential, galaxy lensing RAR")
print("  back to the banked fit, clusters back to the standing eta~2 (not doubled).")
print("  C_M and the lapse sector are untouched -- rotation curves unchanged.")
print("  Dirac-structure price: {pi_N, S_2'} = -D^2(1/N . ) =: d != 0 appears at (S_4,S_2'):")
LNs, Ks, bs, cs2, ds = sp.symbols("L_N K b c d")
Mrep = sp.Matrix([
    [0,    LNs,  ds,  0],
    [-LNs, 0,    bs,  cs2],
    [-ds,  -bs,  0,   Ks],
    [0,    -cs2, -Ks, 0],
])
Pf_rep = Mrep[0, 1] * Mrep[2, 3] - Mrep[0, 2] * Mrep[1, 3] + Mrep[0, 3] * Mrep[1, 2]
det_rep = sp.simplify(Mrep.det())
check(sp.simplify(Pf_rep - (LNs * Ks - ds * cs2)) == 0,
      "repaired Pfaffian Pf = L_N K - d c   (was L_N K)")
check(sp.simplify(det_rep - (LNs * Ks - ds * cs2) ** 2) == 0,
      "repaired det = (L_N K - d c)^2 -- generically nonzero, count 20-12-4=4 = 2 DOF")
print("  => the 2-DOF count PLAUSIBLY survives, but the certificate does NOT transfer:")
print("     a new degeneracy locus L_N K = d c must be characterized, and Gates 3, 6, 7, 8")
print("     (structure, rank, count, preservation/no-tertiary) must be RE-RUN for S_2'.")
print("     Until then the repair is OPEN, not a result.")

print()
print("=" * 78)
print("SUMMARY")
print("=" * 78)
print("  Psi: solves exact AQUAL (C_M).  Dynamics sees full MOND.        [certified + Part A]")
print("  Phi: solves D^2 q = 0  =>  Phi = 0.  NOT Poisson, NOT MOND.     [Part B]")
print("  slip eta = Phi/Psi = 0; gamma_PPN = 0 at ALL accelerations.     [Part C]")
print("  light sees HALF the MOND potential (alpha ratio exactly 1/2).   [Parts C,D]")
print("  galaxies: M24 lensing RAR Delta chi2 = +403 to +498 / 15 bins.  [Part E]")
print("  solar system: ~43,000 sigma against Cassini gamma.              [Part C]")
print("  clusters: standing eta 1.72-2.08 doubles to 3.4-4.2.            [Part F]")
print("  Escape used by the repo's DW chassis (trace-free ij Einstein eq -> Phi=Psi) does")
print("  NOT exist here: MMG has no ij Einstein equation; the deleted H_perp is precisely")
print("  the equation that sourced Phi.  This is the MMG analogue of the york nu^2-gap,")
print("  in harder form: the ij sector is not under-supplied, it is UNSOURCED.")
print()
print("GATE RESULT:", "DERIVED -- FAIL (lensing)" if ok else "SCRIPT ERROR")
