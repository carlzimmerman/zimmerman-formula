"""
agentXX ROUTE 1 — dS-RADIATIVE / CURVATURE-INDUCED c_chi(H).

QUESTION: does the dS background (R = 12 H^2, foliation extrinsic curvature K ~ 3H)
generate a correction delta(c_chi^2) ~ (H/M)^2 that LOCKS the khronon sound speed
c_chi to a function of H, or is the correction negligible ((H/M_Pl)^2 ~ 1e-120)
leaving c_chi a free Lagrangian coupling that must be TUNED to land the edge
coincidence R = G_sat?

Banked from agentU_khronon_m22.md (1711.08845 / 1802.04303 conventions):
  - khronometric action S_u = -(M_ae^2/2) int sqrt(-g) [ a (u.del u)^2 + b (del u)^2 ... ]
  - canonical kinetic term: alpha,beta,gamma are CONSTANT Lagrangian couplings
  - spin-0 (khronon) sound speed: c_chi^2 = f(c_1,c_2,c_3) / (ratio of couplings)
  - bare c_chi^2 in [1.000, 1.033] (Cherenkov edge), FREE
  - c_T^2 = 1/(1-beta), |beta| <~ 1e-15

We compute the LEADING dS-curvature correction to the spin-0 dispersion and ask
whether it ties c_chi to H. Method: write the khronon quadratic action in a dS
background, extract the dispersion w^2 = c_chi^2 k^2 + (curvature terms), and
identify the scale that controls the correction.
"""

import sympy as sp
import mpmath as mp

mp.mp.dps = 40

print("="*78)
print("agentXX ROUTE 1: dS-RADIATIVE c_chi(H) LOCK TEST")
print("="*78)

# ---------------------------------------------------------------------------
# SECTION 1 — the khronon spin-0 sound speed in FLAT space (bare, banked form)
# ---------------------------------------------------------------------------
print("\n[1] BARE spin-0 (khronon) sound speed -- Einstein-aether / khronometric")
print("    convention 1711.08845 / 1802.04303 (c_1..c_4).")

c1, c2, c3, c4 = sp.symbols('c1 c2 c3 c4', real=True)

# Einstein-aether spin-0 (scalar) squared speed (Jacobson, standard result):
#   c_0^2 = [ c_123 (2 - c_14) ] / [ c_14 (1 - c_13)(2 + c_13 + 3 c_2) ]
# with c_ij = c_i + c_j, c_123 = c_1 + c_2 + c_3, c_14 = c_1 + c_4.
c13 = c1 + c3
c14 = c1 + c4
c123 = c1 + c2 + c3
c_scalar2 = (c123 * (2 - c14)) / (c14 * (1 - c13) * (2 + c13 + 3*c2))
print("    c_chi^2 (spin-0) =", c_scalar2)
print("    -> a RATIO of Lagrangian couplings c_i. No H, no curvature scale in it.")
print("    -> bare c_chi^2 is dimensionless, set ENTIRELY by the c_i. FREE coupling.")

# In the khronometric (hypersurface-orthogonal) limit the relevant couplings reduce;
# the structural point survives: c_chi^2 = (couplings)/(couplings), scale-free.

# ---------------------------------------------------------------------------
# SECTION 2 — the khronon quadratic action in a dS BACKGROUND
# ---------------------------------------------------------------------------
print("\n[2] dS background. Flat slicing: ds^2 = -dt^2 + a(t)^2 dx^2, a=exp(H t).")
print("    The khronon T=t in the background (cosmic-aligned foliation);")
print("    fluctuation: T = t + chi(t,x)/  (the spin-0 Goldstone).")

t, x, H, k, w = sp.symbols('t x H k omega', real=True, positive=True)
M = sp.symbols('M', positive=True)      # khronon Lorentz-breaking / aether mass scale (M_ae)
Mpl = sp.symbols('M_Pl', positive=True)
cchi2 = sp.symbols('c_chi2', positive=True)   # bare spin-0 speed squared

# Background scalars of the dS foliation (u = unit normal to T=const leaves; in the
# aligned background u^mu = (1,0,0,0), congruence = comoving observers):
#   expansion theta = del.u = 3H      (K = theta/3 -> extrinsic curvature trace)
#   acceleration a^mu = u.del u = 0    (geodesic comoving congruence)
#   shear = 0, vorticity = 0 (FRW)
#   Ricci scalar R = 12 H^2
theta_bg = 3*H
R_bg = 12*H**2
print("    background: del.u = 3H ;  u.del u = 0 ;  R = 12 H^2 .")

# The khronon Goldstone chi has the quadratic Lagrangian (schematically, EFT of
# inflation / khronometric form):
#   L2 ~ (M_ae^2/2) [ chidot^2 - c_chi^2 (del chi)^2/a^2 - m_eff^2 chi^2 ]
# The dS background can generate:
#   (i) a friction term 3H chidot (Hubble friction) -> shifts the FREQUENCY, not c_chi
#   (ii) an effective MASS m_eff^2 ~ # H^2 (curvature coupling, tadpole of theta=3H)
#   (iii) a possible SHIFT of the gradient coefficient: c_chi^2 -> c_chi^2 + #(H^2/k^2..)
# The dispersion from this L2:
#   w^2 + 3 i H w = c_chi^2 (k/a)^2 + m_eff^2
# The physical question: does the GRADIENT coefficient (the thing that IS c_chi^2)
# get an H-correction that survives at large k (the relevant sub-horizon, fold band)?

print("\n[3] dS dispersion for the khronon Goldstone chi (sub-horizon physical k):")
print("    w^2 + 3 i H w = c_chi^2 k_phys^2 + m_eff^2,   m_eff^2 = xi * H^2")
xi = sp.symbols('xi', real=True)   # O(1) curvature-coupling coefficient
kphys = sp.symbols('k_phys', positive=True)
disp = sp.Eq(w**2 + 3*sp.I*H*w, cchi2*kphys**2 + xi*H**2)
sp.pprint(disp)

# Effective sound speed read off the dispersion at physical wavenumber kphys:
#   c_eff^2(k) = (real part of w^2) / kphys^2  -> c_chi^2 + xi H^2/kphys^2
c_eff2 = cchi2 + xi*H**2/kphys**2
print("    => c_eff^2(k) = c_chi^2 + xi * (H/k_phys)^2 .")
print("    The H-dependence rides on (H/k_phys)^2 : it is a LONG-WAVELENGTH (IR)")
print("    correction that VANISHES as k_phys -> infinity (sub-horizon).")

# ---------------------------------------------------------------------------
# SECTION 3 — SIZE the correction at the RELEVANT (fold-band) scale
# ---------------------------------------------------------------------------
print("\n[4] SIZE the correction at the fold band. The edge coincidence / fold lives")
print("    at k* ~ (c_chi/sqrt(a0)) H  (banked from agentRR). So at the relevant k:")

# Numerical: present-day H0, the MOND scale a0, and the khronon LV scale M.
H0 = mp.mpf('2.2e-18')          # s^-1 (H0 ~ 67 km/s/Mpc)
c_light = mp.mpf('2.998e8')     # m/s
a0 = mp.mpf('1.2e-10')          # m/s^2  (MOND)
Mpl_val = mp.mpf('2.435e18')    # GeV (reduced Planck mass)
# Lorentz-violating / khronon scale: from agentU strong-coupling floor M_SC >~ meV,
# and the aether scale M_ae can be anywhere from ~meV up to ~M_Pl. We bracket it.
print("    inputs: H0 =", H0, "s^-1 ; a0 =", a0, "m/s^2 ; c =", c_light, "m/s")

# (H/k)^2 at the fold band: k_phys = k* ~ (c_chi/sqrt(a0)) * H  (with c_chi ~ c).
# Careful with units: a0 has units m/s^2; c_chi (speed) ~ c. The banked k* combination
# k* ~ (c_chi/sqrt(a0)) H -- check dimension: [c/sqrt(a0)] = (m/s)/sqrt(m/s^2)
#   = (m/s)/(sqrt(m)/s) = sqrt(m). Times H (1/s) -> sqrt(m)/s. That is NOT 1/length.
# The banked k* is a comoving/dimensionful combination from agentRR's units; what we
# need here is the RATIO (H/k_phys)^2 at the fold band. agentRR / agent commits bank
#   k0/k_H ~ c_chi^2/sqrt(a0)  and  k0/k_H ~ 1.1e5  (the fold band sits ~1e5 ABOVE k_H).
kfold_over_kH = mp.mpf('1.1e5')   # banked: fold band is ~1e5 above the horizon scale k_H
# k_H is the horizon-scale wavenumber ~ H/c (physical). So k_phys at fold ~ kfold_over_kH * (H/c).
kH_phys = H0 / c_light           # 1/m, horizon physical wavenumber
kfold_phys = kfold_over_kH * kH_phys
print("    k_H (phys) = H0/c =", kH_phys, "1/m")
print("    k_fold (phys) ~ 1.1e5 * k_H =", kfold_phys, "1/m")

# (H/k_phys) with H in 1/s converted to a wavenumber H/c:
H_as_k = H0 / c_light
ratio_at_fold = (H_as_k / kfold_phys)**2
print("    (H/k_phys)^2 at fold band =", ratio_at_fold)
print("    => the IR curvature correction xi*(H/k)^2 is ~", ratio_at_fold,
      "(times xi~O(1))")
print("    at the FOLD band. NEGLIGIBLE: c_eff^2 = c_chi^2 (1 +", ratio_at_fold, ").")

# ---------------------------------------------------------------------------
# SECTION 4 — the UV / radiative correction: delta(c_chi^2) ~ (H/M)^2
# ---------------------------------------------------------------------------
print("\n[5] UV-side: could a curvature COUPLING shift the GRADIENT coefficient,")
print("    c_chi^2 -> c_chi^2 + #(H/M)^2 with M the LV/aether scale (k-independent)?")
print("    Such an operator is (R/M^2)(del chi)^2 -> delta c_chi^2 = # R/M^2 = #*12 H^2/M^2.")

# Bracket M from meV (strong-coupling floor) to M_Pl.
GeV = mp.mpf('1.0')
eV = mp.mpf('1e-9')      # GeV
meV = mp.mpf('1e-12')    # GeV
# Convert H0 to GeV: hbar*H0. hbar = 6.582e-25 GeV*s.
hbar = mp.mpf('6.582e-25')   # GeV s
H0_GeV = hbar * H0
print("    H0 in energy units = hbar*H0 =", H0_GeV, "GeV")

for label, Mval in [("M = M_Pl (2.4e18 GeV)", Mpl_val),
                    ("M = 1e16 GeV (GUT)", mp.mpf('1e16')),
                    ("M = 1 TeV", mp.mpf('1e3')),
                    ("M = 1 GeV", mp.mpf('1.0')),
                    ("M = 1 eV", eV),
                    ("M = 1 meV (SC floor)", meV)]:
    delta = (H0_GeV / Mval)**2
    print(f"    {label:28s}: (H/M)^2 = {mp.nstr(delta,4)}")

print("\n    Even at the LOWEST physically allowed LV scale (M ~ meV, the strong-")
print("    coupling floor M_SC >~ meV from agentU/1711.08845 Eq.15), (H/M)^2 ~",
      mp.nstr((H0_GeV/meV)**2, 4))
print("    => delta(c_chi^2) ~ 12*(H/M)^2 is ASTRONOMICALLY tiny. c_chi UNMOVED.")

# ---------------------------------------------------------------------------
# SECTION 5 — what scale would be NEEDED for a real lock?
# ---------------------------------------------------------------------------
print("\n[6] INVERT: what M would make delta(c_chi^2) ~ O(c_chi^2) ~ O(1)?")
print("    Need 12 (H/M)^2 ~ 1  =>  M ~ sqrt(12) H ~ 3.5 H.")
M_needed = mp.sqrt(12) * H0_GeV
print("    M_needed ~", mp.nstr(M_needed,4), "GeV =", mp.nstr(M_needed/H0_GeV,4),
      "* H0 (in energy).")
print("    i.e. the LV scale would have to be ~the Hubble scale itself (M ~ H).")
print("    But the khronon LV scale is BOUNDED BELOW at M_SC >~ meV =", meV, "GeV,")
print("    which is ~", mp.nstr(meV/H0_GeV,3), "ORDERS above H0. So M >> H ALWAYS.")
print("    A lock requires M ~ H; the EFT validity / strong-coupling floor FORBIDS it.")

print("\n" + "="*78)
print("PRELIMINARY VERDICT (section-level):")
print("  - c_chi^2 = ratio of Lagrangian couplings c_i: dimensionless, FREE.")
print("  - dS IR correction: rides (H/k)^2, ~1e-10 at the fold band -> negligible.")
print("  - dS UV/radiative correction delta c_chi^2 ~ (H/M)^2: ~1e-60 (meV) to")
print("    1e-122 (M_Pl) -> negligible by 60-122 orders.")
print("  - A genuine lock needs M ~ H, forbidden by the strong-coupling floor M>>meV>>H.")
print("  => c_chi is FREE-MUST-TUNE. dS curvature does NOT lock it to H.")
print("="*78)
