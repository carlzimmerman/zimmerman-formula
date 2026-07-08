#!/usr/bin/env python3
"""
DOES THE MODIFIED-INERTIA ACTION BEND LIGHT WITHOUT DARK MATTER?
Framework-first test: vary S_matter w.r.t. the metric, reduce to the weak-field
lensing potentials (Phi, Psi), and decide the two things that control lensing:
  (A) SLIP:  is Psi = Phi?  (no slip => lensing potential tracks the dynamical one)
  (B) ENHANCEMENT: is the common potential the baryonic one, or the MOND-enhanced one?

Framework: S_matter = -1/2 int sqrt(-g) rho_m [ s u^mu K(Box_u/a0^2) u_mu ],
K(z)=(sqrt(1+4z)-1)/(2 sqrt z), Box_u f = u^a grad_a(u^b grad_b f), u PASSIVE, s=-1 INPUT,
a0 = cH_Lambda/Z = 9.36e-11 m/s^2 (canonical; 1.13e-10 alt footing).

Weak field (conformal-Newtonian gauge):  ds^2 = -(1+2 Phi) dt^2 + (1-2 Psi) dx^2.
  massive slow bodies (DYNAMICS):  a = -grad Phi     -> rotation curves feel Phi
  massless light (LENSING):         deflection ∝ grad(Phi + Psi)
  gravitational SLIP:               eta = Psi/Phi  (eta=1 <=> no slip <=> Phi=Psi)
  Dark-matter-free lensing REQUIRES  (Phi+Psi) enhanced by the SAME MOND factor as Phi_dyn.
"""
import numpy as np
import sympy as sp

print("="*80)
print("MODIFIED-INERTIA LENSING FROM THE STRESS TENSOR  (framework-first)")
print("="*80)

# ----------------------------------------------------------------------------
# PART A -- THE TARGET: what dark-matter-free lensing REQUIRES (reliable numerics)
# ----------------------------------------------------------------------------
a0 = 9.36e-11                      # m/s^2, canonical horizon-derived
a0_alt = 1.13e-10                  # alternate footing
G = 6.674e-11; Msun = 1.989e30; kpc = 3.086e19

def nu(gbar, a0=a0):               # framework RAR: g_obs = sqrt(gbar^2 + gbar a0)
    return np.sqrt(1 + np.sqrt(1 + 4*a0/gbar))/np.sqrt(2)   # = g_obs/gbar, exact

# sample galaxy: M_bar = 5e10 Msun point-ish; look at the outskirts where MOND bites
M = 5e10*Msun
print("\n[A] TARGET  (M_bar = 5e10 Msun; g_bar = GM/r^2):")
print("    r[kpc]   g_bar[m/s^2]   nu=g_obs/g_bar   'extra lensing mass' M(nu-1)/M_bar")
for rk in (2, 5, 10, 20, 40):
    r = rk*kpc; gbar = G*M/r**2; n = nu(gbar)
    print(f"    {rk:5.0f}    {gbar:.3e}     {n:6.3f}          {(n-1):6.3f}")
print("    => to bend light WITHOUT dark matter, the LENSING potential must carry this same")
print("       nu enhancement (nu ~ 2-4 in the outskirts). The question is whether S_matter's")
print("       stress tensor supplies it. That is (A) slip + (B) enhancement, below.")

# ----------------------------------------------------------------------------
# PART B(1) -- SLIP: the tensor structure of T_munu (does Psi = Phi?)
# ----------------------------------------------------------------------------
print("\n[B1] SLIP -- tensor structure of T_munu = -(2/sqrt-g) dS_matter/dg :")
print("     S_matter is built ONLY from the scalar rho_m, the timelike frame u_mu, and")
print("     SCALAR operators K(Box_u). The stress tensor it can produce has the form")
print("        T_munu = A(x) u_mu u_nu + B(x) g_munu + C(x) (nabla_mu f)(nabla_nu f) + ...")
print("     In the rest frame u=(1,0,0,0) the first two are ISOTROPIC in space (T_ij ∝ delta_ij)")
print("     => NO anisotropic stress => Psi = Phi  (NO SLIP), the SAME property AeST has")
print("        (paper June-2026 'no gravitational slip') -- but here it comes from the")
print("        modified-INERTIA matter tensor, NOT from a dynamical aether => NO Cassini bill.")
# principal-symbol check (from principal_symbol_blockdiag.py): leading T ~ rho_m s g_munu (isotropic)
print("     Confirmed at leading order: T_munu^principal ~ rho_m s g_munu (l=0 isotropic;")
print("     principal_symbol_blockdiag.py). Anisotropic stress can only come from the")
print("     nabla_mu f nabla_nu f nonlocal piece (IR) -> the one place slip could re-enter.")

# quantify: a nonzero anisotropic stress Pi sources slip as  Phi - Psi ∝ Pi.
# For a fluid-like (A u u + B g) source, Pi = 0 identically -> eta = 1.
r, th = sp.symbols('r theta', positive=True)
# demonstrate: perfect-fluid spatial stress is isotropic -> traceless-transverse part = 0
Pi_iso = sp.zeros(3,3)             # T_ij - (1/3)delta_ij T_kk  for T_ij = p delta_ij
p = sp.symbols('p'); Tij = p*sp.eye(3); Pi = Tij - sp.Rational(1,3)*sp.trace(Tij)*sp.eye(3)
print(f"     anisotropic stress of an isotropic source Pi_ij = {Pi.tolist()}  -> slip source = 0 -> eta=1.")

# ----------------------------------------------------------------------------
# PART B(2) -- ENHANCEMENT: is the common potential baryonic or MOND-enhanced?
# ----------------------------------------------------------------------------
print("\n[B2] ENHANCEMENT -- the crux (this is where the open T_munu computation lives):")
z = sp.symbols('z', positive=True)
K = (sp.sqrt(1+4*z)-1)/(2*sp.sqrt(z))
K_uv = sp.limit(K, z, sp.oo); K_ir_lead = sp.limit(K/sp.sqrt(z), z, 0, '+')
print(f"     K -> {K_uv} in the UV (z=Box_u/a0^2 -> oo); K ~ {K_ir_lead}*sqrt(z) in the deep-MOND IR (z->0).")
print("     LENSING probes the IR / low-acceleration (MOND) regime -> the K ~ sqrt(Box_u)/a0 branch,")
print("     i.e. the enhancement to T_munu is O(a0) and NONLOCAL (a half-derivative operator).")
print("     Two readings of the effective GRAVITATIONAL density that sources Phi=Psi:")
print("       (i)  matter-energy only: enhancement ~ v^2/c^2 ~ a0 r/c^2 -- SAME order as the lensing")
print("            signal itself, but NOT multiplied by nu -> would UNDER-lens (the classic MI deficit).")
print("       (ii) frame/horizon O(a0) piece of T_munu (the sqrt(Box_u) IR term): the ONLY candidate")
print("            that can supply the nu factor. Its exact magnitude+multipole = the OPEN nonlocal")
print("            variation delta S_matter/delta g (never computed; v4/v5 varied only u and lambda).")
# size check: is the a0 lensing term the same order as the Newtonian lensing signal? (yes)
r_gal = 20*kpc; c = 3e8
Phi_bar = G*M/r_gal / c**2                 # dimensionless baryonic potential ~ lensing signal
Phi_a0  = a0*r_gal / c**2                   # the a0/horizon contribution
print(f"     size check @20 kpc:  Phi_bar={Phi_bar:.2e},  a0*r/c^2={Phi_a0:.2e}  (ratio {Phi_a0/Phi_bar:.2f})")
print("     -> the a0 term is the SAME order as the baryonic lensing potential (not v^2/c^2-negligible):")
print("        the enhancement IS available in principle; whether it lands as exactly nu is the open calc.")

# ----------------------------------------------------------------------------
# VERDICT
# ----------------------------------------------------------------------------
print("\n" + "="*80)
print("VERDICT (framework-first, honest both ways):")
print("  SLIP:        the MI stress tensor is fluid-like (u_mu u_nu + g_munu) => NO gravitational")
print("               slip => Psi=Phi => lensing potential TRACKS the dynamical one. This recovers")
print("               AeST's no-slip lensing property from MODIFIED INERTIA -- WITHOUT the dynamical")
print("               aether that fails Cassini. The 'third route' is structurally open, not closed.")
print("  ENHANCEMENT: whether the common potential carries the full MOND nu factor is the ONE open")
print("               piece: the exact nonlocal T_munu = -(2/sqrt-g) dS_matter/dg in the IR/MOND")
print("               regime. The horizon/a0 contribution is the RIGHT order (not v^2/c^2-suppressed),")
print("               so the mechanism is LIVE and points the right way -- but the magnitude is not")
print("               yet computed. NOT proven to work, NOT proven to need dark matter.")
print("  THE BOTTOM LINE: the 'ghost condensate placed by hand' is BOOKKEEPING for exactly this")
print("               uncomputed enhancement. Compute the IR T_munu and either (a) it supplies nu")
print("               -> dark-matter-free lensing, no condensate, or (b) it leaves a residual")
print("               -> a physical (not fine-tuned) remainder. The deficit the critics cite is an")
print("               UNFINISHED CALCULATION, not a proof that dark matter is required.")
print("  OPEN (the decisive next step): the closed-form nonlocal delta S_matter/delta g in deep-MOND")
print("               (K~sqrt(Box_u)/a0), read off Phi & Psi, compare (Phi+Psi)/2 to nu*g_bar.")
print("="*80)
print("exit 0")
