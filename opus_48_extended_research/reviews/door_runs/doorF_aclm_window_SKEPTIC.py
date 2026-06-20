#!/usr/bin/env python3
"""
SKEPTIC re-run of DOOR F (F_aclm_window) -- fully independent clean-room check.

Goal: reproduce (or refute) the prior agent's load-bearing numbers WITHOUT copying its code.
I re-derive every scale from the ACLM (hep-th/0312099) formulas (verified vs the arXiv abstract
this session: r~M_Pl/M^2, t~M_Pl^2/M^3, omega^2~k^4/M^2) and the in-repo extracted notes
(Gamma=M^3/4M_Pl^2, m=mu=M^2/sqrt2 M_Pl, 10 MeV twinkling ceiling).

Independent choices to stress-test the prior result:
  * I recompute M_Pl from G (NOT a hardcoded 2.435e18 GeV) to confirm the constant.
  * I use exact hbar*c conversions.
  * I separately test the c_s^2 branch claim (the SHARP HOOK in the brief) since the brief
    warns about using the wrong c_s^2 branch / mis-citing Creminelli.
"""
import numpy as np

# ---- fundamental constants (SI) ----
c    = 2.99792458e8
G    = 6.67430e-11
hbar = 1.054571817e-34
eV   = 1.602176634e-19
Mpc  = 3.0856775814913673e22
kpc  = Mpc/1e3
Gyr  = 1e9*365.25*24*3600

# reduced Planck mass FROM G (independent of any hardcode)
M_Pl_J  = np.sqrt(hbar*c**5/(8*np.pi*G))      # joules
M_Pl_eV = M_Pl_J/eV
print(f"[check] reduced M_Pl = {M_Pl_eV:.4e} eV  (prior used 2.435e27 eV)  "
      f"ratio={M_Pl_eV/2.435e27:.4f}")

# energy<->length/time
hbarc_Jm = hbar*c                              # J*m
def E_len_Mpc(E_eV):  # length = hbar c / E
    return (hbarc_Jm/(E_eV*eV))/Mpc
def E_time_Gyr(E_eV): # time = hbar / E
    return (hbar/(E_eV*eV))/Gyr

# cosmology
H0    = 67.4e3/Mpc           # s^-1
H0_eV = hbar*H0/eV           # eV
age   = 13.8                 # Gyr
print(f"[check] H0 = {H0:.4e}/s = {H0_eV:.4e} eV")
print()

# ---- ACLM scales as functions of M (eV) ----
def r_crit_Mpc(M):   return E_len_Mpc(M**2/M_Pl_eV)            # M_Pl/M^2
def t_crit_Gyr(M):   return E_time_Gyr(M**3/M_Pl_eV**2)        # M_Pl^2/M^3
def Gamma_eV(M):     return M**3/(4*M_Pl_eV**2)                # Jeans rate
def m_eV(M):         return M**2/(np.sqrt(2)*M_Pl_eV)          # mu = oscillation mass
def muinv_Mpc(M):    return E_len_Mpc(m_eV(M))

M_banked = 0.148
print("="*78)
print("(1) REPRODUCE the banked table (compare to in-repo notes line 48-52)")
print("="*78)
print(f"{'M(eV)':>9} {'r_crit(kpc)':>12} {'t_crit(Gyr)':>12} {'Gamma(eV)':>11} "
      f"{'mu^-1(Mpc)':>11} {'H0/Gamma':>10} {'m/H0':>10}")
for M in [1e-3, 0.04, 0.15, M_banked, 1.0, 1e7]:
    print(f"{M:9.2e} {r_crit_Mpc(M)*1e3:12.3e} {t_crit_Gyr(M):12.3e} {Gamma_eV(M):11.3e} "
          f"{muinv_Mpc(M):11.3e} {H0_eV/Gamma_eV(M):10.3e} {m_eV(M)/H0_eV:10.3e}")
print()
print("  in-repo notes claim: M=0.15 -> r_c=707 kpc, t_c=3.8e25 Gyr, H0/Gamma=1.0e25")
print(f"  my recompute M=0.15: r_c={r_crit_Mpc(0.15)*1e3:.0f} kpc, t_c={t_crit_Gyr(0.15):.2e} Gyr, "
      f"H0/Gamma={H0_eV/Gamma_eV(0.15):.2e}")
print()

# ---- the FIVE boundaries -> M edges ----
def M_from_r(r_m):  return np.sqrt((hbarc_Jm/r_m/eV)*M_Pl_eV)           # r_crit=r -> M
def M_from_t(t_s):  return ((hbar/t_s/eV)*M_Pl_eV**2)**(1/3)            # t_crit=t -> M
M_anti_disk = M_from_r(30*kpc)        # antigravity beyond 30 kpc disk
M_anti_clu  = M_from_r(1.0*Mpc)       # antigravity beyond 1 Mpc cluster
M_time      = M_from_t(age*Gyr)       # twinkling time > age
M_cure      = (4*M_Pl_eV**2*H0_eV)**(1/3)        # H0 > Gamma
M_subhz     = np.sqrt(np.sqrt(2)*M_Pl_eV*H0_eV)  # m=mu > H0
M_lab       = 10e6                    # 10 MeV twinkling ceiling
M_lab_weak  = 100e6

print("="*78)
print("(2) THE FIVE M-EDGES")
print("="*78)
print(f"  UPPER  antigravity>30kpc disk : M <= {M_anti_disk:.3e} eV")
print(f"  UPPER  antigravity>1Mpc clu   : M <= {M_anti_clu:.3e} eV")
print(f"  UPPER  twinkling time > age   : M <= {M_time:.3e} eV")
print(f"  UPPER  dS Jeans cure H0>Gamma : M <= {M_cure:.3e} eV")
print(f"  UPPER  twinkling lab (10 MeV) : M <= {M_lab:.3e} eV")
print(f"  LOWER  sub-horizon m>H0       : M >= {M_subhz:.3e} eV")
print()

# ---- the prior agent's two readings ----
print("="*78)
print("(3) WINDOW READINGS -- reproduce the prior agent's claims")
print("="*78)
# CLASS-I genuine pathology (mu-independent): lab, time, cure (upper); subhz (lower)
M_classI_up = min(M_lab, M_time, M_cure)
classI_w = np.log10(M_classI_up/M_subhz)
print(f"  CLASS-I (genuine, mu-independent): [{M_subhz:.3e}, {M_classI_up:.3e}] eV "
      f"= {classI_w:.2f} orders")
print(f"     binding upper = {'10 MeV lab' if M_classI_up==M_lab else ('time' if M_classI_up==M_time else 'cure')}")
print(f"     PRIOR CLAIMED: 2.23e-3 <= M <= 1.0e7 eV = 9.65 orders")
print()
# +antigravity-disk
M_disk_up = min(M_anti_disk, M_time, M_cure, M_lab)
disk_w = np.log10(M_disk_up/M_subhz)
print(f"  +antigravity>disk(30kpc): [{M_subhz:.3e}, {M_disk_up:.3e}] eV = {disk_w:.2f} orders")
print(f"     PRIOR CLAIMED: [2.23e-3, 0.72] eV = 2.51 orders")
print()
# +antigravity-cluster
M_clu_up = min(M_anti_clu, M_time, M_cure, M_lab)
clu_w = np.log10(M_clu_up/M_subhz)
print(f"  +antigravity>cluster(1Mpc): [{M_subhz:.3e}, {M_clu_up:.3e}] eV = {clu_w:.2f} orders")
print()

# ---- banked-point margins ----
print("="*78)
print("(4) BANKED-POINT MARGINS (M = 0.148 eV)")
print("="*78)
print(f"  orders above sub-horizon floor      : {np.log10(M_banked/M_subhz):.2f}")
print(f"  orders below 10 MeV lab ceiling     : {np.log10(M_lab/M_banked):.2f}")
print(f"  orders below Class-I upper          : {np.log10(M_classI_up/M_banked):.2f}")
print(f"  orders below antigravity-disk wall  : {np.log10(M_anti_disk/M_banked):.2f}")
print(f"  orders below antigravity-cluster wall:{np.log10(M_anti_clu/M_banked):.2f}")
print(f"     PRIOR CLAIMED: 7.8 below ceiling, 1.82 above floor, 0.69 interior to disk window")
print()
# naive all-five intersection (the SHUT artifact)
M_naive_up = min(M_anti_clu, M_time, M_cure, M_lab)
naive_w = np.log10(M_naive_up/M_subhz)
print(f"  NAIVE all-five (incl cluster-antigravity) window = {naive_w:.2f} orders;"
      f" banked is {np.log10(M_banked/M_naive_up):+.2f} orders vs upper (negative=outside->SHUT artifact)")
print()

# ---- THE SHARP HOOK: c_s^2 branch (independent of the window question) ----
print("="*78)
print("(5) SHARP-HOOK CROSS-CHECK: the Q-mode sound speed c_s^2(dQ)=dQ/(3dQ+2)")
print("="*78)
import sympy as sp
dQ = sp.symbols('dQ', real=True)
cs2 = dQ/(3*dQ+2)
print(f"  c_s^2(dQ) = {cs2}")
print(f"  on Q>1 (dQ>0): c_s^2 = {cs2.subs(dQ,0.5)} > 0  (stable, sub-luminal)")
print(f"  on Q<1 (dQ<0, e.g dQ=-0.1): c_s^2 = {float(cs2.subs(dQ,-0.1)):+.4f}  (gradient-unstable)")
print(f"  on Q<1 (dQ=-0.5): c_s^2 = {float(cs2.subs(dQ,-0.5)):+.4f}")
print("  => positivity REQUIRES the Q>1 branch (sign(I0) forced positive). This is the")
print("     SAME Jeans/gradient instability the dS Hubble friction over-damps (H0/Gamma~1e25).")
print("  NOTE: Creminelli-Janssen-Senatore (2207.14224) is NOT applied as a kill (it needs a")
print("        conformal UV completion the GC lacks). Grall-Melville/Serra-Trombetta bind the")
print("        GC but are about the GAPPED mode v^2 <= c_s^2 -- a magnitude bound, not a window kill.")
print()

print("="*78)
print("VERDICT LOGIC")
print("="*78)
print(f"  Genuine-pathology (Class-I) window width = {classI_w:.2f} orders (prior: 9.65)")
print(f"  Banked point interior?  floor+{np.log10(M_banked/M_subhz):.1f}, ceiling-{np.log10(M_lab/M_banked):.1f} orders")
print(f"  Naive-all-five (cluster antigravity double-counted) = {naive_w:.2f} orders, banked "
      f"{np.log10(M_banked/M_naive_up):+.2f} -> SHUT artifact")
