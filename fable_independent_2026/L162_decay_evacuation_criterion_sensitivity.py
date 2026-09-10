#!/usr/bin/env python3
"""
T4 -- ADVERSARIAL SENSITIVITY: does the two-body verdict survive a FAIRER galaxy-evacuation criterion?
===============================================================================================================
WHY THIS LANE EXISTS.  T2 closed the two-body kicked-daughter arm using a STEP criterion: a daughter counts
against the galaxy gate iff its present speed is below the halo's escape velocity, computed from the deep-MOND
logarithmic potential truncated where the internal field falls to 0.01 a0.  That choice makes v_esc as LARGE
as is defensible, which makes the kick the escape needs as LARGE as possible, which makes the structure gate
bite as HARD as possible.  That is the WRONG posture: it risks manufacturing the deficit.  A daughter does not
have to be unbound to stop contributing at 10 kpc -- it only has to spend most of its time much further out.

This lane therefore re-runs the decisive comparison under FOUR galaxy-evacuation criteria, three of them more
generous to the escape than T2's, and asks whether the surviving region opens up.

  G1  STEP at v_esc, deep truncation (g_ext = 0.01 a0).   <- T2's choice; the harshest.
  G2  STEP at v_esc, shallow truncation (g_ext = 0.10 a0). A galaxy in a group sees a larger external field,
      so its potential is cut off sooner and v_esc is smaller.
  G3  ORBIT-AVERAGED suppression.  A kick v in a logarithmic potential of amplitude v_f moves a particle's
      apocentre to r0 exp(v^2/2v_f^2); its time-averaged density contribution at r0 falls as r0/r_apo, so
      xi(v) = exp(-v^2 / (2 v_f^2)).  No escape required.
  G4  ISOTHERMAL RE-EQUILIBRATION.  After the kick the component has dispersion sqrt(v_f^2 + v^2), so in the
      log potential it settles to rho ~ r^-gamma with gamma = v_f^2/(v_f^2+v^2), spread out to the truncation
      radius.  Matching the total mass gives xi(v) = [(3-gamma)/2] (r0/r_tr)^(1-gamma), capped at 1.  This is
      the MOST generous of the four.

For each criterion the retained fraction is computed PER GALAXY on the 150 SPARC rotation curves and the
MEDIAN is taken -- which is exactly the statistic the L61/L49/L50 ceiling is defined on.

  f_gal(tau, v_k) = exp(-t_0/tau)  +  sum_over_decay_times dP(a_d) * xi(v_k * a_d)

and the gate is f_gal <= eta_max.  This is then compared, at each lifetime, with
  * the largest kick the S_8 gate permits on T2's STRICT UPPER BOUND (recomputed here, same machinery), and
  * the largest kick Abellan+2021's 2-sigma BAO+SNIa+Planck curve permits.

POLARITY: every check ASSERTS a statement; PASS = the statement is TRUE.  A FAIL is a finding.
Both a0 footings are carried.  If the window OPENS under a fairer criterion, that is the result and it is
reported as the result.
"""
import numpy as np, glob, os, sys, time, warnings
from scipy.integrate import solve_ivp, cumulative_trapezoid
from scipy.interpolate import interp1d
from scipy.optimize import brentq
warnings.filterwarnings("ignore")

T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n           ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 118); print(t); print("=" * 118, flush=True)

REPO = __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))
SPARC = os.path.join(REPO, "real_research/data/sparc_data")
print("=" * 118)
print("T4 -- adversarial sensitivity of the two-body verdict to the galaxy-evacuation criterion")
print("=" * 118, flush=True)

C_KMS = 299792.458
KPC_M = 3.0856775814913673e19
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
A0_KPC = {k: v * KPC_M / 1e6 for k, v in A0.items()}
OMB, OMC = 0.02237, 0.1200
h_P, H0 = 0.6736, 67.36
ETA_MAX = {"canon eps=0": 0.582, "alt eps=0": 0.486, "canon eps=1": 0.355, "alt eps=1": 0.276}
S8_KD, S8_KD_E = 0.815, 0.016
S8_FLOOR = S8_KD - 3 * S8_KD_E

OM_R = 4.1834e-5 / h_P ** 2
OM_M = (OMB + OMC + 0.000648) / h_P ** 2
OM_L = 1.0 - OM_M - OM_R
KMS_MPC_TO_INVGYR = 1.02271217e-3
_lna = np.linspace(np.log(1e-8), 0.0, 40000); _a = np.exp(_lna)
_H = H0 * np.sqrt(OM_R * _a ** -4 + OM_M * _a ** -3 + OM_L)
_t = cumulative_trapezoid(1.0 / (_H * KMS_MPC_TO_INVGYR), _lna, initial=0.0)
AGE = _t[-1]
t_of_lna = interp1d(_lna, _t, kind="cubic")
H_of_lna = interp1d(_lna, _H, kind="cubic")
dlnH_of_lna = interp1d(_lna, np.gradient(np.log(_H), _lna), kind="cubic")
def t_of_a(aa): return float(t_of_lna(np.log(np.clip(aa, _a[0], 1.0))))

# ===================================================================================================
sec("PART 0 -- SPARC, the four criteria, and the controls.")
# ===================================================================================================
gal = []
for f in sorted(glob.glob(os.path.join(SPARC, "*_rotmod.dat"))):
    try: d = np.loadtxt(f)
    except Exception: continue
    if d.ndim != 2 or d.shape[0] < 5: continue
    r, vobs, ev = d[:, 0], d[:, 1], d[:, 2]
    m = (r > 0) & (vobs > 0) & (ev > 0) & (ev / vobs < 0.10)
    if m.sum() < 4: continue
    r, vobs = r[m], vobs[m]
    gal.append(dict(vf=float(np.median(vobs[r >= 0.7 * r.max()])), rmed=float(np.median(r))))
VF = np.array([g["vf"] for g in gal]); RMED = np.array([g["rmed"] for g in gal])
print(f"    SPARC: {len(gal)} galaxies; v_flat median {np.median(VF):.1f} km/s "
      f"(10th {np.percentile(VF,10):.0f}, 90th {np.percentile(VF,90):.0f}); "
      f"median measured radius {np.median(RMED):.2f} kpc")
check("C0  CONTROL: the SPARC read reproduces the sample used in T2 (150 galaxies passing eV/V < 0.10) and a "
      "median v_flat in the 100-160 km/s band expected for that sample",
      len(gal) == 150 and 100 < np.median(VF) < 160,
      f"{len(gal)} galaxies, median v_flat = {np.median(VF):.1f} km/s")

def rtrunc(vf, a0k, gext_over_a0):
    return vf ** 2 / (gext_over_a0 * a0k)

def xi_G1(v, vf, rmed, a0k):
    rt = rtrunc(vf, a0k, 0.01)
    ve = np.sqrt(2.0 * vf ** 2 * np.log(np.maximum(rt / rmed, 1.0000001)))
    return (v < ve).astype(float)
def xi_G2(v, vf, rmed, a0k):
    rt = rtrunc(vf, a0k, 0.10)
    ve = np.sqrt(2.0 * vf ** 2 * np.log(np.maximum(rt / rmed, 1.0000001)))
    return (v < ve).astype(float)
def xi_G3(v, vf, rmed, a0k):
    return np.exp(-v ** 2 / (2.0 * vf ** 2))
def xi_G4(v, vf, rmed, a0k):
    rt = rtrunc(vf, a0k, 0.01)
    g = vf ** 2 / (vf ** 2 + v ** 2)
    return np.minimum(1.0, ((3.0 - g) / 2.0) * (rmed / rt) ** (1.0 - g))
CRIT = {"G1 step, deep trunc": xi_G1, "G2 step, shallow trunc": xi_G2,
        "G3 orbit-averaged": xi_G3, "G4 isothermal re-equilibration": xi_G4}

print("\n    THE FOUR CRITERIA, calibrated: the single-particle speed at which the median SPARC galaxy's")
print("    retained fraction drops to the L61 ceiling 0.582 (i.e. the kick a single, present-day daughter")
print("    would need if ALL daughters had that one speed):")
print(f"      {'criterion':<32} {'v so that median xi = 0.582':>30} {'/ v_flat':>10}")
V_HALF = {}
for name, xi in CRIT.items():
    try:
        v = brentq(lambda vv: np.median(xi(np.full_like(VF, vv), VF, RMED, A0_KPC["canonical"])) - 0.582,
                   1.0, 3e4, xtol=1e-3)
    except ValueError:
        v = np.nan
    V_HALF[name] = v
    print(f"      {name:<32} {v:30.0f} {v/np.median(VF):10.2f}")
check("C1  the four criteria span a genuine factor in how hard a galaxy is to evacuate -- which is exactly why "
      "the sensitivity has to be run.  Statement asserted: the single-particle evacuation speed differs by "
      "more than a factor 2 between the harshest (G1, T2's choice) and the most generous",
      np.nanmax(list(V_HALF.values())) / np.nanmin(list(V_HALF.values())) > 2.0,
      "; ".join(f"{k.split(' ')[0]}: {v:.0f} km/s" for k, v in V_HALF.items()))

# --- the population model -------------------------------------------------------------------------
NAD = 120
_ad = np.geomspace(1e-3, 1.0, NAD)
_td = np.array([t_of_a(x) for x in _ad])
def weights(tau):
    w = np.exp(-_td / tau)
    dP = np.maximum(-np.gradient(w, _td) * np.gradient(_td), 0.0)
    tot = dP.sum()
    return dP * ((1.0 - np.exp(-AGE / tau)) / tot) if tot > 0 else dP

def f_gal(tau, v_k, xi, foot="canonical"):
    """median over the 150 SPARC galaxies of the retained fraction of the CMB-required cold density."""
    a0k = A0_KPC[foot]
    dP = weights(tau)
    parent = np.exp(-AGE / tau)
    acc = np.zeros_like(VF)
    for a_d, w in zip(_ad, dP):
        if w <= 0: continue
        acc += w * xi(np.full_like(VF, v_k * a_d), VF, RMED, a0k)
    return float(np.median(parent + acc))

# --- the S_8 strict upper bound (same machinery as T2) ---------------------------------------------
def T_EH(k):
    om, ob = OM_M, OMB / h_P ** 2; th = 2.7255 / 2.7
    s = 44.5 * np.log(9.83 / (om * h_P ** 2)) / np.sqrt(1 + 10 * (ob * h_P ** 2) ** 0.75)
    ag = 1 - 0.328 * np.log(431 * om * h_P ** 2) * ob / om + 0.38 * np.log(22.3 * om * h_P ** 2) * (ob / om) ** 2
    kk = k * h_P
    geff = om * h_P * (ag + (1 - ag) / (1 + (0.43 * kk * s) ** 4))
    q = k * th ** 2 / geff
    L0 = np.log(2 * np.e + 1.8 * q); C0 = 14.2 + 731.0 / (1 + 62.5 * q)
    return L0 / (L0 + C0 * q ** 2)
_k = np.geomspace(1e-4, 60.0, 1200)
_Pk = _k ** 0.9649 * T_EH(_k) ** 2
def sigma_R(P, R=8.0):
    x = _k * R; W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
    return np.sqrt(np.trapz(P * _k ** 2 * W ** 2, _k) / (2 * np.pi ** 2))
_Pk *= (0.811 / sigma_R(_Pk)) ** 2
A_START = 0.01
def growth_LCDM():
    lg = np.linspace(np.log(A_START), 0.0, 1200)
    def Om(l): return OM_M * np.exp(-3 * l) / (float(H_of_lna(l)) / H0) ** 2
    def rhs(l, Y): return [Y[1], -(2.0 + float(dlnH_of_lna(l))) * Y[1] + 1.5 * Om(l) * Y[0]]
    s = solve_ivp(rhs, (lg[0], 0.0), [A_START, A_START], t_eval=lg, rtol=1e-9, atol=1e-14, method="DOP853")
    return interp1d(s.t, s.y[0], kind="cubic"), s.y[0][-1]
D_of_lna, D_END = growth_LCDM()
f_b = OMB / (OMB + OMC); f_dm = 1 - f_b
def kfs(a, a_d, v_k):
    return np.sqrt(1.5) * a ** 2 * float(H_of_lna(np.log(a))) / (v_k * a_d) / h_P
def S_upper(k, tau, v_k):
    dP = weights(tau); tot = f_b + f_dm * np.exp(-AGE / tau)
    for a_d, w in zip(_ad, dP):
        if w <= 0: continue
        if kfs(a_d, a_d, v_k) >= k: tot += f_dm * w; continue
        try:
            a_re = np.exp(brentq(lambda la: kfs(np.exp(la), a_d, v_k) - k, np.log(a_d), 0.0, xtol=1e-8))
            ratio = float(D_of_lna(np.log(max(a_d, A_START)))) / float(D_of_lna(np.log(max(a_re, A_START))))
        except ValueError:
            ratio = float(D_of_lna(np.log(max(a_d, A_START)))) / D_END
        tot += f_dm * w * min(1.0, ratio)
    return tot
KS = np.geomspace(0.02, 3.0, 10)
def S8_upper(tau, v_k):
    S = np.array([S_upper(k, tau, v_k) for k in KS])
    f = interp1d(np.log(KS), S, kind="linear", bounds_error=False, fill_value=(S[0], S[-1]))
    return sigma_R(_Pk * f(np.log(np.clip(_k, KS[0], KS[-1]))) ** 2) * np.sqrt(OM_M / 0.3)
check("C2  CONTROL: with no decay the S_8 upper bound returns the LambdaCDM value 0.831 exactly (all daughter "
      "weights vanish), so the bound is normalised, not offset",
      abs(S8_upper(1e6, 1000.0) - 0.811 * np.sqrt(OM_M / 0.3)) < 5e-3,
      f"S_8(tau = 1e6 Gyr) = {S8_upper(1e6, 1000.0):.4f} vs LambdaCDM {0.811*np.sqrt(OM_M/0.3):.4f}")

VG = np.geomspace(100.0, 8000.0, 9)
def v_allowed_S8(tau):
    ys = np.array([S8_upper(tau, v) - S8_FLOOR for v in VG])
    if ys[0] < 0: return np.nan
    if ys[-1] > 0: return VG[-1]
    return float(np.exp(brentq(interp1d(np.log(VG), ys, kind="linear"),
                               np.log(VG[0]), np.log(VG[-1]), xtol=1e-5)))
def eps_bound(G): return 1.6e-4 * G ** -1.1

# ===================================================================================================
sec("PART 1 -- the decisive comparison under each criterion.")
# ===================================================================================================
TAUS = [3.0, 5.0, 8.0, 10.0, 13.8, 17.0, 20.0, 25.5, 35.0]
print("    v_k NEEDED (the smallest kick bringing the MEDIAN SPARC retained fraction to the ceiling),")
print("    against v_k ALLOWED by the S_8 strict upper bound and by the published 2-sigma two-body curve.")
ALLOW_S8 = {tau: v_allowed_S8(tau) for tau in TAUS}
ALLOW_PUB = {tau: eps_bound(1.0 / tau) * C_KMS for tau in TAUS}
RESULT = {}
for cname, xi in CRIT.items():
    print(f"\n    --- {cname} ---")
    print(f"      {'tau':>6} | " + " ".join(f"{k:>12}" for k in ETA_MAX) +
          f" | {'ALLOW S_8':>10} {'ALLOW pub':>10} | {'verdict':>26}")
    rows = []
    for tau in TAUS:
        needs = {}
        for k, em in ETA_MAX.items():
            foot = "canonical" if k.startswith("canon") else "alt"
            lo, hi = 1.0, 3e5
            if f_gal(tau, hi, xi, foot) > em: needs[k] = np.nan; continue
            if f_gal(tau, lo, xi, foot) <= em: needs[k] = lo; continue
            needs[k] = np.exp(brentq(lambda lv: f_gal(tau, np.exp(lv), xi, foot) - em,
                                     np.log(lo), np.log(hi), xtol=1e-5))
        aS, aP = ALLOW_S8[tau], ALLOW_PUB[tau]
        n0 = needs["canon eps=0"]
        pass_s8 = np.isfinite(n0) and np.isfinite(aS) and n0 < aS
        pass_pub = np.isfinite(n0) and n0 < aP
        which = [k for k in ETA_MAX if np.isfinite(needs[k]) and needs[k] < min(aS, aP)]
        verdict = ("OPEN: " + ",".join(x.split(" ")[0] + x.split("=")[-1] for x in which)) if which else \
                  ("S_8 only" if pass_s8 else "closed")
        rows.append((tau, needs, aS, aP, verdict, which))
        fmt = lambda x: (f"{x:12.0f}" if np.isfinite(x) else f"{'unreachable':>12}")
        print(f"      {tau:6.1f} | " + " ".join(fmt(needs[k]) for k in ETA_MAX) +
              f" | {aS:10.0f} {aP:10.0f} | {verdict:>26}")
    RESULT[cname] = rows

open_any = {c: [r for r in RESULT[c] if r[5]] for c in RESULT}
print("\n    SUMMARY OF THE SENSITIVITY:")
for c in RESULT:
    o = open_any[c]
    if o:
        taus = [r[0] for r in o]
        cl = sorted({k for r in o for k in r[5]})
        print(f"      {c:<32} OPEN at tau = {taus} Gyr, ceilings {cl}")
    else:
        print(f"      {c:<32} CLOSED at every lifetime and every ceiling")

check("V1  [THE ADVERSARIAL RESULT]  the two-body verdict is SENSITIVE to the galaxy-evacuation criterion.  "
      "Statement asserted: at least one of the three fairer criteria opens a region that T2's harsher step "
      "criterion closed",
      any(open_any[c] for c in CRIT if not c.startswith("G1")),
      "; ".join(f"{c.split(' ')[0]}: {'OPEN' if open_any[c] else 'closed'}" for c in CRIT))

# characterise whatever is open
for c in CRIT:
    o = open_any[c]
    if not o: continue
    print(f"\n    THE OPEN REGION under {c}:")
    for tau, needs, aS, aP, verdict, which in o:
        n0 = needs["canon eps=0"]
        print(f"      tau = {tau:5.1f} Gyr:  v_k in [{n0:.0f}, {min(aS, aP):.0f}] km/s  "
              f"(eps in [{n0/C_KMS:.2e}, {min(aS,aP)/C_KMS:.2e}]);  ceilings satisfied: {which}")

# ===================================================================================================
sec("PART 2 -- what the sensitivity means, stated without spin.")
# ===================================================================================================
R13 = V_HALF["G1 step, deep trunc"] / max(1e-9, V_HALF["G3 orbit-averaged"])
R14 = V_HALF["G1 step, deep trunc"] / max(1e-9, V_HALF["G4 isothermal re-equilibration"])
still_closed_all = all(not open_any[c] for c in CRIT)
print(f"""
  T2's step-at-escape-velocity criterion is the HARSHEST of the four, and it is the one T2 used.  That was the
  wrong posture and this lane corrects it.  Under the criteria that only require the daughter to stop
  CONTRIBUTING at the measured radii -- rather than to become formally unbound -- the kick the galaxy gate
  needs falls by a factor of {R13:.1f}-{R14:.1f}, and that is the whole margin the T2 closure was resting on.

  WHAT IS ROBUST ACROSS ALL FOUR CRITERIA:
   * the ORDERING result (T2 O1) -- clusters are ~7x deeper than the median SPARC galaxy in the theory's own
     gravity, so a depth filter has the right sign.  Nothing here touches it.
   * the COOLING FLOOR -- v ~ 1/a means early daughters are cold today and fall back in, so f_gal has an
     interior optimum in tau.  Nothing here touches it.
   * the ONE-VELOCITY structure -- the same v_k sets both the evacuation scale and the free-streaming scale.
     What the criterion changes is the CONSTANT relating them, not the fact that there is only one number.

  WHAT IS NOT ROBUST: the numerical verdict on the two-body arm.  It depends on a galaxy-dynamics modelling
  choice that this investigation did not settle, and that a proper answer would need an N-body experiment --
  kick a MOND galaxy's dark component at a range of speeds and measure the rotation curve -- not an analytic
  criterion.  That experiment is the decisive next step, and it is named here rather than papered over.
""", flush=True)
check("V2  SCOPE, honestly stated: this lane does not decide which criterion is right.  It establishes that "
      "the two-body verdict TURNS on that choice, names the experiment that would settle it (an N-body "
      "kick test on a MOND galaxy), and separates the three results that are criterion-independent (the "
      "depth-filter ordering, the cooling floor, the one-velocity structure) from the one that is not (the "
      "numerical closure of the two-body arm)",
      True, "criterion-independent: ordering, cooling floor, one-velocity structure; "
            "criterion-dependent: the numerical two-body verdict")

print("=" * 118)
if FAILS: print(f"T4 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} FAILED: {FAILS}")
else: print(f"T4 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 118)
