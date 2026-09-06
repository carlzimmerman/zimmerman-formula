#!/usr/bin/env python3
"""
g03x -- swapping the kernel to nu_RAR: the generalised carrier theorem and the Solar-System gate
===================================================================================================
g03w showed that the bounded-boost ceiling selects nu_RAR over the exponential carrier this action currently
carries.  Two gates must be passed before the swap can be made.

(1) THE GENERALISED CARRIER THEOREM.  A matter-sourced scalar obeys div[J_Y grad phi] = 4 pi G rho, so on a sphere
    J_Y(g_phi) g_phi = g_N: the scalar force g_phi must be a SINGLE-VALUED, monotone function of g_N, and its
    longitudinal stiffness d g_N / d g_phi must be positive or the static problem is ill-posed (g03j K2).  With
    g_phi = a0 Delta(s), s = g_N/a0, the stiffness is exactly 1/Delta'(s).  Therefore

        the scalar can carry a kernel only up to the MAXIMUM of Delta, and must saturate at C a0 above it.

    This is the SAME statement as the bounded-boost theorem of g03u: Delta is bounded, so it has a maximum, so the
    map s -> Delta(s) is non-invertible beyond it.  The saturation is therefore UNIVERSAL, not a defect peculiar to
    the exponential kernel -- and every kernel leaves a CONSTANT residual scalar force C a0 at high acceleration,
    which is exactly what the Solar System must screen.  nu_RAR's constant is 1.76x the exponential carrier's, so
    the swap that helps the rotation curves costs Solar-System screening.  That trade is what this script prices.

(2) THE SOLAR-SYSTEM GATE.  The same three gates and the same machinery as g03b: the Park 2026 Q2 ceiling, the
    phantom mass inside Saturn's orbit, and the alpha = 1 sunward ephemeris gate, evaluated on the phantom density
    of the chosen kernel with one Helmholtz output filter of length xi, at three external-field inputs and both
    footings.  Four kernels are run through it: the exponential inverse partner (which reproduces g03b's published
    floors and so validates the machinery), the exponential CARRIED (with its saturation), nu_RAR, and nu_RAR
    CARRIED.  The floor in xi is read off the same tabulated grid, refined.

Checks that can fail:
  Y1 [theorem]    the stiffness d g_N/d g_phi equals 1/Delta'(s) and changes sign exactly at the maximum of Delta,
                  for BOTH kernels: the carrier theorem is the bounded-boost theorem.
  Y2 [saturation] nu_RAR's saturation point and constant residual force, against the exponential carrier's.
  Y3 [validation] run with the exponential inverse partner the gate reproduces g03b's published floors (0.03 pc
                  canonical, 0.05 pc alt) -- if this fails the machinery has been mis-wired and nothing below counts.
  Y4 [GATE]       the xi floor for nu_RAR CARRIED, both footings, all three external-field inputs.
  Y5 [verdict]    whether the nu_RAR floor stays inside the wide-binary window the pre-registration assumes.
"""
import math, sys, os, io, contextlib, numpy as np, warnings; warnings.filterwarnings("ignore")
T0 = __import__("time").time()
HERE = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(HERE, "g02_filtered_efe.py")).read()
head = src[:src.index("# ---------------------------------------------------------------- 3. the scans")]
g = {"__file__": os.path.join(HERE, "g02_filtered_efe.py")}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(head, "g02head", "exec"), g)
PC, GM, A0, eN_of, phantom_density, observables = g["PC"], g["GM"], g["A0"], g["eN_of"], g["phantom_density"], g["observables"]
Q2_CEIL, M_SAT_BOUND, A_SUNWARD, PLANETS, R_SAT, MSUN = g["Q2_CEIL"], g["M_SAT_BOUND"], g["A_SUNWARD"], g["PLANETS"], g["R_SAT"], g["MSUN"]
NU_EXP = g["nu"]                                                             # the exponential inverse partner, as published
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
print("="*118); print("g03x -- nu_RAR as the carried kernel: the generalised carrier theorem and the Solar-System gate"); print("="*118, flush=True)

# ---------------- the four kernels, as nu(s) with s = g_N/a0 ----------------
SS = np.logspace(-8, 8, 800001)
D_exp = SS*(np.asarray(NU_EXP(SS)) - 1.0)                                     # Delta(s) for the exponential partner
D_rar = SS*(1/(1 - np.exp(-np.sqrt(SS))) - 1.0)
i_e = int(np.nanargmax(D_exp)); i_r = int(np.nanargmax(D_rar))
C_exp, s_exp = float(D_exp[i_e]), float(SS[i_e]); C_rar, s_rar = float(D_rar[i_r]), float(SS[i_r])
print(f"  Delta(s) maxima:  exponential partner C = {C_exp:.4f} at g_N = {s_exp:.4f} a0;   nu_RAR C = {C_rar:.4f} at g_N = {s_rar:.3f} a0")
def nu_rar(s):
    s = np.asarray(s, float); return 1/(1 - np.exp(-np.sqrt(np.maximum(s, 1e-300))))
def nu_rar_carried(s):
    s = np.asarray(s, float); return np.where(s <= s_rar, nu_rar(s), 1 + C_rar/np.maximum(s, 1e-300))
def nu_exp_carried(s):
    s = np.asarray(s, float); return np.where(s <= s_exp, np.asarray(NU_EXP(s)), 1 + C_exp/np.maximum(s, 1e-300))

# ---------------- Y1: the carrier theorem IS the bounded-boost theorem ----------------
def stiffness(D):                                                             # d g_N/d g_phi = ds/dDelta = 1/Delta'(s)
    dD = np.gradient(D, SS); return 1.0/np.where(np.abs(dD) < 1e-300, np.nan, dD)
st_e, st_r = stiffness(D_exp), stiffness(D_rar)
def zero_cross(D, smax):                                                      # the sign change of Delta'(s) nearest the maximum
    dD = np.gradient(D, SS); w = (SS > 0.2*smax) & (SS < 5*smax); idx = np.where(w)[0]
    j = idx[np.nanargmin(np.abs(dD[idx]))]; return float(SS[j])
sign_flip_e = zero_cross(D_exp, s_exp); sign_flip_r = zero_cross(D_rar, s_rar)
ok1 = (np.nanmedian(st_e[SS < 0.5*s_exp]) > 0 and np.nanmedian(st_e[(SS > 2*s_exp) & (SS < 20*s_exp)]) < 0
       and np.nanmedian(st_r[SS < 0.5*s_rar]) > 0 and np.nanmedian(st_r[(SS > 2*s_rar) & (SS < 20*s_rar)]) < 0)
print(f"\n  Y1  stiffness d g_N/d g_phi = 1/Delta'(s): positive below each maximum, NEGATIVE above it (a gradient instability for any")
print(f"      single-valued scalar Lagrangian).  Sign change at g_N = {sign_flip_e:.4f} a0 (exponential) and {sign_flip_r:.3f} a0 (nu_RAR), i.e. exactly at the maxima.")
check("Y1 [theorem] for BOTH kernels the scalar's longitudinal stiffness is positive below the maximum of Delta and negative above it, so the carrier theorem is the bounded-boost theorem and the saturation is universal, not peculiar to the exponential kernel",
      ok1, f"sign change at {sign_flip_e:.4f} a0 (exp, max at {s_exp:.4f}) and {sign_flip_r:.3f} a0 (nu_RAR, max at {s_rar:.3f})")

# ---------------- Y2: the price of the swap ----------------
a0c = A0["canonical"]
print(f"\n  Y2  the constant residual scalar force each carried kernel leaves at high acceleration:")
print(f"      exponential carrier: C a0 = {C_exp*a0c:.3e} m/s^2 = {C_exp*a0c/A_SUNWARD:.0f} x the alpha = 1 sunward gate")
print(f"      nu_RAR carried:      C a0 = {C_rar*a0c:.3e} m/s^2 = {C_rar*a0c/A_SUNWARD:.0f} x the same gate   ({C_rar/C_exp:.2f}x the exponential's)")
check("Y2 [saturation] nu_RAR's carried kernel leaves a constant residual force 1.5-2x the exponential carrier's, so the kernel swap that helps the rotation curves makes the Solar-System screening harder, and by a quantified factor",
      1.4 < C_rar/C_exp < 2.2, f"C(nu_RAR)/C(exp) = {C_rar/C_exp:.3f}; both are ~10^3 times the sunward gate before screening")

# ---------------- the gate ----------------
XIS = np.array([0.01, 0.02, 0.03, 0.04, 0.05, 0.07, 0.1, 0.15, 0.3, 1.0])*PC
FIELDS = (("2.00", 2.00e-10), ("2.32", 2.32e-10), ("2.64", 2.64e-10))
def run_gate(nufun, label, verbose_foot=None, grid=None):
    g["nu"] = nufun                                                           # phantom_density and observables resolve nu in this namespace
    out = {}
    for foot, a0 in A0.items():
        rM = math.sqrt(GM/a0); adm = {}
        for tag, gobs in FIELDS:
            eN = eN_of(gobs, a0)
            for xi in (grid if grid is not None else XIS):
                r, th, rho = phantom_density(MSUN, 0.0, "gauss", eN, a0, 1e-4*rM, 1e4*rM)
                ob = observables(r, th, rho, xi, "helmholtz", a0)
                Msat = float(np.interp(R_SAT, r, ob["Menc"]))
                gr = max(abs(float(np.interp(rp, r, ob["g_r"]))) for rp in PLANETS.values())
                adm[(tag, xi)] = (abs(ob["Q2"]) < Q2_CEIL and Msat < M_SAT_BOUND and gr < A_SUNWARD)
                if verbose_foot == foot and tag == "2.32":
                    print(f"      {label:22s} {foot:9s} xi = {xi/PC:5.2f} pc: Q2/ceil {abs(ob['Q2'])/Q2_CEIL:7.3f} | M/bound {Msat/M_SAT_BOUND:7.3f} | g_r/gate {gr/A_SUNWARD:7.3f}  {'admissible' if adm[(tag, xi)] else 'EXCLUDED'}", flush=True)
        ok = [xi for xi in (grid if grid is not None else XIS) if all(adm[(t, xi)] for t, _ in FIELDS)]
        out[foot] = min(ok)/PC if ok else None
    g["nu"] = NU_EXP
    return out

print(f"\n  Y3  validation: the machinery must reproduce g03b's published floors with the exponential inverse partner")
G03B_GRID = np.array([0.01, 0.02, 0.03, 0.05, 0.1, 0.3, 1.0])*PC             # g03b's own tabulated grid, for an exact comparison
F_exp_g03b = run_gate(NU_EXP, "exponential partner", grid=G03B_GRID)
F_exp = run_gate(NU_EXP, "exponential partner")
print(f"      on g03b's own grid: canonical {F_exp_g03b['canonical']} pc, alt {F_exp_g03b['alt']} pc   (g03b published 0.03 and 0.05)")
print(f"      on this script's finer grid: canonical {F_exp['canonical']} pc, alt {F_exp['alt']} pc  (the alt floor resolves to 0.04, a value absent from g03b's grid)")
check("Y3 [validation] run with the published exponential inverse partner on g03b's own tabulated grid this gate reproduces its published floors exactly, 0.03 pc canonical and 0.05 pc alt; on the finer grid used here the alt floor resolves to 0.04 pc, a value g03b did not tabulate",
      F_exp_g03b["canonical"] == 0.03 and F_exp_g03b["alt"] == 0.05, f"g03b grid {F_exp_g03b}; finer grid {F_exp}")

print(f"\n  Y4  the gate for each carried kernel (canonical footing, external field 2.32e-10 shown):")
F_expc = run_gate(nu_exp_carried, "exponential CARRIED", verbose_foot="canonical")
F_rar  = run_gate(nu_rar, "nu_RAR (unsaturated)")
F_rarc = run_gate(nu_rar_carried, "nu_RAR CARRIED", verbose_foot="canonical")
print(f"\n      {'kernel':24s} {'floor xi, canonical':>21s} {'floor xi, alt':>15s}")
for lab, F in (("exponential partner", F_exp), ("exponential CARRIED", F_expc), ("nu_RAR (unsaturated)", F_rar), ("nu_RAR CARRIED", F_rarc)):
    print(f"      {lab:24s} {str(F['canonical'])+' pc':>21s} {str(F['alt'])+' pc':>15s}")
ok4 = F_rarc["canonical"] is not None and F_rarc["alt"] is not None
check("Y4 [GATE] nu_RAR as the carried kernel has a NON-EMPTY admissible window in the coherence length at both footings and all three external-field inputs: the kernel swap survives the Solar System",
      ok4, f"nu_RAR carried floors: canonical {F_rarc['canonical']} pc, alt {F_rarc['alt']} pc; against the exponential carrier's {F_expc['canonical']} and {F_expc['alt']} pc")

# ---------------- Y5: the wide-binary consequence ----------------
print(f"\n  Y5  the coherence length also sets the wide-binary boost (g03g/g03h: gamma_v rises as xi falls, the registered")
print(f"      band is 1.16-1.23 and the candidate returned 1.032/1.040 at the PUBLISHED floors).  A higher floor means a smaller")
print(f"      boost and a gamma_v closer to Newton, which SHARPENS the contrast with the registered MOND band rather than")
print(f"      softening it -- but it also means the published gamma_v was computed at a floor that the carried kernel does")
print(f"      not actually permit, and must be recomputed at the corrected floors.")
if F_rarc["canonical"] and F_expc["canonical"]:
    print(f"      floor ratio nu_RAR/exponential: canonical {F_rarc['canonical']/F_expc['canonical']:.2f}x, alt {F_rarc['alt']/F_expc['alt']:.2f}x")
print(f"      CORRECTION FLAGGED: the repository's standing floors 0.03/0.05 pc were computed with the UNSATURATED inverse")
print(f"      partner; the kernel the scalar can actually carry saturates, and its floors are {F_expc['canonical']}/{F_expc['alt']} pc -- a factor {F_expc['canonical']/0.03:.1f}/{F_expc['alt']/0.05:.0f} higher.")
check("Y5 [verdict, reported] the nu_RAR floor is at most a factor 2 above the exponential carrier's, so the swap does not open a new Solar-System problem, but it does push the coherence length up and therefore the wide-binary boost down",
      ok4 and F_rarc["canonical"]/F_expc["canonical"] <= 2.0,
      f"floors move {F_expc['canonical']} -> {F_rarc['canonical']} pc (canonical) and {F_expc['alt']} -> {F_rarc['alt']} pc (alt)")
print(f"\n  caveats: this is g03b's linear-response PROXY (one Helmholtz output filter on an unfiltered source flux), not the")
print(f"  exact fourth-order nonlinear solve of g03d; the floors are read off a tabulated xi grid, so they are resolved to")
print(f"  the grid spacing; the three gates and their numerical bounds are inherited from g02 unchanged.  total {__import__('time').time()-T0:.0f}s")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
sys.exit(1 if FAILS else 0)
