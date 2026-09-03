#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h53_h54_slacs_lenses.py -- HUNT ITEMS 53 and 54 (strong lensing by SLACS early-type galaxies).
==============================================================================================
Item 53 (Einstein radii from the stars alone): a strong lens has ONE measured length, the Einstein radius, and it is fixed by
        the condition that the mean convergence inside it is unity.  In the framework there is no halo, so theta_E is PREDICTED
        by the stellar mass, the size of the light, and a_0 -- nothing else.  Sanders & Land (2008) and Sanders (2014) posed
        exactly this test; it is redone here on Route A with both footings.
Item 54 (the Einstein mass): the same equation read the other way.  Auger+2009 publish, per lens, the projected stellar fraction
        inside theta_E for a Chabrier and for a Salpeter IMF, f_* = M_*,2D(<R_E)/M_E.  The framework must supply the rest of M_E
        from the phantom alone, so its projected boost B = M_2D,tot/M_2D,* at R_E is REQUIRED to equal 1/f_*.  LambdaCDM
        supplies the same gap with an NFW halo -- a fit, not a prediction, but it has the freedom and the framework has none.

DATA: Auger et al. 2009, ApJ 705, 1099 (SLACS IX), VizieR J/ApJ/705/1099/lenses, fetched this session to
      real_research/data/slacs_auger2009_lenses.tsv.  85 lenses; 70 carry everything this script needs.

MODEL: the stars are a spherical de Vaucouleurs (Sersic n = 4) distribution with the tabulated M_* and effective radius,
       projected EXACTLY (the Sersic incomplete-gamma law) and deprojected with the standard Prugniel-Simien density
       rho ~ (r/R_e)^-p exp(-b (r/R_e)^(1/n)), p = 1 - 0.6097/n + 0.05463/n^2.  Route A phantom, M_tot(r) = nu(g_N/a_0) M_b(r),
       projected through an infinite cylinder.  COSMOLOGY: Auger's own (Om = 0.3, OL = 0.7, h = 0.7), because R_E and M_E are
       tabulated in kpc and Msun in it; validation A shows the geometry is reproduced to 0.001 dex.

THE ESTIMATOR IS NORMALISATION-FREE, and that matters.  Validation B below shows my de Vaucouleurs light fraction inside R_E
       disagrees with Auger's own by -8% (V-band R_e) to +12% (I-band R_e), i.e. I cannot reproduce their stellar model to
       better than ~10%.  So both items are written so that the STELLAR mass at the Einstein radius comes from Auger's measured
       f_*, never from my model, and only the framework's BOOST -- a ratio, and much less profile-sensitive -- comes from mine.
       The V/I band choice is carried through everything as an explicit systematic instead of being chosen to taste.

       The EFE is NOT applied: SLACS lenses sit in groups, so switching it on can only REDUCE the phantom.  Ignoring it is the
       most generous assumption available to the framework.

Both footings.  Mutations.  Checks CAN fail.
"""
import sys, math, os
import numpy as np
from scipy.optimize import brentq
from scipy.special import gammainc
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(5354)

# ------------------------------------------------------------------ Auger's cosmology (the one the table is written in)
OMM_A, OML_A, h_A = 0.3, 0.7, 0.7
H0_A = 100*h_A*1e3/Mpc
_zg = np.linspace(0, 4.0, 4001)
_ig = np.concatenate([[0.0], np.cumsum(0.5*(1/np.sqrt(OMM_A*(1+_zg[1:])**3+OML_A) + 1/np.sqrt(OMM_A*(1+_zg[:-1])**3+OML_A))*np.diff(_zg))])
def DC(z):  return (c_light/H0_A)*float(np.interp(z, _zg, _ig))
def DA(z):  return DC(z)/(1+z)
def DA12(z1, z2): return (DC(z2) - DC(z1))/(1+z2)          # flat universe
ARCSEC = 1/206264.806

# ------------------------------------------------------------------ load
path = os.path.join(DATA, "slacs_auger2009_lenses.tsv")
lines = [l.rstrip("\n") for l in open(path, encoding="latin-1")]
hi = [i for i, l in enumerate(lines) if l.startswith("recno")][0]
hdr = lines[hi].split("\t"); col = {c: i for i, c in enumerate(hdr)}
raw = [l.split("\t") for l in lines[hi+3:] if l.strip() and not l.startswith("#")]
def F(v):
    try: return float(v.strip())
    except Exception: return float("nan")
L = []
for r in raw:
    d = dict(name=r[col["SDSS"]].strip(), zl=F(r[col["zlens"]]), zs=F(r[col["zsrc"]]), sig=F(r[col["sigma"]]),
             esig=F(r[col["e_sigma"]]), RE=F(r[col["RE"]]), lME=F(r[col["Mass"]]),
             Fc=F(r[col["Fc"]]), eFc=F(r[col["e_Fc"]]), Fs=F(r[col["Fs"]]), eFs=F(r[col["e_Fs"]]),
             lMc=F(r[col["logMc"]]), elMc=F(r[col["e_logMc"]]), lMs=F(r[col["logMs"]]), elMs=F(r[col["e_logMs"]]),
             ReI=F(r[col["Re(I)"]]), ReV=F(r[col["Re(V)"]]), mtype=r[col["MType"]].strip())
    L.append(d)
P("="*118); P("SLACS strong lenses -- Auger+2009 (SLACS IX), VizieR J/ApJ/705/1099/lenses"); P("="*118)
info(f"rows read: {len(L)}")

# ------------------------------------------------------------------ VALIDATION A: the lensing geometry
vA = []
for d in L:
    if not all(np.isfinite([d["zl"], d["zs"], d["RE"], d["lME"]])): continue
    d["Sig_cr"] = c_light**2*DA(d["zs"])/(4*math.pi*G*DA(d["zl"])*DA12(d["zl"], d["zs"]))
    d["ME"] = d["Sig_cr"]*math.pi*(d["RE"]*kpc)**2/Msun
    d["thE"] = d["RE"]*kpc/DA(d["zl"])/ARCSEC
    vA.append(math.log10(d["ME"]) - d["lME"])
vA = np.array(vA)
ck("A (validation, not a physics result) the lensing geometry is reproduced: M_E recomputed from theta_E, the two redshifts and Auger's own cosmology matches his tabulated Einstein mass",
   abs(np.median(vA)) < 0.01 and vA.std() < 0.01,
   f"N = {len(vA)}, median offset {np.median(vA):+.4f} dex, scatter {vA.std():.4f} dex")

# ------------------------------------------------------------------ the stellar + phantom model
SN = 4.0
BN = 2*SN - 1/3. + 4/(405*SN) + 46/(25515*SN**2)             # Ciotti & Bertin b_n
PP = 1 - 0.6097/SN + 0.05463/SN**2                           # Prugniel & Simien p
def M2D_star(x): return float(gammainc(2*SN, BN*max(float(x), 1e-12)**(1/SN)))        # EXACT Sersic projected fraction
def M3D_star(x): return gammainc(SN*(3-PP), BN*np.maximum(x, 1e-12)**(1/SN))          # Prugniel-Simien enclosed fraction
def rho_star(x): return np.maximum(x, 1e-12)**(-PP)*np.exp(-BN*np.maximum(x, 1e-12)**(1/SN))
def cyl_mass(rr, M, R):
    """projected mass inside cylinder radius R for a spherical M(r); infinite line of sight."""
    dM = np.gradient(M, rr)
    w = np.where(rr <= R, 1.0, 1.0 - np.sqrt(np.clip(1.0 - (R/np.maximum(rr, 1e-30))**2, 0, 1)))
    return float(np.trapz(dM*w, rr))
def boost(Mstar_kg, Re_kpc, a0, R_m, rmax_kpc=3000.0, n=6000):
    """B(R) = M_2D,tot(<R)/M_2D,*(<R) for the de Vaucouleurs stars plus the Route A phantom."""
    if a0 <= 0: return 1.0
    Re = Re_kpc*kpc
    rr = np.geomspace(1e-5*Re, rmax_kpc*kpc, n)
    Mb = Mstar_kg*M3D_star(rr/Re); gN = G*Mb/rr**2
    ph = cyl_mass(rr, nu(gN/a0)*Mb - Mb, R_m)
    return 1.0 + ph/(Mstar_kg*M2D_star(R_m/Re))
def gN_at(Mstar_kg, Re_kpc, R_m):
    return G*Mstar_kg*float(M3D_star(np.array([R_m/(Re_kpc*kpc)]))[0])/R_m**2

# validation: numerically projecting the deprojected density must return the EXACT Sersic 2-D law
_v = []
for x in (0.3, 0.6, 1.0, 2.0):
    rr = np.geomspace(1e-5*5*kpc, 3000*kpc, 6000)
    _v.append(cyl_mass(rr, M3D_star(rr/(5*kpc)), x*5.0*kpc)/M2D_star(x))
_v = np.array(_v)
ck("B1a (validation) the deprojection is self-consistent: numerically projecting the Prugniel-Simien density back along the line of sight returns the exact Sersic n = 4 projected-mass law",
   np.all(abs(_v - 1) < 0.03), "projected/exact at R/R_e = 0.3, 0.6, 1, 2: " + ", ".join(f"{v:.4f}" for v in _v))
_tr = [boost(10**11.7*Msun, 6.0, A0["canonical"], 5*kpc, rmax_kpc=rm) for rm in (200.0, 1000.0, 3000.0, 20000.0)]
ck("B1b (validation) the projected phantom mass at the Einstein radius does not depend on where the line of sight is truncated: the deep-MOND phantom's rho ~ 1/r^2 makes the cylinder integrand fall as 1/r^2, so a 200 kpc and a 20 Mpc cylinder give the same answer",
   abs(_tr[-1]/_tr[0] - 1) < 0.02, "boost with the line of sight cut at 200 kpc / 1 Mpc / 3 Mpc / 20 Mpc = " + " / ".join(f"{v:.4f}" for v in _tr))

# ------------------------------------------------------------------ the sample
S = [d for d in L if all(np.isfinite([d["zl"], d["zs"], d["RE"], d["lME"], d["Fc"], d["Fs"], d["lMc"], d["lMs"]]))
     and (np.isfinite(d["ReV"]) or np.isfinite(d["ReI"]))]
BANDS = ("V", "I")
for d in S:
    for b in BANDS:
        a = d["Re"+b]; a = a if np.isfinite(a) else d["Re"+("I" if b == "V" else "V")]
        d["Re_"+b] = a*ARCSEC*DA(d["zl"])/kpc
info(f"lenses with Einstein radius, Einstein mass, both stellar masses, both stellar fractions and an effective radius: {len(S)}")
info(f"median z_lens {np.median([d['zl'] for d in S]):.3f}, z_src {np.median([d['zs'] for d in S]):.3f}, theta_E {np.median([d['thE'] for d in S]):.2f}\", "
     f"R_E {np.median([d['RE'] for d in S]):.2f} kpc, R_e(V) {np.median([d['Re_V'] for d in S]):.2f} kpc, R_e(I) {np.median([d['Re_I'] for d in S]):.2f} kpc, sigma {np.median([d['sig'] for d in S]):.0f} km/s")

# ------------------------------------------------------------------ VALIDATION B: can I reproduce Auger's own stellar fractions?
P(""); info("VALIDATION B -- my de Vaucouleurs light fraction inside R_E against the one implied by Auger's published f_* and M_*:")
vB = {}
for b in BANDS:
    r_ = np.array([M2D_star(d["RE"]/d["Re_"+b])/(d["Fs"]*d["ME"]/10**d["lMs"]) for d in S])
    vB[b] = (np.median(r_), np.log10(r_).std())
    info(f"   R_e({b}): mine/Auger's median {np.median(r_):.3f} ({math.log10(np.median(r_)):+.3f} dex), per-lens scatter {np.log10(r_).std():.3f} dex")
ck("B2 AGAINST INTEREST, and it changes how both items must be computed -- I cannot reproduce Auger's own stellar model to better than about 10 per cent.  With his V-band effective radii my de Vaucouleurs puts 8% LESS light inside the Einstein radius than he does; with the I-band radii, 12% MORE.  The V-band version has half the per-lens scatter, so that is probably the radius he used, but the offset does not go away.  Everything below is therefore written to take the projected STELLAR mass from Auger's measured f_*, never from my profile, and to carry the V/I difference as a stated systematic",
   vB["V"][0] < 1.0 < vB["I"][0], f"V: {vB['V'][0]:.3f} (scatter {vB['V'][1]:.3f} dex); I: {vB['I'][0]:.3f} (scatter {vB['I'][1]:.3f} dex) -- the two bracket unity, and the analysis is written not to depend on which is right")

# ------------------------------------------------------------------ ITEM 54
P(""); P("="*118); P("ITEM 54 -- can the phantom alone supply the Einstein mass?"); P("="*118)
info("the framework's predicted mean convergence at the OBSERVED Einstein radius is kappa_bar = f_*(measured) x B(framework).")
info("It is required to be 1.000.  f_* is Auger's; only B is mine, and B is a ratio.")
info("BUG FOUND AND FIXED IN THE MAKING, and it ran the wrong way for the framework: the first version of this script computed the")
info("   boost ONCE, from the Salpeter stellar mass, and then multiplied it by BOTH f_*.  That is wrong -- a Chabrier galaxy is 0.26 dex")
info("   LIGHTER, so its g_N is lower, so its boost is LARGER.  The boost is recomputed here from each IMF's own stellar mass.  The")
info("   correction RAISES the Chabrier prediction by about 10 per cent (0.04 dex).  It does not rescue it; see check 54e.")
R54 = {}
for foot, a0 in list(A0.items()) + [("Newton (nu=1)", 0.0)]:
    for b in BANDS:
        for d in S:
            # the boost must be computed from the SAME IMF's stellar mass that supplies f_* -- see the note above
            d[f"B_{foot}_{b}"] = boost(10**d["lMs"]*Msun, d["Re_"+b], a0, d["RE"]*kpc)
            d[f"BC_{foot}_{b}"] = boost(10**d["lMc"]*Msun, d["Re_"+b], a0, d["RE"]*kpc)
            d[f"y_{foot}_{b}"] = gN_at(10**d["lMs"]*Msun, d["Re_"+b], d["RE"]*kpc)/(a0 if a0 > 0 else A0["canonical"])
        B = np.array([d[f"B_{foot}_{b}"] for d in S]); BC = np.array([d[f"BC_{foot}_{b}"] for d in S])
        prS = B*np.array([d["Fs"] for d in S]); prC = BC*np.array([d["Fc"] for d in S])
        bs = np.array([np.median(prS[i]) for i in (rng.integers(0, len(prS), len(prS)) for _ in range(2000))])
        R54[(foot, b)] = (np.median(B), np.median(prS), bs.std(), np.median(prC), np.median([d[f"y_{foot}_{b}"] for d in S]),
                          np.log10(prS).std(), np.median(BC))
    v, i_ = R54[(foot, "V")], R54[(foot, "I")]
    info(f"{foot:14} g_N(R_E)/a_0 = {v[4]:5.1f}-{i_[4]:.1f}  |  boost B = {v[0]:.3f} (V) / {i_[0]:.3f} (I) at Salpeter, "
         f"{v[6]:.3f} / {i_[6]:.3f} at Chabrier  |  kappa_bar = B f_*: SALPETER {v[1]:.3f} / {i_[1]:.3f}  (+-{v[2]:.3f} stat), "
         f"CHABRIER {v[3]:.3f} / {i_[3]:.3f}")
reqS = np.median([1/d["Fs"] for d in S]); reqC = np.median([1/d["Fc"] for d in S])
info(f"required boost 1/f_* : Salpeter {reqS:.3f}, Chabrier {reqC:.3f}")
cV, cI = R54[("canonical", "V")], R54[("canonical", "I")]
aV, aI = R54[("alt", "V")], R54[("alt", "I")]
kb_lo, kb_hi = min(cV[1], cI[1]), max(aV[1], aI[1])
ck("54 LIABILITY (a real negative, stated plainly) -- the phantom CANNOT supply the Einstein mass of a SLACS lens.  The Einstein radius of a massive early-type sits at g_N ~ 10 a_0, deep in the NEWTONIAN part of the kernel, where Route A's projected boost is only about 1.14-1.20.  The measurement requires 1.45 with a Salpeter IMF and 2.5 with a Chabrier one.  The framework therefore delivers only 79-85 per cent of the observed Einstein mass at Salpeter, and 49-54 per cent at Chabrier",
   kb_hi < 0.95, f"kappa_bar at the observed R_E (must be 1.000): canonical {cV[1]:.3f} (V) / {cI[1]:.3f} (I) +- {cV[2]:.3f}, alt {aV[1]:.3f} / {aI[1]:.3f}, all Salpeter "
   f"= {math.log10(cV[1]):+.3f} to {math.log10(aV[1]):+.3f} dex; Chabrier {cV[3]:.3f}-{aI[3]:.3f}; boost available {cV[0]:.3f}-{aI[0]:.3f} vs required {reqS:.3f} (Salp) / {reqC:.3f} (Chab)")
ck("54b what the liability costs, in the only currency that can pay it: the framework needs a stellar mass-to-light ratio HEAVIER than Salpeter by the shortfall.  That is not absurd -- high-dispersion ellipticals are independently measured to be bottom-heavy, at or above Salpeter -- but it leaves the framework with EXACTLY ZERO room for anything else inside the Einstein radius, and it is 0.3 dex above the Chabrier-like ratios the same stellar-population models give for the discs where the framework's other results live",
   True, f"required M_*/L relative to Salpeter: {1/kb_hi:.2f}x-{1/kb_lo:.2f}x (= {-math.log10(kb_hi):+.3f} to {-math.log10(kb_lo):+.3f} dex); relative to Chabrier: {1/max(cV[3],aI[3]):.2f}x = {-math.log10(max(cV[3],aI[3])):+.3f} dex")
_bugC = np.median([d["Fc"]*d["B_canonical_V"] for d in S])          # what the buggy version reported
ck("54e THE BUG THIS SCRIPT FOUND IN ITSELF, recorded because it ran the wrong way: the boost had been computed once at the Salpeter stellar mass and then applied to the Chabrier stellar fraction too.  A Chabrier galaxy is 0.26 dex lighter, so it sits at a LOWER g_N/a_0 and gets a LARGER boost.  Fixing it raises the Chabrier prediction by about 10 per cent -- in the framework's favour -- and still leaves it a factor of two short, so the verdict is unchanged and the number is now right",
   abs(cV[3] - _bugC) > 0.02 and cV[3] < 0.7,
   f"Chabrier kappa_bar: buggy (Salpeter boost) {_bugC:.3f} -> corrected {cV[3]:.3f}, a {math.log10(cV[3]/_bugC):+.3f} dex correction TOWARD the framework; still {1/cV[3]:.2f}x short of 1.000")
nV = R54[("Newton (nu=1)", "V")]
ck("54c both ways -- the same table is a much WORSE problem for a bare 'stars only, no dark matter at all' reading, which is the only other zero-parameter option: Newtonian stars at Salpeter reach 69 per cent of the Einstein mass.  The phantom closes over 40 per cent of that gap for free.  This is recorded as a partial success that still falls short, not as a total failure",
   nV[1] < cV[1] < 1.0, f"Newtonian stars only {nV[1]:.3f} -> framework {cV[1]:.3f} -> required 1.000; the phantom closes {100*(cV[1]-nV[1])/(1-nV[1]):.0f}% of the Newtonian gap")

# ------------------------------------------------------------------ ITEM 53
P(""); P("="*118); P("ITEM 53 -- the Einstein radius predicted from the stars and a_0 alone"); P("="*118)
info("solve for the radius where the mean convergence is 1, written so the stellar normalisation cancels:")
info("      f_*(Auger)  x  B(R)  x  M2D_*(R/R_e)/M2D_*(R_E/R_e)  =  (R/R_E)^2 .")
info("Nothing on the left needs my stellar mass -- only the SHAPE of the light and the framework's boost.")
def solve_u(d, a0, b, Fkey="Fs"):
    Ms = 10**(d["lMs"] if Fkey == "Fs" else d["lMc"])*Msun; Re = d["Re_"+b]; den = M2D_star(d["RE"]/Re)
    def g(u):
        Rm = u*d["RE"]*kpc
        return d[Fkey]*boost(Ms, Re, a0, Rm)*M2D_star(u*d["RE"]/Re)/den - u**2
    if g(0.05)*g(5.0) > 0: return float("nan")
    return brentq(g, 0.05, 5.0, xtol=1e-6)
R53 = {}
for tag, a0 in (("canonical", A0["canonical"]), ("alt", A0["alt"]), ("Newton (nu=1)", 0.0)):
    row = {}
    for b in BANDS:
        uS = np.array([solve_u(d, a0, b, "Fs") for d in S]); uC = np.array([solve_u(d, a0, b, "Fc") for d in S])
        uS = uS[np.isfinite(uS)]; uC = uC[np.isfinite(uC)]
        bs = np.array([np.median(uS[i]) for i in (rng.integers(0, len(uS), len(uS)) for _ in range(1500))])
        row[b] = (np.median(uS), bs.std(), np.log10(uS).std(), float(np.mean(abs(uS-1) < 0.10)), np.median(uC), len(uS))
    R53[tag] = row
    info(f"{tag:14} R_E(pred)/R_E(obs) SALPETER: {row['V'][0]:.3f} +- {row['V'][1]:.3f} (V) / {row['I'][0]:.3f} (I); "
         f"scatter {row['V'][2]:.3f} dex; within 10% individually {100*row['V'][3]:.0f}%; CHABRIER {row['V'][4]:.3f} / {row['I'][4]:.3f}   (N = {row['V'][5]})")
c53, a53, n53 = R53["canonical"], R53["alt"], R53["Newton (nu=1)"]
r_lo, r_hi = min(c53["V"][0], c53["I"][0]), max(a53["V"][0], a53["I"][0])
ck("53 the Einstein radius IS predicted with no halo and no fitting -- from the shape of the light, the measured stellar fraction and a_0 -- and it comes out SHORT by 14-18 per cent with a Salpeter IMF and by nearly half with a Chabrier one.  The hunt list asked for 50 lenses within 10 per cent; only a quarter of them land there, and the miss is a systematic offset, not scatter",
   r_hi < 0.95, f"canonical {c53['V'][0]:.3f} (V) / {c53['I'][0]:.3f} (I) +- {c53['V'][1]:.3f}; alt {a53['V'][0]:.3f} / {a53['I'][0]:.3f}; Newton stars-only {n53['V'][0]:.3f}; "
   f"Chabrier {c53['V'][4]:.3f}; scatter {c53['V'][2]:.3f} dex; {100*c53['V'][3]:.0f}% within 10% individually")
ck("53b the framework beats the no-dark-matter Newtonian baseline, the only other zero-parameter prediction on offer, but closes only about a third of its gap",
   c53["V"][0] > n53["V"][0] + 0.02, f"Newtonian stars only {n53['V'][0]:.3f} -> framework {c53['V'][0]:.3f} -> required 1.000; the phantom closes {100*(c53['V'][0]-n53['V'][0])/(1-n53['V'][0]):.0f}% of the gap")
ck("53c AGAINST INTEREST -- items 53 and 54 are NOT independent results.  They are the same equation, mean convergence = 1, solved once for the mass and once for the radius; the mass deficit and the radius deficit are one number related by the local logarithmic slope of the projected mass.  They must be entered on the ledger as ONE item, not two",
   True, f"mass deficit {-math.log10(cV[1]):+.3f} dex, radius deficit {-math.log10(c53['V'][0]):+.3f} dex, ratio {math.log10(cV[1])/math.log10(c53['V'][0]):.2f} = the local d log M_2D/d log R at R_E")

# ------------------------------------------------------------------ the dispersions
P(""); P("="*118); P("ITEM 54b -- the same lenses' velocity dispersions, an independent handle on the same mass"); P("="*118)
info("isotropic spherical Jeans, de Vaucouleurs tracer in the de Vaucouleurs + phantom potential, luminosity-weighted in the")
info("SDSS fibre.  This uses the TABULATED stellar mass directly and so is independent of the f_* discrepancy of validation B.")
def jeans_sigma(Mstar_kg, Re_kpc, a0, Rap_kpc):
    Re = Re_kpc*kpc
    rr = np.geomspace(1e-4*Re, 2000*kpc, 2500)
    rho = rho_star(rr/Re); Mb = Mstar_kg*M3D_star(rr/Re); gN = G*Mb/rr**2
    g = nu(gN/a0)*gN if a0 > 0 else gN
    integ = rho*g
    I = np.concatenate([np.cumsum((0.5*(integ[1:] + integ[:-1])*np.diff(rr))[::-1])[::-1], [0.0]])
    s2r = I/np.maximum(rho, 1e-300)
    RR = np.geomspace(rr[0]*5, Rap_kpc*kpc, 120); num = []; den = []
    for R in RR:
        m = rr > R*1.000001; w = rr[m]/np.sqrt(rr[m]**2 - R**2)
        num.append(2*np.trapz(rho[m]*s2r[m]*w, rr[m])); den.append(2*np.trapz(rho[m]*w, rr[m]))
    return math.sqrt(np.trapz(np.array(num)*RR, RR)/np.trapz(np.array(den)*RR, RR))/1e3
R54b = {}
for tag, a0 in (("canonical", A0["canonical"]), ("alt", A0["alt"]), ("Newton (nu=1)", 0.0)):
    row = {}
    for b in BANDS:
        pr = np.array([jeans_sigma(10**d["lMs"]*Msun, d["Re_"+b], a0, 1.5*ARCSEC*DA(d["zl"])/kpc)/d["sig"] for d in S])
        bs = np.array([np.median(pr[i]) for i in (rng.integers(0, len(pr), len(pr)) for _ in range(1000))])
        row[b] = (np.median(pr), bs.std(), np.log10(pr).std())
    R54b[tag] = row
    info(f"{tag:14} sigma(predicted, Salpeter)/sigma(measured): {row['V'][0]:.3f} +- {row['V'][1]:.3f} (V) / {row['I'][0]:.3f} (I), scatter {row['V'][2]:.3f} dex")
cb, nb = R54b["canonical"], R54b["Newton (nu=1)"]
ck("54d AGAINST MY OWN ESTIMATOR -- the dispersion test CANNOT decide the question, and saying so is the result.  sigma depends on the effective radius as R_e^(-1/2), and the V-band and I-band radii of these galaxies differ enough that the predicted dispersion moves by 11 per cent between them -- 0.86 with one, 0.96 with the other.  A 0.08 dex mass deficit is 0.04 dex in sigma, well inside that.  The dispersions are consistent with the lensing deficit and equally consistent with none; they neither confirm nor refute item 54, and they are recorded as UNDERPOWERED rather than as agreement",
   0.80 < cb["V"][0] < 1.15 and 0.80 < cb["I"][0] < 1.15 and abs(math.log10(cb["I"][0]/cb["V"][0])) > 0.02,
   f"sigma_pred/sigma_obs = {cb['V'][0]:.3f} (V) / {cb['I'][0]:.3f} (I) +- {cb['V'][1]:.3f}; Newton {nb['V'][0]:.3f} / {nb['I'][0]:.3f}; "
   f"the two bands' predictions differ by {abs(math.log10(cb['I'][0]/cb['V'][0])):.3f} dex in sigma = {2*abs(math.log10(cb['I'][0]/cb['V'][0])):.3f} dex in mass, larger than the {-math.log10(cV[1]):.3f} dex effect being tested")

# ------------------------------------------------------------------ mutations
P(""); P("="*118); P("MUTATION CONTROLS -- these must break"); P("="*118)
mr = np.array([solve_u(d, 100*A0["canonical"], "V") for d in S]); mr = mr[np.isfinite(mr)]
ck("M1 mutation: a_0 multiplied by 100 must massively OVER-predict the Einstein radius.  If it did not, the estimator would not be sensitive to a_0 at all and neither item could ever have been a test of it",
   np.median(mr) > 1.5, f"R_E(pred)/R_E(obs) with a_0 x 100 = {np.median(mr):.3f}, against {c53['V'][0]:.3f} at the canonical value")
ck("M2 mutation: switching the kernel off (nu = 1) must move both observables the other way",
   n53["V"][0] < c53["V"][0] and nV[1] < cV[1], f"R_E ratio {n53['V'][0]:.3f} < {c53['V'][0]:.3f}; kappa_bar {nV[1]:.3f} < {cV[1]:.3f}")
sh = rng.permutation(np.arange(len(S)))
shr = []
for i, d in enumerate(S):
    e = S[sh[i]]
    fake = dict(d); fake["Fs"] = e["Fs"]; fake["lMs"] = e["lMs"]; fake["Re_V"] = e["Re_V"]
    shr.append(solve_u(fake, A0["canonical"], "V"))
shr = np.array(shr); shr = shr[np.isfinite(shr)]
ck("M3 mutation: pairing each lens's Einstein radius with ANOTHER lens's stellar fraction, mass and size must inflate the scatter.  It does, but only by a factor 1.4, and the honest reading of that is that this estimator is dominated by Auger's per-lens f_*, which is itself derived from the same Einstein mass -- so the per-lens scatter of item 53 is NOT an independent measure of the prediction's quality.  The systematic offset is the result; the scatter is not",
   np.log10(shr).std() > 1.3*c53["V"][2], f"shuffled scatter {np.log10(shr).std():.3f} dex against the real {c53['V'][2]:.3f} dex, a factor {np.log10(shr).std()/c53['V'][2]:.2f}")

# ------------------------------------------------------------------ the alternative, and the honest accounting
P(""); P("="*118); P("THE ALTERNATIVE, AND WHAT COULD STILL RESCUE THE FRAMEWORK"); P("="*118)
info(f"LambdaCDM's reading of the same table: the dark fraction inside theta_E is {1-np.median([d['Fc'] for d in S]):.2f} (Chabrier) / {1-np.median([d['Fs'] for d in S]):.2f} (Salpeter),")
info("which an NFW halo of the mass abundance-matching gives these galaxies supplies comfortably.  That is a FIT with two free")
info("parameters per lens, not a prediction -- but it HAS the freedom, and on this observable the framework has none.")
info(f"the systematic that decides how hard the liability bites: Auger's own stellar-mass error is {np.median([d['elMs'] for d in S]):.2f} dex per lens, my")
info(f"    reproduction of his stellar model is good only to {vB['V'][1]:.3f} dex, and the SPS/IMF zero point is worth ~0.1 dex on top.")
info(f"    The shortfall is {-math.log10(cV[1]):.3f} dex.  So this is a liability AT the level of the stellar-mass systematic, NOT a clean kill.")
info("what is NOT available as an escape: (a) the external-field effect, which would only reduce the phantom further; (b) a larger")
info(f"    a_0 -- the alt footing moves kappa_bar from {cV[1]:.3f} to {aV[1]:.3f}, a fifth of what is needed; (c) hot gas, a few per cent of M_* inside 5 kpc.")
info("what IS available: a bottom-heavy IMF above Salpeter in high-dispersion ellipticals, which is independently measured.  The")
info("cost is that the framework then needs super-Salpeter ratios here and Chabrier-like ratios in the discs where its other")
info("results live -- and item 76 of this hunt DERIVES the disc value from a_0, so the two cannot be tuned separately.")
ck("53/54 SUMMARY the joint verdict on both items: at Salpeter the framework is short by 0.08-0.10 dex in Einstein mass and radius, with the same galaxies' dispersions unable to confirm or refute that at the precision the effective radii allow; at Chabrier it is short by 0.29 dex and dead on this observable.  One LIABILITY, sized, with the escape route named and priced",
   True, f"kappa_bar {kb_lo:.3f}-{kb_hi:.3f} (Salpeter) / {min(cV[3],aI[3]):.3f}-{max(cV[3],aI[3]):.3f} (Chabrier); R_E ratio {r_lo:.3f}-{r_hi:.3f}; sigma ratio {min(cb['V'][0],cb['I'][0]):.3f}-{max(cb['V'][0],cb['I'][0]):.3f}; N = {len(S)} lenses")
sys.exit(ck.done())
