"""z01: the implied a0(z) law of every declared Machian cutoff candidate, with controls and mutations.

DECLARED BEFORE COMPUTING (p11's candidates, no additions to make a law fit anything):
  d_p  proper particle horizon at t(z);  d_e  proper event horizon at t(z);  c/H(z);  R* = c/sqrt(G rho_Lambda) (z-independent);  2R*.
  a0(z) = c^2 / R_c(z).  Radius vs diameter (factor 2) and c/H vs cH/Z change the LEVEL a0(0), never the SHAPE a0(z)/a0(0).
References (not candidates; the record's own laws, shown for the same axis): LambdaCDM-native (+0.33 dex at z = 2.5),
  T = t(z)/t0 (CFG175's accumulation law), MUSE-DARK III's linear fit 1 + 1.59 z.
Expected before running (my hand estimates, to be checked): particle-horizon law > H(z) law at every z > 0 (radiation and Lambda make d_p H/c < 2 at high z and > 3 today).
Run: python3 z01_cutoff_laws.py   (exit 0 iff every check passes)
"""
import sys, json, math
import numpy as np
from zcommon import *

ok = []


def chk(name, cond, detail=""):
    ok.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (("\n       " + detail) if detail else ""))


cos = Cosmo(**PLANCK)
ZS = (0.5, 1.0, 2.0, 2.5, 3.0, 5.0)
Rp, Re, RH = cos.dp(0.0), cos.de(0.0), 1.0
Rst = cos.Rstar()
print(f"Planck-like LCDM+radiation (H0 {PLANCK['H0']}, Om {PLANCK['Om']}, Or {PLANCK['Or']}): today, in units c/H0 and Gly:")
cH0_gly = C / cos.H0 / (C * GYR)
for nm, v in (("particle horizon R_p", Rp), ("event horizon R_e", Re), ("Hubble radius", RH), ("R*", Rst), ("2R*", 2 * Rst)):
    print(f"   {nm:22s} {v:7.4f} c/H0 = {v * cH0_gly:7.2f} Gly   a0 = c^2/R = {C * C / (v * C / cos.H0):.4e}   / SPARC = {C * C / (v * C / cos.H0) / A0_SPARC:.3f}")

# ---------------------------------------------------------------- controls
print("\n--- controls (analytic limits; p11 reproduction) ---")
p11 = {0.5: 1.74, 1.0: 2.63, 2.5: 6.05, 5.0: 13.68}
L = laws(cos)
D = L["particle horizon d_p (radius OR diameter)"]
chk("C1 reproduces p11: R_p = 46.14 Gly, R_e = 16.68 Gly, and the diameter law 1.74/2.63/6.05/13.68 at z = 0.5/1/2.5/5",
    abs(Rp * cH0_gly - 46.14) < 0.01 and abs(Re * cH0_gly - 16.68) < 0.01 and all(abs(D(z) - v) < 0.006 for z, v in p11.items()),
    "D(z): " + ", ".join(f"z{z}: {D(z):.3f}" for z in p11))
eds = Cosmo(H0=67.4, Om=1.0, Or=0.0, amin=1e-24)      # amin 1e-24: the truncated matter-era tail 2 sqrt(amin) = 2e-12 (first run used 1e-12: tail 2e-6, my check tolerance 1e-9 was wrong)
eds.OL = 0.0
zt = (0.5, 1.0, 3.0, 10.0)
err_eds = max(abs(eds.dp(z) - 2.0 * eds.dH(z)) for z in zt)
chk("C2 EdS limit: d_p = 2c/H(z) (numeric horizon integral vs analytic, to the truncation 2 sqrt(a_min) = 2e-12), hence the particle-horizon law equals the H(z) law (1+z)^(3/2) in a matter-only universe",
    err_eds < 1e-9 and all(abs(eds.dp(0.0) / eds.dp(z) - (1 + z) ** 1.5) < 1e-8 for z in zt), f"max |d_p - 2c/H| = {err_eds:.2e}")
dS = Cosmo(H0=67.4, Om=0.0, Or=0.0)
dS.OL = 1.0; dS.Omeff = 0.0
err_dS = max(abs(dS.de(z) - 1.0) for z in (0.0, 1.0, 5.0))
chk("C3 de Sitter limit: the event horizon is c/H0 at every time (event-horizon law exactly flat there)", err_dS < 1e-6, f"max |d_e - c/H0| = {err_dS:.2e}")
rad = Cosmo(H0=67.4, Om=1.0, Or=1.0)
rad.OL = 0.0; rad.Omeff = 0.0
err_rad = max(abs(rad.dp(z) - rad.dH(z)) for z in (1.0, 10.0, 100.0))
chk("C4 radiation-only limit: d_p = c/H exactly (a ~ t^(1/2): d_p = 2ct = c/H)", err_rad < 1e-6, f"max |d_p - c/H| = {err_rad:.2e}")
# comoving-vs-proper mutation: dropping the factor a must break C2 (a detector, not a result)
bad = max(abs(eds.chi_p(1.0 / (1 + z)) - 2.0 * eds.dH(z)) for z in zt)
chk("C5 MUTATION (drop the factor a: use the comoving horizon): C2 would FAIL, so C2 does detect a wrong horizon definition", bad > 0.1, f"comoving error vs 2c/H = {bad:.3f}")
# radiation switched off: how much does it matter for the shape (this is a claim of p11's check 6, re-tested)
nor = Cosmo(H0=67.4, Om=0.315, Or=0.0)
r_rad = {z: (D(z), nor.dp(0.0) / nor.dp(z)) for z in ZS}
chk("C6 radiation matters for the horizon law at <= 5% for z <= 5 and moves it in the expected direction (radiation shortens d_p, raising a0(z)): reported",
    all(abs(a / b - 1) < 0.05 and a >= b for a, b in r_rad.values()), "with/without radiation: " + ", ".join(f"z{z}: {a:.3f}/{b:.3f}" for z, (a, b) in r_rad.items()))

# ---------------------------------------------------------------- the table
print("\n--- THE TABLE: a0(z)/a0(0) (ratio; dex in brackets) ---")
rows = {}
extra = {
    "LambdaCDM-native emergent (L274, DM14, 1e12)": lambda z: lcdm_native(z),
    "T = t(z)/t0 (CFG175 accumulation law; falls)": lambda z: tratio(z),
    "MUSE-DARK III linear 1 + 1.59 z (fit, z<=1.44)": lambda z: 1 + 1.59 * z,
}
allL = dict(L); allL.update(extra)
print(f"{'law':52s}" + "".join(f"  z={z:<5}" for z in ZS))
for nm, f in allL.items():
    vals = [f(z) for z in ZS]
    rows[nm] = {str(z): dict(ratio=v, dex=math.log10(v)) for z, v in zip(ZS, vals)}
    print(f"{nm:52s}" + "".join(f"  {v:7.3f}" for v in vals))
    print(f"{'':52s}" + "".join(f"  {math.log10(v):+7.3f}" for v in vals))

print("\n--- absolute a0 (units 1e-10 m/s^2) if the law is normalised by its OWN candidate at z = 0 (the level problem, separate from the shape) ---")
absr = {}
for nm, R_, ff in (("d_p radius: c^2/d_p", Rp, L["particle horizon d_p (radius OR diameter)"]), ("d_p diameter: c^2/(2 d_p)", 2 * Rp, L["particle horizon d_p (radius OR diameter)"]),
                   ("event horizon: c^2/d_e", Re, L["event horizon d_e at t(z)"]), ("R*: c^2/R*  (flat)", Rst, L["flat (R*, 2R*: z-independent)"]),
                   ("2R*: c^2/(2R*) (premise, flat)", 2 * Rst, L["flat (R*, 2R*: z-independent)"]), ("c/H0: cH0  (unnormalised)", RH, L["Hubble radius c/H(z)  [a0 = cH(z)/Z]"])):
    a00 = C * cos.H0 / R_
    absr[nm] = [a00 * ff(z) / 1e-10 for z in (0.0,) + ZS]
    print(f"   {nm:34s} z=0: {a00 / 1e-10:6.3f} (SPARC x{a00 / A0_SPARC:5.3f});   z = " + ", ".join(f"{z}: {a00 * ff(z) / 1e-10:.3f}" for z in ZS))
aH0 = C * cos.H0 / Z_FW
print(f"   cH0/Z (the H0-footing law, Z = {Z_FW:.4f}): z=0: {aH0 / 1e-10:.3f} (x{aH0 / A0_SPARC:.3f});   z = " + ", ".join(f"{z}: {aH0 * cos.Ez(z) / 1e-10:.3f}" for z in ZS))
chk("C7 the framework's two footings: a0 = cH_L/Z = 0.936e-10 (H_L = H0 sqrt(OL)) and cH0/Z = 1.131e-10; 2R* premise = the first",
    abs(C * cos.H0 * math.sqrt(cos.OL) / Z_FW / 1e-10 - 0.9362) < 5e-4 and abs(aH0 / 1e-10 - 1.131) < 2e-3 and abs(C * cos.H0 / (2 * Rst) / 1e-10 - 0.9362) < 5e-4)

# ---------------------------------------------------------------- structure statements (each recomputed)
print("\n--- structure (each computed) ---")
E_ = L["Hubble radius c/H(z)  [a0 = cH(z)/Z]"]
chk("S1 the particle-horizon law lies ABOVE the H(z) law at every tabulated z > 0 (steeper than the rival footing), by x1.46 at z = 1 and x1.60 at z = 2.5",
    all(D(z) > E_(z) for z in ZS) and abs(D(1.0) / E_(1.0) - 1.46) < 0.02 and abs(D(2.5) / E_(2.5) - 1.60) < 0.02,
    "D/E: " + ", ".join(f"z{z}: {D(z) / E_(z):.3f}" for z in ZS))
xz = {z: cos.dp(z) * cos.Ez(z) for z in (0.0, 1.0, 2.5, 10.0, 50.0, 1000.0)}
print("   d_p H / c :", ", ".join(f"z={z}: {v:.3f}" for z, v in xz.items()))
chk("S2 d_p H/c = 3.18 today, falls to 2.2 at z = 1 and to about 1.8 at z = 50 (matter era 2, radiation lowers it; radiation era 1): the D/E ratio is (3.18 / (d_p H/c)) and is NOT constant",
    abs(xz[0.0] - 3.181) < 0.005 and 2.0 < xz[1.0] < 2.4 and 1.6 < xz[50.0] < 1.9 and xz[1000.0] < xz[50.0])
LE = L["event horizon d_e at t(z)"]
print("   event-horizon law: " + ", ".join(f"z={z}: {LE(z):.3f}" for z in ZS))
chk("S3 the event-horizon law RISES with z too (d_e shrinks toward the past) but much less steeply than the H(z) law at z <= 3",
    all(LE(z) > 1 for z in ZS) and all(LE(z) < E_(z) for z in ZS if z <= 3.0), "")
chk("S4 today's slopes d ln a0/dz at z = 0: particle horizon = 1 + c/(H0 d_p) = 1.314; H(z) law = 3 Om/2 = 0.4725; flat 0 (analytic vs numerical derivative)",
    abs((math.log(D(1e-4)) - math.log(D(0.0))) / 1e-4 - (1 + 1 / Rp)) < 2e-3 and abs((math.log(E_(1e-4))) / 1e-4 - 1.5 * cos.Om) < 2e-3,
    f"D slope numeric {(math.log(D(1e-4)) - math.log(D(0.0))) / 1e-4:.4f} vs analytic {1 + 1 / Rp:.4f}; E slope {math.log(E_(1e-4)) / 1e-4:.4f}")
slope0 = 1 + 1 / Rp

# ---------------------------------------------------------------- cosmology sensitivity of the SHAPE
print("\n--- cosmology sensitivity of the shape (H0 cancels: both the horizon law and R* scale as c/H0) ---")
sens = {}
for Om in (0.28, 0.30, 0.315, 0.34):
    for Or in (0.0, 9.1e-5):
        c2 = Cosmo(H0=67.4, Om=Om, Or=Or)
        d2 = c2.dp(0.0)
        sens[(Om, Or)] = dict(D25=d2 / c2.dp(2.5), E25=c2.Ez(2.5), D1=d2 / c2.dp(1.0))
        print(f"   Om {Om:5.3f} Or {Or:.1e}:  D(1) {sens[(Om, Or)]['D1']:.3f}  D(2.5) {sens[(Om, Or)]['D25']:.3f} ({math.log10(sens[(Om, Or)]['D25']):+.3f} dex)   E(2.5) {sens[(Om, Or)]['E25']:.3f}")
lo, hi = min(v["D25"] for v in sens.values()), max(v["D25"] for v in sens.values())
chk(f"S5 the particle-horizon law at z = 2.5 stays in [{lo:.2f}, {hi:.2f}] over Om 0.28-0.34 and radiation on/off (i.e. +{math.log10(lo):.2f}..+{math.log10(hi):.2f} dex): the shape is a robust prediction of the candidate",
    lo > 5.0 and hi < 7.5)
# DESI-like w0wa background for the particle horizon (aside; w0, wa = DESY5 best fit of the record)
dw = Cosmo(H0=67.4, Om=0.319, Or=9.1e-5, w0=-0.752, wa=-0.86)
Dw = dw.dp(0.0) / dw.dp(2.5)
print(f"   aside (DESY5-like w0 -0.752, wa -0.86, Om 0.319): D(2.5) = {Dw:.3f} ({math.log10(Dw):+.3f} dex); E(2.5) = {dw.Ez(2.5):.3f}")
chk("S6 a DESI-like evolving dark energy moves the particle-horizon law at z = 2.5 by < 8% relative to LCDM (it is a matter/radiation-era integral): the shape does not depend on the Lambda sector", abs(Dw / D(2.5) - 1) < 0.08, f"ratio {Dw / D(2.5):.3f}")
# a_min dependence of the horizon (the inflation caveat): the hot-big-bang horizon converges at early times
cmin = {a: Cosmo(H0=67.4, Om=0.315, Or=9.1e-5, amin=a).dp(0.0) for a in (1e-6, 1e-9, 1e-12, 1e-20, 1e-30)}
print("   d_p(0) vs the lower limit a_min of the integral (c/H0): " + ", ".join(f"{a:.0e}: {v:.5f}" for a, v in cmin.items()))
# my first expectation (change < 2e-6 for a_min 1e-6 -> 1e-30) was WRONG: the radiation-era tail is Int_0^amin da/sqrt(Or) = amin/sqrt(Or) = 1.05e-4 at amin = 1e-6; fixed below and disclosed
tail = {a: cmin[1e-30] - v for a, v in cmin.items()}
chk("S7 the horizon integral converges at early times as a_min/sqrt(Or) (radiation era): 1e-4 c/H0 at a_min = 1e-6, < 1e-7 at 1e-9, none below; well defined for a hot-big-bang start, undefined (much larger) if inflation precedes it -- a conceptual, not numerical, caveat",
    all(abs(tail[a] - a / math.sqrt(9.1e-5)) < 0.05 * a / math.sqrt(9.1e-5) + 1e-9 for a in (1e-6, 1e-9)) and tail[1e-12] < 2e-9,
    "shortfall vs a_min -> 0: " + ", ".join(f"{a:.0e}: {tail[a]:.2e} (a/sqrt(Or) = {a / math.sqrt(9.1e-5):.2e})" for a in (1e-6, 1e-9, 1e-12)))
json.dump(dict(pass_=sum(ok), n=len(ok), today=dict(Rp=Rp, Re=Re, Rstar=Rst, RstarOverRp=Rst / Rp), table=rows, absolute=absr, slope0_D=slope0, sensitivity={f"{k[0]}|{k[1]}": v for k, v in sens.items()}),
          open("z01_results.json", "w"), indent=1)
print(f"\n{sum(ok)}/{len(ok)}")
sys.exit(0 if all(ok) else 1)
