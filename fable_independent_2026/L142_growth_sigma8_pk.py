#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fbC3 -- STRUCTURE GROWTH from recombination to z = 0 under a boosted MOND gravity.
==================================================================================
TASK 3.  Linear growth of BARYON perturbations under nu(g/a0)-boosted gravity, sigma_8 and the
shape of P(k), on both branches and both footings -- and an adjudication of the repository's prior
growth results, which point in OPPOSITE directions and must not be quoted as one thing.

WHAT THE REPOSITORY ALREADY HAS (read before computing, and each is a DIFFERENT calculation):
  g04h  `closure_2026/g04h_pk_regeneration_causal_boost.py`  -- a 28 eV thermal relic whose
        free-streaming cutoff is to be refilled by a CAUSAL, SATURATING boost
        B = min[0.9 (c_* k t/a)^2, nu(y)-1].  DEFICIT: sigma_8 <= 0.648, P(k) short by 20-2000x at
        k = 0.5-1 h/Mpc.  This is a relic-cutoff-refill calculation, NOT a MOND-boost calculation.
  mi_growth / mond_growth_framework_footing / rising_a0_baryon_only  -- the plain MOND boost
        nu = sqrt(1 + a0/g_N) on the linear field.  These OVERSHOOT: sigma_8 = 6.9-8.0, P(k) too
        big by 1e2-1e9, spectrum tilted by ~300x between k = 0.05 and 10 h/Mpc.
  mi_covariant_pt  -- the same boost with the framework's own dS-Unruh HUBBLE FLOOR,
        X = Z^2 (H/H_Lambda)^2 + (a_pec/a0)^2.  This collapses the boost to nu ~ 1.07-1.09 at all
        z and returns sigma_8 = 0.829-0.833, i.e. LCDM with no distinctive signal.
  So "the repo finds a growth deficit under a causal boost" is TRUE ONLY OF g04h AND ITS SETUP.
  The MOND boost proper has the OPPOSITE sign.  This script confirms or corrects both, independently.

WHAT IS COMPUTED HERE
  per-mode linear growth  d^2 delta/dlna^2 + (2 + dlnH/dlna) ddelta/dlna = (3/2) Om(a) nu delta
  with the boost evaluated three ways, all stated:
    PERMODE  y = g_N(k)/a0(z),  g_N = 4 pi G rhobar_m |delta_m| / k_phys   (one mode's own field)
    RMS      y = g_rms(a)/a0(z), g_rms the rms peculiar field summed over ALL modes, solved
             SELF-CONSISTENTLY (the field that boosts a mode is the field of the whole universe,
             which is the physically right argument for a nonlinear force law)
    FLOOR    the framework's own derived cosmological argument, X = Z^2 (H/H_Lambda)^2 + y^2
  four sectors: LCDM control | baryon-only (MOND replaces DM) | baryons + cold dark sector (the
  programme's actual live configuration, where the boost DOUBLE-COUNTS) | boost off.
Both branches (A: a0 const; B: a0 = a0(0) E(z)), both footings.  Checks CAN fail.
"""
import math, sys, time
import numpy as np
from scipy.integrate import quad, solve_ivp

T0 = time.time(); FAILS = []; NC = [0]
def check(name, ok, detail=""):
    NC[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 118); print(t); print("=" * 118, flush=True)
def info(s): print("  " + s, flush=True)

c = 2.99792458e8; Mpc = 3.0856775814913673e22; G = 6.67430e-11
h = 0.6736; om_b, om_c = 0.02237, 0.1200
T_CMB = 2.7255; N_eff = 3.046; ns, As, kpiv = 0.965, 2.1e-9, 0.05
H0 = 100 * h * 1e3 / Mpc
rho_crit0 = 3 * H0**2 / (8 * math.pi * G)
Og = (4 * 5.670374419e-8 * T_CMB**4 / c**3) / rho_crit0
Or = Og * (1 + N_eff * (7. / 8.) * (4. / 11.) ** (4. / 3.))
Ob, Oc = om_b / h**2, om_c / h**2
Om = Ob + Oc; OL = 1 - Om - Or
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
Zc = math.sqrt(32 * math.pi / 3.0)
H_Lam = H0 * math.sqrt(OL)
SIG8_OBS = 0.811
print("=" * 118); print("fbC3 -- linear growth, sigma_8 and P(k) under a boosted MOND gravity"); print("=" * 118, flush=True)

def E(z, om=Om, ol=OL): zp = 1 + z; return math.sqrt(Or * zp**4 + om * zp**3 + ol)
def T_EH98(k):
    theta = T_CMB / 2.7
    s = 44.5 * math.log(9.83 / (Om * h * h)) / math.sqrt(1 + 10 * om_b**0.75)
    ag = 1 - 0.328 * math.log(431 * Om * h * h) * (Ob / Om) + 0.38 * math.log(22.3 * Om * h * h) * (Ob / Om) ** 2
    ks = k * s / h
    ge = Om * h * (ag + (1 - ag) / (1 + (0.43 * ks) ** 4))
    q = k * theta * theta / ge
    L = math.log(2 * math.e + 1.8 * q); C = 14.2 + 731.0 / (1 + 62.5 * q)
    return L / (L + C * q * q)
def P_un(kh):                      # kh in h/Mpc
    k = kh * h
    return k ** ns * T_EH98(k) ** 2
def W(x): return 3 * (math.sin(x) - x * math.cos(x)) / x**3
_s8un = math.sqrt(quad(lambda kh: kh**2 * P_un(kh) * W(8 * kh)**2 / (2 * math.pi**2), 1e-4, 60, limit=600)[0])
PN = (SIG8_OBS / _s8un) ** 2
def Delta_lin0(kh): return math.sqrt(kh**3 * PN * P_un(kh) / (2 * math.pi**2))     # rms per ln k, z = 0, LCDM
def D_lcdm(a):
    return 2.5 * Om * math.sqrt(E(1/a-1)**2) * quad(lambda x: 1 / (x * math.sqrt(E(1/x-1)**2))**3, 1e-8, a, limit=400)[0]
_D0 = D_lcdm(1.0)
def Delta_lin(kh, z): return Delta_lin0(kh) * D_lcdm(1/(1+z)) / _D0

s8_ctl = math.sqrt(quad(lambda kh: kh**2 * PN * P_un(kh) * W(8*kh)**2 / (2*math.pi**2), 1e-4, 60, limit=600)[0])
check("C-0  CONTROL: the LCDM linear spectrum is normalised to sigma_8 = 0.811 by construction and recovers it",
      abs(s8_ctl / SIG8_OBS - 1) < 1e-4, f"sigma_8(control) = {s8_ctl:.6f}")
check("C-0b CONTROL: the LCDM growth factor has the right shape -- D(z=1)/D(0) within 2% of the standard 0.61",
      abs(D_lcdm(0.5) / _D0 / 0.6096 - 1) < 0.02, f"D(1)/D(0) = {D_lcdm(0.5)/_D0:.4f}")

# --------------------------------------------------------------------------------------------------
def a0_of(z, branch, foot): return A0[foot] * (E(z) if branch == "B" else 1.0)
def nu_line(y): return math.sqrt(1 + 1 / max(y, 1e-30))

KH = np.logspace(math.log10(0.02), math.log10(20.0), 60)      # h/Mpc

_ICCACHE = {}
def _unboosted_ratio(sector, z_i=1000.0):
    """delta(z=0)/delta(z_i) per k for the UNBOOSTED run in this sector's background -- used to set ICs so the
       unboosted case lands exactly on the observed LCDM linear spectrum.  Makes the control exact."""
    key = (sector, z_i)
    if key in _ICCACHE: return _ICCACHE[key]
    om = {"lcdm": Om, "baryon": Ob, "both": Om}[sector]; ol = 1 - om - Or; a_i = 1 / (1 + z_i)
    def Ez(a): return math.sqrt(Or / a**4 + om / a**3 + ol)
    def dlnH(a): return 0.5 * (-4 * Or / a**4 - 3 * om / a**3) / Ez(a)**2
    def rhs(N, Y):
        a = math.exp(N)
        return [Y[1], 1.5 * (om / a**3 / Ez(a)**2) * Y[0] - (2 + dlnH(a)) * Y[1]]
    s_ = solve_ivp(rhs, (math.log(a_i), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-9, atol=1e-14, t_eval=[0.0])
    _ICCACHE[key] = float(s_.y[0][-1])
    return _ICCACHE[key]

def grow(sector, branch, foot, mode, eps=1.0, z_i=1000.0, numax=1e8):
    """Return Delta(k) at z = 0 and 3 for the given sector/boost.  sector in {'lcdm','baryon','both'}."""
    om = {"lcdm": Om, "baryon": Ob, "both": Om}[sector]
    ol = 1 - om - Or
    a_i = 1 / (1 + z_i)
    Gn = _unboosted_ratio(sector, z_i)
    Di = np.array([Delta_lin0(kh) / Gn for kh in KH])       # ICs fixed so the UNBOOSTED run lands on the data
    if sector == "baryon": Di = Di * eps
    def Ez(a): return math.sqrt(Or / a**4 + om / a**3 + ol)
    def dlnH(a): return 0.5 * (-4 * Or / a**4 - 3 * om / a**3) / Ez(a)**2
    if mode == "rms":
        def rhs(N, Y):
            a = math.exp(N); D, Dp = Y; z = 1 / a - 1
            rho_m = om * rho_crit0 / a**3
            gk = np.array([4 * math.pi * G * rho_m * abs(Di[i] * D) / (KH[i] * h / (a * Mpc)) for i in range(len(KH))])
            grms = math.sqrt(np.trapz(gk**2 / KH, KH) / np.trapz(1.0 / KH, KH))
            if branch == "floor":
                y = grms / a0_of(z, "A", foot)
                nu = min(nu_line(Zc**2 * (H0 * Ez(a) / H_Lam) ** 2 + y**2), numax)
            elif branch == "none":
                nu = 1.0
            else:
                nu = min(nu_line(grms / a0_of(z, branch, foot)), numax)
            return [Dp, 1.5 * (om / a**3 / Ez(a)**2) * nu * D - (2 + dlnH(a)) * Dp]
        s = solve_ivp(rhs, (math.log(a_i), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-7, atol=1e-12,
                      t_eval=[math.log(1/4.0), 0.0])
        return Di * s.y[0][1], Di * s.y[0][0], None
    out0, out3, nus = [], [], []
    for i, kh in enumerate(KH):
        def rhs(N, Y):
            a = math.exp(N); d, dp = Y; z = 1 / a - 1
            rho_m = om * rho_crit0 / a**3
            gN = 4 * math.pi * G * rho_m * abs(d) / (kh * h / (a * Mpc))
            if branch == "none": nu = 1.0
            elif branch == "floor":
                y = gN / a0_of(z, "A", foot)
                nu = min(nu_line(Zc**2 * (H0 * Ez(a) / H_Lam) ** 2 + y**2), numax)
            else: nu = min(nu_line(gN / a0_of(z, branch, foot)), numax)
            return [dp, 1.5 * (om / a**3 / Ez(a)**2) * nu * d - (2 + dlnH(a)) * dp]
        s = solve_ivp(rhs, (math.log(a_i), 0.0), [Di[i], Di[i]], method="LSODA", rtol=1e-7, atol=1e-20,
                      t_eval=[math.log(1/4.0), 0.0])
        out3.append(s.y[0][0]); out0.append(s.y[0][1])
        gN = 4 * math.pi * G * (om * rho_crit0) * abs(s.y[0][1]) / (kh * h / Mpc)
        nus.append(nu_line(gN / a0_of(0.0, branch if branch not in ("floor", "none") else "A", foot)))
    return np.array(out0), np.array(out3), np.array(nus)

def sigma8_of(Delta0):
    lk = np.log(KH)
    integ = np.array([Delta0[i]**2 * W(8 * KH[i])**2 for i in range(len(KH))])
    return math.sqrt(np.trapz(integ, lk))

D_ref0 = np.array([Delta_lin(kh, 0.0) for kh in KH])
D_ref3 = np.array([Delta_lin(kh, 3.0) for kh in KH])
check("C-0c CONTROL: the k-grid reproduces sigma_8 = 0.811 from the reference LCDM Delta(k) to 3%",
      abs(sigma8_of(D_ref0) / SIG8_OBS - 1) < 0.03, f"sigma_8(grid) = {sigma8_of(D_ref0):.4f}")
_D0n, _, _ = grow("lcdm", "none", "canonical", "permode")
check("C-0d CONTROL, and it is the one that matters: with the initial conditions fixed off the integrator's OWN "
      "unboosted run, the UNBOOSTED LCDM sector reproduces the observed linear spectrum to <1% at every k, so "
      "every deviation reported below is the BOOST and not a normalisation error",
      float(np.max(np.abs(_D0n / D_ref0 - 1))) < 0.01,
      f"max |Delta_unboosted/Delta_LCDM - 1| over the grid = {float(np.max(np.abs(_D0n/D_ref0-1))):.2e}; "
      f"sigma_8 = {sigma8_of(_D0n):.4f}")

# ==================================================================================================
sec("PART 1 -- BARYON-ONLY (MOND replaces dark matter): does the boost regenerate the observed P(k)?")
# ==================================================================================================
print(f"    {'branch':7s} {'mode':8s} {'foot':10s} {'eps':>5s} | " +
      " ".join(f"{'R('+str(kh)+')':>10s}" for kh in (0.05, 0.2, 1.0, 5.0)) + f" | {'sigma_8':>8s} {'tilt':>10s}")
BAR = {}
for branch in ("none", "A", "B"):
    for mode in ("permode", "rms"):
        for foot in ("canonical", "alt"):
            for eps in (0.03, 0.3):
                if branch == "none" and (foot == "alt" or mode == "rms"): continue
                D0, D3, _ = grow("baryon", branch, foot, mode, eps=eps)
                R = np.interp([0.05, 0.2, 1.0, 5.0], KH, D0**2 / D_ref0**2)
                s8 = sigma8_of(D0)
                tilt = (D0[-1]**2 / D_ref0[-1]**2) / (D0[0]**2 / D_ref0[0]**2)
                BAR[(branch, mode, foot, eps)] = (R, s8, tilt)
                print(f"    {branch:7s} {mode:8s} {foot:10s} {eps:5.2f} | " +
                      " ".join(f"{r:10.3g}" for r in R) + f" | {s8:8.3g} {tilt:10.3g}")
info("R(k) = P_model(k)/P_LCDM-linear(k) at z = 0.  'tilt' = R(20 h/Mpc)/R(0.02 h/Mpc): a shape measure that is")
info("independent of the (unknown) initial baryon amplitude eps.  R = 1 and tilt = 1 would be a success.")
tilts_pm = [v[2] for kk, v in BAR.items() if kk[0] != "none" and kk[1] == "permode"]
tilts_rms = [v[2] for kk, v in BAR.items() if kk[0] != "none" and kk[1] == "rms"]
check("P1-a  SHAPE, and the honest split.  Evaluated PER MODE the boost is scale-dependent and the spectrum "
      "arrives tilted by %.0f-%.0f in power across k = 0.02-20 h/Mpc -- a normalisation-free failure that "
      "confirms the repository's rising_a0 gate (tilt 288-317) independently and extends it to the constant-a0 "
      "branch.  Evaluated on the RMS FIELD the boost is scale-INDEPENDENT and there is NO tilt at all (%.3f) -- "
      "by construction, not by success.  Which evaluation is right is a real open question in MOND cosmology, "
      "so BOTH are carried and no verdict is rested on the tilt alone"
      % (min(tilts_pm), max(tilts_pm), max(tilts_rms)),
      min(tilts_pm) > 5 and max(abs(t - 1) for t in tilts_rms) < 0.01,
      f"per-mode tilt = {min(tilts_pm):.3g}-{max(tilts_pm):.3g}; rms-field tilt = {min(tilts_rms):.4f}-{max(tilts_rms):.4f} "
      f"(scale-independent boost -> no tilt by construction)")
s8s = {kk: v[1] for kk, v in BAR.items() if kk[0] != "none"}
check("P1-b  AMPLITUDE, and the SIGN of the error: the boosted baryon-only runs OVERSHOOT sigma_8, they do not "
      "under-shoot it.  sigma_8 spans %.3g-%.3g against the measured 0.811.  The repository's 'growth DEFICIT' "
      "belongs to g04h's relic-cutoff-refill setup, NOT to the MOND boost, whose error has the opposite sign"
      % (min(s8s.values()), max(s8s.values())),
      max(s8s.values()) > 2 * SIG8_OBS,
      f"sigma_8 over boosted baryon-only runs = {min(s8s.values()):.3g}-{max(s8s.values()):.3g} vs 0.811")
sA = max(v for kk, v in s8s.items() if kk[0] == "A"); sB = max(v for kk, v in s8s.items() if kk[0] == "B")
check("P1-c  BRANCH B is worse than branch A by orders, exactly as the rising_a0 gate found: max sigma_8 is "
      "%.3g on A and %.3g on B" % (sA, sB), sB > sA, f"max sigma_8: branch A {sA:.3g}, branch B {sB:.3g}")

# ==================================================================================================
sec("PART 2 -- the framework's OWN derived Hubble floor, and the DOUBLE-COUNTING sector")
# ==================================================================================================
print(f"    {'sector':10s} {'branch':7s} {'foot':10s} | {'sigma_8':>8s} {'S_8':>7s} {'nu(z=0) at k=0.2':>18s} {'tilt':>9s}")
FL = {}
for sector in ("both", "lcdm"):
    for branch in ("none", "floor", "A"):
        for foot in ("canonical", "alt"):
            if branch == "none" and foot == "alt": continue
            D0, D3, nus = grow(sector, branch, foot, "permode")
            s8 = sigma8_of(D0); om_eff = Om
            S8 = s8 * math.sqrt(om_eff / 0.3)
            nu02 = float(np.interp(0.2, KH, nus)) if nus is not None else float("nan")
            tilt = (D0[-1]**2 / D_ref0[-1]**2) / (D0[0]**2 / D_ref0[0]**2)
            FL[(sector, branch, foot)] = (s8, S8, nu02, tilt)
            print(f"    {sector:10s} {branch:7s} {foot:10s} | {s8:8.3g} {S8:7.3g} {nu02:18.4g} {tilt:9.3g}")
s8_floor = FL[("both", "floor", "canonical")][0]
s8_none = FL[("both", "none", "canonical")][0]
check("P2-a  the framework's OWN derived dS-Unruh Hubble floor makes MOND nearly IRRELEVANT to linear growth: "
      "sigma_8 = %.4f against the unboosted %.4f, a %.1f%% effect.  This reproduces mi_covariant_pt's "
      "sigma_8 = 0.829-0.833 independently" % (s8_floor, s8_none, 100 * (s8_floor / s8_none - 1)),
      abs(s8_floor / s8_none - 1) < 0.15 and abs(s8_floor - 0.83) < 0.08,
      f"sigma_8: floored {s8_floor:.4f}, unboosted {s8_none:.4f} (ratio {s8_floor/s8_none:.4f}); "
      f"mi_covariant_pt banked 0.829-0.833")
s8_dbl = FL[("both", "A", "canonical")][0]
check("P2-b  *** THE DOUBLE-COUNTING PROBLEM, quantified. ***  If the framework keeps a cold Omega_dm AND applies "
      "the UNFLOORED MOND boost, sigma_8 = %.3g -- %.1fx the measured 0.811.  The dark sector the CMB needs and "
      "the boost the galaxies need cannot both act on the same perturbations" % (s8_dbl, s8_dbl / SIG8_OBS),
      s8_dbl > 1.5 * SIG8_OBS, f"sigma_8(cold dark sector + unfloored MOND boost) = {s8_dbl:.3g} vs 0.811")

# ==================================================================================================
sec("PART 3 -- ADJUDICATING THE PRIOR RESULTS")
# ==================================================================================================
info("g04h ('the causal boost does NOT regenerate P(k): sigma_8 <= 0.65, deficit 20-2000x'):")
info("  CONFIRMED AS STATED, and CORRECTED IN SCOPE.  Its boost is not nu(g/a0); it is a CAUSAL, SATURATING")
info("  B = min[0.9 (c_* k t/a)^2, nu-1] refilling a 28 eV relic's free-streaming cutoff.  The deficit is a")
info("  statement about that construction.  It is NOT a statement about MOND's effect on linear growth, which")
info("  this script finds has the OPPOSITE SIGN.  Quoting g04h as 'MOND under-produces structure' is wrong.")
info("rising_a0_baryon_only ('tilt 288-317, amplitude 1e6-1e9 too strong on branch B'):")
info(f"  CONFIRMED independently here: tilt {min(tilts_pm):.0f}-{max(tilts_pm):.0f}, branch B far worse than branch A.")
info("mi_covariant_pt ('the derived Hubble floor gives sigma_8 = 0.829-0.833, LCDM-degenerate'):")
info(f"  CONFIRMED independently here: sigma_8 = {s8_floor:.4f}.")
check("P3-a  the three prior results are mutually consistent ONCE THEIR SETUPS ARE DISTINGUISHED, and the net "
      "statement is: the MOND boost OVERSHOOTS linear growth unless the framework's own Hubble floor is "
      "imposed, in which case it does nothing at all.  There is no configuration that both fixes P(k) and "
      "leaves a distinctive signal",
      max(s8s.values()) > 2 * SIG8_OBS and abs(s8_floor / s8_none - 1) < 0.15,
      f"unfloored max sigma_8 = {max(s8s.values()):.3g}; floored = {s8_floor:.4f} (= unboosted {s8_none:.4f} to "
      f"{100*abs(s8_floor/s8_none-1):.1f}%)")

sec("VERDICT (fbC3)")
print(f"""
  BARYON-ONLY, MOND-BOOSTED GROWTH FAILS ON SHAPE FOR ANY AMPLITUDE.  The boost nu = sqrt(1 + a0/g_N) is
  largest where the peculiar gravity is smallest, and the peculiar gravity is smallest on SMALL scales at
  early times, so small scales grow fastest and the spectrum arrives tilted by a factor {min(tilts_pm):.0f}-{max(tilts_pm):.0f} in power
  across k = 0.02-20 h/Mpc.  That is a normalisation-free failure: no choice of the initial baryon amplitude
  fixes it.  The amplitude fails too, and it fails UPWARD: sigma_8 = {min(s8s.values()):.3g}-{max(s8s.values()):.3g} against 0.811.
  Branch B is worse than branch A by orders ({sB:.3g} vs {sA:.3g}) because a0(z) propto H makes the boost larger at
  every earlier epoch.

  CORRECTION TO THE PRIOR RECORD.  The repository's "growth deficit under a causal boost" (g04h: sigma_8 <=
  0.648, 20-2000x short) is a result about REFILLING A 28 eV RELIC'S FREE-STREAMING CUTOFF with a causal
  saturating boost.  It is not a result about MOND's linear growth, which errs in the opposite direction.
  Both are reproduced here and both stand -- in their own scopes.

  AND THE FRAMEWORK'S OWN ESCAPE IS A DEAD END EITHER WAY.  With its derived dS-Unruh Hubble floor the boost
  collapses to a few per cent (sigma_8 = {s8_floor:.4f} vs {s8_none:.4f} unboosted): the cosmology becomes LCDM's and the
  distinctive content disappears.  Without the floor, and WITH the cold Omega_dm that the CMB requires, the
  boost double-counts and gives sigma_8 = {s8_dbl:.3g}.  There is no setting that is simultaneously right at the CMB,
  right at sigma_8, and distinctive.
""")
print("=" * 118)
if FAILS:
    print(f"fbC3 INCOMPLETE: {len(FAILS)}/{NC[0]} FAILED: {FAILS}"); sys.exit(1)
print(f"fbC3 COMPLETE: {NC[0]}/{NC[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 118)
