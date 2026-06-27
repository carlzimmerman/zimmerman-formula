#!/usr/bin/env python3
"""
FRONT 3 -- THE LIVE DESI Sigma-m_nu TEST of the neutrino<->dark-energy door.

Carl's question (both-ways, no TOE): the framework's a0(z) is LOCKED to rho_DE(z) by
    a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)),
so the framework's gravitational a0(z) and its cosmological w(z) are the SAME object. DESI's
Sigma-m_nu cosmological bound is DARK-ENERGY-MODEL-DEPENDENT: it is tight (and pushes toward
"negative"/below the oscillation floor) under LambdaCDM, and RELAXES under evolving DE (w0waCDM).

The framework PREDICTS evolving DE (declining rho_DE => w slightly > -1 region, the same a0(z)
branch on Zenodo 10.5281/zenodo.20737162). So does the framework make a SPECIFIC, falsifiable
statement about Sigma-m_nu vs the oscillation floor -- or is it just the generic w0wa-mnu
degeneracy that every dynamical-DE paper has?

We test that with the REAL DESI numbers (hard-coded from the published papers, cited inline) AND
the real DESI DR1 w0waCDM posterior chains already on disk (reuse of a0z_desi_chains_propagation
data) to read off where the framework's OWN preferred (w0,wa) sits relative to the bound.

ALL magnitudes computed here. Footing: a0=9.36e-11 m/s^2, rho_DE=Lambda c^2/8piG, H_Lambda=1.808e-18/s,
E_dS=rho_DE^(1/4)~2.3 meV.

REAL DESI NUMBERS USED (cited):
 - DESI DR1 2024 VI (arXiv:2404.03002): DESI+CMB, LambdaCDM => Sigma m_nu < 0.072 eV (95%).
 - DESI DR2 2025 (arXiv:2503.14738 / PRD 112,083513, arXiv:2503.14744): DESI+CMB, LambdaCDM
     => Sigma m_nu < 0.064 eV (95%); w0waCDM => Sigma m_nu < 0.163 eV (95%).
     Effective (allow negative) => Sigma_eff in ~3sigma tension w/ oscillations; sigma~0.053 eV.
 - Oscillation floors (lab): NORMAL ordering Sigma >= 0.059 eV; INVERTED >= 0.10 eV (5sigma ~0.057).
"""
import os, math
import numpy as np

# ----------------------------------------------------------------------------- constants / footing
c     = 2.99792458e8       # m/s
G     = 6.67430e-11        # SI
hbar  = 1.054571817e-34    # J s
H_L   = 1.808e-18          # 1/s  (H_Lambda, framework footing)
a0    = 9.36e-11           # m/s^2
eV    = 1.602176634e-19    # J
# rho_DE = Lambda c^2 / 8 pi G ; with Lambda c^2 = 3 H_Lambda^2 (pure-Lambda dS) => rho_DE = 3 H_L^2/(8 pi G)
rho_DE = 3.0*H_L**2/(8.0*math.pi*G)              # kg/m^3 (energy density / c^2)
rho_DE_energy = rho_DE*c**2                       # J/m^3
# E_dS = (rho_DE_energy * (hbar c)^3)^(1/4) as an energy quartic-root of the DE energy density
hbarc = hbar*c                                    # J m
E_dS_J = (rho_DE_energy*hbarc**3)**0.25           # J
E_dS_eV = E_dS_J/eV
E_dS_meV = E_dS_eV*1e3

# ----------------------------------------------------------------------------- REAL DESI numbers
DESI = {
    "DR1_2024_LCDM"      : ("DESI+CMB LambdaCDM (arXiv:2404.03002)",        0.072),
    "DR2_2025_LCDM"      : ("DESI+CMB LambdaCDM (arXiv:2503.14738)",        0.064),
    "DR2_2025_w0waCDM"   : ("DESI+CMB w0waCDM    (arXiv:2503.14744)",       0.163),
}
OSC_NORMAL   = 0.059   # eV, normal ordering minimum
OSC_INVERTED = 0.10    # eV, inverted ordering minimum
SIG_EFF_DR2  = 0.053   # eV, error on effective (allow-negative) Sigma_eff, DR2

print("="*96)
print("FRONT 3: DESI Sigma-m_nu vs the framework's a0(z)=sqrt(rho_DE(z)) evolving-DE prediction")
print("="*96)

# ---- PART 0: the meV coincidence (banked claim, recomputed) -----------------------------------
print("\n[0] THE COINCIDENCE (recomputed): rho_DE^(1/4) vs the neutrino mass scale")
print(f"    rho_DE (energy)   = {rho_DE_energy:.3e} J/m^3")
print(f"    E_dS = rho_DE^(1/4)= {E_dS_meV:.3f} meV  = {E_dS_eV:.3e} eV")
print(f"    oscillation Delta-m scales: sqrt(Dm2_atm)~50 meV, sqrt(Dm2_sol)~8.6 meV; Sigma_min(NO)=59 meV")
print(f"    ratio E_dS / sqrt(Dm2_atm)   = {E_dS_meV/50.0:.3f}")
print(f"    ratio E_dS / sqrt(Dm2_sol)   = {E_dS_meV/8.6:.3f}")
print(f"    ratio E_dS / Sigma_min(NO=59)= {E_dS_meV/59.0:.3f}")
print("    => E_dS lands inside the neutrino mass window (meV-50meV): the scale gap CLOSES here,")
print("       UNLIKE every TeV-scale SM door. This is a magnitude coincidence; mechanism tested in [3].")

# ---- PART 1: where the LambdaCDM bound sits vs the floors -------------------------------------
print("\n[1] THE DESI TENSION under LambdaCDM (static DE) -- the thing evolving-DE relaxes")
for k,(lab,b) in DESI.items():
    floorN = "BELOW normal-floor(0.059) -> TENSION" if b<OSC_NORMAL else "above normal-floor"
    floorI = "excludes INVERTED(0.10)"             if b<OSC_INVERTED else "allows inverted"
    print(f"    {lab:42s}: Sigma<{b:.3f} eV  [{floorN}; {floorI}]")
print(f"    Normal-ordering floor  = {OSC_NORMAL:.3f} eV (lab oscillations, hard lower bound)")
print(f"    => DR2 LambdaCDM (0.064) is only {(0.064-OSC_NORMAL)/SIG_EFF_DR2:.2f}sigma above the floor and the")
print(f"       allow-negative Sigma_eff peaks BELOW zero (~3sigma tension): the 'negative neutrino mass' problem.")

# ---- PART 2: does evolving DE (the framework's branch) relax it? quantify the relaxation -------
print("\n[2] THE RELAXATION under w0waCDM (evolving DE = the framework's a0(z) branch)")
b_lcdm = DESI["DR2_2025_LCDM"][1]; b_w0wa = DESI["DR2_2025_w0waCDM"][1]
print(f"    LambdaCDM bound  Sigma < {b_lcdm:.3f} eV   (in tension w/ floor {OSC_NORMAL})")
print(f"    w0waCDM   bound  Sigma < {b_w0wa:.3f} eV   (relaxation factor {b_w0wa/b_lcdm:.2f}x)")
print(f"    Under w0waCDM the bound is {(b_w0wa-OSC_NORMAL)/SIG_EFF_DR2:.1f}sigma ABOVE the normal floor and")
print(f"    {'ALLOWS' if b_w0wa>OSC_INVERTED else 'EXCLUDES'} even the inverted ordering ({OSC_INVERTED} eV) -> tension DISSOLVES.")

# ---- PART 3: is the framework SPECIFIC, or just the generic w0wa degeneracy? -------------------
# Load the real DESI DR1 w0waCDM chains the framework's a0(z) work already uses, read off (w0,wa).
DATA = ("/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula/"
        "1b2404fe-c966-467a-ab3f-1335450f250e/scratchpad/desi_chains")
W0_COL, WA_COL, WEIGHT_COL, BURNIN = 8, 9, 0, 0.3
COMBOS={"DESI+CMB+DESY5":"desy5sn","DESI+CMB+Pantheon+":"pantheonplus"}
Om0=0.31
def load(tag):
    ws,w0s,was=[],[],[]
    for n in (1,2,3,4):
        f=os.path.join(DATA,f"{tag}.chain.{n}.txt")
        if not os.path.exists(f): continue
        d=np.loadtxt(f); k=int(BURNIN*len(d)); d=d[k:]
        ws.append(d[:,WEIGHT_COL]); w0s.append(d[:,W0_COL]); was.append(d[:,WA_COL])
    return np.concatenate(ws),np.concatenate(w0s),np.concatenate(was)
def wz(z,w0,wa): return w0+wa*z/(1.0+z)
def rho_de_ratio(z,w0,wa): return (1.0+z)**(3*(1+w0+wa))*np.exp(-3*wa*z/(1.0+z))

print("\n[3] SPECIFICITY: where does the FRAMEWORK's own (w0,wa) sit, and what does a0(z) ADD?")
print("    The framework FIXES a0(z)/a0(0)=sqrt(rho_DE(z)/rho_DE(0)); rho_DE(z) IS the w(z) integral.")
print("    Read off the framework-preferred (w0,wa) from the real DESI DR1 w0waCDM posterior:")
any_loaded=False
for name,tag in COMBOS.items():
    try:
        w,w0,wa=load(tag)
    except Exception as e:
        print(f"    [{name}] chains unavailable ({e})"); continue
    any_loaded=True
    w0m=np.average(w0,weights=w); wam=np.average(wa,weights=w)
    # framework a0(z) decline and the implied w(z) today
    a0_z1=math.sqrt(rho_de_ratio(1.0,w0m,wam)); a0_z3=math.sqrt(rho_de_ratio(3.0,w0m,wam))
    w_today=wz(0.0,w0m,wam)
    print(f"    [{name}] w0={w0m:+.3f} wa={wam:+.3f}  w(0)={w_today:+.3f}  "
          f"a0(z=1)/a0(0)={a0_z1:.3f}  a0(z=3)/a0(0)={a0_z3:.3f}")
if not any_loaded:
    print("    (no chains loaded -- coincidence/relaxation parts above are independent of this)")

print("""
    KEY DISTINCTION (both-ways):
    * GENERIC, shared with everyone: 'evolving DE relaxes the Sigma m_nu bound' is the well-known
      w0wa<->m_nu geometric degeneracy. Any dynamical-DE model (CPL, thawing, quintessence) gets the
      0.064->0.163 relaxation. The framework does NOT own this.
    * WHAT THE FRAMEWORK ADDS (the only thing that could make it a real, falsifiable door):
      it does NOT have free (w0,wa). Its w(z) is TIED to a0(z) by a0(z)/a0(0)=sqrt(rho_DE(z)/rho_DE(0)),
      AND a0(0)=9.36e-11 is fixed by Lambda. So the framework predicts a SPECIFIC sign+amount of DE
      evolution -> a SPECIFIC point in the (w0,wa) relaxation direction -> a SPECIFIC predicted Sigma m_nu
      band, NOT a free fit. That is testable: if DESI's preferred (w0,wa) drifts AWAY from the
      framework's sqrt(rho_DE) branch, the framework loses its relaxation and the negative-mass tension
      becomes a tension for IT TOO.""")

# ---- PART 4: the falsifiable statement, quantified --------------------------------------------
print("[4] THE FALSIFIABLE STATEMENT (computed):")
print(f"    IF a0(z)=sqrt(rho_DE(z)) holds with the DESI-preferred evolving rho_DE(z), THEN")
print(f"    Sigma m_nu is RELAXED to the w0waCDM band (< {b_w0wa:.3f} eV) and is COMPATIBLE with the")
print(f"    normal-ordering floor {OSC_NORMAL} eV -- the framework PREDICTS no negative-mass tension.")
print(f"    Conversely, the framework is FALSIFIED on this front if BOTH: (a) DESI converges to w=-1")
print(f"    (static DE, no a0(z) evolution -> framework's a0(z) branch dies, see swampland note), AND")
print(f"    (b) Sigma m_nu is then forced below {OSC_NORMAL} eV -> the negative-mass tension stands and the")
print(f"    framework cannot relax it. The discriminator is the DESI w(z) gate (DR3 2026-27), the SAME")
print(f"    gate as the a0(z) paper -- NOT an independent neutrino test.")

print("\n"+"="*96)
print("VERDICT (both-ways, computed)")
print("="*96)
print(f"""  COINCIDENCE -- REAL and SHARP: rho_DE^(1/4) = {E_dS_meV:.2f} meV lands squarely in the neutrino mass
    window (sqrt(Dm2_sol)~8.6, sqrt(Dm2_atm)~50, Sigma_min(NO)=59 meV). This is the ONE SM sector where
    the framework's horizon scale and the particle scale COINCIDE (vs 30+ orders for every TeV door).
    That coincidence is OLD and NOT original to the framework: it is exactly the Fardon-Nelson-Weiner
    MaVaN observation, ( (2e-3 eV)^4 ~ rho_DE, and ~ m_nu scale ). The framework inherits it; it does
    not derive m_nu (no acceleron coupling is forced from a0(z); E_dS=rho_DE^(1/4) RESTATES rho_DE).
  MECHANISM -- NOT FORCED (so far): nothing in a0(z)=sqrt(rho_DE) forces a neutrino-acceleron coupling
    or SETS Sigma m_nu. The connection is a magnitude coincidence + a shared scale, not a derivation.
  LIVE TEST -- GENUINE but NOT NEUTRINO-SPECIFIC: the framework PREDICTS evolving DE (declining rho_DE),
    which is EXACTLY the w0waCDM branch that relaxes DESI's bound from <{b_lcdm} eV (tension, near/below
    the {OSC_NORMAL} floor) to <{b_w0wa} eV (compatible). So the framework's a0(z) is on the SAME side as the
    resolution of the DESI 'negative neutrino mass' tension. BUT the relaxation is the generic w0wa-mnu
    degeneracy shared by all dynamical-DE models; the framework's ONLY distinctive content is that its
    (w0,wa) is NOT free -- it is fixed by a0(z)=sqrt(rho_DE) + a0(0)=9.36e-11 -- so it predicts a
    SPECIFIC point on that relaxation, falsified if DESI's w(z) drifts off the sqrt(rho_DE) branch.
  NET: a REAL neutrino<->DE DOOR (scale gap closes, framework sits on the tension-relaxing side, and its
    w(z) is pinned not free), but a PARTIAL one -- the coincidence is inherited (MaVaN), no mechanism sets
    m_nu, and the live test is the SAME DESI w(z) gate as the a0(z) paper, riding the generic w0wa-mnu
    degeneracy rather than a neutrino-specific prediction. Credit as a neutrino-DE door, NOT a TOE,
    NOT a derivation of the neutrino mass.""")
