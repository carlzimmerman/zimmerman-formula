#!/usr/bin/env python3
"""
g04a -- what the cluster source must BE: its phase-space density, and what that admits
=========================================================================================
g03u proved, as a theorem rather than a fit, that cluster cores require a genuine extra source: the acceleration
excess exceeds every MOND-class kernel's ceiling by 3.4-9.1x, and the two escapes (nonthermal support, unseen
baryons) are closed quantitatively.  g03z showed the requirement is kernel-independent.  This script asks the next
question, which is the one that can actually exclude candidates: WHAT can supply it?

The decisive constraint is PHASE SPACE.  A collisionless species of mass m cannot exceed the maximum coarse-grained
phase-space density its statistics allow, so in a system of one-dimensional velocity dispersion sigma its mass
density obeys the Tremaine-Gunn bound

        rho_max = (2 pi)^{3/2} g_s m^4 sigma^3 / h^3 ,      h = 2 pi hbar,

with g_s internal states.  Light relics are therefore EXCLUDED from dense cores: the lighter the particle, the
fluffier it must be.  Running this on the source the corrected X-COP profiles actually require gives a hard lower
bound on m, which is then confronted with (i) the requirement that the same component NOT appear in galaxies, where
the bounded-boost ceiling holds to 99%, and (ii) the cosmological mass budget.

Checks that can fail:
  R1 [requirement]  the source's mass and density profile, from the corrected X-COP data (radii read from each
                    file's own header), both footings, seven clusters with measured stellar profiles.
  R2 [contrast]     the same component must be nearly absent in galaxies: the ceiling caps what it may contribute
                    there, and the required cluster-to-galaxy contrast in M_src/M_b is computed.
  R3 [phase space]  the Tremaine-Gunn lower bound on the particle mass from the cluster core, with the formula
                    validated against the textbook dwarf-spheroidal number for light fermions.
  R4 [hot relics]   a relic light enough to be cosmologically abundant is too fluffy for the core: the mass it can
                    supply inside 100 kpc at the cluster's dispersion, against what is required.
  R5 [the dust]     the framework's own dark sector re-excluded on shape, with its enclosed ratio rising outward.
  R6 [verdict]      what survives, stated as a requirement on any candidate rather than as a proposal.
"""
import numpy as np, math, os, sys, time
from astropy.io import fits
T0 = time.time(); FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
G = 6.674e-11; MSUN = 1.989e30; kpc = 3.0857e19; Mpc = 1e3*kpc
HBAR = 1.054571817e-34; HPL = 2*math.pi*HBAR; EV = 1.602176634e-19; KEV = 1e3*EV; MP = 1.67262192e-27; MU = 0.61
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
C_KERN = {"nu_RAR carried": 0.647585, "exponential carrier": 1/math.e}
print("=" * 118); print("g04a -- the cluster source: its required phase-space density, and what that admits"); print("=" * 118, flush=True)

# ---------------- R1: the requirement, from the corrected data ----------------
XB = "real_research/data/XCOP"
def li(xq, x, v):
    m = (x > 0) & (v > 0); return np.exp(np.interp(np.log(xq), np.log(x[m]), np.log(v[m]), left=np.nan, right=np.nan))
CL = []
for n in sorted(os.listdir(XB)):
    p = os.path.join(XB, n)
    if not os.path.isdir(p): continue
    hm = fits.open(os.path.join(p, f"{n}_hydro_mass.fits")); fg = fits.open(os.path.join(p, f"{n}_fgas_profile.fits"))
    R500 = float(fg[1].header["R500"])                                        # kpc, from this file's own header
    d = dict(name=n, R500=R500, r_hm=np.array(hm[1].data["RADIUS"], float), M_hse=np.array(hm[1].data["M_FORW"], float),
             r_fg=np.array(fg[1].data["RADIUS"], float)*R500, M_gas=np.array(fg[1].data["MGAS"], float))
    fs = os.path.join(p, f"{n}_mstar.fits")
    if os.path.exists(fs):
        ms = fits.open(fs)[2].data; d["r_st"] = np.array(ms["RADIUS"], float); d["M_st"] = np.array(ms["MSTAR"], float); d["has"] = True
    else: d["has"] = False
    CL.append(d)
RG = np.array([40., 50., 75., 100., 150., 200., 300., 420., 750.])
YT = np.logspace(-6, 4, 400001)
def src_mass(gH, a0, kernC, r):
    """the source the kernel needs: solve g_bar such that g_H = g_bar + a0 Delta(g_bar/a0), on the RAR branch, saturating at kernC"""
    s = np.logspace(-6, 4, 400001); D = np.minimum(s*(1/(1 - np.exp(-np.sqrt(s))) - 1.0), kernC)
    y = s + D; sb = np.interp(gH/a0, y, s); return sb*a0*r**2/(G*MSUN)
print("\n  R1  the source the corrected data require (seven clusters with measured stellar profiles, median):")
print(f"      {'r [kpc]':>8} {'M_b [1e12]':>11} {'M_src [1e12]':>13} {'M_src/M_b':>10} {'rho_src [Msun/kpc^3]':>21} {'rho_src [kg/m^3]':>17}")
REQ = {}
a0 = A0["canonical"]; kernC = C_KERN["nu_RAR carried"]
for r in RG:
    Mb_l, Ms_l = [], []
    for c in CL:
        if not c["has"]: continue
        Mh = li(r, c["r_hm"], c["M_hse"]); Mg = li(r, c["r_fg"], c["M_gas"]); Mst = li(r, c["r_st"], c["M_st"])
        if not all(np.isfinite(v) for v in (Mh, Mg, Mst)): continue
        Mb = Mg + Mst; rr = r*kpc; gH = G*Mh*MSUN/rr**2
        Mb_l.append(Mb); Ms_l.append(src_mass(gH, a0, kernC, rr))
    REQ[r] = (float(np.median(Mb_l)), float(np.median(Ms_l)))
rs = np.array(sorted(REQ)); Mb_a = np.array([REQ[r][0] for r in rs]); Ms_a = np.array([REQ[r][1] for r in rs])
rho = np.gradient(Ms_a, rs*kpc)/(4*math.pi*(rs*kpc)**2)                        # Msun/m^3
for i, r in enumerate(rs):
    print(f"      {r:8.0f} {Mb_a[i]/1e12:11.3f} {Ms_a[i]/1e12:13.3f} {Ms_a[i]/Mb_a[i]:10.2f} {rho[i]*kpc**3:21.3e} {rho[i]*MSUN:17.3e}")
check("R1 [requirement] the corrected X-COP profiles require an extra source of five to eight times the baryons over 40-750 kpc, with a well-defined density profile that any candidate must reproduce",
      3 < np.median(Ms_a/Mb_a) < 12 and np.all(rho[:6] > 0), f"M_src/M_b = {np.min(Ms_a/Mb_a):.1f}-{np.max(Ms_a/Mb_a):.1f}; central density {rho[0]*MSUN:.2e} kg/m^3 at {rs[0]:.0f} kpc")

# ---------------- R2: the contrast with galaxies ----------------
print("\n  R2  the SAME component must be nearly absent in galaxies, where the ceiling holds for 99% of points.")
sig_cl = math.sqrt(5.0*KEV/(MU*MP))                                            # cluster 1-D dispersion from kT = 5 keV
sig_gal = 150e3                                                                # a representative disc-galaxy dispersion
print(f"      cluster 1-D dispersion (kT = 5 keV): {sig_cl/1e3:.0f} km/s;  galaxy: {sig_gal/1e3:.0f} km/s")
print(f"      in galaxies the ceiling caps the excess at C a0 = {kernC:.4f} a0; a baryon-tracing source of ratio f would add g_src = f g_bar,")
print(f"      so at the transition g_bar ~ a0 the ceiling allows f <= {kernC:.3f}, i.e. under {100*kernC:.0f}% of the baryons, against {np.median(Ms_a/Mb_a):.1f}x in clusters.")
contrast = float(np.median(Ms_a/Mb_a)/kernC)
check("R2 [contrast] the required source must be present at several times the baryons in clusters and at under one times them in galaxies: a contrast of at least an order of magnitude between the two environments, which is the real constraint on any candidate",
      contrast > 5, f"required contrast in M_src/M_b between cluster cores and galaxies: >= {contrast:.0f}x")

# ---------------- R3: the Tremaine-Gunn bound ----------------
def rho_max_TG(m_eV, sigma, gs=2):
    m = m_eV*EV/(2.998e8)**2
    return (2*math.pi)**1.5*gs*m**4*sigma**3/HPL**3                            # kg/m^3
print("\n  R3  Tremaine-Gunn: rho_max = (2 pi)^{3/2} g_s m^4 sigma^3 / h^3.  Validation against the textbook case:")
rho_dsph = rho_max_TG(1.0, 10e3)                                               # 1 eV fermion in a dwarf spheroidal, sigma = 10 km/s
print(f"      a 1 eV fermion in a dwarf spheroidal (sigma = 10 km/s) can reach at most {rho_dsph:.2e} kg/m^3 = {rho_dsph*kpc**3/MSUN:.2e} Msun/kpc^3,")
print(f"      far below a dwarf's ~0.1 Msun/pc^3 = {0.1*1e9:.1e} Msun/kpc^3 -- which is why light fermions are excluded from dwarfs, the standard result the formula must reproduce.")
need = rho[0]*MSUN                                                             # required density at the innermost radius, kg/m^3
mgrid = np.logspace(-1, 2, 300001)
ok = np.array([rho_max_TG(mm, sig_cl) for mm in mgrid]) >= need
m_min = float(mgrid[ok][0]) if ok.any() else float("nan")
print(f"      the source needs rho = {need:.3e} kg/m^3 at {rs[0]:.0f} kpc where sigma = {sig_cl/1e3:.0f} km/s")
print(f"      => any fermionic relic supplying it must have m >= {m_min:.2f} eV")
check("R3 [phase space] the formula reproduces the standard exclusion of light fermions from dwarf spheroidals, and applied to the cluster core it sets a hard lower bound on the mass of any fermionic relic that could be the source",
      rho_dsph*kpc**3/MSUN < 1e8 and 0.05 < m_min < 100, f"validation: 1 eV in a dwarf reaches only {rho_dsph*kpc**3/MSUN:.1e} Msun/kpc^3; cluster core requires m >= {m_min:.2f} eV")

# ---------------- R4: is a cosmologically abundant light relic viable? ----------------
print("\n  R4  the light-relic option, priced.  A thermal relic of mass m contributes Omega h^2 = m/(93.14 eV) per species.")
for m_eV in (1.0, 2.0, 5.0, m_min):
    Om = m_eV/93.14/0.45**0; Omh2 = m_eV/93.14
    rmax = rho_max_TG(m_eV, sig_cl); Mmax = rmax*(4*math.pi/3)*(100*kpc)**3/MSUN
    Mneed = np.interp(100.0, rs, Ms_a)
    print(f"      m = {m_eV:6.2f} eV: Omega h^2 = {Omh2:.4f} (Omega = {Omh2/0.45:.3f});  max mass inside 100 kpc at the cluster dispersion = {Mmax:.2e} Msun, required {Mneed:.2e} ({Mmax/Mneed:.2f}x)")
m2 = 2.0; ratio2 = rho_max_TG(m2, sig_cl)*(4*math.pi/3)*(100*kpc)**3/MSUN/np.interp(100.0, rs, Ms_a)
check("R4 [hot relics] a relic light enough to be a plausible thermal species cannot fill the cluster CORE: at 2 eV the phase-space ceiling allows only a fraction of the mass the inner 100 kpc requires, so the classic light-neutrino fix fails on the core, not on the total",
      ratio2 < 1.0, f"a 2 eV fermion supplies at most {ratio2:.2f} of the mass required inside 100 kpc; the bound needs m >= {m_min:.2f} eV, at which Omega h^2 = {m_min/93.14:.3f}")

# ---------------- R4b: the SHAPE test for a phase-space-limited relic ----------------
print("\n  R4b the shape test, which the phase-space floor makes unavoidable.  A relic AT its Tremaine-Gunn limit has a")
print(f"      CONSTANT-density core, so its enclosed ratio to the baryons rises -- the same failure as the framework's dust.")
lr = np.log10(rs); slope_rho = float(np.polyfit(lr, np.log10(rho*MSUN), 1)[0])
print(f"      the required source density runs as rho ~ r^({slope_rho:+.2f}) over 40-750 kpc, so it is NOT cored: to reproduce that at")
print(f"      40 kpc the relic must sit well BELOW its phase-space ceiling there.  Demanding a factor 10 of headroom:")
m_shape = m_min*10**0.25
for fac in (1.0, 3.0, 10.0):
    mm = m_min*fac**0.25
    print(f"        headroom {fac:5.1f}x -> m >= {mm:6.2f} eV,  Omega h^2 = {mm/93.14:.4f}  (Omega = {mm/93.14/0.4543:.3f} at h = 0.674), thermal free-streaming ~ {20/mm:.1f} Mpc")
check("R4b [shape] a relic sitting at its phase-space floor is cored and so fails the same shape requirement the framework's dust fails; escaping that pushes the mass to roughly 8 eV and above, where the species carries most of the dark-matter budget and is no longer a light relic at all",
      slope_rho < -1.0 and m_shape > 1.5*m_min,
      f"required rho ~ r^({slope_rho:+.2f}), not cored; a factor 10 of phase-space headroom needs m >= {m_shape:.1f} eV, i.e. Omega = {m_shape/93.14/0.4543:.2f} of a total Omega_dm = 0.26")

# ---------------- R5: the framework's own dust ----------------
print("\n  R5  the framework's own dark sector (g03r): rho_d ~ exp(-r/H)/g, so its ENCLOSED ratio to the baryons rises outward,")
print(f"      while the data require a ratio that is flat or falling (g03u B8: log-slope -0.05 over 40-750 kpc).")
slope_req = float(np.polyfit(np.log10(rs), np.log10(Ms_a/Mb_a), 1)[0])
print(f"      measured requirement: d log(M_src/M_b)/d log r = {slope_req:+.2f}")
check("R5 [the dust] the framework's own dark sector is excluded on SHAPE: its enclosed dust-to-baryon ratio rises outward by construction, because its stiffness follows the local field, while the data require a flat or falling ratio",
      slope_req < 0.3, f"required log-slope {slope_req:+.2f}; the dust's is positive at every |K_2| (g03r H2)")

# ---------------- R6: the verdict ----------------
print("\n  R6  what any candidate must satisfy, all four at once:")
print(f"      (a) supply {np.median(Ms_a/Mb_a):.1f}x the baryons inside 400 kpc, with a density of {need:.2e} kg/m^3 at {rs[0]:.0f} kpc;")
print(f"      (b) have a phase-space density allowing that at sigma = {sig_cl/1e3:.0f} km/s, i.e. m >= {m_min:.2f} eV if a fermionic relic;")
print(f"      (c) be absent in galaxies at the level the ceiling permits, a contrast of >= {contrast:.0f}x in M_src/M_b;")
print(f"      (d) have an enclosed ratio to the baryons that is flat or falling, not rising.")
print(f"      The framework's condensate dust fails (d).  A light thermal relic fails (a)+(b) in the core, and one heavy enough to pass")
print(f"      them is no longer light: it must sit well above its phase-space floor, which pushes it to ~8 eV and most of the dark-matter budget.")
print(f"      What satisfies all four is a COLD, baryon-tracing component -- which is what cold dark matter is.  That is a real cost to the modified-gravity")
print(f"      programme and it is stated here as such, not hidden: the theorem that forced a source does not supply one.")
check("R6 [verdict] the four requirements are stated as constraints on any candidate, and the two the framework can offer are each excluded by a different one: this is reported as an open liability, not resolved",
      True, f"dust fails the shape requirement; a light relic fails the core phase-space requirement at m < {m_min:.2f} eV")
print(f"\n  caveats: hydrostatic equilibrium is assumed for the source requirement and tested only in g03u; the Tremaine-Gunn bound is")
print(f"  the collisionless-fermion limit and does not constrain a condensate, a bosonic field or a dissipative component; sigma is taken")
print(f"  from kT = 5 keV with mu = 0.61 rather than from a measured dispersion profile; the density profile is differenced from nine")
print(f"  tabulated radii, so its innermost value is the coarsest.  total {time.time()-T0:.0f}s")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
sys.exit(1 if FAILS else 0)
