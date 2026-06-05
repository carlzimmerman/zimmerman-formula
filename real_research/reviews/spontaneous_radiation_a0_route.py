#!/usr/bin/env python3
"""
SPONTANEOUS RADIATION -> a0?  The decisive horizon test, computed honestly.
===========================================================================
QUESTION (the task's discriminating route): does tying a0 to vacuum/"spontaneous" radiation from the
future EVENT horizon (set by Lambda; Li 2004 holographic DE) give a0 ~ sqrt(rho_DE) (DECLINING at high z,
the framework's bet) -- while the HUBBLE/particle horizon (c/H(z)) gives a0 ~ cH(z) ~ sqrt(rho_total)
(RISING)?  If so, the *density/event-horizon* radiation reading naturally yields the framework's declining
evolution and the *Hubble-horizon* radiation reading (McCulloch QI) does not.

We compute a0(z)/a0(0) at z=1,2,3 for EVERY horizon/radiation reading on the table, plus the present-day
VALUE each predicts (to test the 9.36e-11 number), and the de Sitter / Unruh temperatures. No fitting.
Reproducible: python spontaneous_radiation_a0_route.py . Needs numpy, scipy.
"""
import numpy as np
from scipy.integrate import quad

# ---- constants / cosmology ----
c   = 2.99792458e8
G   = 6.674e-11
hbar= 1.054571817e-34
kB  = 1.380649e-23
Mpc = 3.0857e22
H0  = 67.4e3/Mpc                 # 1/s
Om, OL = 0.315, 0.685
LAM = 3*OL*H0**2/c**2            # cosmological constant, 1/m^2
RHO_L = LAM*c**2/(8*np.pi*G)     # dark-energy density, kg/m^3
H_LAM = c*np.sqrt(LAM/3)         # asymptotic de Sitter rate = sqrt(OL)*H0
A0_FRAME = c**2*np.sqrt(LAM/(32*np.pi))

# DESI DR2-like dynamical dark energy (CPL): w(a) = w0 + wa(1-a). Constant-L is w0=-1, wa=0.
W0, WA = -0.83, -0.62            # representative DESI DR2 best-fit-ish CPL

def rho_de_ratio(z, w0=-1.0, wa=0.0):
    """rho_DE(z)/rho_DE(0) for CPL w(a)."""
    a = 1/(1+z)
    # rho_DE(a)/rho0 = a^{-3(1+w0+wa)} * exp(-3 wa (1-a))
    return a**(-3*(1+w0+wa))*np.exp(-3*wa*(1-a))

def E_LCDM(z):                   # H(z)/H0 on a LCDM (constant-Lambda) background
    return np.sqrt(Om*(1+z)**3+OL)

def E_de(z, w0=-1.0, wa=0.0):    # H(z)/H0 with dynamical DE
    a = 1/(1+z)
    return np.sqrt(Om*a**-3 + OL*rho_de_ratio(z, w0, wa))

# instantaneous future event horizon radius R_e(z) in units c/H0, on a LCDM background
Ea = lambda a: np.sqrt(Om*a**-3+OL)
def Re(z):
    a=1/(1+z)
    return a*quad(lambda ap: 1/(ap**2*Ea(ap)), a, np.inf)[0]

def banner(t): print("\n"+"="*100+"\n"+t+"\n"+"="*100)

def main():
    print("#"*100)
    print("# SPONTANEOUS RADIATION -> a0 :  which horizon gives the framework's DECLINING a0(z)?")
    print("#"*100)
    print(f"\n  rho_L = {RHO_L:.3e} kg/m^3 ;  H_Lambda(de Sitter) = {H_LAM:.3e} /s ;  framework a0 = {A0_FRAME:.3e} m/s^2")
    print(f"  c*sqrt(G rho_L) = {c*np.sqrt(G*RHO_L):.3e} ;  (c/2)sqrt(G rho_L) = {0.5*c*np.sqrt(G*RHO_L):.3e}")
    print(f"  cH0 = {c*H0:.3e} ;  cH0/2pi = {c*H0/(2*np.pi):.3e} ;  c*H_Lambda = {c*H_LAM:.3e}")

    # ---------- (0) temperatures ----------
    banner("(0) the two relevant temperatures (is 'spontaneous radiation' even thermally at the a0 scale?)")
    T_dS  = hbar*H_LAM/(2*np.pi*kB)            # Gibbons-Hawking de Sitter T
    T_dS_V= hbar*H_LAM/(np.pi*kB)              # Volovik T = H/pi (2x GH)
    T_Ua0 = hbar*A0_FRAME/(2*np.pi*c*kB)       # Unruh T at a=a0
    print(f"   Gibbons-Hawking  T_dS = hbar H_L/2pi kB      = {T_dS:.3e} K")
    print(f"   Volovik          T    = hbar H_L/pi  kB (2x) = {T_dS_V:.3e} K")
    print(f"   Unruh at a0      T_U  = hbar a0/2pi c kB     = {T_Ua0:.3e} K")
    print(f"   ratio T_dS/T_U(a0) = {T_dS/T_Ua0:.2f}   (a ~ a0 <=> Unruh T ~ de Sitter T to within this factor)")
    print("   => a0 IS the acceleration whose Unruh temperature ~ the de Sitter horizon temperature. Same SCALE.")

    # ---------- (1) the evolution fork: a0(z)/a0(0) for each radiation/horizon reading ----------
    banner("(1) a0(z)/a0(0): does the EVENT/density reading DECLINE and the HUBBLE reading RISE?")
    zs = [0,1,2,3]
    Re0 = Re(0)
    rows = {
        "HUBBLE horizon  a0~cH(z)~sqrt(rho_tot)   [McCulloch QI; Cai-Kim]": lambda z: E_LCDM(z),
        "instantaneous EVENT-horizon RADIUS a0~1/R_e(z)  [Li-cutoff, radius]": lambda z: Re0/Re(z),
        "EVENT/DENSITY  a0~sqrt(rho_DE), const-Lambda (w=-1)": lambda z: np.sqrt(rho_de_ratio(z,-1.0,0.0)),
        "EVENT/DENSITY  a0~sqrt(rho_DE), DESI dyn-DE (w0,wa)": lambda z: np.sqrt(rho_de_ratio(z,W0,WA)),
    }
    hdr = "  {:<58}".format("reading")+"".join(f"z={z:<6}" for z in zs)
    print(hdr)
    for name,f in rows.items():
        print("  {:<58}".format(name)+"".join(f"{f(z):<8.3f}" for z in zs))
    print("\n   directions:")
    print(f"     HUBBLE  cH(z):              z=1->{E_LCDM(1):.2f}, z=2->{E_LCDM(2):.2f}, z=3->{E_LCDM(3):.2f}   RISES (x3 at z=2)")
    print(f"     EVENT radius 1/R_e(z):      z=1->{Re0/Re(1):.2f}, z=2->{Re0/Re(2):.2f}, z=3->{Re0/Re(3):.2f}   RISES mildly")
    print(f"     EVENT density sqrt(rhoDE) [const-L]: flat (1.00) -- the safe core")
    print(f"     EVENT density sqrt(rhoDE) [DESI]:    z=1->{np.sqrt(rho_de_ratio(1,W0,WA)):.2f}, z=2->{np.sqrt(rho_de_ratio(2,W0,WA)):.2f}, z=3->{np.sqrt(rho_de_ratio(3,W0,WA)):.2f}   DECLINES")

    # ---------- (2) the crux: 1/R_e(z) is NOT sqrt(rho_DE(z)) ----------
    banner("(2) CRUX: is 'a0 ~ 1/(event-horizon radius)' the SAME as 'a0 ~ sqrt(rho_DE)'? (the framework needs the latter)")
    print("   The framework's declining branch is a0 ~ sqrt(rho_DE) (the dark-energy DENSITY).")
    print("   Holographic DE (Li 2004) sets rho_DE ~ 1/R_e^2  =>  sqrt(rho_DE) ~ 1/R_e.  So IF (and only if) one")
    print("   takes the *holographic* relation rho_DE = (3 c_h^2 /8piG) /R_e^2, then sqrt(rho_DE) ~ 1/R_e -- the two")
    print("   readings COINCIDE.  But that makes rho_DE DYNAMICAL (it tracks 1/R_e^2), which is NOT constant-Lambda.")
    print(f"   {'z':>4}{'1/R_e(z) [norm]':>18}{'sqrt(rhoDE),const-L':>22}{'sqrt(rhoDE),holo=1/Re':>24}")
    for z in zs:
        holo = Re0/Re(z)   # if rho_DE ~ 1/Re^2 then sqrt(rho_DE) ~ 1/Re, same column
        print(f"   {z:>4}{Re0/Re(z):>18.3f}{1.00:>22.3f}{holo:>24.3f}")
    print("   => '1/R_e(z)' RISES (+76% at z=3). 'sqrt(rho_DE)' on a CONSTANT-Lambda background is FLAT.")
    print("      They are equal ONLY in the holographic case rho_DE~1/R_e^2 -- and then BOTH rise, NOT decline.")
    print("      The framework's DECLINING branch requires DESI-style w>-1 dynamical DE, i.e. rho_DE that FALLS")
    print("      toward the past -- which is the OPPOSITE of holographic rho_DE~1/R_e^2 (R_e smaller in past => rho up).")

    # ---------- (3) the Volovik 'spontaneous radiation of matter' reading ----------
    banner("(3) Volovik/Klinkhamer de Sitter vacuum DECAY ('spontaneous radiation of matter'): does it set a0?")
    # decay-rate scaling: Gamma ~ H, energy radiation rate (d rho_vac/dt) ~ H^5 (m_Pl^2 in nat. units) [Volovik]
    mPl = np.sqrt(hbar*c/G)                    # Planck mass (kg)
    EPl = mPl*c**2
    lPl = np.sqrt(hbar*G/c**3)
    # vacuum energy density in Planck units ~ (H/H_Pl)^2 ; decay rate of rho_vac ~ H^5/H_Pl^... -> express timescale
    HPl = c/lPl                                # Planck frequency
    # Volovik: rho_vac ~ H^2 m_Pl^2 (nat); d rho_vac/dt ~ -H^5 m_Pl^2 (nat) => fractional rate ~ H (H/m_Pl)^2... let's get t_break
    # quantum breaking time t_q ~ (1/H)(m_Pl/H)^2 ; check it's astronomically long => NO effect on a0 today
    t_break = (1/H_LAM)*(EPl/(hbar*H_LAM))**2
    Gyr = 3.156e16
    print(f"   Planck freq H_Pl = {HPl:.3e}/s ; H_Lambda/H_Pl = {H_LAM/HPl:.3e} (this tiny ratio controls the decay).")
    print(f"   Volovik decay law: rho_vac ~ H^2 m_Pl^2; radiation rate d rho/dt ~ H^5 m_Pl^2 (Planck units).")
    print(f"   => fractional decay rate (1/rho)drho/dt ~ H (H/m_Pl)^2 ; quantum-breaking time t_q ~ (1/H)(m_Pl/H)^2")
    print(f"      t_q ~ {t_break/Gyr:.2e} Gyr  (age of universe ~ 13.8 Gyr).")
    print(f"   So over a Hubble time the vacuum decays by a fraction ~ (H/m_Pl)^2 ~ {(hbar*H_LAM/EPl)**2:.2e} -- UTTERLY negligible.")
    print("   VERDICT on Volovik route: it DOES give a declining rho_DE (vacuum slowly radiates away), and it is tied")
    print("   to H (Hubble), NOT to a fixed Lambda. BUT (a) the decline is ~1e-122 per Hubble time -> ZERO at z<=3,")
    print("   so it cannot produce the framework's ~25% decline by z=3; and (b) the papers contain NO a0, no MOND, no")
    print("   c*sqrt(G rho) acceleration scale. It is a cosmological-constant-relaxation mechanism, not an a0 mechanism.")

    # ---------- (4) the VALUE each radiation principle predicts today ----------
    banner("(4) VALUE today: does any radiation principle predict a0 ~ 9.36e-11 (not just the scale)?")
    cand = [
        ("de Sitter horizon accel c*H_Lambda (Z=1)",      c*H_LAM),
        ("Gibbons-Hawking / Unruh:  cH_Lambda/2pi",       c*H_LAM/(2*np.pi)),
        ("McCulloch QI:  2c^2/Theta = 2cH0",              2*c*H0),
        ("McCulloch QI alt:  c^2/Theta = cH0",            c*H0),
        ("Milgrom/Bernal:  c sqrt(Lambda/3)/2pi = cH_L/2pi", c*np.sqrt(LAM/3)/(2*np.pi)),
        ("vacuum free-fall (c/2)sqrt(G rho_L) [FRAMEWORK]", 0.5*c*np.sqrt(G*RHO_L)),
    ]
    print(f"   {'principle':<48}{'a0 pred':>12}{'/9.36e-11':>12}")
    for n,v in cand:
        print(f"   {n:<48}{v:>12.3e}{v/A0_FRAME:>12.2f}")
    print("   => The DENSITY/free-fall form (c/2)sqrt(G rho_L) and the thermal cH_L/2pi land at the right value;")
    print("      the bare horizon accel cH_Lambda and McCulloch 2cH0 are ~6x and ~3x too big (need the /2pi or /2).")

    banner("BOTTOM LINE")
    print(f"""  * Hubble/particle-horizon radiation (McCulloch QI; Cai-Kim apparent horizon): a0 ~ cH(z) ~ sqrt(rho_total),
      RISES (x3 at z=2). This is a real 'radiation' route (Unruh from the Hubble horizon) but it is the DISFAVORED
      rising branch, and McCulloch's value 2cH0={2*c*H0:.2e} is ~3x the data.
  * Event-horizon RADIUS reading a0 ~ 1/R_e(z): RISES mildly (1.76x at z=3) -- distinctive & data-viable, but it is
      NOT the framework's sqrt(rho_DE) declining branch. (It only equals sqrt(rho_DE) in the holographic case
      rho_DE~1/R_e^2, and then it RISES, not declines.)
  * Event-horizon DENSITY reading a0 ~ sqrt(rho_DE): FLAT for constant-Lambda; DECLINES only if DESI's dynamical DE
      (w>-1, rho_DE falling to the past) is real. THIS is the only reading that gives the framework's declining a0(z),
      and it is tied to the dark-energy DENSITY, not to any radiation rate.
  * Volovik/Klinkhamer 'de Sitter vacuum spontaneously radiates matter': gives a DECLINING rho_DE tied to H -- the
      right DIRECTION -- but the magnitude is ~1e-122 per Hubble time (zero at z<=3) and the mechanism contains NO a0.
  NET: 'spontaneous/vacuum radiation' does NOT *derive* a0, and the radiation routes that are quantitative
      (McCulloch, Cai-Kim) tie a0 to the HUBBLE horizon (RISING), the OPPOSITE of the framework's declining bet.
      The framework's declining sqrt(rho_DE) comes from the dark-energy DENSITY (holographic Li-2004 cutoff /
      DESI dynamical DE), which is a separate idea from any spontaneous-radiation rate.""")
    print("#"*100)

if __name__ == "__main__":
    main()
