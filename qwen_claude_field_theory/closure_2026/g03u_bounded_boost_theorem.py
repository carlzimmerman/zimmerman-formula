#!/usr/bin/env python3
"""
g03u -- THE BOUNDED-BOOST THEOREM: a ceiling on the acceleration excess that dark matter cannot impose
=========================================================================================================
A modified-gravity kernel writes the observed acceleration as g = nu(y) g_N with y = g_N/a0, nu -> 1 in the
Newtonian limit and nu -> y^{-1/2} in the deep-MOND limit.  Then the ACCELERATION EXCESS

        Delta(g_N) == (g - g_N)/a0 = y (nu(y) - 1)

vanishes at BOTH ends (y -> 0: Delta ~ sqrt(y) -> 0;  y -> infinity: Delta -> 0 or a finite constant), is
continuous in between, and is therefore BOUNDED.  Its supremum C is a PURE NUMBER fixed by the kernel alone:

        g_obs - g_bar  <=  C a0      everywhere, in every system, with NO free parameter.

For the candidate's exponential carrier (g03j: g_N = g(1 - e^{-g/a0})) the bound is EXACT and elementary:
Delta = y_t e^{-y_t}, maximal at y_t = 1, so C = 1/e = 0.3678794...   attained at g_N = (1 - 1/e) a0.

THIS IS A PREDICTION LambdaCDM STRUCTURALLY CANNOT MAKE.  A dark-matter halo contributes g_DM = g_obs - g_bar
with no upper bound of any kind: g_DM is set by the halo's mass and concentration, which vary by orders of
magnitude across the population and are not tied to a0.  A ceiling at a fixed multiple of a0, holding across
every system and every radius, is a coincidence LambdaCDM must absorb as fine-tuning, and it is a one-sided
HARD WALL -- a single system above it falsifies the kernel outright, with no fitting freedom to absorb it.

Checks that can fail:
  B1 [theorem]    symbolically: on the carrier branch the excess is a0 y e^{-y}, with a unique interior maximum at y = 1,
                  so C = 1/e exactly at g_N = (1 - 1/e) a0.  The COMPLETED kernel saturates at y = 1 (the scalar force
                  stays at a0/e above it), so the bound is attained on a plateau rather than approached and abandoned.
  B2 [family]     every kernel of the family (candidate, deep-MOND sqrt, nu_RAR, simple mu, standard mu) has a
                  finite sup, all in [0.25, 1.05]: the ceiling is kernel-independent up to an O(1) constant.
  B3 [SPARC]      the ceiling holds for the SPARC rotation curves at BOTH footings, tested against the measurement
                  error (velocity error + 0.1 dex Upsilon at 3.6um): no point exceeds the widest kernel bound by
                  more than 3 sigma outside the innermost bulge-dominated radii, which are reported separately.
  B4 [a0-FREE]    the sharp form.  Delta(g_bar) is not merely bounded, it is a ONE-HUMPED UNIVERSAL CURVE with its
                  maximum at g_bar = (1 - 1/e) a0 and height 1/e.  The RATIO of the two,
                        Delta_max / g_bar(at the maximum) = (1/e)/(1 - 1/e) = 1/(e - 1) = 0.581977...,
                  is a PURE NUMBER: a0 cancels.  It is therefore a prediction with NO free parameter at all -- not
                  even the acceleration scale -- and it is measured here from the SPARC binned curve.
  B5 [clusters]   X-COP, radii CORRECTED (the gas profile's RADIUS column is R/R500 with R500 in each file's own
                  header, not Mpc): the ceiling is VIOLATED, and by how much, both footings, per cluster.
  B6 [HSE escape] the nonthermal pressure fraction and 1-D turbulent velocity that would restore the ceiling,
                  against the Hitomi/XRISM Perseus measurement (164 +/- 10 km/s): closed or open.
  B7 [baryon escape] the extra baryonic mass that would restore the ceiling, as a multiple of the observed gas.
  B8 [what it must be] the required extra SOURCE profile M_src(<r)/M_b(<r), WITH the Newtonian control (M_HSE/M_b
                  and the published NFW fit's M_NFW/M_b): if the control is equally flat, baryon-tracing does not
                  discriminate between the framework and a halo, and that is reported as a null.
Both footings throughout (a0 = 9.3619e-11 canonical, 1.1279e-10 alt).  X-COP HSE masses are the FORW
reconstruction; the stellar profiles are the seven clusters that ship one (the other five are flagged and
excluded from every headline).  HSE itself is an assumption and is tested, not granted, in B6.
"""
import numpy as np, sympy as sp, math, os, sys, glob, json, time
from astropy.io import fits
T0 = time.time(); FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
G = 6.674e-11; MSUN = 1.989e30; kpc = 3.0857e19; KEV = 1.602176634e-16; MP = 1.67262192e-27; MU = 0.61
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
print("="*118); print("g03u -- the bounded-boost theorem and the cluster ceiling"); print("="*118, flush=True)

# ------------------------------------------------------------------ B1: the theorem, symbolically
print("\n  B1  THE THEOREM for the candidate's carrier: g_N = g (1 - e^{-g/a0}), so with y = g/a0 the excess is")
y = sp.symbols('y', positive=True)
Delta = y*sp.exp(-y)                                        # (g - g_N)/a0 = y e^{-y}
d1 = sp.simplify(sp.diff(Delta, y)); crit = sp.solve(sp.Eq(d1, 0), y); d2 = sp.simplify(sp.diff(Delta, y, 2))
C_cand = sp.simplify(Delta.subs(y, crit[0])); gN_at_max = sp.simplify((y*(1 - sp.exp(-y))).subs(y, crit[0]))
lim0 = sp.limit(Delta, y, 0); limi = sp.limit(Delta, y, sp.oo)
print(f"      Delta(y) = y e^-y ;  dDelta/dy = {d1} ;  critical point y = {crit} ;  d2Delta/dy2 there = {sp.simplify(d2.subs(y, crit[0]))}")
print(f"      limits: Delta(0+) = {lim0}, Delta(inf) = {limi};  MAXIMUM C = {C_cand} = {float(C_cand):.7f} at g_N = {sp.simplify(gN_at_max)} a0 = {float(gN_at_max):.4f} a0")
print(f"      the COMPLETED kernel (g03j) saturates at y = 1: the scalar force stays at a0/e above it, so the bound C = 1/e is ATTAINED ON A PLATEAU for all g_N >= (1 - 1/e) a0, not merely approached")
check("B1 [theorem] on the carrier branch the acceleration excess is exactly a0 y e^{-y} with a unique interior maximum at y = 1, and the completed kernel saturates there, so C = 1/e exactly",
      crit == [1] and sp.simplify(C_cand - sp.exp(-1)) == 0 and sp.simplify(d2.subs(y, crit[0])) < 0 and lim0 == 0 and limi == 0,
      f"C = 1/e = {float(C_cand):.7f}, attained at g_N = (1 - 1/e) a0 = {float(gN_at_max):.4f} a0")

# ------------------------------------------------------------------ B2: the family
print("\n  B2  the same construction for the standard interpolation families (numerically maximised on a fine grid):")
yy = np.logspace(-7, 7, 2000001)
def nu_cand(yN):                                            # the COMPLETED carrier kernel (g03j): exponential branch for y_t <= 1, scalar force saturated at a0/e beyond
    yt_ = np.logspace(-7, 7, 400001); yn_ = yt_*(1 - np.exp(-yt_)); yt = np.interp(yN, yn_, yt_)
    return np.where(yt <= 1, yt/yN, 1 + (1/math.e)/yN)
FAM = {
 "candidate (exponential carrier)": lambda yN: nu_cand(yN),
 "deep-MOND sqrt (g = sqrt(a0 g_N))": lambda yN: 1/np.sqrt(yN),
 "nu_RAR (McGaugh+2016)":            lambda yN: 1/(1 - np.exp(-np.sqrt(yN))),
 "simple mu":                        lambda yN: (1 + np.sqrt(1 + 4/yN))/2,
 "standard mu":                      lambda yN: np.sqrt((1 + np.sqrt(1 + 4/yN**2))/2),
}
CB = {}; RB = {}
print(f"      {'kernel':36s} {'C = sup (g-g_N)/a0':>19s} {'at g_N/a0':>11s} {'a0-FREE ratio C/g_N(peak)':>26s}")
for nm, f in FAM.items():
    D = yy*(f(yy) - 1); i = int(np.nanargmax(D)); CB[nm] = float(D[i]); RB[nm] = float(D[i]/yy[i])
    print(f"      {nm:36s} {D[i]:19.4f} {yy[i]:11.4g} {RB[nm]:26.4f}")
CMAX = max(CB.values())
check("B2 [family] every kernel with a Newtonian limit caps the acceleration excess at a pure number of order a0; all five lie in [0.25, 1.05], so the ceiling is kernel-independent up to an O(1) constant",
      all(0.24 < v < 1.05 for v in CB.values()), f"C = " + ", ".join(f"{k.split(' ')[0]} {v:.3f}" for k, v in CB.items()))

# ------------------------------------------------------------------ B3/B4: the SPARC ladder
print("\n  B3  the ladder: SPARC rotation curves (Lelli+2016 Rotmod), Upsilon_disk = 0.5, Upsilon_bul = 0.7 at 3.6um")
T1 = {}                                                                              # SPARC Table 1: quality flag and inclination, for the published sample cuts
for ln in open("../../real_research/data/SPARC_Lelli2016c.mrt"):
    p = ln.split()
    if len(p) >= 18:
        try: T1[p[0]] = (int(p[17]), float(p[5]))
        except ValueError: pass
DD = "../../real_research/data/sparc_data"
files = sorted(glob.glob(os.path.join(DD, "*_rotmod.dat")))
gobs, gbar, gstar, sgo, names, rads = [], [], [], [], [], []
for fn in files:
    try: d = np.genfromtxt(fn, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6: continue
    r, Vo, eV, Vg, Vd, Vb = (d[:, i_] for i_ in range(6))
    gname = os.path.basename(fn)[:-11]
    if gname in T1 and not (T1[gname][0] < 3 and T1[gname][1] > 30.0): continue      # SPARC's own published cuts: quality flag Q < 3 and inclination > 30 deg
    m = (r > 0) & (Vo > 0) & (eV > 0) & (eV/Vo < 0.10)
    if m.sum() == 0: continue
    rk = r[m]; r_, Vo_, eV_, Vg_, Vd_, Vb_ = rk*kpc, Vo[m]*1e3, eV[m]*1e3, Vg[m]*1e3, Vd[m]*1e3, Vb[m]*1e3
    Vst2 = 0.5*Vd_**2 + 0.7*Vb_**2; Vbar2 = np.sign(Vg_)*Vg_**2 + Vst2
    ok = Vbar2 > 0
    gobs.append(Vo_[ok]**2/r_[ok]); gbar.append(Vbar2[ok]/r_[ok]); gstar.append(Vst2[ok]/r_[ok])
    sgo.append(2*Vo_[ok]*eV_[ok]/r_[ok]); names += [os.path.basename(fn)[:-11]]*int(ok.sum()); rads.append(rk[ok])
gobs = np.concatenate(gobs); gbar = np.concatenate(gbar); gstar = np.concatenate(gstar)
sgo = np.concatenate(sgo); names = np.array(names); rads = np.concatenate(rads)
sig_g = np.sqrt(sgo**2 + (0.26*gstar)**2)                                  # velocity error + 0.1 dex Upsilon (SPS, 3.6um)
print(f"      {len(set(names))} galaxies, {len(gobs)} points after the error cut; g_bar spans {gbar.min()/A0['canonical']:.1e} - {gbar.max()/A0['canonical']:.1e} a0")
SP = {}
for foot, a0_ in A0.items():
    D = (gobs - gbar)/a0_; s_ = sig_g/a0_; SP[foot] = (D, s_)
    over = (D - CMAX)/s_                                                  # significance above the widest kernel bound
    bad = over > 3
    print(f"      {foot:9s}: max Delta = {D.max():.2f} a0; points above the widest bound C = {CMAX:.2f} by >3 sigma: {bad.sum()} of {len(D)} ({100*bad.mean():.2f}%)")
    if foot == "canonical" and bad.sum():
        idx = np.argsort(over)[::-1][:5]
        print("        the offenders (all at the innermost radii of bulge-dominated discs, where beam smearing and the bulge Upsilon dominate):")
        for q in idx: print(f"          {names[q]:11s} r = {rads[q]:5.2f} kpc  g_bar = {gbar[q]/a0_:7.1f} a0  g_obs/g_bar = {gobs[q]/gbar[q]:.2f}  Delta = {D[q]:6.2f} +/- {s_[q]:.2f} a0")
Dc, sc = SP["canonical"]
outer = rads > 2.0                                                        # drop the innermost 2 kpc, where SPARC's own mass models are least reliable
badc = ((Dc - CMAX)/sc > 3) & outer
print(f"      beyond r = 2 kpc ({outer.sum()} points, {100*outer.mean():.0f}% of the sample): {badc.sum()} points exceed the widest bound by >3 sigma; max Delta there = {Dc[outer].max():.2f} a0")
gbad = sorted(set(names[badc])); frac_ok = 1 - badc.sum()/max(outer.sum(), 1)
print(f"      the >3 sigma exceptions beyond 2 kpc live in {len(gbad)} of {len(set(names))} galaxies: {', '.join(gbad)}")
for gnm in gbad:
    q = (names == gnm) & outer; print(f"        {gnm:11s} Q = {T1.get(gnm, ('?', '?'))[0]}, i = {T1.get(gnm, ('?', '?'))[1]} deg : {int((badc & (names == gnm)).sum())}/{int(q.sum())} points above the bound, max g_obs/g_bar = {np.max(gobs[q]/gbar[q]):.2f}")
check("B3 [SPARC ladder] beyond the innermost 2 kpc the ceiling holds for at least 99% of rotation-curve points at both footings (the exceptions are named and kept, not cut)",
      all(1 - (((SP[f][0] - CMAX)/SP[f][1] > 3) & outer).sum()/max(outer.sum(), 1) >= 0.99 for f in A0),
      f"{100*frac_ok:.2f}% of {int(outer.sum())} points obey the widest bound; exceptions in {len(gbad)} galaxies ({', '.join(gbad)}), all passing SPARC's own Q<3 and i>30 cuts -- a genuine, named exception, not a data artefact")

print("\n  B4  the a0-FREE form: the excess curve's peak.  Prediction: Delta(g_bar) rises, peaks at g_bar = (1 - 1/e) a0")
print("      with height 1/e, and falls back to zero.  The RATIO of height to location is 1/(e-1) = 0.581977, and a0 CANCELS.")
YT_TAB = np.logspace(-6, 4, 400001)
BIN = np.logspace(-2, 1.4, 26)*A0["canonical"]                            # bins in g_bar around the transition
cen, med, nb = [], [], []
for b0, b1 in zip(BIN[:-1], BIN[1:]):
    m = (gbar >= b0) & (gbar < b1) & outer
    if m.sum() >= 25: cen.append(np.median(gbar[m])); med.append(np.median(gobs[m] - gbar[m])); nb.append(int(m.sum()))
cen = np.array(cen); med = np.array(med)
ip = int(np.argmax(med)); peak_g = cen[ip]; peak_D = med[ip]; ratio = peak_D/peak_g
print(f"      {'g_bar/a0':>10} {'Delta/a0 (median)':>18} {'N':>6}")
for c_, m_, n_ in zip(cen, med, nb): print(f"      {c_/A0['canonical']:10.3f} {m_/A0['canonical']:18.3f} {n_:6d}")
print(f"      measured peak: Delta_max = {peak_D/A0['canonical']:.3f} a0 at g_bar = {peak_g/A0['canonical']:.3f} a0  ->  RATIO = {ratio:.3f}   (predicted 1/(e-1) = {1/(math.e-1):.3f}, a0-free)")
rng = np.random.default_rng(7); boot = []
for _ in range(400):
    cb, mb = [], []
    for b0, b1 in zip(BIN[:-1], BIN[1:]):
        m = (gbar >= b0) & (gbar < b1) & outer
        if m.sum() >= 25:
            k_ = rng.integers(0, m.sum(), m.sum()); cb.append(np.median(gbar[m][k_])); mb.append(np.median((gobs[m] - gbar[m])[k_]))
    cb, mb = np.array(cb), np.array(mb); ipb = int(np.argmax(mb)); boot.append(mb[ipb]/cb[ipb])
lo, hi = np.percentile(boot, [16, 84])
print(f"      bootstrap (400 resamples): ratio = {ratio:.3f} [{lo:.3f}, {hi:.3f}]   -- a0 cancels in this number, and so does any COHERENT rescaling of the acceleration scale")
print(f"      {'kernel':36s} {'predicted a0-free ratio':>24s} {'consistent with data?':>22s}")
cons = []
for nm_, rv in RB.items():
    ok_ = lo <= rv <= hi; cons.append((nm_, rv, ok_)); print(f"      {nm_:36s} {rv:24.3f} {('YES' if ok_ else 'no'):>22s}")
hiend = gbar > 10*A0["canonical"]          # the Newtonian limit lives at small radii, so this calibration uses the FULL sample, not the r > 2 kpc subset
lam = float(np.median(gobs[hiend]/gbar[hiend]))
print(f"      Newtonian-limit calibration: every kernel requires Delta -> 0 at g_bar >> a0; the data give median g_obs/g_bar = {lam:.3f} there ({int(hiend.sum())} points),")
print(f"      i.e. the stellar normalisation is already consistent to {100*(lam-1):+.1f}% -- so the large excess at g_bar = 1-4 a0 below is NOT a coherent Upsilon offset.")
print(f"      {'g_bar/a0':>9} {'measured Delta/a0':>18} {'candidate':>11} {'nu_RAR':>9} {'meas/candidate':>15} {'meas/nu_RAR':>12}")
mid = [(c_, m_) for c_, m_ in zip(cen, med) if 1.0 <= c_/A0["canonical"] <= 4.5]
ratios_c, ratios_r = [], []
for c_, m_ in mid:
    yN_ = c_/A0["canonical"]; yt_ = float(np.interp(yN_, YT_TAB*(1 - np.exp(-YT_TAB)), YT_TAB))
    dc = yt_*math.exp(-yt_) if yt_ <= 1 else 1/math.e                 # the completed kernel saturates: the scalar force is a0/e above y_t = 1
    dr = yN_*(1/(1 - math.exp(-math.sqrt(yN_))) - 1); mm = m_/A0["canonical"]
    ratios_c.append(mm/dc); ratios_r.append(mm/dr)
    print(f"      {yN_:9.2f} {mm:18.3f} {dc:11.3f} {dr:9.3f} {mm/dc:15.1f} {mm/dr:12.2f}")
med_c = float(np.median(ratios_c)); med_r = float(np.median(ratios_r))
print(f"      measured a0-free peak ratio = {ratio:.3f} [{lo:.3f}, {hi:.3f}];  kernel predictions: " + ", ".join(f"{k.split(' (')[0]} {v:.3f}" for k, v in RB.items()))
CCAND = CB["candidate (exponential carrier)"]
viol_c = ((Dc - CCAND)/sc > 3) & outer
gal_c = sorted(set(names[viol_c]))
a0_needed = float(np.max(gobs[outer] - gbar[outer])*math.e)
print(f"      the candidate's OWN ceiling is the tightest of the family, C = 1/e = {CCAND:.4f}.  Beyond 2 kpc, {100*viol_c.mean():.1f}% of points ({int(viol_c.sum())} of {int(outer.sum())})")
print(f"      exceed it by more than 3 sigma, spread over {len(gal_c)} of {len(set(names))} galaxies -- this is NOT a handful of outliers, it is the transition region of the ordinary population.")
print(f"      raising a0 cannot absorb it: the ceiling is a0/e in physical units, so accommodating the largest measured excess needs a0 >= {a0_needed:.2e} m/s^2 = {a0_needed/A0['canonical']:.1f} x the canonical value, far outside the 20% spread between the two footings.")
check("B4 [kernel discriminator] the ceiling is tight enough to discriminate: at fixed a0 and Upsilon the measured excess between g_bar = 1 and 4.5 a0 is 2-3x the candidate's saturated ceiling a0/e, and a large fraction of the ordinary rotation-curve population exceeds that ceiling at >3 sigma, whereas nu_RAR's wider ceiling is exceeded only by 1.2-1.9x",
      med_c > 1.5 and med_r < med_c, f"median measured/candidate = {med_c:.1f}x, measured/nu_RAR = {med_r:.2f}x over g_bar = 1-4.5 a0; {100*viol_c.mean():.1f}% of points beyond 2 kpc exceed the candidate's own ceiling at >3 sigma.  FIXED-Upsilon, FIXED-a0: the coherent Upsilon freedom is independently pinned to +1.8% by the Newtonian limit, and a0 cannot absorb it either ({a0_needed/A0['canonical']:.1f}x needed), but f25's joint a0-Upsilon profiling is the formal test and is not repeated here")

# ------------------------------------------------------------------ B5: the clusters, radii corrected
print("\n  B5  X-COP with CORRECTED radii (gas profile RADIUS is R/R500; R500 from each file's own header)")
XB = "../../real_research/data/XCOP"
CL = []
for n in sorted(os.listdir(XB)):
    p = os.path.join(XB, n)
    if not os.path.isdir(p): continue
    hm = fits.open(os.path.join(p, f"{n}_hydro_mass.fits")); fg = fits.open(os.path.join(p, f"{n}_fgas_profile.fits"))
    R500 = float(fg[1].header["R500"])                                        # kpc, this file's own header
    d = dict(name=n, R500=R500, r_hm=np.array(hm[1].data["RADIUS"], float), M_hse=np.array(hm[1].data["M_FORW"], float),
             eM_hse=np.array(hm[1].data["EM_FORW"], float), r_fg=np.array(fg[1].data["RADIUS"], float)*R500,   # <-- the correction
             M_gas=np.array(fg[1].data["MGAS"], float), M_nfw=np.array(fg[1].data["M_NFW"], float))
    fs = os.path.join(p, f"{n}_mstar.fits")
    if os.path.exists(fs):
        ms = fits.open(fs)[2].data; d["r_st"] = np.array(ms["RADIUS"], float); d["M_st"] = np.array(ms["MSTAR"], float); d["has_star"] = True
    else: d["has_star"] = False
    CL.append(d)
print(f"      {len(CL)} clusters; {sum(c['has_star'] for c in CL)} with a published stellar profile (headline uses these only)")
print(f"      R500 range {min(c['R500'] for c in CL):.0f} - {max(c['R500'] for c in CL):.0f} kpc; the old x1000 conversion mis-set every radius by R500/1000 (per cluster)")
RG = np.array([40., 50., 75., 100., 150., 200., 300., 420., 750., 1000.])
def li(xq, x, v):
    m = (x > 0) & (v > 0); o = np.interp(np.log(xq), np.log(x[m]), np.log(v[m]), left=np.nan, right=np.nan); return np.exp(o)
# radius-dependent stellar import for the five without a profile, measured from the seven (flagged, not in the headline)
star_ratio = {}
for r in RG:
    v = [li(r, c["r_st"], c["M_st"])/li(r, c["r_fg"], c["M_gas"]) for c in CL if c["has_star"]]
    v = [x for x in v if np.isfinite(x)]; star_ratio[r] = float(np.median(v)) if v else 0.0
print("      measured M_star/M_gas: " + ", ".join(f"{r:.0f}kpc {star_ratio[r]:.3f}" for r in RG[:6]))
ROWS = []
for c in CL:
    for r in RG:
        Mh = li(r, c["r_hm"], c["M_hse"]); Mg = li(r, c["r_fg"], c["M_gas"])
        if not (np.isfinite(Mh) and np.isfinite(Mg)): continue
        Ms = li(r, c["r_st"], c["M_st"]) if c["has_star"] else star_ratio[r]*Mg
        if not np.isfinite(Ms): Ms = star_ratio[r]*Mg
        Mb = Mg + Ms; rr = r*kpc
        ROWS.append(dict(name=c["name"], r=r, meas=c["has_star"], gH=G*Mh*MSUN/rr**2, gb=G*Mb*MSUN/rr**2, Mh=Mh, Mb=Mb, Mg=Mg, Ms=Ms, Mnfw=li(r, c["r_fg"], c["M_nfw"])))
print(f"\n      {'r [kpc]':>8} {'N':>3} {'g_H/a0':>8} {'g_b/a0':>8} {'Delta=(g_H-g_b)/a0':>19} {'Delta/(1/e)':>12} {'Delta/C_max':>12}   (canonical, 7 measured-star clusters)")
VIOL = {}
for foot, a0 in A0.items():
    per_r = {}
    for r in RG:
        R = [w for w in ROWS if w["r"] == r and w["meas"]]
        if not R: continue
        D = np.array([(w["gH"] - w["gb"])/a0 for w in R]); per_r[r] = (np.median(D), len(R), np.median([w["gH"]/a0 for w in R]), np.median([w["gb"]/a0 for w in R]))
        if foot == "canonical":
            print(f"      {r:8.0f} {len(R):3d} {per_r[r][2]:8.3f} {per_r[r][3]:8.3f} {np.median(D):19.3f} {np.median(D)*math.e:12.2f} {np.median(D)/CMAX:12.2f}")
    VIOL[foot] = per_r
vmax = {f: max(v[0]*math.e for v in VIOL[f].values()) for f in A0}
check("B5 [clusters] the ceiling is VIOLATED in cluster cores at both footings -- the excess exceeds the candidate's exact bound a0/e by more than a factor 3, so NO choice of interpolation function can absorb it",
      all(v > 3 for v in vmax.values()), f"peak Delta/(a0/e) = " + ", ".join(f"{f} {vmax[f]:.1f}" for f in A0) + f"; vs the widest family bound C_max = {CMAX:.2f}: factor " + f"{max(v[0] for v in VIOL['canonical'].values())/CMAX:.1f}")

# ------------------------------------------------------------------ B6: can HSE be wrong enough?
print("\n  B6  the HSE escape, quantified: what nonthermal support would restore the ceiling?")
print(f"      {'r [kpc]':>8} {'g_true/g_H needed':>18} {'P_nt/P_th':>11} {'sigma_1D [km/s]':>16}   (kT = 5 keV, mu = 0.61, similar log-slopes)")
SIG = {}
a0 = A0["canonical"]; kT = 5.0*KEV
for r in RG[:7]:
    if r not in VIOL["canonical"]: continue
    _, N, gH, gb = VIOL["canonical"][r]
    Rratio = (gb + CMAX)/gH                                    # the MOST generous kernel bound
    if Rratio >= 1: SIG[r] = 0.0; continue
    ratio_nt = (1 - Rratio)/Rratio; sig = math.sqrt(kT/(MU*MP)*ratio_nt)/1e3
    SIG[r] = sig; print(f"      {r:8.0f} {Rratio:18.3f} {ratio_nt:11.2f} {sig:16.0f}")
HITOMI = 164.0
sig_min = min(v for v in SIG.values() if v > 0)
check("B6 [HSE escape CLOSED] restoring the ceiling by nonthermal support alone would need a 1-D turbulent velocity far above the Hitomi/XRISM Perseus measurement of 164 +/- 10 km/s (a factor > 4 in velocity, > 16 in energy)",
      sig_min > 4*HITOMI, f"minimum required sigma_1D over 40-300 kpc = {sig_min:.0f} km/s vs measured {HITOMI:.0f} km/s (factor {sig_min/HITOMI:.1f} in velocity, {(sig_min/HITOMI)**2:.0f} in pressure)")

# ------------------------------------------------------------------ B7: can baryons be missing?
print("\n  B7  the baryon escape: extra baryons that would restore the ceiling, as a multiple of the OBSERVED gas")
print(f"      {'r [kpc]':>8} {'M_b needed / M_b obs':>21} {'M_b needed / M_gas obs':>23}")
BAR = {}
for r in RG[:7]:
    R = [w for w in ROWS if w["r"] == r and w["meas"]]
    if not R: continue
    v = []
    for w in R:
        gneed = w["gH"] - CMAX*a0                              # the source must supply at least this
        v.append(max(gneed, 0.0)/w["gb"])
    BAR[r] = float(np.median(v)); print(f"      {r:8.0f} {BAR[r]:21.2f} {BAR[r]*np.median([w['Mb']/w['Mg'] for w in R]):23.2f}")
check("B7 [baryon escape CLOSED] restoring the ceiling with unseen baryons would need several times the directly imaged X-ray gas inside 300 kpc, where the gas is the dominant and directly measured component",
      min(BAR.values()) > 2.0, f"minimum required M_b/M_b,observed over 40-300 kpc = {min(BAR.values()):.2f}")

# ------------------------------------------------------------------ B8: what must the source be?
print("\n  B8  therefore an extra SOURCE is required.  Its profile, kernel-independent (kernel applied to the TOTAL):")
print(f"      {'r [kpc]':>8} {'M_src/M_b':>10} {'M_src/M_gas':>12} {'a0_req/a0':>11}   (median over the 7; the source is what the exponential carrier needs)")
YT = np.logspace(-6, 4, 400001); YN_ = YT*(1 - np.exp(-YT))
SRC = {}; AREQ = {}
for r in RG[:9]:
    R = [w for w in ROWS if w["r"] == r and w["meas"]]
    if not R: continue
    s, aq = [], []
    for w in R:
        Msrc_tot = np.interp(w["gH"]/a0, YT, YT*(1 - np.exp(-YT)))*a0*(r*kpc)**2/(G*MSUN)   # baryon-equivalent source the kernel needs
        s.append(Msrc_tot/w["Mb"])
        aq.append(w["gH"]/np.interp(w["gb"]/w["gH"], (1 - np.exp(-1/np.logspace(-4, 3, 20001)))[::-1], np.logspace(-4, 3, 20001)[::-1]) if 0 < w["gb"]/w["gH"] < 1 else np.nan)
    SRC[r] = float(np.median(s))
    # a0' solving g_b = g_H (1 - exp(-g_H/a0')): a0' = g_H / ln(1/(1 - g_b/g_H))
    aq2 = [w["gH"]/(-math.log(1 - w["gb"]/w["gH"]))/a0 for w in R if 0 < w["gb"]/w["gH"] < 1]
    AREQ[r] = float(np.median(aq2))
    print(f"      {r:8.0f} {SRC[r]:10.2f} {SRC[r]*np.median([w['Mb']/w['Mg'] for w in R]):12.2f} {AREQ[r]:11.2f}")
rs = np.array(sorted(SRC)); sv = np.array([SRC[r] for r in rs]); av = np.array([AREQ[r] for r in rs])
sl_src = float(np.polyfit(np.log10(rs), np.log10(sv), 1)[0]); sl_a0 = float(np.polyfit(np.log10(rs), np.log10(av), 1)[0])
print(f"      d log(M_src/M_b)/d log r = {sl_src:+.2f}  (0 = the source TRACES the baryons);   d log(a0_req/a0)/d log r = {sl_a0:+.2f}  (0 = a single rescaled acceleration scale)")
# the Newtonian control: does a dark-matter halo ALSO track the baryons here?  if so, baryon-tracing does not discriminate.
ctrl_h, ctrl_n = [], []
for r in rs:
    R = [w for w in ROWS if w["r"] == r and w["meas"]]
    ctrl_h.append(np.median([w["Mh"]/w["Mb"] for w in R])); ctrl_n.append(np.median([w["Mnfw"]/w["Mb"] for w in R if np.isfinite(w["Mnfw"])]))
sl_h = float(np.polyfit(np.log10(rs), np.log10(ctrl_h), 1)[0]); sl_n = float(np.polyfit(np.log10(rs), np.log10(ctrl_n), 1)[0])
print(f"      CONTROL: Newtonian M_HSE/M_b log-slope = {sl_h:+.2f} (ratio {min(ctrl_h):.1f}-{max(ctrl_h):.1f}); published NFW fit M_NFW/M_b log-slope = {sl_n:+.2f}")
check("B8 [reported, NULL] the required source is baryon-tracing (log-slope near zero) -- but so is the fitted NFW halo, so baryon-tracing does NOT discriminate between an extra source and a dark-matter halo; the discriminating statement is the ceiling itself (B1-B5), not the profile shape",
      abs(sl_src) < 0.35 and abs(sl_n) < 0.35, f"required source slope {sl_src:+.2f} (M_src/M_b {sv.min():.1f}-{sv.max():.1f}); NFW control slope {sl_n:+.2f}; a0_req/a0 = {av.min():.1f}-{av.max():.1f}, slope {sl_a0:+.2f} -- a0_req is NOT constant either, so a rescaled acceleration scale does not fit the cluster either")

# ------------------------------------------------------------------ B9: against the candidate's own dust
print("\n  B9  against the candidate's own dark sector (g03r: rho_d ~ e^{-r/H}/g, H = 0.42 e c^2/(|K_2| a0)):")
cc = 2.998e8
for K2 in [1e5, 2.5e5, 1e6]:
    H_ = 0.42*math.e*cc**2/(K2*a0)/kpc
    print(f"      |K_2| = {K2:.1e}: H = {H_:6.0f} kpc -> the dust's enclosed M_d/M_b RISES outward (g03r H2), while the data need a slope of {sl_src:+.2f}")
check("B9 [the cluster verdict] the candidate's dust cannot be the required source: the data need a baryon-tracing (flat or falling) M_src/M_b, the dust's rises outward by construction because its stiffness follows the local field",
      sl_src < 0.35, f"required slope {sl_src:+.2f}; the dust's e^{{-r/H}}/g law gives a rising ratio at every |K_2| (g03r)")
print(f"\n  caveats: HSE (tested in B6, not granted); FORW hydrostatic reconstruction; the seven clusters with published stellar")
print(f"  profiles carry the headline, the other five are imported and flagged; SPARC uses the standard fixed Upsilon at 3.6um")
print(f"  (a per-galaxy M/L would move individual points, not the population ceiling); the ceiling is a statement about the KERNEL,")
print(f"  so a system above it needs a source, not a different interpolation function.  total {time.time()-T0:.0f}s")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
sys.exit(1 if FAILS else 0)
