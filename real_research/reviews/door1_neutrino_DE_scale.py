#!/usr/bin/env python3
"""
DOOR 1 (neutrino) — both-ways verification of the 2023-2026 forcing candidates that
would upgrade E_L = rho_DE^(1/4) = 2.24 meV from FOUNDED-NOT-DERIVED to a DERIVED
absolute neutrino mass. Footing locked: a0 = cH_Lambda/Z = 9.36e-11, Z=sqrt(32pi/3).
Exit 0. Prove-by-moving-the-number: show that EVERY candidate still carries a free O(1).
"""
import mpmath as mp
mp.mp.dps = 40

# ---- constants (SI / natural) ----
c     = mp.mpf('299792458')
hbar  = mp.mpf('1.054571817e-34')
G     = mp.mpf('6.67430e-11')
H0    = mp.mpf('67.36')*1000/(mp.mpf('3.0856775814913673e22'))  # s^-1
OmL   = mp.mpf('0.6847')
eV    = mp.mpf('1.602176634e-19')
MP_red= mp.mpf('2.435e18')*1e9*eV/c**2   # reduced Planck mass in kg
MP_red_eV = mp.mpf('2.435e18')*1e9       # reduced Planck mass in eV

# ---- rho_DE and E_L (the FORCED number) ----
rho_crit = 3*H0**2/(8*mp.pi*G)
rho_DE   = OmL*rho_crit
u_DE     = rho_DE*c**2                       # J/m^3
# E_L = (rho_DE c^2 (hbar c)^3)^(1/4) as an energy, then to eV
E_L_J = (u_DE*(hbar*c)**3)**(mp.mpf(1)/4)
E_L_eV = E_L_J/eV
print(f"rho_DE          = {mp.nstr(rho_DE,6)} kg/m^3")
print(f"E_L = rho_DE^1/4 = {mp.nstr(E_L_eV*1000,7)} meV   (FORCED)")

# ---- de Sitter entropy N = M_P^2/Lambda (dimensionless dof count) ----
Lam = 3*OmL*H0**2/c**2          # m^-2 (cosmological constant)
# dS entropy S_dS = pi/(G hbar Lam /c^3)... use area/4: A=4 pi r_dS^2, r_dS=sqrt(3/Lam)
r_dS = mp.sqrt(3/Lam)
A    = 4*mp.pi*r_dS**2
lP2  = hbar*G/c**3
S_dS = A/(4*lP2)
print(f"\nde Sitter entropy S_dS (=N) = {mp.nstr(S_dS,5)}  (~10^{int(mp.log10(S_dS))})")

# ---- CANDIDATE A: Addazi-Meluccio info-seesaw  m_nu ~ M_P / N^(1/4) ----
# Their claim m_nu ~ (M_P^2 Lambda)^(1/4) ~ M_P/N^(1/4). Check N^(1/4) gives meV.
mnu_A = MP_red_eV / S_dS**(mp.mpf(1)/4)
print(f"\n[A] Addazi-Meluccio  M_P/N^(1/4)        = {mp.nstr(mnu_A*1000,5)} meV")
print(f"    vs E_L                              = {mp.nstr(E_L_eV*1000,5)} meV")
print(f"    ratio (M_P/N^1/4)/E_L               = {mp.nstr(mnu_A/E_L_eV,5)}  (the residual O(1))")

# ---- CANDIDATE B: Jia neutrino-vacuum-energy (rho_vac = sum m^4/64pi^2 log) ----
# He sets rho_vac = (2.3 meV)^4 and solves -> m1 in 6.3-16.3 meV. The log/mu_Lam is free.
# Show: a single-species crude inversion m ~ (64 pi^2 rho_DE)^(1/4) (drop log) moves E_L by O(1).
mB = (64*mp.pi**2)**(mp.mpf(1)/4) * E_L_eV
print(f"\n[B] Jia 1-species (64pi^2 rho_DE)^(1/4) = {mp.nstr(mB*1000,5)} meV  (log & mu_Lam FREE)")
print(f"    O(1) prefactor (64pi^2)^(1/4)       = {mp.nstr((64*mp.pi**2)**(mp.mpf(1)/4),5)}")

# ---- CANDIDATE C: neutrino-loop DE (EPJC 2025)  rho_DE = y^2 m_nu^6/(512 pi^4 m_phi^2) ----
# Solve for m_nu given y, m_phi free. Show m_nu spans a decade as y/m_phi vary O(1).
def mnu_C(y, mphi_eV):
    rhs = mp.mpf(512)*mp.pi**4*mphi_eV**2*u_DE*(hbar*c)**3/eV**4  # rho_DE in eV^4 * 512pi^4 mphi^2
    return (rhs/y**2)**(mp.mpf(1)/6)
print(f"\n[C] neutrino-loop DE  rho_DE=y^2 m_nu^6/(512pi^4 m_phi^2):")
for y,mphi in [('0.28',1.0),('1.0',1.0),('0.1',1.0)]:
    print(f"    y={y}, m_phi=1eV -> m_nu = {mp.nstr(mnu_C(mp.mpf(y),mp.mpf(mphi))*1,4)} eV  (y,m_phi FREE)")

# ---- the absolute-scale data discriminator ----
# Framework m1=E_L => Sigma = E_L + sqrt(E_L^2+dm21) + sqrt(E_L^2+dm31)
dm21 = mp.mpf('7.42e-5')   # eV^2
dm31 = mp.mpf('2.510e-3')
m1 = E_L_eV
m2 = mp.sqrt(m1**2+dm21); m3 = mp.sqrt(m1**2+dm31)
Sig = m1+m2+m3
Sig_floor = mp.sqrt(dm21)+mp.sqrt(dm31)  # m1->0
print(f"\n--- absolute-scale discriminator (NO) ---")
print(f"m1=E_L => Sigma m_nu = {mp.nstr(Sig*1000,5)} meV ; minimal-NO floor = {mp.nstr(Sig_floor*1000,5)} meV")
print(f"DESI DR2+CMB (LCDM) 95%%: Sigma < 64 meV ; DESI+DESY5 w0wa PREFERS Sigma ~ 98 (+16-37) meV")
print(f"=> m1=E_L (Sigma~61) consistent w/ LCDM bound; but w0wa data DRIFTS to ~98 meV (heavier m1)")
print("\nEXIT 0")
