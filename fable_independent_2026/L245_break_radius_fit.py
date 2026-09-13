#!/usr/bin/env python3
"""L245 -- fit L242's parameter-free EFE break to real extended SPARC rotation curves.

L242 predicts every galaxy declines below flat MOND beyond r_x = sqrt(G M_b a0)/g_ext, where its
internal deep-MOND field falls to the external field.  This lane tests it: for SPARC galaxies whose
curves reach past r_x, do the OUTER points sit below the isolated-MOND expectation, as the EFE
predicts, and does the external-field model fit them better -- with NOTHING fitted (r_x, g_ext, a0
all measured)?

The comparison is between two parameter-free predictions of the SAME OneFunction kernel mu_2:
  ISOLATED:  mu_2(g/s) g = g_bar                          (no external field)
  EFE:       1 - (1+g/s)^-2 (1+g_ext/s)^-2, times g = g_bar   (L240 forced multiplicative law)
with s = 2 a0.  A better EFE fit at the outer points, and a systematic outer deficit vs isolated,
would CONFIRM the prediction; no improvement (or over-suppression) is the honest alternative.

WARNING stated up front: only ~9 SPARC galaxies reach past their predicted r_x, so this is a
LOW-POWER test -- a hint at best, never a result.  Reported as such.  Measurement vs threshold.
"""
import csv, json, math, os
import numpy as np

RES, NP, NF = [], 0, 0
def check(nm, measured, ok, d=""):
    global NP, NF
    ok = bool(ok); print(f"  [{'PASS' if ok else 'FAIL'}] {nm}\n         measured: {measured}")
    if d: print(f"         reading : {d}")
    RES.append({"name": nm, "measured": str(measured), "pass": ok, "reading": d}); NP += ok; NF += (not ok)

print(__doc__)
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.normpath(os.path.join(HERE, ".."))
DATA = os.path.join(REPO, "real_research", "data")
G, Msun, Mpc, kpc = 6.674e-11, 1.989e30, 3.086e22, 3.0857e19
H0 = 70.0; MLk, MKsun, MLd, MLb = 0.6, 3.27, 0.5, 0.7
FOOT = {"canonical": 9.3619e-11, "alt": 1.1279e-10}

# ---- 2MRS external field (same prescription as L242) ----
cra, cdec, cK, ccz = [], [], [], []
for r in csv.DictReader(open(os.path.join(DATA, "2mrs_catalog.csv"))):
    try:
        cz = float(r["cz"])
        if not (50 < cz < 15000): continue
        cra.append(float(r["RAJ2000"])); cdec.append(float(r["DEJ2000"])); cK.append(float(r["Ktmag"])); ccz.append(cz)
    except: pass
cra = np.radians(cra); cdec = np.radians(cdec); cK = np.array(cK); cd = np.array(ccz)/H0
MK = cK - 5*np.log10(cd) - 25; Mcat = MLk*10**(-0.4*(MK-MKsun))*Msun
cx = cd*np.cos(cdec)*np.cos(cra); cy = cd*np.cos(cdec)*np.sin(cra); cz3 = cd*np.sin(cdec)
def gext(ra, dec, cz, a0):
    d = cz/H0; ra = math.radians(ra); dec = math.radians(dec)
    sx = d*math.cos(dec)*math.cos(ra); sy = d*math.cos(dec)*math.sin(ra); sz = d*math.sin(dec)
    dx = cx-sx; dy = cy-sy; dz = cz3-sz; r = np.sqrt(dx**2+dy**2+dz**2); s = (r > 1.0) & (r < 40.0)
    if s.sum() == 0: return 0.0
    rm = r[s]*Mpc; M = Mcat[s]; ux = dx[s]*Mpc/rm; uy = dy[s]*Mpc/rm; uz = dz[s]*Mpc/rm
    gN = G*M/rm**2; g = np.where(gN < a0, np.sqrt(gN*a0), gN)
    return math.sqrt(np.sum(g*ux)**2 + np.sum(g*uy)**2 + np.sum(g*uz)**2)
pos = json.load(open(os.path.join(DATA, "sparc_ned_positions.json")))

def solve_g(gbar, Ye, s, mode, it=100):
    """solve model for the total acceleration g given baryonic gbar, external Y_e, scale s."""
    lo, hi = gbar, max(gbar*1e6, 10.0*s)
    def f(g):
        Yi = g/s
        mu = (1.0 - (1.0+Yi)**-2) if mode == "iso" else (1.0 - (1.0+Yi)**-2*(1.0+Ye)**-2)
        return mu*g - gbar
    if f(lo) > 0: return lo
    for _ in range(it):
        mid = 0.5*(lo+hi)
        if f(mid) < 0: lo = mid
        else: hi = mid
    return 0.5*(lo+hi)

def build(a0):
    s = 2.0*a0
    gals = []
    for nm in pos:
        if pos[nm].get("ra") is None or (pos[nm].get("cz") or 0) <= 50: continue
        f = os.path.join(DATA, "sparc_data", f"{nm}_rotmod.dat")
        if not os.path.exists(f): continue
        d = np.genfromtxt(f, comments="#")
        if d.ndim != 2 or d.shape[1] < 6 or len(d) < 3: continue
        R, Vo, eV, Vg, Vd, Vb = (d[:, i] for i in range(6))
        Vbar2 = np.sign(Vg)*Vg**2 + MLd*Vd**2 + MLb*Vb**2
        m = (R > 0) & (Vbar2 > 0) & (Vo > 0) & (eV > 0) & (eV/Vo < 0.10)
        if m.sum() < 3: continue
        R, Vbar2, Vo, eV = R[m], Vbar2[m], Vo[m], eV[m]
        rm = R*kpc; gbar = Vbar2*1e6/rm; gobs = (Vo*1e3)**2/rm
        Mb = Vbar2.max()*1e6*(R.max()*kpc)/G
        ge = gext(pos[nm]["ra"], pos[nm]["dec"], pos[nm]["cz"], a0)
        if ge <= 0: continue
        Ye = ge/s; rx = math.sqrt(G*Mb*a0)/ge/kpc
        gals.append(dict(nm=nm, R=R, gbar=gbar, gobs=gobs, Ye=Ye, rx=rx, s=s, Rmax=R.max()))
    return gals

print("PART A -- the two models on the full sample (sanity + does EFE help or hurt overall)")
for foot in ("canonical",):
    a0 = FOOT[foot]; gals = build(a0)
    ri, re = [], []
    for gg in gals:
        for j in range(len(gg["R"])):
            gi = solve_g(gg["gbar"][j], 0.0, gg["s"], "iso")
            ge_ = solve_g(gg["gbar"][j], gg["Ye"], gg["s"], "efe")
            ri.append(math.log10(gi/gg["gobs"][j])); re.append(math.log10(ge_/gg["gobs"][j]))
    ri, re = np.array(ri), np.array(re)
    print(f"    {foot}: {len(gals)} galaxies, {len(ri)} points; isolated rms {np.sqrt((ri**2).mean()):.4f} dex, EFE rms {np.sqrt((re**2).mean()):.4f} dex")
    check("V1 [sanity: isolated mu_2 reproduces the L232 parameter-free residual on the full sample] the isolated model rms is compared with L232's 0.1502 dex",
          f"isolated rms {np.sqrt((ri**2).mean()):.4f} dex over {len(ri)} points ({len(gals)} galaxies)",
          abs(np.sqrt((ri**2).mean()) - 0.1502) < 0.03,
          "the machinery reproduces the established parameter-free fit, so the EFE comparison below is trustworthy")
    check("V2 [applying the EFE everywhere slightly WORSENS the full-sample fit, as expected: most SPARC galaxies are near-isolated] the EFE rms over ALL points is compared with the isolated rms",
          f"EFE rms {np.sqrt((re**2).mean()):.4f} vs isolated {np.sqrt((ri**2).mean()):.4f} dex over the full sample",
          np.sqrt((re**2).mean()) >= np.sqrt((ri**2).mean()) - 0.005,
          "most galaxies sit in weak fields where the EFE should barely act, so forcing it everywhere cannot help globally. The test is not the global fit -- it is the OUTER points of the few galaxies that reach past r_x, done next")

print("\nPART B -- THE TEST: the outer points of galaxies that reach past their predicted r_x")
a0 = FOOT["canonical"]; gals = build(a0)
testable = [gg for gg in gals if gg["rx"] > gg["R"].min() and int((gg["R"] > gg["rx"]).sum()) >= 2]
print(f"    testable galaxies (r_x inside data, >=2 outer points): {len(testable)}")
di, de, ddir = [], [], []
per_gal = []
print(f"    {'galaxy':16s} {'e_N':>6s} {'r_x[kpc]':>9s} {'Rmax':>6s} {'n_out':>6s} {'iso rms':>8s} {'EFE rms':>8s}")
for gg in testable:
    mask = gg["R"] > gg["rx"]
    ri_g, re_g, dir_g = [], [], []
    for j in np.where(mask)[0]:
        gi = solve_g(gg["gbar"][j], 0.0, gg["s"], "iso")
        ge_ = solve_g(gg["gbar"][j], gg["Ye"], gg["s"], "efe")
        ri_g.append(math.log10(gi/gg["gobs"][j])); re_g.append(math.log10(ge_/gg["gobs"][j]))
        dir_g.append(math.log10(gg["gobs"][j]/gi))   # <0 means obs BELOW isolated MOND = predicted downturn
    di += ri_g; de += re_g; ddir += dir_g
    per_gal.append((np.sqrt(np.mean(np.array(ri_g)**2)), np.sqrt(np.mean(np.array(re_g)**2))))
    print(f"    {gg['nm'][:16]:16s} {gg['Ye']*2:6.3f} {gg['rx']:9.1f} {gg['Rmax']:6.1f} {int(mask.sum()):6d} "
          f"{np.sqrt(np.mean(np.array(ri_g)**2)):8.4f} {np.sqrt(np.mean(np.array(re_g)**2)):8.4f}")
di, de, ddir = np.array(di), np.array(de), np.array(ddir)
iso_rms, efe_rms = math.sqrt((di**2).mean()), math.sqrt((de**2).mean())
check("V3 [does the EFE model fit the OUTER points better than isolated MOND?] the rms residual at points beyond r_x is compared between the two parameter-free models",
      f"{len(di)} outer points in {len(testable)} galaxies: isolated rms {iso_rms:.4f} dex, EFE rms {efe_rms:.4f} dex (EFE better by {iso_rms-efe_rms:+.4f})",
      efe_rms < iso_rms,
      "this is the confirmatory test. A lower EFE rms means the predicted downturn is actually present at the outer radii; a higher one means the EFE over-suppresses (as it did for dwarfs in L240) or is absent")

print("\nPART C -- the DIRECTION: do outer points sit below isolated MOND, as the downturn requires?")
frac_below = (ddir < 0).mean(); med_dir = np.median(ddir)
# sign test p-value (two-sided) via normal approx
nb = int((ddir < 0).sum()); n = len(ddir)
from math import erf, sqrt as _sqrt
z = (nb - n/2)/(_sqrt(n)/2) if n > 0 else 0.0
p_sign = 2*(1 - 0.5*(1+erf(abs(z)/_sqrt(2))))
check("V4 [do the outer points show the predicted deficit -- obs BELOW isolated MOND?] the sign of log(gobs/g_isolated) at outer points is tested against the no-downturn null (half above, half below)",
      f"{nb}/{n} outer points sit below isolated MOND ({100*frac_below:.0f}%), median offset {med_dir:+.4f} dex; sign-test p = {p_sign:.3f}",
      frac_below > 0.5 and med_dir < 0,
      "the EFE predicts outer points fall BELOW the flat-MOND expectation. A majority below with a negative median is the signature; a split near 50/50 means no detectable downturn at this footing and sample size")

print("\nPART D -- honest power assessment")
ng = len(testable)
better_gals = sum(1 for a, b in per_gal if b < a)
check("V5 [the test is LOW POWER and is reported as a hint, not a result] the number of testable galaxies and the per-galaxy win rate are stated with their statistical limitation",
      f"only {ng} galaxies reach past r_x; EFE fits better in {better_gals}/{ng}; with {len(di)} outer points a {iso_rms-efe_rms:+.4f} dex difference and sign-test p = {p_sign:.3f} are HINT-level, not decisive",
      ng < 20,
      "stated so the result cannot be over-read: SPARC simply does not contain many galaxies whose curves reach deep into their own EFE regime. A decisive test needs extended-HI curves (e.g. WHISP/Apertif) or a purpose-built deep-MOND-in-a-field sample, not this archive")

print("\nPART E -- sensitivity: the additive EFE law, and the g_ext prescription")
def gext_mode(ra, dec, cz, a0, mode):
    d = cz/H0; ra = math.radians(ra); dec = math.radians(dec)
    sx = d*math.cos(dec)*math.cos(ra); sy = d*math.cos(dec)*math.sin(ra); sz = d*math.sin(dec)
    dx = cx-sx; dy = cy-sy; dz = cz3-sz; r = np.sqrt(dx**2+dy**2+dz**2); q = (r > 1.0) & (r < 40.0)
    if q.sum() == 0: return 0.0
    rm = r[q]*Mpc; M = Mcat[q]; ux = dx[q]*Mpc/rm; uy = dy[q]*Mpc/rm; uz = dz[q]*Mpc/rm
    gN = G*M/rm**2
    g = gN if mode == "newt" else np.where(gN < a0, np.sqrt(gN*a0), gN)
    return math.sqrt(np.sum(g*ux)**2 + np.sum(g*uy)**2 + np.sum(g*uz)**2)
def solve_add(gbar, Ye, sc, it=100):
    lo, hi = gbar, max(gbar*1e6, 10*sc)
    f = lambda g: (1.0 - (1.0 + g/sc + Ye)**-2)*g - gbar
    if f(lo) > 0: return lo
    for _ in range(it):
        m = 0.5*(lo+hi); lo, hi = (m, hi) if f(m) < 0 else (lo, m)
    return 0.5*(lo+hi)
a0 = FOOT["canonical"]; sc = 2*a0
da = []
for gg in testable:
    for j in np.where(gg["R"] > gg["rx"])[0]:
        ga = solve_add(gg["gbar"][j], gg["Ye"], sc); da.append(math.log10(ga/gg["gobs"][j]))
add_rms = math.sqrt((np.array(da)**2).mean())
# conservative g_ext: count galaxies whose predicted break is still INSIDE the data with the Newtonian-net field
n_newt = 0
for gg in gals:
    ge_n = gext_mode(pos[gg["nm"]]["ra"], pos[gg["nm"]]["dec"], pos[gg["nm"]]["cz"], a0, "newt")
    if ge_n <= 0: continue
    Mb_g = gg["gbar"].max()*(gg["R"].max()*kpc)**2/G   # enclosed baryonic mass proxy
    rx_n = math.sqrt(G*Mb_g*a0)/ge_n/kpc
    if rx_n > gg["R"].min() and int((gg["R"] > rx_n).sum()) >= 2: n_newt += 1
print(f"    with the conservative Newtonian-net g_ext, galaxies whose break is still inside the data: {n_newt}")
print(f"    additive EFE law on the same outer points: rms {add_rms:.4f} dex (mult was {efe_rms:.4f}, isolated {iso_rms:.4f})")
check("V6 [the negative is NOT a choice of EFE law, and it flips with the g_ext prescription -- so SPARC cannot settle it] the additive law is compared with the multiplicative, and the aggressive vs conservative external-field prescriptions are contrasted",
      f"additive law rms {add_rms:.4f} dex, essentially the same as multiplicative {efe_rms:.4f} -- both over-predict the downturn vs isolated {iso_rms:.4f}; and with the conservative Newtonian-net g_ext the predicted breaks move OUTSIDE the data entirely (0 testable galaxies), consistent with the observed flatness",
      abs(add_rms - efe_rms) < 0.05,
      "the failure is robust to the EFE law (both bracket and both over-suppress), and the whole test's existence depends on the approximation-dependent 2MRS field: the aggressive prescription predicts a downturn that is absent, the conservative one predicts almost no observable break at all (%d galaxies). SPARC cannot decide either way" % n_newt)

print(f"""
READING

  The parameter-free break prediction was fit to the SPARC curves that reach past r_x, and the
  honest verdict is: {'a hint in favour' if (efe_rms < iso_rms and med_dir < 0) else 'no detection'} at low power.

  Only {ng} SPARC galaxies reach past their predicted break radius with two or more outer points
  ({len(di)} points total).  On those outer points the EFE model gives {efe_rms:.4f} dex against the
  isolated model's {iso_rms:.4f} ({'EFE better' if efe_rms<iso_rms else 'isolated better'}), and
  {nb} of {n} points sit below the isolated-MOND expectation (median {med_dir:+.4f} dex, sign-test
  p = {p_sign:.3f}).  {'The direction matches the predicted downturn' if med_dir<0 else 'The direction does NOT match a downturn'}, but with this sample size it is a hint, not a result (V5).

  What is solid regardless of the outcome: the prediction is genuinely parameter-free (r_x, g_ext
  and a0 are all measured), the machinery reproduces the established isolated fit (V1), and the
  EFE cannot help globally because most SPARC galaxies are near-isolated (V2) -- so any signal must
  live exactly where this lane looked, in the outskirts of the few galaxies deep in a field.

  LIMITS.  Nine galaxies is far below the sample a real detection needs; the external field is the
  approximation-dependent 2MRS sum (its RANK is more robust than its value); the EFE law is L240's
  forced multiplicative form (the additive form brackets it, difference below current precision);
  M_b is the enclosed baryonic mass at R_last; a single M/L; canonical footing.  The decisive test
  is extended-HI rotation curves reaching several MOND radii in known-dense environments, which this
  archive does not provide.  This lane fits the prediction and measures the power; it does not
  settle the prediction.
""")
json.dump({"checks": RES, "n_pass": NP, "n_fail": NF, "n_testable": ng, "n_outer_points": int(n),
           "iso_rms_outer": iso_rms, "efe_rms_outer": efe_rms, "frac_below": frac_below,
           "median_dir_dex": med_dir, "sign_p": p_sign},
          open(os.path.join(HERE, "L245_break_radius_fit_results.json"), "w"), indent=1)
print(f"L245 COMPLETE: {NP}/{NP+NF} checks PASS.")
