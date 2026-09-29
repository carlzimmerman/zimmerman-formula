"""
CFG97 -- independent re-derivation of the CFG41 headline (Di Teodoro+2023 HI curves of 15 massive spirals, four S0/S0a) with my own code.  FROZEN before any run.

BLINDNESS.  I read only: CFG41_README.md, CFG53_README.md, CFG64 README, the two CFG41 DOCSTRINGS (main + selbias_mc, extracted with ast.get_docstring), and the
three diteodoro2023_*.tsv data files.  I did NOT open, read, exec or import any CFG41/CFG53 script or .out/_results.json, nor CFG36 (whose machinery CFG41 exec's).

QUESTION.  Do independently written code and the documented model reproduce CFG41's LAW-side headline (S0/S0a corrected +0.004 +- 0.071 dex, +0.05 sigma; 15 disks corrected
-0.028 +- 0.066; uncorrected +0.048 / S0 +0.080), the selection-bias B = 0.076 +- 0.030, and CFG53's observed-slope-minus-law numbers; and how fragile are they to the size of B,
the HI-to-baryon conversion, inclination, distance and leave-one-out?

MODEL AS READ.  Data: 15 galaxies; M_* = 10^logMs_W1 (WISE, Upsilon 0.6, the paper's), M_gas = 10^logMgas (1.36 M_HI, the paper's); tabulated v_flat +- dvflat; recovered curves R,V,dV.
 Radius R_f = mean radius of the points included by the Lelli+2016 flat-part algorithm (my implementation, below).  Law: g_N = G M_b/R^2 (point mass, HEADLINE), g = g_N nu(g_N/a0),
 v_law^2 = g R.  Brackets: exponential Freeman disc R_d = 8 kpc (v^2 = (2GM/R_d) y^2 [I0K0 - I1K1], y = R/2R_d) and the spherical enclosed mass M[1-(1+R/R_d)e^-R/R_d] at R_d = 8 kpc.
 Offset_i = log10(v_flat_i / v_law_i) - B.  kernel nu_mono := nu_RAR = 1/(1-exp(-sqrt(y))) (ASSUMPTION: agrees with the campaign's nu_mono to 3e-9 for y<=0.1 and 2.3% to y=30, per the CFG64 README;
 nu_mono(1)=1.582 = nu_RAR(1)); P2 = sqrt(1+1/y) as sensitivity.  a0: FOOTINGS (ASSUMPTION, from the standing memory 'both footings 9.36e-11 / 1.13e-10' and the README's alt-minus-canonical
 law shift -0.017 dex, which requires the alt to be the LARGER a0): canonical a0 = 9.36e-11, alt a0 = 1.13e-10 m/s^2; a0 = 1.2e-10 as a reported extra.  B = 0.076 +- 0.030 (the README's value; the
 primary comparison isolates the law) and, separately, B_mine from my own MC (cfg97_selbias_mc.py).
 Sample stat: mean over N with (std ddof=1)/sqrt(N); floor in quadrature = baryon-structure (half the range of the mean over point/Freeman/sphere), M_* +-0.2 dex (stellar part only, all galaxies at once,
 half the +/- difference of the mean), M_gas +-0.1 dex, radius +-25%, B error 0.030.  S0/S0a = RC3 T <= 0: NGC1167, NGC5790, UGC12591, UGC12811.  (ddof=0 also reported.)
 Lelli+2016 algorithm as I implement it (declared): take the outermost 3 points; require them within 5% of their mean; else the flat part is the outermost point alone (V_last, R_last);
 extend inward one point at a time while |V - mean(included)|/mean <= 5% (mean recomputed); v_f = mean of included V, R_f = mean of included R.
 Shape (CFG53 law side): outer slope of ln V vs ln R over points with R >= R_max/2, weights (V/dV)^2, formal error x sqrt2; s_law from the law's speeds at the same radii, same weights;
 red = T<=0 (4), blue = the other 11; statistic <s_obs - s_law>_red, _blue with error sqrt(sum sigma_i^2)/N.
 RULE (cold-mass rule f_ex, B's derived rule): NOT reconstructable from the permitted reading (Mandelbaum masses, Dutton-Maccio, the conservation form at x_e=0.40 and the definition of f_ex live in
 CFG36's machinery, which the task forbids me to read).  I therefore do NOT claim to reproduce '-0.105 +- 0.131 (-0.80 sigma)'.  A CONSISTENCY-ONLY row takes the README's f_ex
 (0.31, 0.31, 0.78, 0.49 for NGC1167, NGC5790, UGC12591, UGC12811) as an INPUT (not independent) and asks whether v_rule^2 = v_law^2 (1+f) [D1] or v_law^2/(1-f) [D2] reproduces the README's
 rule-minus-law shift on the four (0.004-(-0.105) = 0.109 dex) within 0.010.  Neither is a reproduction of the rule.

PRE-DECLARED CONTROLS (a failed control is a failure; exit code 1)
  C1 data: 15 galaxies, 216 recovered points, NGC5440 v_flat = 303 +- 25.
  C2 my Lelli algorithm reproduces tabulated v_flat within 3 km/s for >= 12 of 15 (CFG41 declared 12, got 10; I keep 12).
  C3a Freeman closed form vs an independent numerical ring integration of the exponential disc (elliptic-K potential, finite-difference force), rel. diff < 1e-5 at R/Rd = 0.5,1,2.15,5,10.
  C3b Freeman peak: v_max = 0.6218 sqrt(GM/R_d) (+-0.002) at R = 2.15 R_d (+-0.1).
  C4 limits: nu=1 gives Newton exactly; deep-MOND limit v^4 -> G M a0 to 1e-3 at y = 1e-6; nu_RAR(1) = 1.582 (+-0.001), P2(1) = sqrt2.
  C5 the selection MC (cfg97_selbias_mc.py): its own controls pass and B_mine within 0.010 of 0.076 (read from its results json).
  C6 MUTATE=1 (velocities x0.5, v_flat and V): H1 must FAIL (offset ~ -0.30), and the script exits 1.
PRE-DECLARED HYPOTHESES / READING
  H1 (law fits, corrected, canonical): |mean_15 - B| < 2 sigma with B = 0.076.
  H2 (law, four S0/S0a, corrected): |mean_4 - B| < 2 sigma_S0.
  REPRODUCTION TIERS for every CFG41 number: EXACT if |diff| <= 0.0015 dex (3-decimal rounding); CLOSE if |diff| <= 0.010 dex and |diff in sigma| <= 0.15; else DIFFERENT (cause stated).
  No claim of framework-favouring; kappa = 1/2 fitted; a fit to the law here says nothing about the rule.
ATTACKS (reported; the reading rules are declared here)
  A1 B size: recompute every corrected offset for B in {0, B_mine, 0.076, 0.058 (referee), B from the M_*-error MC}; H1 verdict per B.  A conclusion is 'B-fragile' if H1/H2 flip.
  A2 galaxy-specific B: b_i = (s_int^2/s_c) phi(z_i)/Phi(z_i), z_i = (log v_law(M_b,i) - log 300)/s_c averaged over the MC's MATCH rows; the S0 four sit higher in mass so b_i < B is expected;
     report corrected S0 and 15 means with b_i instead of B.
  A3 HI-to-baryon: gas x {0, 1, 1.25, 1.5, 2}; Upsilon x {0.5/0.6, 1, 0.7/0.6}; M_* from the rotation-curve decomposition (logMs_RC); law mean and S0 mean shifts.
  A4 inclination: delta log v = -cot(i) di/ln10 for i in {45,60,75} deg, di = 3 deg (inclinations are not in the tables); a 60 deg 3-deg common systematic is added to a 'floor+' row.
  A5 distance: (i) per-galaxy D' = D + dD N(0,1) (truncated at 0.3 D), R ~ D', M_*, M_gas ~ D'^2, 4000 draws: shift and SD of the mean offset; (ii) common +-5% scale.  Added to a 'floor+' row.
  A6 leave-one-out (15, and the 4 S0): the range of the corrected mean, jackknife SE, and whether any single galaxy changes the sign or moves the mean by more than the stat error of the mean.
  A7 kernel P2, a0 alternatives, structure brackets, inverse-variance weighted mean, WISE-colour and flagged-excluded subsets (README: law -0.028 and -0.038 (-0.60 sigma)).
Run: python3 cfg97_massive_spirals_hi.py  (MUTATE=1 control).  Uses cfg97_selbias_mc_results.json.
"""
import os, sys, json
import numpy as np
from scipy.special import i0, i1, k0, k1, ellipk
from scipy.integrate import quad
MUT = os.environ.get("MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
D = os.path.join(os.environ.get("ZF_REPO") or os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")), "real_research", "data") + "/"
G = 6.6743e-11; MSUN = 1.98847e30; KPC = 3.0856775814913673e19
checks = []; out = {"mutate": MUT}
def chk(n, ok, d):
    checks.append((n, bool(ok), d)); print(("PASS " if ok else "FAIL ") + n + " -- " + d)
# ---------------- data ----------------
def rd(fn):
    rows = [l.rstrip("\n").split("\t") for l in open(D + fn) if l.strip() and not l.startswith("#")]
    return rows[0], rows[1:]
h, t = rd("diteodoro2023_massive_spirals.tsv"); cols = {c: i for i, c in enumerate(h)}
names = [r[0] for r in t]
def col(c): return np.array([float(r[cols[c]]) for r in t])
Dm, dD, lMs, lMg, vf, dvf, lMsRC, flag = col("D_Mpc"), col("dD"), col("logMs_W1"), col("logMgas"), col("vflat"), col("dvflat"), col("logMs_RC"), col("flag_uncertain")
h2, t2 = rd("diteodoro2023_hi_rotation_curves.tsv")
curves = {n: [] for n in names}
for r in t2: curves[r[0]].append((float(r[1]), float(r[2]), float(r[3])))
curves = {n: np.array(sorted(v)) for n, v in curves.items()}
h3, t3 = rd("diteodoro2023_morphology.tsv"); T = {r[0]: float(r[1]) for r in t3}; W23 = {r[0]: float(r[2]) for r in t3}
npts = sum(len(v) for v in curves.values())
chk("C1 data", len(names) == 15 and npts == 216 and abs(vf[names.index("NGC5440")] - 303) < 1e-9 and abs(dvf[names.index("NGC5440")] - 25) < 1e-9, f"{len(names)} galaxies, {npts} points")
S0 = np.array([(np.isfinite(T[n]) and T[n] <= 0) for n in names])   # RC3 T<=0 red; T>=1 or no T blue
if MUT:
    vf = vf * 0.5; dvf = dvf * 0.5
    curves = {n: np.column_stack([c[:, 0], 0.5 * c[:, 1], 0.5 * c[:, 2]]) for n, c in curves.items()}
# ---------------- Lelli flat algorithm (my implementation) ----------------
def lelli(c):
    R, V = c[:, 0], c[:, 1]; n = len(R)
    if n < 3: return V[-1], R[-1], 1, False
    inc = [n-3, n-2, n-1]; m = V[inc].mean()
    if np.any(np.abs(V[inc] - m) / m > 0.05): return V[-1], R[-1], 1, False
    i = n - 4
    while i >= 0 and abs(V[i] - V[inc].mean()) / V[inc].mean() <= 0.05:
        inc.append(i); i -= 1
    return V[inc].mean(), R[inc].mean(), len(inc), True
LL = {n: lelli(curves[n]) for n in names}
Rf = np.array([LL[n][1] for n in names]); vL = np.array([LL[n][0] for n in names])
ok2 = np.abs(vL - vf) <= 3.0
chk("C2 Lelli algorithm within 3 km/s of tabulated v_flat for >=12/15", ok2.sum() >= 12, f"{ok2.sum()}/15; misses: " + ", ".join(f"{n}({vL[i]:.0f} vs {vf[i]:.0f})" for i, n in enumerate(names) if not ok2[i]))
# ---------------- physics ----------------
def nu_mono(y): y = np.asarray(y, float); return 1.0 / (1.0 - np.exp(-np.sqrt(y)))
def nu_p2(y): y = np.asarray(y, float); return np.sqrt(1.0 + 1.0 / y)
A0C, A0A = 9.36e-11, 1.13e-10
def gN(kind, M, R, Rd=8.0):   # M in Msun, R in kpc -> m/s^2
    Rm = R * KPC
    if kind == "point": return G * M * MSUN / Rm**2
    if kind == "sphere": return G * M * MSUN * (1 - (1 + R/Rd) * np.exp(-R/Rd)) / Rm**2
    if kind == "freeman":
        y = R / (2 * Rd); v2 = (2 * G * M * MSUN / (Rd * KPC)) * y**2 * (i0(y)*k0(y) - i1(y)*k1(y)); return v2 / Rm
def vlaw(kind, M, R, a0=A0C, nu=nu_mono):   # km/s
    g = gN(kind, M, R); return np.sqrt(g * nu(g / a0) * R * KPC) / 1e3
def Mstar(): return 10.0**lMs
def Mgas(): return 10.0**lMg
def offs(kind="point", a0=A0C, nu=nu_mono, ms=None, mg=None, R=None, v=None, Dscale=None):
    ms = Mstar() if ms is None else ms; mg = Mgas() if mg is None else mg
    R = Rf if R is None else R; v = vf if v is None else v
    return np.log10(v / vlaw(kind, ms + mg, R, a0, nu))
# ---------------- C3/C4 controls ----------------
def ring_gR(R, Rd=1.0, M=1.0):
    S0_ = M / (2 * np.pi * Rd**2)
    def phi(r):
        f = lambda a: -G_ * 2 * np.pi * a * S0_ * np.exp(-a / Rd) * (2 / (np.pi * (a + r))) * ellipk(4 * a * r / (a + r)**2)
        s = quad(f, 0, r, limit=400, epsabs=0, epsrel=1e-12)[0] + quad(f, r, 60 * Rd, limit=400, epsabs=0, epsrel=1e-12)[0]
        return s
    h = 1e-4 * R
    return (phi(R + h) - phi(R - h)) / (2 * h)
G_ = 1.0
rel = []
for x in (0.5, 1.0, 2.15, 5.0, 10.0):
    g_num = ring_gR(x); y = x / 2
    g_cf = 2 * y**2 * (i0(y)*k0(y) - i1(y)*k1(y)) / x          # units G M / Rd^2 with Rd=1, M=1: v^2 = 2 y^2[..], g=v^2/R
    rel.append(abs(g_num / g_cf - 1))
chk("C3a Freeman closed form vs independent ring integration (<1e-5)", max(rel) < 1e-5, "max rel diff %.2e" % max(rel))
xs = np.linspace(0.5, 6, 5501); yy = xs / 2; v2 = 2 * yy**2 * (i0(yy)*k0(yy) - i1(yy)*k1(yy)); j = np.argmax(v2)
chk("C3b Freeman peak 0.6218 sqrt(GM/Rd) at 2.15 Rd", abs(np.sqrt(v2[j]) - 0.6218) < 0.002 and abs(xs[j] - 2.15) < 0.1, f"v_max {np.sqrt(v2[j]):.4f} at {xs[j]:.3f}")
Mt, Rt = 3e11, 30.0
newt = np.sqrt(G * Mt * MSUN / (Rt * KPC)) / 1e3
c4a = abs(vlaw("point", Mt, Rt, 1e-30, lambda y: np.ones_like(np.asarray(y, float))) / newt - 1) < 1e-12
Rbig = 1e7; dm = vlaw("point", 3e11, Rbig, A0C) ** 4 / (G * 3e11 * MSUN * A0C * 1e-12)
chk("C4 limits (Newton exact; deep MOND v^4=GMa0 at y~1e-6; nu_RAR(1)=1.582; P2(1)=sqrt2)",
    c4a and abs(dm - 1) < 1e-3 and abs(nu_mono(1.0) - 1.582) < 1e-3 and abs(nu_p2(1.0) - np.sqrt(2)) < 1e-12, f"deep ratio {dm:.6f}, nu_RAR(1) {float(nu_mono(1.0)):.4f}")
# ---------------- statistics ----------------
B_README, B_ERR = 0.076, 0.030
def mean_err(o, idx, ddof=1):
    x = o[idx]; N = x.sum() if x.dtype == bool else len(x)
    return x.mean() if x.dtype != bool else o[x].mean(), None
def sample_stat(o, m, ddof=1):
    x = o[m]; return x.mean(), x.std(ddof=ddof) / np.sqrt(len(x))
def floors(m, a0=A0C, nu=nu_mono):
    """quadrature components for a subset mask m (offsets without B)"""
    base = offs("point", a0, nu)[m].mean()
    br = [offs(k, a0, nu)[m].mean() for k in ("point", "freeman", "sphere")]
    fs = 0.5 * (max(br) - min(br))
    fM = 0.5 * abs(offs(ms=Mstar() * 10**0.2, a0=a0, nu=nu)[m].mean() - offs(ms=Mstar() * 10**-0.2, a0=a0, nu=nu)[m].mean())
    fG = 0.5 * abs(offs(mg=Mgas() * 10**0.1, a0=a0, nu=nu)[m].mean() - offs(mg=Mgas() * 10**-0.1, a0=a0, nu=nu)[m].mean())
    fR = 0.5 * abs(offs(R=Rf * 1.25, a0=a0, nu=nu)[m].mean() - offs(R=Rf * 0.75, a0=a0, nu=nu)[m].mean())
    return dict(structure=fs, Mstar=fM, gas=fG, radius=fR, B=B_ERR, tot=float(np.sqrt(fs**2 + fM**2 + fG**2 + fR**2 + B_ERR**2)))
def headline(m, B, a0=A0C, nu=nu_mono, ddof=1):
    o = offs("point", a0, nu); mu, se = sample_stat(o, m, ddof); fl = floors(m, a0, nu)
    sig = float(np.hypot(se, fl["tot"])); return dict(raw=float(mu), corr=float(mu - B), stat=float(se), floor=fl["tot"], sigma=sig, nsig=float((mu - B) / sig), comps=fl)
ALL = np.ones(15, bool)
res = {}
res["law15"] = headline(ALL, B_README); res["law4"] = headline(S0, B_README)
res["law15_alt"] = headline(ALL, B_README, A0A); res["law4_alt"] = headline(S0, B_README, A0A)
res["law15_a0_1.2e-10"] = headline(ALL, B_README, 1.2e-10)
res["law15_noflag"] = headline(flag == 0, B_README); res["law4_noflag"] = headline(S0 & (flag == 0), B_README)
res["law15_ddof0"] = headline(ALL, B_README, ddof=0); res["law4_ddof0"] = headline(S0, B_README, ddof=0)
# WISE colour subset (T-independent law): red = W2-W3<2.0 (nan -> blue)
Wred = np.array([(np.isfinite(W23[n]) and W23[n] < 2.0) for n in names]); res["law_WISEred"] = headline(Wred, B_README)
out["res"] = res
# ---------------- MC json ----------------
mcf = "cfg97_selbias_mc_results.json"
mc = json.load(open(mcf)) if os.path.exists(mcf) else None
B_mine = mc["B_mine"] if mc else float("nan")
if mc:
    mcpass = all(c[1] for c in mc["checks"] if not c[0].startswith("R1")) if not MUT else True
    chk("C5 selection MC: own controls pass and B_mine within 0.010 of 0.076", mcpass and abs(B_mine - 0.076) <= 0.010, f"B_mine {B_mine:.4f} (MATCH {mc['match_lo']:.4f}..{mc['match_hi']:.4f}, n={mc['n_match']})")
else:
    chk("C5 selection MC present", False, "no results json")
# ---------------- reproduction table ----------------
def tier(mine, tgt, sm=None, st=None):
    d = mine - tgt; dσ = None if (sm is None or st is None) else sm - st
    if abs(d) <= 0.0015 and (dσ is None or abs(dσ) <= 0.015): return "EXACT"
    if abs(d) <= 0.010 and (dσ is None or abs(dσ) <= 0.15): return "CLOSE"
    return "DIFFERENT"
R15, R4 = res["law15"], res["law4"]
rep = [
 ("15 raw law (canonical)", R15["raw"], 0.048, None, None),
 ("15 law corrected (canon)", R15["corr"], -0.028, R15["nsig"], -0.43),
 ("15 law sigma", R15["sigma"], 0.066, None, None),
 ("15 law corrected (alt)", res["law15_alt"]["corr"], -0.045, res["law15_alt"]["nsig"], -0.69),
 ("S0 raw law", R4["raw"], 0.080, None, None),
 ("S0 law corrected", R4["corr"], 0.004, R4["nsig"], 0.05),
 ("S0 law sigma", R4["sigma"], 0.071, None, None),
 ("15 law excl. 2 flagged", res["law15_noflag"]["corr"], -0.038, res["law15_noflag"]["nsig"], -0.60),
 ("15 law, WISE colours (law is colour-blind)", res["law15"]["corr"], -0.028, None, None),
]
print("\nREPRODUCTION vs CFG41 README (law side)")
out["repro"] = []
for n, a, b, sa, sb in rep:
    tr = tier(a, b, sa, sb); out["repro"].append(dict(q=n, mine=float(a), cfg41=b, nsig_mine=None if sa is None else float(sa), nsig_cfg41=sb, tier=tr))
    print(f"{n:44s} mine {a:+.3f}  CFG41 {b:+.3f}  diff {a-b:+.3f}  " + ("" if sa is None else f"[{sa:+.2f}s vs {sb:+.2f}s] ") + tr)
print("\nsigma components 15:", {k: round(v, 4) for k, v in R15["comps"].items()}, " stat", round(R15["stat"], 4))
print("sigma components S0:", {k: round(v, 4) for k, v in R4["comps"].items()}, " stat", round(R4["stat"], 4))
h1 = abs(R15["nsig"]) < 2; h2 = abs(R4["nsig"]) < 2
if not MUT:
    chk("H1 law fits the 15 after B (|n sigma|<2)", h1, f"{R15['corr']:+.3f} +- {R15['sigma']:.3f} ({R15['nsig']:+.2f} sigma)")
    chk("H2 law fits the four S0/S0a after B (|n sigma|<2)", h2, f"{R4['corr']:+.3f} +- {R4['sigma']:.3f} ({R4['nsig']:+.2f} sigma)")
else:
    chk("C6 MUTATE: H1 must FAIL under v x0.5", not h1, f"offset {R15['corr']:+.3f} ({R15['nsig']:+.2f} sigma)")
    chk("C6b MUTATE: H2 must FAIL", not h2, f"{R4['corr']:+.3f} ({R4['nsig']:+.2f} sigma)")
# ---------------- per-galaxy table ----------------
o = offs("point")
print("\nper galaxy (canonical, raw offset log v_flat/v_law): name S0 R_f v_f(tab) v_L(mine) nflat offset")
for i, n in enumerate(names):
    print(f"{n:9s} {'S0' if S0[i] else '  '} {Rf[i]:6.1f} {vf[i]:5.0f} {vL[i]:6.1f} {LL[n][2]:2d} {o[i]:+.3f}")
out["per_galaxy"] = [dict(name=n, S0=bool(S0[i]), Rf=float(Rf[i]), vflat=float(vf[i]), vL=float(vL[i]), nflat=LL[n][2], off=float(o[i])) for i, n in enumerate(names)]
# ---------------- rule consistency-only ----------------
fex = {"NGC1167": .31, "NGC5790": .31, "UGC12591": .78, "UGC12811": .49}
f4 = np.array([fex.get(n, 0.0) for n in names])
D1 = 0.5 * np.log10(1 + f4); D2 = -0.5 * np.log10(1 - f4)
tgt = 0.004 - (-0.105)
cons = dict(target_shift=tgt, D1=float(D1[S0].mean()), D2=float(D2[S0].mean()))
print("\nRULE consistency-only (f_ex taken from README as INPUT): README rule-minus-law shift on four =", round(tgt, 3), " D1 (1+f):", round(cons["D1"], 3), " D2 (1/(1-f)):", round(cons["D2"], 3))
out["rule_consistency"] = cons
out["rule_reproduced"] = False
# ---------------- A1: B size ----------------
Bset = {"0": 0.0, "B_mine": B_mine, "0.076 (CFG41)": 0.076, "0.058 (referee)": 0.058}
if mc and mc["attacks"].get("A1_Mstar_err_0.2", {}).get("centre") is not None: Bset["B_Mstar-err MC"] = mc["attacks"]["A1_Mstar_err_0.2"]["centre"]
A1 = {}
print("\nA1 dependence on B (canonical law; sigma as headline, B error kept 0.030)")
for k, B in Bset.items():
    a, b = headline(ALL, B), headline(S0, B); A1[k] = dict(B=B, c15=a["corr"], n15=a["nsig"], c4=b["corr"], n4=b["nsig"])
    print(f"  B={k:18s} {B:+.3f}: 15 {a['corr']:+.3f} ({a['nsig']:+.2f}s)   S0 {b['corr']:+.3f} ({b['nsig']:+.2f}s)")
out["A1"] = A1
# ---------------- A2: galaxy-specific B ----------------
from scipy.stats import norm
A2 = None
if mc:
    mr = [r for r in mc["grid"]["BASE"] if r["match"]]
    if mr:
        M_b = Mstar() + Mgas(); mm = 0.25 * np.log10(G * M_b * MSUN * 1.2e-10) - 3.0; zc = np.log10(300.0)
        bi = np.mean([[(r["s_int"]**2 / np.hypot(r["s_int"], r["s_w"])) * norm.pdf((mm[i] - zc) / np.hypot(r["s_int"], r["s_w"])) / norm.cdf((mm[i] - zc) / np.hypot(r["s_int"], r["s_w"])) for i in range(15)] for r in mr], axis=0)
        oo = offs("point"); a = oo.mean() - bi.mean(); a4 = oo[S0].mean() - bi[S0].mean()
        fl15, fl4 = R15["floor"], R4["floor"]
        A2 = dict(b_mean15=float(bi.mean()), b_mean4=float(bi[S0].mean()), corr15=float(a), corr4=float(a4), n15=float(a / np.hypot(R15["stat"], fl15)), n4=float(a4 / np.hypot(R4["stat"], fl4)), b_i=[float(x) for x in bi])
        print("\nA2 galaxy-specific bias b_i (avg over MC MATCH rows): mean over 15 %.3f, over S0 %.3f -> corrected law 15 %+.3f (%+.2fs), S0 %+.3f (%+.2fs)" % (bi.mean(), bi[S0].mean(), a, A2["n15"], a4, A2["n4"]))
out["A2"] = A2
# ---------------- A3: baryon conversion ----------------
A3 = {}
print("\nA3 HI-to-baryon / stellar conversions (shift of the raw mean offset relative to canonical, dex)")
base15, base4 = o.mean(), o[S0].mean()
for gm in (0.0, 1.0, 1.25, 1.5, 2.0):
    oo = offs(mg=Mgas() * gm); A3[f"gas x{gm}"] = (float(oo.mean() - base15), float(oo[S0].mean() - base4))
for nm, f in (("Ups 0.5", 0.5 / 0.6), ("Ups 0.7", 0.7 / 0.6)):
    oo = offs(ms=Mstar() * f); A3[nm] = (float(oo.mean() - base15), float(oo[S0].mean() - base4))
oo = offs(ms=10.0**lMsRC); A3["M* from RC decomposition"] = (float(oo.mean() - base15), float(oo[S0].mean() - base4))
for k, v in A3.items(): print(f"  {k:28s} 15 {v[0]:+.4f}   S0 {v[1]:+.4f}")
out["A3"] = A3
# ---------------- A4: inclination ----------------
A4 = {}
for i_deg in (45, 60, 75):
    A4[i_deg] = float(-(1 / np.tan(np.radians(i_deg))) * np.radians(3.0) / np.log(10))
print("\nA4 inclination: shift of v_flat for a +3 deg common error (dex):", {k: round(v, 4) for k, v in A4.items()})
out["A4"] = A4
# ---------------- A5: distance ----------------
rngD = np.random.default_rng(97)
Rf0, ms0, mg0 = Rf.copy(), Mstar(), Mgas(); sh15 = []; sh4 = []
for _ in range(4000):
    f = np.clip(1 + (dD / Dm) * rngD.standard_normal(15), 0.3, None)
    oo = offs(ms=ms0 * f**2, mg=mg0 * f**2, R=Rf0 * f)
    sh15.append(oo.mean() - base15); sh4.append(oo[S0].mean() - base4)
A5 = dict(rand15_mean=float(np.mean(sh15)), rand15_sd=float(np.std(sh15)), rand4_mean=float(np.mean(sh4)), rand4_sd=float(np.std(sh4)))
for s in (0.95, 1.05):
    oo = offs(ms=ms0 * s**2, mg=mg0 * s**2, R=Rf0 * s); A5[f"common_x{s}"] = (float(oo.mean() - base15), float(oo[S0].mean() - base4))
print("\nA5 distance:", {k: (np.round(v, 4) if not isinstance(v, float) else round(v, 4)) for k, v in A5.items()})
out["A5"] = A5
fl15p = float(np.sqrt(R15["sigma"]**2 + A5["rand15_sd"]**2 + (0.5*(abs(A5["common_x0.95"][0]) + abs(A5["common_x1.05"][0])))**2 + A4[60]**2))
fl4p = float(np.sqrt(R4["sigma"]**2 + A5["rand4_sd"]**2 + (0.5*(abs(A5["common_x0.95"][1]) + abs(A5["common_x1.05"][1])))**2 + A4[60]**2))
print(f"  floor+ (adds random D, common D 5%, inclination 3deg at 60): sigma15 {R15['sigma']:.3f} -> {fl15p:.3f}; sigma4 {R4['sigma']:.3f} -> {fl4p:.3f}")
out["floorplus"] = dict(s15=fl15p, s4=fl4p, n15=float(R15["corr"] / fl15p), n4=float(R4["corr"] / fl4p))
# ---------------- A6: leave-one-out ----------------
def loo(mask):
    idx = np.where(mask)[0]; full = o[idx].mean() - B_README; rows = []
    for j in idx:
        k = idx[idx != j]; rows.append((names[j], float(o[k].mean() - B_README)))
    v = np.array([r[1] for r in rows]); n = len(v); jk = np.sqrt((n - 1) / n * ((v - v.mean())**2).sum())
    return dict(full=float(full), rows=rows, lo=float(v.min()), hi=float(v.max()), jackknife_se=float(jk), sign_flip=bool(np.any(np.sign(v) != np.sign(full))))
out["A6_15"] = loo(ALL); out["A6_4"] = loo(S0)
for k, tag in (("A6_15", "15"), ("A6_4", "S0 four")):
    r = out[k]; print(f"\nA6 LOO {tag}: full {r['full']:+.3f}; range {r['lo']:+.3f}..{r['hi']:+.3f}; jackknife SE {r['jackknife_se']:.3f}; sign flip {r['sign_flip']}")
    print("   " + ", ".join(f"-{n} {v:+.3f}" for n, v in r["rows"]))
# ---------------- A7 ----------------
A7 = {}
for nm, kw in (("P2 kernel", dict(nu=nu_p2)), ("a0 1.2e-10", dict(a0=1.2e-10)), ("a0 alt 1.13e-10", dict(a0=A0A))):
    a = headline(ALL, B_README, **kw); b = headline(S0, B_README, **kw); A7[nm] = (a["corr"], a["nsig"], b["corr"], b["nsig"])
for k in ("freeman", "sphere"):
    oo = offs(k); A7[f"bracket {k} raw"] = (float(oo.mean()), float(oo[S0].mean()))
A7["bracket point raw"] = (float(o.mean()), float(o[S0].mean()))
w = (vf / dvf * np.log(10))**2; A7["inverse-variance weighted raw 15"] = (float((o * w).sum() / w.sum()), float(1 / np.sqrt(w.sum())))
print("\nA7:"); [print(f"  {k}: {v}") for k, v in A7.items()]
out["A7"] = {k: [float(x) for x in v] for k, v in A7.items()}
# ---------------- CFG53 law-side shapes ----------------
def slope(R, V, dV, wts=None):
    x = np.log(R); y = np.log(V); w = (V / dV)**2 if wts is None else wts
    xb = (w * x).sum() / w.sum(); yb = (w * y).sum() / w.sum(); sxx = (w * (x - xb)**2).sum()
    return (w * (x - xb) * (y - yb)).sum() / sxx, 1 / np.sqrt(sxx)
def shape(ms=None, kind="point", a0=A0C):
    ms = Mstar() if ms is None else ms; res_ = []
    for i, n in enumerate(names):
        c = curves[n]; keep = c[:, 0] >= c[:, 0].max() / 2
        R, V, dV = c[keep, 0], c[keep, 1], c[keep, 2]
        if len(R) < 3: res_.append((np.nan, np.nan)); continue
        so, se = slope(R, V, dV); w = (V / dV)**2
        vl = vlaw(kind, ms[i] + Mgas()[i], R, a0)
        sl, _ = slope(R, vl, dV, wts=w); res_.append((so - sl, se * np.sqrt(2)))
    return np.array(res_)
sh = shape(); okm = np.isfinite(sh[:, 0]); red = S0 & okm; blue = (~S0) & okm
def grp(m): return float(sh[m, 0].mean()), float(np.sqrt((sh[m, 1]**2).sum()) / m.sum())
sr, sb = grp(red), grp(blue)
Dm_lo = shape(ms=Mstar() * 10**-0.2); Dm_hi = shape(ms=Mstar() * 10**0.2)
print("\nCFG53 law-side shape (mine): red %+.3f +- %.3f ; blue %+.3f +- %.3f ; red abs %.2f sigma ; points-used red/blue %d/%d galaxies" % (sr[0], sr[1], sb[0], sb[1], sr[0]/sr[1], red.sum(), blue.sum()))
print("   M_* +-0.2 dex moves red by %.4f, blue by %.4f" % (0.5*abs(np.nanmean(Dm_hi[red, 0]) - np.nanmean(Dm_lo[red, 0])), 0.5*abs(np.nanmean(Dm_hi[blue, 0]) - np.nanmean(Dm_lo[blue, 0]))))
print("   CFG53: red +0.014 +- 0.124 ; blue +0.052 +- 0.041 ; red absolute +0.11 sigma vs the law")
out["shape"] = dict(red=sr, blue=sb, cfg53_red=(0.014, 0.124), cfg53_blue=(0.052, 0.041))
out["checks"] = checks
json.dump(out, open(f"cfg97_massive_spirals_hi{TAG}_results.json", "w"), indent=1, default=float)
fails = [c[0] for c in checks if not c[1]]
print("\nFAILED:", fails); sys.exit(1 if fails else 0)
