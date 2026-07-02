#!/usr/bin/env python3
"""
LANE L2 -- Cluster gravitational-redshift discriminator for the Zimmerman framework.
=====================================================================================
Observable: stacked velocity offset Delta = c*<z_gal - z_BCG> of cluster members
relative to the BCG. Gravitational part: Delta_grav(R) = [Phi(r_BCG) - <Phi(r)>_LOS]/c < 0
(members sit higher in the well than the BCG -> net BLUEshift).

Published detections (potential-term scale ~ -10 km/s):
  W11 : Wojtak, Hansen & Hjorth 2011, Nature 477, 567 (arXiv:1109.6571)
        Delta = -7.7 +/- 3.0 km/s integrated within R < 6 Mpc, 7800 GMBCG clusters,
        bins at R = 0.6, 1.6, 3.3, 5.2 Mpc; mean mass ~ 2e14 Msun (richness 16).
        Their TeVeS(-with-80%-Newtonian-mass) profile rejected at 95% CL (shape).
  S15 : Sadeh, Feng & Lahav 2015, PRL 114, 071103 (arXiv:1410.5262)
        Delta = -11 (+7/-5) km/s (SDSS+BOSS; includes Kaiser-2013 kinematic terms).
  J15 : Jimeno+ 2015, MNRAS 448, 1999: GMBCG + redMaPPer detections, ~ -10 km/s scale,
        Kaiser-2013 effects included.
  R23 : Rosselli+ 2023, A&A 669, A29 (arXiv:2206.05313)
        Delta = -11.4 +/- 3.3 km/s, 3058 SDSS clusters z<0.5; GR/DGP consistent,
        strong-field f(R) marginally disfavored.
  Kaiser 2013, MNRAS 435, 1278 (arXiv:1303.3663): transverse-Doppler (+), light-cone,
        SB-modulation terms, few km/s; SHARED by all gravity readings below when
        anchored to the same observed kinematics (they depend on velocities, not on
        which potential produced them) -> they CANCEL in the discriminator.
  Bekenstein & Sanders 2012 (arXiv:1110.5048): rebuttal to W11's TeVeS curve --
        finite MONDian isothermal spheres + residual matter can refit the redshifts.

READINGS COMPUTED (all on the framework's own terms first, rule #1):
 (1) GR + DM halo          : photons & galaxies feel Phi_NFW(M200_total). Standard.
 (2) Framework, AeST/ghost-condensate realization (banked eta(R500)~2.33: the
     residual matter IS there as the condensate): the metric potential is the
     dynamically calibrated one == (1) by construction. Prediction: GR-like.
 (3) PURE-MI, NO extra matter, worldline reading: modified INERTIA changes the
     worldline response of slowly-accelerating massive bodies; photons are null and
     propagate on the metric sourced (via ordinary GR) by the BARYONS ALONE.
     -> grav-z = baryon-only potential (gas f_gas*NFW-like + BCG Hernquist spike).
 (4) MG-MOND (AQUAL/phantom-potential comparator): photons feel the MOND-boosted
     potential from baryons alone. Framework interpolation g=sqrt(gb^2+gb*a0)
     [nu(y)=sqrt(1+1/y)] PRIMARY; Milgrom 'simple' nu as named comparator;
     a0 = 9.36e-11 canonical and 1.13e-10 footing fork (rule 4).

Anchor-free core test: readings (1),(2) are CALIBRATED to the same kinematics the
measurements come from, so data/GR ~= 1; reading (3) is then f_b(Phi) * that.
Exit 0. No fetched data needed; masses/baryon budget from cited literature.
"""
import numpy as np

G   = 6.674e-11          # m^3 kg^-1 s^-2
c   = 2.998e8            # m/s
Msun= 1.989e30           # kg
Mpc = 3.0857e22          # m
kpc = Mpc/1e3
rho_cr = 9.20e-27        # kg/m^3 (h=0.70, z=0; stack z~0.2 raises rho_cr ~ few 10%,
                         #  absorbed in the mass bracket below)

A0_CANON = 9.36e-11      # framework canonical a0 = c^2 sqrt(Lambda/32pi) = cH_L/Z
A0_FORK  = 1.13e-10      # rho_total/cH0 footing fork (rule 4)

# ---------- cluster model ------------------------------------------------------
def nfw_pars(M200, c200):
    r200 = (3*M200/(4*np.pi*200*rho_cr))**(1/3)
    rs   = r200/c200
    mc   = np.log(1+c200) - c200/(1+c200)
    Ms   = M200/mc                      # 4 pi rho_s rs^3
    return r200, rs, Ms

def M_nfw(r, rs, Ms):
    x = r/rs
    return Ms*(np.log(1+x) - x/(1+x))

def M_hernquist(r, Mb, a):
    return Mb*r**2/(r+a)**2

# baryon budget (clusters, M200 ~ 2-5e14):
FGAS  = 0.125            # gas fraction (Chiu+18/Eckert+19 scale; within r500, extended)
FSTAR = 0.015            # satellite stars
FB    = FGAS + FSTAR     # 0.14  (cosmic = 0.157 used as upper bracket)
M_BCG = 1.0e12*Msun      # BCG stellar mass
A_BCG = 30*kpc           # Hernquist scale

def g_profiles(M200, c200, fb, a0, r):
    """returns dict of g(r) [m/s^2] for each reading."""
    r200, rs, Ms = nfw_pars(M200, c200)
    Mtot = M_nfw(r, rs, Ms)
    # baryons: fb * NFW (generous: gas actually shallower -> smaller |Delta|_baryon)
    Mbar = fb*M_nfw(r, rs, Ms) + M_hernquist(r, M_BCG, A_BCG)
    g_tot = G*Mtot/r**2
    g_bar = G*Mbar/r**2
    # framework's OWN interpolation: g_dyn = sqrt(g_bar^2 + g_bar*a0)
    g_mi  = np.sqrt(g_bar**2 + g_bar*a0)
    # Milgrom 'simple' nu comparator: nu = 1/2 + sqrt(1/4 + 1/y)
    y = g_bar/a0
    g_simple = g_bar*(0.5 + np.sqrt(0.25 + 1.0/y))
    return dict(GR_DM=g_tot, BARYON=g_bar, MOND_FW=g_mi, MOND_SIMPLE=g_simple,
                r200=r200)

def phi_from_g(r, g):
    """Phi(r) - Phi(0) = int_0^r g dr'  (finite; observable never needs Phi(inf))."""
    dphi = np.concatenate([[0.0], np.cumsum(0.5*(g[1:]+g[:-1])*np.diff(r))])
    return dphi   # = Phi(r)-Phi(0) >= 0

# ---------- projection: galaxy-weighted LOS average ----------------------------
def delta_profile(r, dphi, rs, Ms, R_arr, rmax):
    """Delta_grav(R) = -<dphi(r)>_LOS / c  [km/s]; galaxies trace NFW rho, r<rmax."""
    out = []
    for R in R_arr:
        zz = np.linspace(0, np.sqrt(max(rmax**2 - R**2, 0)), 4000)[1:]
        rr = np.sqrt(R**2 + zz**2)
        x  = rr/rs
        rho = 1.0/(x*(1+x)**2)                      # NFW galaxy tracer
        w   = rho
        dp  = np.interp(rr, r, dphi)
        out.append(-np.sum(w*dp)/np.sum(w)/c/1e3)   # km/s
    return np.array(out)

def integrated_delta(r, dphi, rs, Ms, Rmax):
    """count-weighted mean of Delta(R) over aperture R<Rmax (weight 2piR Sigma(R))."""
    R_arr = np.linspace(0.03*Mpc, Rmax, 60)
    d = delta_profile(r, dphi, rs, Ms, R_arr, Rmax)
    # projected counts weight
    Sig = []
    for R in R_arr:
        zz = np.linspace(0, np.sqrt(Rmax**2 - R**2), 2000)[1:]
        rr = np.sqrt(R**2+zz**2); x = rr/rs
        Sig.append(np.sum(1.0/(x*(1+x)**2)))
    w = np.array(Sig)*R_arr
    return np.sum(w*d)/np.sum(w)

# ---------- run ---------------------------------------------------------------
BINS_W11 = np.array([0.6, 1.6, 3.3, 5.2])*Mpc     # Wojtak Fig.2 bin centres
APERTURE = 6.0*Mpc
r = np.logspace(np.log10(1*kpc), np.log10(10*Mpc), 6000)

MEAS = [  # (label, value km/s, +err, -err, note)
    ("W11  Wojtak+2011  (R<6 Mpc)",  -7.7, 3.0, 3.0, "grav-z only modelled (pre-Kaiser)"),
    ("S15  Sadeh+2015",             -11.0, 7.0, 5.0, "Kaiser terms modelled"),
    ("R23  Rosselli+2023",          -11.4, 3.3, 3.3, "Kaiser terms modelled"),
]

print("="*100)
print("L2: CLUSTER GRAVITATIONAL-REDSHIFT DISCRIMINATOR")
print(f"baryon budget: f_gas={FGAS}, f_star={FSTAR}, f_b={FB} (+BCG 1e12 Msun Hernquist)")
print("="*100)

results = {}
for M200_msun, c200, tag in [(2e14, 5.0, "M200=2e14 (W11 mean mass)"),
                             (4e14, 5.0, "M200=4e14 (count-weighted bracket)")]:
    M200 = M200_msun*Msun
    for a0, a0tag in [(A0_CANON, "a0=9.36e-11 canonical"), (A0_FORK, "a0=1.13e-10 fork")]:
        gp = g_profiles(M200, c200, FB, a0, r)
        r200, rs, Ms = nfw_pars(M200, c200)
        print(f"\n--- {tag}   r200={r200/Mpc:.2f} Mpc   [{a0tag}] ---")
        print(f"{'reading':<28}{'0.6':>8}{'1.6':>8}{'3.3':>8}{'5.2 Mpc':>9}{'  <R<6Mpc>':>11}")
        for key, label in [("GR_DM",      "(1) GR+DM  == (2) AeST/cond."),
                           ("BARYON",     "(3) pure-MI baryon-only"),
                           ("MOND_FW",    "(4a) MG-MOND framework nu"),
                           ("MOND_SIMPLE","(4b) MG-MOND simple nu")]:
            if key in ("GR_DM","BARYON") and a0 is A0_FORK:
                pass  # a0-independent; still print for alignment on canonical only
            dphi = phi_from_g(r, gp[key])
            prof = delta_profile(r, dphi, rs, Ms, BINS_W11, APERTURE)
            intg = integrated_delta(r, dphi, rs, Ms, APERTURE)
            results[(tag,a0tag,key)] = (prof, intg)
            print(f"{label:<28}" + "".join(f"{v:8.2f}" for v in prof) + f"{'':1}{intg:10.2f}")

# eta sanity tie-in: MOND-from-baryons vs GR+DM acceleration at ~r500 (0.66 r200)
gp = g_profiles(2e14*Msun, 5.0, FB, A0_CANON, r)
r200 = gp["r200"]; i500 = np.argmin(np.abs(r - 0.66*r200))
eta_g = gp["GR_DM"][i500]/gp["MOND_FW"][i500]
print(f"\nsanity: g_GR/g_MOND-from-baryons at ~r500 = {eta_g:.2f}"
      f"  (banked cluster residual eta(R500)~2.33 in mass; same 'MOND misses ~2x' regime)")

# ---------- confrontation ------------------------------------------------------
print("\n" + "="*100)
print("CONFRONTATION (anchor-free ratio test: GR+DM is calibrated to the same")
print("kinematics -> use measured value as the (1)/(2) prediction; reading (3) is")
print("then the baryon-potential fraction of it; Kaiser kinematic terms SHARED, cancel)")
print("="*100)
# baryon potential fraction (bracket over mass + aperture systematics):
fr = []
for tag in ["M200=2e14 (W11 mean mass)","M200=4e14 (count-weighted bracket)"]:
    b = results[(tag,"a0=9.36e-11 canonical","BARYON")][1]
    g = results[(tag,"a0=9.36e-11 canonical","GR_DM")][1]
    fr.append(b/g)
frac_lo, frac_hi = min(fr), max(fr)
print(f"baryon-only / GR+DM potential-signal fraction: {frac_lo:.3f} - {frac_hi:.3f}")
print(f"(pure f_b={FB} without the BCG spike would give {FB:.3f}; cosmic-f_b upper "
      f"bracket 0.157 + spike -> ~{frac_hi+0.017:.2f})")

print(f"\n{'measurement':<32}{'measured':>12}{'(3) baryon-only pred':>22}{'tension':>10}")
for lab, val, ep, em, note in MEAS:
    pred = val*np.mean(fr)            # scale measured GR-consistent signal by fraction
    # conservative: use model prediction directly too
    pred_model = np.mean([results[(t,"a0=9.36e-11 canonical","BARYON")][1]
                          for t in ["M200=2e14 (W11 mean mass)",
                                    "M200=4e14 (count-weighted bracket)"]])
    err = ep if val < pred_model else em
    sig = (pred_model - val)/err
    print(f"{lab:<32}{val:>7.1f} km/s {pred_model:>14.2f} km/s {sig:>8.1f} sigma  ({note})")

# reading (4) tensions vs the two well-errored integrated measurements
print("\nreading (4) MG-MOND-from-baryons (framework nu, both a0 footings) vs data:")
for lab, val, ep, em, note in [MEAS[0], MEAS[2]]:
    for a0tag in ["a0=9.36e-11 canonical", "a0=1.13e-10 fork"]:
        preds = [results[(t,a0tag,"MOND_FW")][1]
                 for t in ["M200=2e14 (W11 mean mass)","M200=4e14 (count-weighted bracket)"]]
        p = np.mean(preds)
        sig = (p - val)/(ep if val < p else em)
        print(f"  {lab:<30} [{a0tag:>22}]  pred {p:6.2f} km/s   {sig:4.1f} sigma")

print("""
NOTES ON READING (4) MG-MOND-no-extra-matter: g_MOND-from-baryons(r) crosses ABOVE
g_GR+DM only beyond ~2.5-3 Mpc (log-growing phantom potential), so within the 6 Mpc
aperture the cumulative potential signal stays ~40-50% BELOW GR+DM: too-little
blueshift, ~1-2 sigma per measurement (see table above) -- disfavored, NOT killed.
CAUTION: W11's famous 95%-CL TeVeS rejection is a DIFFERENT reading -- they gave
TeVeS 80% of the NEWTONIAN dynamical mass (matter included), which matches inner
dynamics and then log-DIVERGES -> too-MUCH blueshift at large R. Bekenstein &
Sanders 2012 rebut with finite MONDian isothermal models + residual matter, i.e.
they rescue MOND by ADDING the matter -> collapses into reading (2). Either way the
no-extra-matter corner is squeezed from both directions.""")
print("exit 0")
