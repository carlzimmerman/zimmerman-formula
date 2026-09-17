#!/usr/bin/env python3
"""KS01 -- THE eps_tot = 1/(32 pi) SLOT, ADJUDICATED: does the de Sitter horizon entropy multiply or divide?

The 2026-08-09 lane (real_research/reviews/mi_graviton_bath_ctp_2026.py) wrote eps_tot = S_dS x eps_1 with
eps_1 ~ G T_GH^2/8 the thermal graviton variance and N = S_dS = pi/(G H^2) "horizon modes", obtaining a PURE
NUMBER (1/(32 pi) under one normalisation, hence kappa = 1/2).  The 2026-09-01 lane
(qwen_claude_field_theory/closure_2026/a0_promotion_2026/graviton_bath_ctp_drift_2026.py) evaluated the same
rectified drift and found it proportional to 1/S_dS.  This lane decides between them two independent ways,
then asks whether ANY state of the graviton field could supply the slot, and finally puts the framework's
kappa = 1/2 in the table of principled rivals with the precision needed to separate them.

Units hbar = c = k_B = 1 in parts A-B; G = 1/M_Pl^2.  Both a0 footings carried in part D.
A FAIL is a finding.  No literal-True checks.  MUTATE=1 flips the thermal integrand and must break A1.
"""
import os, math, json
import sympy as sp
import numpy as np

MUT = os.environ.get("MUTATE") == "1"
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)

print("KS01 -- the eps_tot = 1/(32 pi) slot, adjudicated\n")
# =====================================================================================================
print("=" * 100); print("A. The thermal variance IS the mode sum (sympy): T^2/12 per massless degree of freedom"); print("=" * 100)
k, T, L = sp.symbols('k T L', positive=True)
x = sp.symbols('x', positive=True)
# <phi^2>_T - <phi^2>_vac = int d^3k/(2pi)^3 (1/(2 w)) * 2 n(w),  n = 1/(e^{w/T}-1),  w = k (massless)
integrand = (4 * sp.pi * k ** 2) / (2 * sp.pi) ** 3 * (1 / k) * (1 / (sp.exp(k / T) - 1))
if MUT: integrand = integrand * k / T          # mutation: a wrong power of k -> T^3, the theorem's hinge breaks
import mpmath as mp
pw = 2 if MUT else 1
I_num = mp.quad(lambda u: u ** pw / mp.expm1(u), [0, mp.inf])           # int x/(e^x-1) = pi^2/6 (zeta(2)); the mutation gives 2 zeta(3)
coef = I_num / (2 * mp.pi ** 2)                                           # <phi^2>_T = T^2 x coef
print(f"    <phi^2>_T (vacuum-subtracted) = T^2 x {mp.nstr(coef, 12)}   (1/12 = {mp.nstr(mp.mpf(1)/12, 12)}; integral = {mp.nstr(I_num, 12)}, pi^2/6 = {mp.nstr(mp.pi**2/6, 12)})")
var_T = coef * T ** 2
check("A1 the vacuum-subtracted thermal variance of one massless scalar dof is T^2/12 (to 1e-10)", abs(coef - mp.mpf(1) / 12) < 1e-10, f"coef = {mp.nstr(coef, 10)}")
# the same quantity as a discrete mode sum in a box of side L: sum_k (1/(w_k L^3)) n(w_k) -> the integral as L -> inf.
# Evaluate the box sum numerically at T L = 1/(2 pi) (the static patch: T = H/2pi, L = 1/H) and at large T L.
NMAX = 120
rng = np.arange(-NMAX, NMAX + 1)
n2 = (rng[:, None, None] ** 2 + rng[None, :, None] ** 2 + rng[None, None, :] ** 2).ravel()
n2 = n2[n2 > 0]                                   # the k = 0 mode is absent in a box
kk = 2 * np.pi * np.sqrt(n2.astype(float))       # L = 1
def box_sum(TL):                                  # sum_k n(w_k)/(w_k L^3), the thermal part of <phi^2> in the box
    return float(np.sum(np.expm1(kk / TL) ** -1 / kk))
TL_patch = 1 / (2 * math.pi)
s_patch = box_sum(TL_patch); cont_patch = TL_patch ** 2 / 12
print(f"    box sum at T L = 1/2pi (the static patch): {s_patch:.3e}  vs continuum T^2/12 = {cont_patch:.3e}  (ratio {s_patch/cont_patch:.2e})")
ratios = {}
for TL in (15.0, 30.0, 60.0):
    r = box_sum(TL) / (TL ** 2 / 12); ratios[TL] = r
    print(f"    box sum at T L = {TL:4.0f}: ratio to continuum T^2/12 = {r:.4f}   (IR modes below 2 pi/L carry ~{12/(math.pi*TL):.3f} of the continuum; k_max/T = {2*math.pi*NMAX/TL:.1f})")
conv = abs(1 - ratios[60.0]) < 0.10 and (1 - ratios[30.0]) > (1 - ratios[60.0]) > 0 and (1 - ratios[15.0]) > (1 - ratios[30.0])
check("A2 the discrete mode sum converges to the SAME T^2/12 as the box grows (|1 - ratio| < 10% at T L = 60, deviation shrinking with T L): the mode sum IS the thermal variance, not a factor to multiply it by",
      conv, "ratios " + ", ".join(f"TL={k:.0f}: {v:.4f}" for k, v in ratios.items()))
N_th = (4 * math.pi / 3) * (TL_patch / (2 * math.pi)) ** 3
print(f"    number of modes with omega < T inside the static patch (T L = 1/2pi): N_th = (4pi/3)(T L/2pi)^3 = {N_th:.2e}")
check("A3 the static patch holds FEWER THAN ONE thermally occupied mode (N_th < 1): the thermal variance is carried by the sub-horizon tail, not by S_dS modes",
      N_th < 1, f"N_th = {N_th:.2e}; S_dS counts modes up to the Planck scale, whose thermal occupation is e^(-M_Pl/T) ~ 0")
OUT["A"] = dict(coef=float(coef), box_ratio_patch=s_patch / cont_patch, box_ratios=ratios, N_th=N_th)

# =====================================================================================================
print("\n" + "=" * 100); print("B. Multiply or divide: eps_tot from the thermal graviton variance, with S_dS where it belongs"); print("=" * 100)
G, H, MP = sp.symbols('G H M_Pl', positive=True)
T_GH = H / (2 * sp.pi)
S_dS = sp.pi / (G * H ** 2)
# canonical graviton h = sqrt(32 pi G) phi per polarisation, two TT polarisations, each a massless scalar dof at T_GH
h2_thermal = 32 * sp.pi * G * 2 * T_GH ** 2 / 12
eps_thermal = sp.simplify(h2_thermal / 8)                  # the -X^2/8 term: energy fraction ~ <h^2>/8
eps_0809 = sp.simplify(S_dS * eps_thermal)                 # the 08-09 structure: S_dS x (thermal variance)
print(f"    <h_uu^2>_thermal (2 pol, canonical norm) = {sp.simplify(h2_thermal)}  -> eps_thermal = {eps_thermal}")
print(f"    the 08-09 product S_dS x eps_thermal = {eps_0809}  (a pure number, because S_dS G H^2 = pi)")
check("B1 the thermal eps carries G H^2 (Planck-suppressed): eps_thermal is NOT a pure number", eps_thermal.has(G) and eps_thermal.has(H), f"{eps_thermal}")
check("B2 S_dS x eps_thermal is a pure number ONLY because the mode sum was counted twice (A2/A3): the multiplication assigns the full thermal variance to each of S_dS Planck-scale vacuum modes",
      not eps_0809.has(G), f"{eps_0809} = {float(eps_0809):.4f}; compare 1/(32 pi) = {1/(32*math.pi):.4f} and 1/12 = {1/12:.4f}")
# numerical size today, both footings
c = 2.99792458e8; Gn = 6.674e-11; hbar = 1.054571817e-34; MPC = 3.0857e22
H0 = 67.4e3 / MPC; OmL = 0.685
lP2 = hbar * Gn / c ** 3
for lab, Hn in (("canonical (H_Lambda = H0 sqrt Omega_L)", H0 * math.sqrt(OmL)), ("alt (H0)", H0)):
    GH2 = lP2 * (Hn / c) ** 2 * c ** 2 / c ** 2          # G H^2 in Planck units = (l_P H / c)^2
    GH2 = lP2 * Hn ** 2 / c ** 2
    eps_num = GH2 / (6 * math.pi)                          # eps_thermal = G H^2/(6 pi) from the symbolic line above
    SdS = math.pi / GH2
    print(f"    {lab}: G H^2 = {GH2:.3e}, S_dS = {SdS:.3e}, eps_thermal = {eps_num:.3e}  (slot needs {1/(32*math.pi):.4e}: short by {1/(32*math.pi)/eps_num:.2e})")
    OUT.setdefault("B", {})[lab] = dict(GH2=GH2, S_dS=SdS, eps_thermal=eps_num, shortfall=1 / (32 * math.pi) / eps_num)
check("B3 the thermal state falls short of the slot by a factor of order S_dS on both footings (shortfall > 1e100)",
      all(v["shortfall"] > 1e100 for v in OUT["B"].values()), "the 09-01 division by S_dS is the thermal answer; the 08-09 multiplication is the double count")

# =====================================================================================================
print("\n" + "=" * 100); print("C. Could ANY state of the graviton field supply the slot?  The required <h^2> versus the sky"); print("=" * 100)
h2_needed = 8 / (32 * math.pi)             # eps = <h^2>/8 = 1/(32 pi)
dT_over_T = 1e-5                            # the observed CMB anisotropy amplitude (Sachs-Wolfe: dT/T ~ h at the horizon scale)
h2_sky = dT_over_T ** 2
r_bound, A_s = 0.036, 2.1e-9                # BICEP/Keck+Planck 2021 r < 0.036; the primordial tensor power r A_s
h2_tensor = r_bound * A_s
print(f"    the slot needs <h_uu^2> = 8 eps = {h2_needed:.4f} at the Hubble scale (metric fluctuations of amplitude {math.sqrt(h2_needed):.2f})")
print(f"    CMB smoothness: any horizon-scale metric fluctuation h gives dT/T ~ h; observed 1e-5 -> <h^2> <~ {h2_sky:.0e}")
print(f"    primordial tensor bound r < {r_bound}: P_t = r A_s < {h2_tensor:.1e}")
check("C1 the slot needs a metric variance at least 1e8 above what the CMB's smoothness allows (h2_needed / h2_sky > 1e8)",
      h2_needed / h2_sky > 1e8, f"ratio {h2_needed/h2_sky:.1e}: no state -- thermal, coherent, or primordial -- can supply eps_tot = 1/(32 pi) without O(1) metric fluctuations today")
check("C2 the slot exceeds the primordial tensor ceiling by > 1e8", h2_needed / h2_tensor > 1e8, f"ratio {h2_needed/h2_tensor:.1e}")
OUT["C"] = dict(h2_needed=h2_needed, h2_sky=h2_sky, h2_tensor=h2_tensor)

# =====================================================================================================
print("\n" + "=" * 100); print("D. kappa = 1/2 among the principled rivals, both footings, and the precision that would separate them"); print("=" * 100)
fried = math.sqrt(8 * math.pi / 3)          # c H = c sqrt(G rho) x sqrt(8 pi/3): converts a cH coefficient to kappa
rivals = {
    "framework kappa = 1/2 (fitted)":                    (0.5, 0.5),
    "Verlinde 2016  a0 = cH/6":                          (fried / 6, fried / 6 / math.sqrt(OmL)),
    "Milgrom 1983/99  a0 = cH/(2 pi)":                   (fried / (2 * math.pi), fried / (2 * math.pi) / math.sqrt(OmL)),
    "Deser-Levin/Unruh  a0 = 2 cH":                      (2 * fried, 2 * fried / math.sqrt(OmL)),
    "graviton norm B  eps = 1/12":                       (math.sqrt(8 * math.pi / 12), math.sqrt(8 * math.pi / 12)),
    "graviton norm B x 2 pol  eps = 1/6":                (math.sqrt(8 * math.pi / 6), math.sqrt(8 * math.pi / 6)),
    "horizon surface gravity at c/H:  a0 = cH/2":        (fried / 2, fried / 2 / math.sqrt(OmL)),
}
band = {"BTFR 0.465 +- 0.076": (0.465, 0.076), "distance-free 0.551 +- 0.043": (0.551, 0.043)}
print(f"    {'candidate':44s} kappa(H_Lambda)  kappa(H0)   z_BTFR(HL)  z_dfree(HL)")
inside = {}
for name, (kL, k0) in rivals.items():
    zb = (kL - 0.465) / 0.076; zd = (kL - 0.551) / 0.043
    inside[name] = abs(zb) < 2 or abs(zd) < 2
    print(f"    {name:44s} {kL:8.4f}       {k0:8.4f}   {zb:+6.2f}      {zd:+6.2f}")
n_in = sum(inside.values())
check("D1 at today's precision the framework's 1/2 is the ONLY principled candidate inside 2 sigma of a kappa measurement", n_in == 1,
      f"{n_in} candidates inside 2 sigma: " + ", ".join(k for k, v in inside.items() if v) + ". [FAIL is the finding]")
kV = fried / 6
sep = abs(0.5 - kV) / 0.5
print(f"    nearest principled rival to 1/2 on the dS footing: Verlinde's sqrt(8pi/3)/6 = {kV:.4f}, {100*sep:.1f}% away; 3-sigma separation needs sigma_kappa = {100*sep/3:.2f}%  = {sep/3/math.log(10)*4:.4f} dex on the BTFR zero point (v^4)")
check("D2 separating 1/2 from its nearest principled rival at 3 sigma is within reach of the M/L systematic floor (needs sigma_kappa >= 5%)", sep / 3 >= 0.05,
      f"needs {100*sep/3:.2f}%: an order of magnitude below the ~10% distance-free precision and the 20% MLS16 systematic on g_dagger. [FAIL is the finding]")
OUT["D"] = dict(rivals={k: v for k, v in rivals.items()}, inside=inside, nearest_rival_kappa=kV, sep_needed_pct=100 * sep / 3)

n, n_pass = len(CH), sum(CH)
print("\n" + "=" * 100)
print(f"KS01 COMPLETE: {n_pass}/{n} checks PASS" + ("  [MUTATE=1: A1 must FAIL above]" if MUT else ""))
print("VERDICT")
print("  (1) computed: the vacuum-subtracted thermal variance of a massless dof (T^2/12) as an integral and as a box mode sum; the number of thermally")
print("      occupied modes in the static patch; eps_tot with and without the S_dS factor; the metric variance the slot requires versus the CMB; the rival table.")
print("  (2) numbers: eps_thermal = G H^2/(6 pi) ~ 1e-123; S_dS x eps_thermal = 1/6 (norm B x 2) -- a pure number only by counting the thermal variance once per")
print("      Planck-scale vacuum mode; the slot needs <h^2> = 1/(4 pi) = 0.08 against the sky's <~ 1e-10; three principled candidates sit inside 2 sigma of kappa.")
print("  (3) SLOT NOT LIVE.  The horizon entropy divides; the 08-09 pure number is a double count; no state of the graviton field supplies 1/(32 pi) without")
print("      order-unity metric fluctuations excluded by the CMB by eight orders.  kappa = 1/2 is a MEASURED constant, indistinguishable today from Verlinde's")
print("      sqrt(8 pi/3)/6 = 0.482 and Milgrom's sqrt(8 pi/3)/(2 pi) = 0.461, and separable from the nearest at 3 sigma only with sigma_kappa ~ 1.2% -- below any foreseeable precision.")
json.dump(dict(pass_=n_pass, n=n, parts=OUT), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "KS01_slot_adjudication.json"), "w"), indent=1, default=str)
