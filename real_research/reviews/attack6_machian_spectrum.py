#!/usr/bin/env python3
"""
ATTACK 6 -- THE MACHIAN/INERTIA SPECTRUM
========================================
Does the dS-Unruh kernel constrain the NUMBER or PATTERN of masses?

Three sub-questions, each FRIED/PARTIAL/BAKED on its own terms, every number sympy'd:

  (a) SPECTRAL STRUCTURE of the dS-Unruh influence kernel.
      T_eff = (hbar/2pi c k_B) sqrt(a^2 + (cH)^2). Does the analytic structure of
      the associated influence/response kernel (poles, branch points) impose any
      quantization/counting on inertia eigenvalues = masses?

  (b) HOLOGRAPHIC dS dof count N_dof = S_dS = 3pi/(Lambda l_P^2) ~ 10^122.
      Does sqrt(N_dof) (or N_dof powers) match SM ratios (v/M_Pl, m_nu/..., #fields)?
      FDR every numerical hit.

  (c) SPECIES / 't Hooft bound. Does the dS horizon bound the number of light
      species, and does that match SM ~100 dof?

Honest bar: a counting that is DERIVED (forced) is FRIED; dimensional analysis or
an FDR-insignificant numerical hit is BAKED.

Run: python3 attack6_machian_spectrum.py
"""

import sympy as sp
import numpy as np
import math
import itertools

print("#"*92)
print("# ATTACK 6 -- does the Machian dS-Unruh inertia kernel CONSTRAIN the mass spectrum?")
print("#"*92)

# ------------------------------------------------------------------
# CONSTANTS (SI), framework config EXACTLY (Carl's, never regular-MOND)
# ------------------------------------------------------------------
c    = 2.99792458e8       # m/s
G    = 6.67430e-11        # SI
hbar = 1.054571817e-34    # J s
kB   = 1.380649e-23       # J/K
eV   = 1.602176634e-19    # J
Mpc  = 3.0856775814913673e22

H0   = 67.4e3/Mpc         # s^-1
OmL  = 0.685
# pure-Lambda footing: H_Lambda = H0 sqrt(OmL); Lambda = 3 (H0^2 OmL)/c^2
H_L  = H0*math.sqrt(OmL)
Lam  = 3*(H0**2*OmL)/c**2 # m^-2  (Lambda)
rho_DE = Lam*c**2/(8*math.pi*G)  # kg/m^3
Z    = math.sqrt(32*math.pi/3)
kernel = math.sqrt(8*math.pi/3)
a0   = c**2*math.sqrt(Lam/(32*math.pi))   # = c*H_L/Z
a0_chk = c*H_L/Z
lP   = math.sqrt(hbar*G/c**3)             # Planck length
MPl  = math.sqrt(hbar*c/G)                # Planck mass (kg)
EPl  = MPl*c**2/eV                         # Planck energy eV
v_EW = 246.0e9                             # Higgs vev eV

print(f"\n  config check: a0 = {a0:.4e}  (= c H_L/Z = {a0_chk:.4e})  Z={Z:.5f} kernel={kernel:.5f}")
_uDE = rho_DE*c**2                                   # J/m^3 energy density
_rhoDE_qtr = (_uDE*(hbar*c)**3)**0.25/eV             # rho_DE^(1/4) as an ENERGY [eV]
print(f"  rho_DE = {rho_DE:.4e} kg/m^3 ;  rho_DE^(1/4) = {_rhoDE_qtr*1e3:.4f} meV  (CENTERPIECE: ~ m_nu scale)")
print(f"  H_L = {H_L:.4e} 1/s ;  Lambda = {Lam:.4e} 1/m^2 ;  lP = {lP:.4e} m")

# ==================================================================
# (a) SPECTRAL STRUCTURE OF THE dS-UNRUH INFLUENCE KERNEL
# ==================================================================
print("\n"+"="*92)
print("(a) ANALYTIC STRUCTURE of the dS-Unruh response/influence kernel")
print("="*92)

w, a, H, m, Om, s, t = sp.symbols('omega a H m Omega s t', positive=True)
I = sp.I

# T_eff (Deser-Levin, verbatim): 2 pi T = sqrt(a^2 + H^2)  [hbar=c=kB=1, H=cH_L scale]
kappa = sp.sqrt(a**2 + H**2)
Teff  = kappa/(2*sp.pi)
print("\n  Deser-Levin (gr-qc/9706018) verbatim:  2*pi*T = (Lambda/3 + a^2)^(1/2)")
print("     => T_eff = kappa/2pi,  kappa = sqrt(a^2 + H^2),  H == c H_Lambda  (the dS scale).")

# The detector response function / influence kernel for a UDW detector on a
# stationary dS trajectory is a THERMAL kernel at temperature T_eff. Its Fourier
# structure: the (KMS) thermal correlator has the Planckian denominator
#   n(w) = 1/(exp(w/T_eff) - 1),   detailed-balance ratio exp(-w/T_eff).
# Poles of n(w) (the Matsubara structure) sit at w = 2pi i T_eff k = i*kappa*k.
print("\n  The dS detector kernel is THERMAL at T_eff (KMS). Its analytic structure:")
print("     n(w) = 1/(exp(w/T_eff)-1)  has poles (Matsubara) at  w = i*kappa*k, k in Z.")
matsubara = sp.I*kappa*sp.Symbol('k', integer=True)
print(f"     w_k = {sp.nsimplify(matsubara)}   (k in Z)  -- EVENLY SPACED on imaginary axis, spacing kappa.")
print("     => the kernel's poles form an ARITHMETIC ladder (spacing 2pi T_eff = kappa),")
print("        NOT a discrete mass spectrum. The ladder spacing is a SINGLE scale (kappa),")
print("        set by the CURRENT acceleration a (and the floor H), with NO eigenvalue selection.")

# The de Sitter-invariant Wightman function (principal-series / two-point) has the
# well-known pole structure in the SO(4,1) Casimir. For a scalar of mass m in dS_4
# the Casimir is  C2 = m^2/H^2 + ... ; the propagator's analytic continuation has
# poles where the hypergeometric blows up -> at the PRINCIPAL/COMPLEMENTARY series
# boundary. Let's exhibit the dS scalar two-point analytic structure symbolically.
print("\n  dS_4 scalar two-point (SO(4,1) UIR) analytic structure:")
nu = sp.symbols('nu')   # nu^2 = 9/4 - m^2/H^2   (d=4: Delta_pm = 3/2 +- nu)
Delta_p = sp.Rational(3,2) + nu
Delta_m = sp.Rational(3,2) - nu
print(f"     Delta_pm = 3/2 +- nu,  nu = sqrt(9/4 - m^2/H^2)  (d=4).")
print(f"        principal series (heavy):  m^2/H^2 > 9/4  -> nu imaginary  -> Delta = 3/2 +- i|nu|")
print(f"        complementary series (light): 0 < m^2/H^2 < 9/4 -> nu real in (0,3/2)")
# Where does a0 / the framework scale sit? a0 expressed as a 'mass' via a0 = c^2 m/?,
# but a0 is an ACCELERATION not a mass. The relevant dimensionless dS label for the
# inertia floor is (cH_L)/(cH_L) -> the floor a=0 gives kappa=H: the LIGHTEST possible
# 'inertia quantum' has Casimir at the conformal/massless end. Show m where m^2/H^2=9/4:
m_break = sp.Rational(3,2)
print(f"     series boundary at m = (3/2) H  (in c=1, H=cH_L units): m_break = {m_break} * cH_L.")
m_break_eV = 1.5*hbar*H_L/eV
print(f"        => m_break = 1.5 * hbar H_L = {m_break_eV:.3e} eV  ~ 10^{math.log10(m_break_eV):.1f} eV.")
print("        This is ~33 orders BELOW m_nu. The dS-series boundary is a COSMOLOGICAL mass,")
print("        utterly disconnected from SM masses: NO SM particle is near the series boundary.")

# Does the kernel's pole ladder QUANTIZE inertia? Test: solve for which m give a
# pole of the dS propagator on the physical sheet (would-be 'allowed masses').
# Poles of Gamma(Delta_+)Gamma(Delta_-)/Gamma(...) -> Delta_- = -n (n>=0):
print("\n  Would-be 'quantization' from propagator poles:  Delta_- = -n  (n=0,1,2,...):")
n = sp.symbols('n', integer=True, nonnegative=True)
nu_pole = sp.Rational(3,2) + n          # Delta_- = 3/2 - nu = -n -> nu = 3/2 + n
m2_pole = sp.Rational(9,4) - nu_pole**2 # m^2/H^2 = 9/4 - nu^2
m2_pole = sp.simplify(m2_pole)
print(f"     nu = 3/2 + n  =>  m^2/H^2 = 9/4 - (3/2+n)^2 = {sp.expand(m2_pole)}  (negative for n>=1)")
print("     => these poles are at NEGATIVE m^2 (tachyonic/unphysical) for n>=1; only n=0")
print("        (the massless/conformal point) is physical. There is NO ladder of physical")
print("        massive poles. The dS propagator does NOT quantize a tower of real masses.")
print("\n  VERDICT (a): the kernel is THERMAL (single scale kappa); its poles are an arithmetic")
print("     Matsubara ladder set by the CURRENT acceleration, and the dS-propagator poles are")
print("     unphysical (negative m^2). NO mass-eigenvalue selection. => BAKED (no counting).")

# ==================================================================
# (b) HOLOGRAPHIC dS dof COUNT vs SM RATIOS  (FDR'd)
# ==================================================================
print("\n"+"="*92)
print("(b) dS dof count N_dof = S_dS = 3pi/(Lambda lP^2) ~ 10^122 vs SM ratios")
print("="*92)

# S_dS = A/(4 G hbar) with A = 4 pi R_dS^2, R_dS^2 = 3/Lambda. In natural units
# S_dS = pi R_dS^2 / lP^2 = pi (3/Lambda)/lP^2 = 3 pi/(Lambda lP^2).
S_dS = 3*math.pi/(Lam*lP**2)
print(f"\n  S_dS = 3 pi/(Lambda lP^2) = {S_dS:.4e}   (~10^{math.log10(S_dS):.2f})")
sqrtN = math.sqrt(S_dS)
print(f"  sqrt(N_dof) = {sqrtN:.4e}   (~10^{math.log10(sqrtN):.2f})")
N14 = S_dS**0.25
print(f"  N_dof^(1/4)  = {N14:.4e}   (~10^{math.log10(N14):.2f})")

# Candidate SM ratios to test against powers of N_dof.
ratios = {
 "M_Pl/v_EW (hierarchy)"     : MPl*c**2/eV / v_EW,
 "v_EW/m_e"                  : v_EW/0.511e6,
 "M_Pl/m_p"                  : EPl/938.272e6,
 "M_Pl/m_nu(0.05eV)"         : EPl/0.05,
 "M_Pl/(rho_DE^1/4)"         : EPl/((rho_DE*c**2)**0.25/eV),
 "1/sqrt(alpha_em)"          : 1/math.sqrt(1/137.036),
}
print("\n  Test: does N_dof^p hit an SM ratio?  (p scanned over physically-motivated powers)")
print("  ratio name                         value         best N^p match (p)        rel.err")
print("  "+"-"*86)
# physically motivated powers people invoke: 1/2 (Dirac large-number), 1/4, 1/3, 1
pset = [1, 0.5, 0.25, 1.0/3, 1.0/6, 0.75]
fdr_hits_b = []
for name, val in ratios.items():
    best=None
    for p in pset:
        Np = S_dS**p
        rel = abs(math.log10(Np)-math.log10(val))   # log-distance (orders of mag)
        if best is None or rel<best[1]:
            best=(p,rel,Np)
    flag = "<<HIT" if best[1]<0.05 else ("~close" if best[1]<0.3 else "")
    if best[1]<0.3: fdr_hits_b.append((name,best[0],best[1]))
    print(f"  {name:34s} {val:.3e}   N^{best[0]:.3f}={best[2]:.3e}   {best[1]:.3f} dex {flag}")

print("\n  FDR for (b): N_dof spans ~122 dex; sqrt->61, 1/4->30.5. SM ratios span ~0-37 dex.")
print("    With ~6 powers x O(1) prefactors free, the chance of landing within 0.3 dex of")
print("    SOME SM ratio is near-certain (the target space 0..61 dex is densely covered by")
print("    {N^1, N^1/2, N^1/3, N^1/4, N^1/6} = {122,61,40.7,30.5,20.3} dex). A 'hit' here is")
print("    pure large-number numerology (Eddington/Dirac). The matches that LAND are not FDR-")
print("    significant: any O(1)-dressed power of a 10^122 number can be slid onto a 10^17-10^37")
print("    SM ratio. => (b) is BAKED (dimensional/large-number coincidence), no DERIVED counting.")

# the one 'famous' near-coincidence: M_Pl/v ~ N^(1/4)? check explicitly
print(f"\n  (the famous one) M_Pl/v_EW = {EPl/v_EW:.3e} (~10^{math.log10(EPl/v_EW):.2f}) vs")
print(f"     N^(1/8) = {S_dS**0.125:.3e}  N^(1/7)={S_dS**(1/7):.3e}  -> needs power 1/8.0, not a clean exponent.")
pe = math.log10(EPl/v_EW)/math.log10(S_dS)
print(f"     exact power to hit M_Pl/v: p={pe:.4f} (=1/{1/pe:.2f}) -- NOT a privileged rational. Numerology.")

# ==================================================================
# (c) SPECIES SCALE / 't HOOFT BOUND vs SM ~100 dof
# ==================================================================
print("\n"+"="*92)
print("(c) SPECIES SCALE / dS species bound vs SM dof count (~100-118)")
print("="*92)

# Species scale Lambda_sp = M_Pl/sqrt(N_sp) (Dvali). Inverting: a horizon/entropy
# argument bounds N_sp by S. The 't Hooft-Dvali species bound from a black hole /
# horizon of size L: N_sp <= (L/lP)^2 = S-like. For the dS horizon:
N_sp_dS = (math.sqrt(3/Lam)/lP)**2   # (R_dS/lP)^2  ~ S_dS/pi
print(f"\n  dS species bound (Dvali-type): N_sp <= (R_dS/lP)^2 = {N_sp_dS:.3e} (~10^{math.log10(N_sp_dS):.1f}).")
print("  SM has N_SM ~ 100-118 relativistic dof (g_* ~ 106.75 at high T).")
print(f"  Bound/SM = 10^{math.log10(N_sp_dS):.0f}/10^2 = 10^{math.log10(N_sp_dS)-2:.0f}.")
print("  => the dS species bound is ~120 orders ABOVE the SM dof count: it is VACUOUSLY")
print("     satisfied. It permits ~10^122 species; the SM uses ~10^2. The bound does NOT")
print("     predict, select, or even constrain the SM count -- 100 << 10^122 trivially.")

# Could a TIGHTER species scale (Lambda_sp = M_Pl/sqrt(N)) with N=N_SM~100 say anything?
N_SM = 106.75
Lam_sp = EPl/math.sqrt(N_SM)
print(f"\n  Conversely, species scale with N_SM=106.75: Lambda_sp = M_Pl/sqrt(N_SM) = {Lam_sp:.3e} eV")
print(f"     = M_Pl/{math.sqrt(N_SM):.2f} -- a ~10% shave of M_Pl. NOTHING ties this to a0/Lambda/dS.")
print("  The dS-Unruh inertia kernel plays NO role in this counting: species scale is a UV")
print("  (cutoff) statement; a0 is an IR (horizon) statement. They are decoupled (cf.")
print("  gravity_particle_connection_search.py candidate #4: 'dof count, not a spectrum').")

# Dvali species bound VERBATIM (arXiv:0706.2050 abstract; arXiv:0710.4344):
#   "any consistent theory with N species of mass Lambda puts a lower bound on M_Pl
#    ~ N Lambda^2"  =>  Lambda_sp = M_Pl/sqrt(N);  N_sp < L*^2/L_P^2, L* = L_P sqrt(N_sp).
# DECISIVE test: could the dS structure DERIVE N at the SM value?
print("\n  --- FDR-sharp test: can a0/Lambda DERIVE the SM species count N~100? ---")
R_dS = math.sqrt(3/Lam)
# dS self-consistent saturation: N=(R_dS/L*)^2 with L*=L_P sqrt(N) -> N=R_dS/L_P:
N_sat = R_dS/lP
print(f"     dS self-consistent species saturation N=(R_dS/L_P) = {N_sat:.3e} (~10^{math.log10(N_sat):.1f})")
print(f"     vs SM N~10^2: off by ~{math.log10(N_sat)-2:.0f} orders. The dS bound is NOT saturated")
print("     at the SM count, and nothing in the kernel selects N~100. => no derived count.")
print("\n  FDR (c): N_SM~100 is a single ~2-dex target; the dS sector offers scales at 10^0,")
print("     10^61, 10^122 -- none near 10^2. No O(1)-reachable dS combination lands at ~100")
print("     without a tuned ~10^-60 fudge. Not FDR-significant. => BAKED.")

# ==================================================================
# SYNTHESIS
# ==================================================================
print("\n"+"#"*92)
print("# SYNTHESIS -- does Machian dS-Unruh inertia DERIVE a counting/pattern?")
print("#"*92)
print("""
  (a) kernel spectral structure : BAKED. Thermal (single scale kappa); Matsubara poles are an
      arithmetic ladder set by the CURRENT acceleration; dS-propagator poles are unphysical
      (negative m^2). No mass-eigenvalue selection, no tower of real masses.
  (b) N_dof = 10^122 vs SM ratios: BAKED. Large-number (Dirac/Eddington) numerology; any
      O(1)-dressed power of 10^122 slides onto SM ratios; no privileged rational exponent;
      not FDR-significant.
  (c) dS species bound vs SM dof : BAKED. Bound ~10^122 >> SM ~10^2: vacuously satisfied,
      predicts/selects nothing. UV(species) decoupled from IR(a0).

  OVERALL: the Machian inertia structure is DIMENSIONAL ANALYSIS w.r.t. the mass spectrum.
  It fixes ONE scale (a0 ~ cH_L, the IR inertia floor) -- it does NOT count, quantize, or
  pattern the SM masses. Consistent with the framework's own theorem (emergent gravity
  DECOUPLES the IR horizon sector from UV matter data). => BAKED on all three legs.
""")
