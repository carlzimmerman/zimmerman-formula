#!/usr/bin/env python3
"""
DOOR 1 (THE NEUTRINO) -- EXHAUSTION SCRIPT.

Question Carl wants settled, both-ways: does ANY swept lead supply a FORCED
absolute neutrino mass m_nu from Lambda -- i.e. upgrade the framework's
  E_L = rho_DE^(1/4) = 2.24 meV   (FOUNDED-NOT-DERIVED)
to a DERIVED m_nu_lightest with NO free O(1) coefficient -- or do they all
remain bounds / coincidences / fits?

Footing locked (the framework's OWN premises, never the standard-MOND lens):
  a0 = c H_Lambda / Z,  Z = sqrt(32 pi / 3),  modified INERTIA from the
  de Sitter-Unruh horizon.  rho_DE sets BOTH a0 and E_dS = rho_DE^(1/4).

The blade this script computes: the COEFFICIENT k in
        m_nu_lightest = k * E_L = k * rho_DE^(1/4).
If any swept mechanism FIXES k with no free parameter -> founded becomes derived.
We show, lead by lead, that every mechanism leaves k FREE (a Yukawa / vev /
log / cutoff), exactly as the framework's own m1 = E_L sets k = 1 BY FIT
(inversion), not by derivation. => founded-not-derived STAYS.

Prove-by-moving-the-number: each lead prints the k it implies and what makes
k free.  Exit 0.  No git push.
"""
import mpmath as mp
mp.mp.dps = 50

# ---------------- constants (SI) ----------------
c    = mp.mpf('299792458')
hbar = mp.mpf('1.054571817e-34')
G    = mp.mpf('6.67430e-11')
H0   = mp.mpf('67.36')*1000/mp.mpf('3.0856775814913673e22')   # s^-1
OmL  = mp.mpf('0.6847')
eV   = mp.mpf('1.602176634e-19')
MP_red_eV = mp.mpf('2.435e18')*1e9        # reduced Planck mass [eV]

# ---------------- rho_DE and the FORCED number E_L ----------------
rho_crit = 3*H0**2/(8*mp.pi*G)
rho_DE   = OmL*rho_crit
u_DE     = rho_DE*c**2                      # J/m^3
E_L_eV   = (u_DE*(hbar*c)**3)**(mp.mpf(1)/4)/eV
E_L_meV  = E_L_eV*1000
print("="*70)
print("FORCED by the framework (same rho_DE that sets a0):")
print(f"  E_L = rho_DE^(1/4) = {mp.nstr(E_L_meV,7)} meV   (k == 1 BY FIT, not derived)")
print("="*70)

# de Sitter entropy N = A/4 l_P^2  (the '1/N' the holographic leads use)
Lam  = 3*OmL*H0**2/c**2
r_dS = mp.sqrt(3/Lam)
N    = 4*mp.pi*r_dS**2 / (4*hbar*G/c**3)
print(f"de Sitter entropy N = {mp.nstr(N,5)}  (~1e{int(mp.log10(N))})\n")

# oscillation data (NuFIT-class, normal ordering)
dm21 = mp.mpf('7.42e-5')      # eV^2
dm31 = mp.mpf('2.510e-3')     # eV^2
m_atm = mp.sqrt(dm31)*1000    # meV scale set by sqrt(dm31)
print(f"OSCILLATION DATA (the absolute scale is NOT fixed by it):")
print(f"  sqrt(dm21) = {mp.nstr(mp.sqrt(dm21)*1000,4)} meV ; sqrt(dm31) = {mp.nstr(m_atm,4)} meV")
print(f"  -> data fixes SPLITTINGS only; m_lightest is FREE in [0, ~ bound].\n")

# swampland bound (Gonzalo-Ibanez-Valenzuela 2109.10961): m_nu,1 <= Lambda_4^(1/4)
# i.e. m1 <= E_L (an INEQUALITY, saturation NOT forced)
print("SWAMPLAND BOUND (Gonzalo-Ibanez-Valenzuela 2109.10961):")
print(f"  m_nu,1 <= Lambda^(1/4) ~ E_L = {mp.nstr(E_L_meV,5)} meV   (<=, NOT '=')")
print(f"  -> the framework's m1 = E_L is the SATURATED EDGE: a CHOICE, not a")
print(f"     theorem. k <= 1 permitted; k = 1 not forced.\n")

print("-"*70)
print("LEAD-BY-LEAD both-ways: implied k = m_nu / E_L and WHY k is free")
print("-"*70)

def line(tag, k, freedom):
    print(f"[{tag}] k = {mp.nstr(k,4):>8s} x E_L   <- FREE via {freedom}")

# [A] Addazi & Meluccio, Particles 9 (2026) 11 / arXiv:2604.26982
# Eq 82: m_nu ~ rho_vac^(1/4) ~ (M_P^2 Lambda)^(1/4) ~ M_P / N^(1/4)   (all '~')
# Eq 85: L > phi_h nu nu-bar,  <phi_h> = rho_vac^(1/4)  -- Yukawa O(1) UNDETERMINED.
# Majorana character (nu^T C nu). 1/N counting does NOT fix the absolute scale.
k_A_geom = (MP_red_eV / N**(mp.mpf(1)/4)) / E_L_eV    # the bare M_P/N^(1/4) geometric value
line("A Addazi-Meluccio  M_P/N^1/4", k_A_geom,
     "hairon Yukawa in Eq.85 (PROP '~', coupling undetermined); Majorana")
print("     -> CONFIRMED from arXiv HTML: Eq.82 uses '~' not '='; Eq.85 coupling")
print("        carries a free O(1); '1/N does NOT fix the absolute scale uniquely'.")
print("        STRONGEST forcing candidate -> still NOT parameter-free. k FREE.")

# [B] Jia 2410.06604: rho_vac = sum (-1)^2j g_i m_i^4/64pi^2 log(m^2/mu^2) == rho_DE
# drop log -> single-species k = (64 pi^2)^(1/4); log & cutoff mu_Lam are FREE.
k_B = (64*mp.pi**2)**(mp.mpf(1)/4)
line("B Jia vacuum-energy inversion", k_B, "log(m^2/mu^2) & cutoff mu_Lam (=> m1 spans 6-16 meV)")

# [C] neutrino-loop DE, EPJC 85 (2025): rho_DE = y^2 m_nu^6/(512 pi^4 m_phi^2)
# REVERSE direction (rho_DE FROM m_nu); two free params y, m_phi => m_nu spans a decade.
def mnu_C(y, mphi_eV):
    rhs = mp.mpf(512)*mp.pi**4*mphi_eV**2*u_DE*(hbar*c)**3/eV**4
    return (rhs/y**2)**(mp.mpf(1)/6)
k_C_lo = mnu_C(mp.mpf('1.0'),mp.mpf('1.0'))/E_L_eV
k_C_hi = mnu_C(mp.mpf('0.1'),mp.mpf('1.0'))/E_L_eV
print(f"[C neutrino-loop DE]   k in [{mp.nstr(k_C_lo,4)}, {mp.nstr(k_C_hi,4)}] x E_L"
      f"   <- FREE via (y, m_phi); REVERSE direction (rho_DE FROM m_nu)")

# [D] Dark-dimension RHN (Montero-Vafa-Valenzuela + 2406.14609 + 2512.09052):
# m_nu = y^2 <H>^2/<Phi>^2 * m_KK,  m_KK ~ Lambda^(1/4).  FUNCTION differs from m=E_L;
# carries free y, <Phi>. Lands ~0.1 eV at natural O(1) -> k ~ 40 but tunable.
print("[D dark-dimension RHN] k FREE via y, <Phi> (m_nu = y^2 <H>^2/<Phi>^2 m_KK);")
print("                       DIFFERENT functional than m=E_L; ~0.1 eV at natural O(1).")

# [E] McCulloch Unruh-vs-KATRIN (2025): predicts m_nu ~ 0.45 eV by matching the
# KATRIN UPPER LIMIT using a DIFFERENT acceleration/Unruh scale (NOT rho_DE^1/4).
# A rival coincidence at a LARGER scale; does not force E_L; (mirage, banked).
k_E = mp.mpf('0.45')/E_L_eV
line("E McCulloch Unruh-KATRIN", k_E, "different Unruh scale; matches the 0.45 eV BOUND, not the meV scale")

# [F] Quintessential inflation (2602.20349, 2026) & MaVaN: BOUND only (Sigma<0.067 eV),
# absolute m_nu free; degeneracy-breaking, not a derivation.
print("[F quintess.-infl / MaVaN] BOUND only (Sigma < 0.067 eV); absolute scale FREE.\n")

print("-"*70)
print("ABSOLUTE-SCALE DATA blade (both-ways, CORRECTED this sweep):")
print("-"*70)
m1 = E_L_eV
m2 = mp.sqrt(m1**2+dm21); m3 = mp.sqrt(m1**2+dm31)
Sig = (m1+m2+m3)*1000
Sig_floor = (mp.sqrt(dm21)+mp.sqrt(dm31))*1000
print(f"  framework m1 = E_L => Sigma = {mp.nstr(Sig,5)} meV ; minimal-NO floor = {mp.nstr(Sig_floor,5)} meV")
print(f"  (m1 = E_L sits only {mp.nstr(Sig-Sig_floor,3)} meV above the floor -> ~indistinguishable from minimal-NO)")
print( "  LCDM (DESI DR2+CMB) 95%: Sigma < 65 meV  -> m1=E_L (61) OK, but RIGHT AT the wall.")
print( "  w0waCDM / CPL (DESI DR2): Sigma < 66-79 meV (Elbers; only MODEST relaxation);")
print( "    the 2.7sigma 'positive Sigma~98 meV' preference is DE-MODEL DEGENERATE.")
print( "  => HONEST GRADE: NON-DECISIVE. Not robustly favored NOR robustly disfavored.")
print( "     (Lead's 'mildly DISFAVORED' was too strong: dynamical DE LOOSENS, not")
print( "      tightens, the bound -> it RELIEVES pressure on m1=E_L, not adds it.)")
print( "  Live falsifier 2026-2028: DESI DR3-era Sigma + JUNO ordering (first data 2026-06-10).\n")

print("="*70)
print("VERDICT: every swept lead leaves the coefficient k = m_nu/E_L FREE")
print("(Yukawa / vev / log / cutoff / different-scale).  NO forcing shown.")
print("=> FOUNDED-NOT-DERIVED STAYS.  E_L is forced; the neutrino's ABSOLUTE")
print("   mass is NOT.  Sharpened, not closed.  Door stays OPEN.")
print("="*70)
print("\nEXIT 0")
