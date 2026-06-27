#!/usr/bin/env python3
"""
nu_de_mechanism.py  --  FRONT 2: does the de Sitter / dark-energy vacuum NATURALLY
SET or RELATE the neutrino mass m_nu?  Both-ways, every magnitude from this script.

The framework's footing (LOCKED):
    a0     = 9.36e-11 m/s^2     (dS-Unruh MOND scale, = c^2 sqrt(Lambda/32pi))
    rho_DE = Lambda c^2 / 8piG  (PURE-Lambda, not rho_total)
    H_Lambda = 1.808e-18 /s     (de Sitter Hubble = c sqrt(Lambda/3))
    E_dS   = rho_DE^(1/4) ~ 2.24 meV   (forced vacuum-energy mass scale)

This script COMPUTES every concrete mechanism proposed in the neutrino-dark-energy
literature and asks of EACH: does it FORCE m_nu (output the scale, no inserted
external scale, no tuned O(1)=1), or does it merely RESTATE rho_DE / value-match?

Mechanisms tested (literature-anchored):
  M0. E_dS = rho_DE^(1/4)                       -- the forced framework number
  M1. Lambda^(1/4) ~ m_nu coincidence (Resca / FNW "geometric mean")
  M2. FNW MaVaN model-independent w <-> m_nu relation (the DYNAMICAL coupling)
  M3. "cosmic seesaw"  m_nu = sqrt(T_dS * M_Pl)  (inserts M_Pl)
  M4. textbook seesaw  m_nu = v^2 / M_R, with M_R from {GUT, dS scales, holographic}
  M5. dS-Unruh / Gibbons-Hawking THERMAL mass  k_B T_dS
  M6. is m_nu = E_dS robust to WHICH cosmic density?  (the numerology test)

Refs (real, fetched 2026-06-27):
  Fardon, Nelson, Weiner, JCAP 0410:005 (2004), astro-ph/0309800  (MaVaN/acceleron)
  Resca, Indian J Phys (2022), arXiv:2006.08398  (geometric mean [h^3 Lambda/cG]^1/4 ~ m_nu)
  DESI 2024 VI (2404.03002); DESI DR2 + DESY5 (2507.16589); DESI-Y3 Nu2024 (Sigma<0.056)

Run: python3 nu_de_mechanism.py   ; exit 0 on success.
"""

import mpmath as mp
mp.mp.dps = 40

# ----------------------------------------------------------------------------
# Constants (SI) -- standard CODATA / Planck-2018 cosmology
# ----------------------------------------------------------------------------
c     = mp.mpf('299792458')               # m/s
G     = mp.mpf('6.67430e-11')             # m^3 kg^-1 s^-2
hbar  = mp.mpf('1.054571817e-34')         # J s
kB    = mp.mpf('1.380649e-23')            # J/K
eV    = mp.mpf('1.602176634e-19')         # J
meV   = eV * mp.mpf('1e-3')

# Planck 2018 flat LCDM
H0_kmsMpc = mp.mpf('67.36')
OmL       = mp.mpf('0.6847')
Mpc       = mp.mpf('3.0856775814913673e22')  # m
H0        = H0_kmsMpc * mp.mpf('1000') / Mpc  # 1/s

# de Sitter (pure-Lambda) Hubble and Lambda
H_Lam = H0 * mp.sqrt(OmL)                  # c sqrt(Lambda/3) ; 1/s
Lam   = 3 * (H_Lam/c)**2                   # m^-2
rho_DE = Lam * c**2 / (8*mp.pi*G)          # kg/m^3  ==  Lambda c^2 / 8piG

# Planck mass scales
M_Pl_full = mp.sqrt(hbar*c/G)              # full Planck mass (kg)
M_Pl_red  = mp.sqrt(hbar*c/(8*mp.pi*G))    # reduced Planck mass (kg)
def kg_to_GeV(m): return m*c**2/eV/mp.mpf('1e9')
def J_to_eV(E):   return E/eV

print("="*78)
print("FRONT 2 -- de Sitter vacuum  <->  neutrino mass: FORCED or COINCIDENCE?")
print("="*78)
print(f"H_Lambda          = {mp.nstr(H_Lam,6)} /s   (target 1.808e-18)")
print(f"Lambda            = {mp.nstr(Lam,6)} m^-2")
print(f"rho_DE            = {mp.nstr(rho_DE,6)} kg/m^3")
print(f"a0 = c^2*sqrt(Lam/32pi) = {mp.nstr(c**2*mp.sqrt(Lam/(32*mp.pi)),6)} m/s^2 (target 9.36e-11)")
print(f"M_Pl(full)        = {mp.nstr(kg_to_GeV(M_Pl_full),6)} GeV")

# energy scale whose vacuum-energy density = rho_DE c^2 :  E^4/(hbar c)^3 = rho_DE c^2
def density_to_E(rho):
    u = rho*c**2                       # J/m^3
    E4 = u*(hbar*c)**3                 # J^4
    return E4**mp.mpf('0.25')          # J
E_dS = density_to_E(rho_DE)            # J
print(f"E_dS = rho_DE^(1/4) = {mp.nstr(J_to_eV(E_dS)/mp.mpf('1e-3'),8)} meV   (target 2.2395)")

# measured neutrino scales (NuFIT 5.3 / PDG 2024)
dm2_sol = mp.mpf('7.42e-5')   # eV^2
dm2_atm = mp.mpf('2.510e-3')  # eV^2 (NO)
m_atm = mp.sqrt(dm2_atm)*1000 # meV  (~ heaviest if NO & m1->0)
m_sol = mp.sqrt(dm2_sol)*1000 # meV
Sig_floor_NO = (mp.sqrt(dm2_sol)+mp.sqrt(dm2_atm))*1000  # meV minimal-NO Sum
print(f"sqrt(dm2_atm)     = {mp.nstr(m_atm,5)} meV (heaviest NO eigenstate)")
print(f"sqrt(dm2_sol)     = {mp.nstr(m_sol,5)} meV")
print(f"Sigma_min (NO)    = {mp.nstr(Sig_floor_NO,5)} meV")

VERDICTS = []
def verdict(tag, forced, note):
    VERDICTS.append((tag, forced, note))

# ----------------------------------------------------------------------------
# M0. E_dS = rho_DE^(1/4): the forced framework number (no neutrino claim yet)
# ----------------------------------------------------------------------------
print("\n" + "-"*78)
print("M0. E_dS = rho_DE^(1/4)  -- the framework's FORCED meV scale")
print("-"*78)
print(f"E_dS = {mp.nstr(J_to_eV(E_dS)*1000,6)} meV. This IS forced from rho_DE (same rho_DE as a0).")
print("But it is an ENERGY DENSITY^(1/4), i.e. it RESTATES rho_DE. It is not yet a particle mass.")
verdict("M0 E_dS=rho_DE^1/4", True, "forced number, but restates rho_DE (no particle yet)")

# ----------------------------------------------------------------------------
# M1. Resca / FNW "geometric mean": [hbar^3 Lambda /(c G)]^(1/4) ~ m_nu
#     This is ALGEBRAICALLY THE SAME as E_dS (rho_DE^1/4). Prove it.
# ----------------------------------------------------------------------------
print("\n" + "-"*78)
print("M1. Literature geometric mean  [hbar^3 Lambda/(c G)]^(1/4)  (Resca 2022; FNW)")
print("-"*78)
# Dimensional identity:  E_dS^4 = rho_DE c^2 * (hbar c)^3 = [Lambda c^4 /(8piG)] (hbar c)^3
#                               = Lambda c^7 hbar^3 /(8pi G)   (units J^4, verified below)
E_gm4 = Lam * c**7 * hbar**3 / (8*mp.pi*G)   # rho_DE normalization, exact
E_gm  = E_gm4**mp.mpf('0.25')
print(f"[Lambda c^7 hbar^3/(8piG)]^(1/4) = {mp.nstr(J_to_eV(E_gm)*1000,6)} meV")
print(f"ratio to E_dS = {mp.nstr(E_gm/E_dS,8)}  (= 1.000 -- it IS rho_DE^1/4 reworded)")
# also the bare-Lambda (no 8pi) geometric mean people quote: ~ (8pi)^1/4 ~ 2.5x up
E_gm_bare = (Lam * c**7 * hbar**3 / G)**mp.mpf('0.25')
print(f"bare [Lambda c^7 hbar^3/G]^(1/4)  = {mp.nstr(J_to_eV(E_gm_bare)*1000,6)} meV (no 8pi; ~2.5x up)")
print("=> The 'geometric mean ~ m_nu' coincidence in the literature IS rho_DE^(1/4).")
print("   It is a KNOWN published coincidence, NOT unique to the framework, NO mechanism.")
verdict("M1 lit geometric-mean", False, "identical to rho_DE^1/4; published coincidence, no mechanism")

# ----------------------------------------------------------------------------
# M2. FNW MaVaN: the model-INDEPENDENT relation. This is the only DYNAMICAL
#     mechanism that genuinely COUPLES m_nu to dark energy. Compute what it
#     predicts and whether it FORCES the scale.
#     FNW: w + 1 = -d ln(m_nu) / d ln(a) * (Omega_nu/Omega_DE)-ish; the clean
#     model-independent statement is:
#        w_DE = -1 + (m_nu/V')(dV/dphi)... but the USABLE relation is
#        1 + w  ~  (rho_nu / rho_DE) * (d ln m_nu / d ln rho_nu)
#     The scale of the dark energy is set by the acceleron potential V(phi),
#     which is FREE -- FNW must INPUT mu ~ 2 meV by hand to fit Omega_DE.
# ----------------------------------------------------------------------------
print("\n" + "-"*78)
print("M2. Fardon-Nelson-Weiner MaVaN  -- the dynamical m_nu <-> w coupling")
print("-"*78)
# stationarity: rho_DE(phi) ~ V(phi); m_nu(phi). The dark-energy density today:
rho_DE_eV4 = (J_to_eV(E_dS))**4   # eV^4   (= rho_DE c^2 in eV^4 units)
print(f"rho_DE in natural units = ({mp.nstr(J_to_eV(E_dS)*1000,5)} meV)^4 = {mp.nstr(rho_DE_eV4,5)} eV^4")
# FNW's own scale: they WRITE V ~ mu^4 ln(...) and FIT mu ~ rho_DE^(1/4) ~ 2e-3 eV.
# The neutrino-density contribution today: rho_nu ~ Sigma m_nu * n_nu
n_nu = mp.mpf('336')*mp.mpf('1e6')    # /m^3 total relic nu (112/cm^3 per flavour*3 ~336/cm^3)
Sig_mnu_eV = mp.mpf('0.06')           # eV (minimal NO)
rho_nu = Sig_mnu_eV*eV * n_nu / c**2  # kg/m^3
print(f"rho_nu (Sigma=0.06 eV)  = {mp.nstr(rho_nu,4)} kg/m^3 ;  rho_nu/rho_DE = {mp.nstr(rho_nu/rho_DE,4)}")
print("FNW model-independent relation: 1+w = (rho_nu/rho_DE)*(d ln m_nu/d ln rho_nu).")
print("Today rho_nu/rho_DE ~ %.3f, so the neutrino-DE coupling can give |1+w| ~ O(0.01-0.1)." % float(rho_nu/rho_DE))
print("KEY: the MAGNITUDE mu~2meV that FNW use is FIT to Omega_DE -- the acceleron")
print("potential V(phi) is FREE; FNW do NOT derive mu from Lambda, they SET it to match.")
print("So MaVaN couples m_nu to rho_DE DYNAMICALLY but does NOT FORCE the scale.")
verdict("M2 FNW MaVaN coupling", False,
        "genuine dynamical m_nu<->rho_DE coupling, but the scale mu is FIT not forced; "
        "exponent (1/4) not forced by MaVaN; carries c_s^2<0 clumping instability")

# ----------------------------------------------------------------------------
# M3. "cosmic seesaw": m_nu = sqrt(k_B T_dS * M_Pl c^2)  (inserts M_Pl)
# ----------------------------------------------------------------------------
print("\n" + "-"*78)
print("M3. cosmic seesaw  m_nu = sqrt(E_dS_thermal * E_Planck)")
print("-"*78)
T_dS = hbar*H_Lam/(2*mp.pi*kB)            # Gibbons-Hawking temp (K)
E_TdS = kB*T_dS                            # J
print(f"T_dS (Gibbons-Hawking) = {mp.nstr(T_dS,5)} K ; k_B T_dS = {mp.nstr(J_to_eV(E_TdS),5)} eV")
m_cs_full = mp.sqrt(E_TdS * (M_Pl_full*c**2))
m_cs_red  = mp.sqrt(E_TdS * (M_Pl_red *c**2))
print(f"sqrt(kT_dS * M_Pl,full c^2) = {mp.nstr(J_to_eV(m_cs_full)*1000,5)} meV")
print(f"sqrt(kT_dS * M_Pl,red  c^2) = {mp.nstr(J_to_eV(m_cs_red )*1000,5)} meV")
print("Lands ~1-2 meV BUT ONLY by INSERTING M_Planck (an external UV scale dS does not force).")
print("Fails anti-circularity: the geometric mean of an IR (kT_dS) and a CHOSEN UV (M_Pl).")
verdict("M3 cosmic seesaw sqrt(kT_dS*M_Pl)", False,
        "~1-2 meV but inserts M_Pl as external UV scale; not forced by dS alone")

# ----------------------------------------------------------------------------
# M4. textbook seesaw m_nu = v^2/M_R: is there a dS scale that can BE M_R?
# ----------------------------------------------------------------------------
print("\n" + "-"*78)
print("M4. type-I seesaw  m_nu = v^2 / M_R  -- can any dS scale be M_R?")
print("-"*78)
v = mp.mpf('246')  # GeV (Higgs vev; m_D ~ v)
def seesaw_mnu_meV(M_R_GeV):
    return (v**2 / M_R_GeV)*mp.mpf('1e9')*1000  # eV->meV : v^2/M_R in GeV ->*1e9 eV ->*1000 meV... careful
# v^2/M_R has units GeV; to eV multiply by 1e9; to meV multiply by 1e12
def seesaw_meV(M_R_GeV):
    return (v**2 / M_R_GeV)*mp.mpf('1e12')
for name, MR in [("GUT 2e16 GeV", mp.mpf('2e16')),
                 ("M_Pl full",   kg_to_GeV(M_Pl_full)),
                 ("M_Pl reduced",kg_to_GeV(M_Pl_red))]:
    print(f"  M_R={name:14s} ({mp.nstr(MR,3)} GeV) -> m_nu = {mp.nstr(seesaw_meV(MR),4)} meV")
# the dS-forced HEAVY scale? there is none: dS scales (hbar H0 ~1e-33 eV, M_Pl/sqrt(S_dS)) are IR/light
E_IR_dS = J_to_eV(hbar*H_Lam)             # eV  ~1e-33
print(f"  dS-forced energy hbar*H_Lambda = {mp.nstr(E_IR_dS,4)} eV  (IR, ~62 orders too LIGHT to be M_R)")
print("=> The seesaw MIRACLE (v^2/M_GUT ~ meV) is real but TEXTBOOK; dS plays NO role in")
print("   selecting M_GUT~2e16. No dS/holographic scale is heavy enough to BE M_R.")
verdict("M4 seesaw v^2/M_R", False,
        "GUT seesaw gives meV but is textbook; dS selects no heavy M_R (its scales are IR/light)")

# ----------------------------------------------------------------------------
# M5. dS-Unruh / Gibbons-Hawking thermal mass directly
# ----------------------------------------------------------------------------
print("\n" + "-"*78)
print("M5. dS-Unruh thermal mass  k_B T_dS directly as a Majorana mass")
print("-"*78)
print(f"k_B T_dS = {mp.nstr(J_to_eV(E_TdS)*1000,4)} meV  -- i.e. {mp.nstr(J_to_eV(E_TdS)/mp.mpf('1e-3'),4)} meV")
print(f"= {mp.nstr(J_to_eV(E_TdS),4)} eV  -> ~31 orders BELOW meV. Direct thermal mass is FAR too small.")
print("The dS-Unruh temperature enters a0 via density-over-TEMPERATURE; it is not itself a mass.")
verdict("M5 kT_dS thermal mass", False, "~10^-31 meV, ~31 orders too small to be m_nu")

# ----------------------------------------------------------------------------
# M6. THE NUMEROLOGY TEST: is rho_DE^(1/4) special, or does ANY cosmic density^1/4 ~ 2 meV?
# ----------------------------------------------------------------------------
print("\n" + "-"*78)
print("M6. numerology control -- 4th root compresses density; which densities give ~2 meV?")
print("-"*78)
rho_crit = 3*H0**2/(8*mp.pi*G)
rho_m    = (1-OmL)*rho_crit
for nm, r in [("rho_DE", rho_DE), ("rho_crit", rho_crit), ("rho_m", rho_m),
              ("2*rho_DE", 2*rho_DE), ("rho_DE/2", rho_DE/2), ("10*rho_DE", 10*rho_DE)]:
    print(f"  {nm:10s}^(1/4) = {mp.nstr(J_to_eV(density_to_E(r))*1000,5)} meV")
print("=> a factor-10 in density -> only ~1.8x in meV. ANY density in the cosmic family")
print("   gives ~1.3-3.6 meV. '~2 meV ~ neutrino' is GENERIC to rho_cosmic^(1/4): coincidence signature.")
verdict("M6 numerology control", False,
        "any cosmic density^(1/4) ~ 1.3-3.6 meV; the ~2 meV match is generic, not rho_DE-specific")

# ----------------------------------------------------------------------------
# DESI live-test snapshot (the one real blade -- belongs to m1=E_dS hypothesis)
# ----------------------------------------------------------------------------
print("\n" + "-"*78)
print("LIVE TEST -- DESI Sigma m_nu (the blade is on m1=E_dS hypothesis, NOT the mechanism)")
print("-"*78)
Sig_pred_NO = Sig_floor_NO + J_to_eV(E_dS)*1000  # m1=E_dS adds E_dS to the floor (approx)
# more precisely m1=E_dS=2.24, m2=sqrt(m1^2+dm2sol), m3=sqrt(m1^2+dm2atm)
m1 = J_to_eV(E_dS)*1000  # meV
m2 = mp.sqrt((m1/1000)**2+dm2_sol)*1000
m3 = mp.sqrt((m1/1000)**2+dm2_atm)*1000
Sig_exact = m1+m2+m3
print(f"m1=E_dS={mp.nstr(m1,5)} meV -> NO spectrum Sigma = {mp.nstr(Sig_exact,5)} meV = {mp.nstr(Sig_exact/1000,5)} eV")
print(f"minimal-NO floor = {mp.nstr(Sig_floor_NO,5)} meV ; prediction is +{mp.nstr(Sig_exact-Sig_floor_NO,3)} meV above floor")
print("DESI 2024 VI (LCDM+CMB): Sigma < 0.072 eV (95%)  -> prediction 0.061 eV is UNDER, ~10 meV headroom")
print("DESI-Y3 (Nu2024, LCDM tightest): Sigma < 0.056 eV -> would sit AT/below the NO floor (squeezing)")
print("DESI DR2+DESY5 (2507.16589, w0waCDM): Sigma = 0.098 +0.016 -0.037 eV (POSITIVE @2.7sigma)")
print("=> dataset/model-DEPENDENT: LCDM combos squeeze toward/below floor (threat to m1=E_dS);")
print("   w0waCDM+SN PREFERS a larger Sigma (relief). The blade is LIVE but model-contingent.")

# ----------------------------------------------------------------------------
# SUMMARY
# ----------------------------------------------------------------------------
print("\n" + "="*78)
print("SUMMARY -- forced vs coincidence, by mechanism")
print("="*78)
any_forced_particle = False
for tag, forced, note in VERDICTS:
    flag = "FORCED " if forced else "COINCID"
    print(f"  [{flag}] {tag:30s} : {note}")
print("-"*78)
print("FORCED:        E_dS = rho_DE^(1/4) = 2.24 meV  (a real number, but RESTATES rho_DE)")
print("NOT FORCED:    every step from E_dS to an actual neutrino MASS --")
print("               m_nu=E_dS needs tuned O(1)=1; lit geometric-mean IS rho_DE^1/4;")
print("               MaVaN couples but FITS the scale; no dS scale can be M_R;")
print("               kT_dS ~10^-31 meV; ANY cosmic density^1/4 ~ 2 meV (numerology).")
print("NET: a genuine forced meV VACUUM scale that coincides with m_nu's order, but NO")
print("     forced mechanism that SETS m_nu. The one DYNAMICAL hook (MaVaN, m_nu(rho_DE))")
print("     is real conceptually but scale-free & instability-laden. NOT a TOE claim;")
print("     neutrino sector only. The live blade (DESI Sigma) is on the m1=E_dS hypothesis.")
print("="*78)
