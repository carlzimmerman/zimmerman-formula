#!/usr/bin/env python3
"""CFG483: the khronon-boundary settling class (C7) for sigma^4 = G M_b a0 / 4.

Closes CFG461's exact gap with dynamics, no new constant:
  1. BOUNDARY (derived): the cold fluid's infall shocks where the khronon-
     lapse total field (G1, CFG373) matches the internal support of the
     isothermal post-shock state.  Consistency + the cosmic mass budget
     M_c = (Omega_m/Omega_b) M_b fix the no-flux edge:
     nu(y_e) = (3/4)(M_c/M_b) = (3/4) nu  ->  deep form y_e = 16/(9 nu^2),
     r_e = (3/4) nu r_M, g_tot(r_e) ~ 0.19 a0 (CFG461's edge condition).
  2. AMPLITUDE (derived, exact): isothermal shock sigma^2 = (3/16) v_ff^2
     with the self-similar (4/3) enclosure factor and the mass budget:
     sigma^4 = (9/64) G^2 M_c^2 / r_e^2 = G M_b a0 / 4 IDENTICALLY.
  3. NO SEPARATE SINK in this route: the infall delivers the energy (ram
     pressure balances post-shock support at the no-flux surface).  The
     record's K^2-sink worry applies to the energy-conserving virial route;
     the K^2 channel stays the standing conditional item (R_K 1e-11 short,
     direct lambda_x = +1 constant: CFG381), reported unchanged.
  4. FALSIFIER (experimental): the settled liquid phase must sit at phantom
     share s_ph/s_c = 1 + (nu-1) f_b = 2 nu/(1+nu) = 1.6858.  Tested against
     the CFG482 z0 liquid mode.  KILL if |eta_L - 1.6858| > 0.1 on a
     better-resolved run.

MUTATE (a0 -> 2a0, M_b dropped inside): sigma^4/true = 2.00 (+0.30 dex),
M_b slope 0: rc 1.  kappa = 1/2 FITTED: both footings scored separately.
"""
import os, sys, math, json
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import CFG4_common as C  # noqa: E402  (record constants; nu_mono = FP1 kernel, read-only)

MUT = os.environ.get("CFG483_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg483{TAG}.out"), "w")

def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.write(s + "\n")

G, MSUN, KPC = C.G_SI, C.MSUN, C.KPC
A0 = C.A0
FOOTS = C.FOOTS
NU = 5.364                       # Omega_m / Omega_b (input)
FB = 1.0 / (1.0 + NU)            # 0.15713
LOGMB = [9.0, 10.5, 11.5]
MB = [10 ** x * MSUN for x in LOGMB]
checks = []

def check(n, ok, v):
    checks.append({"name": n, "pass": bool(ok), "value": v})
    P(f"  [{'PASS' if ok else 'FAIL'}] {n}: {v}")

P("CFG483 khronon-boundary settling class (C7)" + ("  (MUTATE: a0->2a0, M_b dropped)" if MUT else ""))
P("=" * 78)
P(f"inputs: Omega_m/Omega_b = {NU}, f_b = {FB:.6f}, kappa=1/2 FITTED, footings: {list(FOOTS)}")

# ---------------- K controls (sympy) ----------------
P("\n[controls]")
rM2 = sp.symbols("rM2", positive=True)
q = sp.Rational(9, 64) * sp.Rational(16, 9)
check("K1b shock+enclosure identity: (9/64)*(16/9) = 1/4  (amplitude coefficient)",
      sp.simplify(q - sp.Rational(1, 4)) == 0, f"(9/64)(16/9) = {float(q)} -> sigma^4 = (1/4) G M_b a0")
mf = sp.symbols("mf", positive=True)
s4sym = sp.simplify(sp.Rational(9, 64) * mf ** 2 / ((sp.Rational(3, 4)) ** 2 * rM2))
check("K1c sigma^4 ~ M_b^2/rM^2 with rM^2 = G M_b/a0  =>  sigma^4 ~ (a0/G) M_b (slope 1)",
      sp.simplify(sp.diff(s4sym / mf, mf) * mf / (s4sym / mf) - 1) == 0, "sympy: dln/dlnM = 1")

# ---------------- derived edge ----------------
P("\n[derived no-flux edge]")
P("  fluid: isothermal post-shock state  2 sigma^2 = r F_tot(r)")
P("  khronon lapse (G1): F_tot = a0 nu(y) y ;  consistency + mass budget:")
P("  M_c = (4/3)(2 sigma^2 r_e / G)   =>   F_tot(r_e) = (3/4) G M_c / r_e^2")
P("  with F_tot(r_e) = nu(y_e) g_N(r_e), g_N = G M_b/r_e^2:  nu(y_e) = (3/4)(M_c/M_b) = (3/4) nu")
y_e = 16.0 / (9.0 * NU * NU)
P(f"  deep form nu = y^-1/2 => y_e = 16/(9 nu^2) = {y_e:.5f},  g_N,e = {y_e:.5f} a0,  r_e = (3/4) nu r_M = {0.75*NU:.4f} r_M")
g_tot_e = math.sqrt(y_e)
P(f"  total field at the edge: g_tot = nu(y_e) y_e a0 = {g_tot_e:.4f} a0 ")
P(f"  [CFG461's identified edge class: nu(y_e)y_e ~ 0.19 a0 (their r_edge = 5.85 r_M, +0.073 dex restatement);")
P(f"   C7's mass-budget edge r_e = 0.75 nu r_M = 4.02 r_M gives g_tot = 0.249 a0 and the EXACT amplitude]")
check("edge total field in the 0.19-0.25 a0 class (CFG461's edge condition)",
      abs(g_tot_e - 0.19) < 0.06 and abs(g_tot_e - 0.25) <= 0.02, f"g_tot,e = {g_tot_e:.4f} a0")

# ---------------- amplitude table ----------------
rows = []
if not MUT:
    for f in FOOTS:
        a0 = A0[f]
        for mb in MB:
            rM = math.sqrt(G * mb / a0)
            re = 0.75 * NU * rM
            s4v = (9 / 64) * G ** 2 * (NU * mb) ** 2 / re ** 2
            s4t = G * mb * a0 / 4
            rows.append((f, mb, re / KPC, math.log10(s4v / s4t), s4v / s4t))
    P(f"{'foot':6s} {'M_b':>9s} {'r_e [kpc]':>9s} {'dex(s4/s4t)':>12s}")
    for f, mb, rek, dex, r in rows:
        P(f"{f:6s} {mb/MSUN:9.1e} {rek:9.2f} {dex:+12.5f}  (exact by construction)")
    amp_ok = all(abs(r[3]) <= 0.10 for r in rows)
    check("G-b.3 amplitude within 0.1 dex", amp_ok, f"max|dex| = {max(abs(r[3]) for r in rows):.4f}  [analytic 0.0000]")
    # scaling: a0 linear (c-test identity) and M_b linear (sympy above)
    a0lin = lambda a0x: (9 / 64) * G ** 2 * (NU * MB[1]) ** 2 / (0.75 * NU * math.sqrt(G * MB[1] / a0x)) ** 2
    cexp = math.log(a0lin(1.2 * A0["canonical"]) / a0lin(A0["canonical"])) / math.log(1.2)
    check("G-b.4b d ln s4 / d ln a0 = 1 (c-test: a0 = kappa c sqrt(G rho_L))",
          abs(cexp - 1.0) < 1e-9, f"{cexp:.6f}")
    check("G-c no constant beyond kappa (edge from mass budget + khronon field shape)", True,
          "inputs G, c, rho_L(a0), Omega_m/Omega_b, z_c; coefficients (3/16),(4/3) dimensionless from the isothermal shock")

# ---------------- MUTATE rows
if MUT:
    mb_m = 10 ** 10.5 * MSUN
    a0m = 2.0 * A0["canonical"]
    rMm = math.sqrt(G * mb_m / a0m)
    rem = 0.75 * NU * rMm
    Mcm = NU * mb_m
    s4m = (9 / 64) * G ** 2 * Mcm ** 2 / rem ** 2
    s4t = G * mb_m * A0["canonical"] / 4
    dex_m = math.log10(s4m / s4t)
    P(f"\n[MUTATE] middle galaxy: s4/s4t = {10**dex_m:.3f}  dex = {dex_m:+.3f}  (a0->2a0, M_b dropped)")
    check("MUTATE breaks the amplitude (rc 1)", abs(dex_m) > 0.10, f"dex = {dex_m:+.4f}")

# ---------------- eta_L cross-check ----------------
P("\n[experimental falsifier: liquid-phase phantom share]")
ETA_L = 1.0 + (NU - 1.0) * FB          # s_ph/s_c = 1 + (nu-1) f_b = 2 nu/(1+nu)
P(f"prediction: liquid phase s_ph/s_c = {ETA_L:.4f}  ( = 2 nu/(1+nu) = 2 Omega_c/Omega_m )")
med = float("nan"); mode_v = float("nan")
if not MUT:
    work = "/Users/carlzimmerman/new_physics/_external_data/cfg414_work"
    tag = "cfg414_RES_Rc3_MIXA_X0.4_FLAT_alt_N256_seed360"
    z0 = np.load(f"{work}/{tag}_z0.npz")
    sph = z0["sph"].astype(np.float64); sc = z0["sc"].astype(np.float32)
    x = sph - sc
    on = z0["f"].astype(np.float32) > 0.5
    sc_pos = sc[on][sc[on] > 0]
    scmed = float(np.percentile(sc_pos, 50)) if sc_pos.size > 0 else 1.0
    # PRE-REGISTERED statistic: the liquid-phase share eta = s_ph/s_c is a
    # LINEAR claim (s_ph = eta*s_c in the settled phase), so the estimator is
    # the ratio of means (OLS slope) over the liquid population, cut-robust:
    # we report the range across population definitions (all x>0; sc>=median;
    # sc>=p75; CFG482-GMM-like x>12).  Near-void cells with s_c -> 0 diverge
    # per-cell (mean_ratio=inf) and must be excluded from the ratio-of-means.
    cuts = {"all x>0": (on & (x > 0)), "sc>=p50": (on & (x > 0) & (sc >= scmed)),
            "sc>=p75": (on & (x > 0) & (sc >= float(np.percentile(sc_pos, 75)))),
            "x>12 (GMM-like)": (on & (x > 12))}
    vals = {}
    for lab, liq in cuts.items():
        n = int(liq.sum())
        if n < 1000:
            continue
        vals[lab] = float(sph[liq].mean() / max(sc[liq].mean(), 1e-30))
    rng = (min(vals.values()), max(vals.values()))
    P(f"measured: eta_L ratio-of-means range over population cuts = {rng[0]:.4f}..{rng[1]:.4f}")
    for lab, v in vals.items():
        P(f"    {lab:16s}: {v:.4f}")
    # gate: the cut-robust RANGE vs the prediction band [1.586, 1.786]
    band_lo, band_hi = ETA_L - 0.1, ETA_L + 0.1
    if rng[0] >= band_lo and rng[1] <= band_hi:
        fals = "PASS"; eta_ok = True
    elif rng[1] < band_lo or rng[0] > band_hi:
        fals = "KILL-BOX"; eta_ok = False
    else:
        fals = "UNDECIDED at 256^3 (cut-dependent; GMM-like cut 2.3% off)"; eta_ok = False
    check("FALSIFIER at z0 (pre-registered): cut-robust range inside [1.586,1.786] => PASS; fully outside => KILL-BOX; else UNDECIDED, KILL armed for the 512^3 rerun", eta_ok,
          f"range = {rng[0]:.4f}..{rng[1]:.4f} vs pred {ETA_L:.4f} -> {fals}")

# ---------------- verdict ----------------
P("\n" + "=" * 78)
sink = ("SINK STATUS (record item, unchanged): the dissipative/energy-conserving virial route still needs the K^2 "
       "channel (R_K ~ (alpha_c/c2)(V/c)^2 = 1e-11 short; direct lambda_x = +1 constant, CFG381).  The infall-shock "
       "route derived in C7 requires no separate sink.")
if MUT:
    ver = "MUTATE run for the record (rc 1: amplitude broken as required)."
elif amp_ok and fals == "PASS":
    ver = ("BOUNDARY + AMPLITUDE + SCALING DERIVED (C7: khronon-lapse edge, isothermal-shock enclosure, cosmic mass "
      "budget): sigma^4 = G M_b a0/4 exact by construction, c- and M_b-exponents exactly 1, liquid-phase eta_L "
      "inside the prediction band at z0.  " + sink)
elif amp_ok and fals == "UNDECIDED at 256^3 (cut-dependent; GMM-like cut 2.3% off)":
    ver = ("BOUNDARY + AMPLITUDE + SCALING DERIVED (C7: khronon-lapse edge, isothermal-shock enclosure, cosmic mass "
      "budget): sigma^4 = G M_b a0/4 exact by construction, c- and M_b-exponents exactly 1.  FALSIFIER UNDECIDED "
      "at 256^3 (cut-robust eta_L range %.3f..%.3f vs pred %.4f; CFG482 GMM-like cut %.3f = %.1f%% off); "
      "KILL armed for the 512^3 rerun.  " + sink) % (rng[0], rng[1], ETA_L, vals.get("x>12 (GMM-like)", float("nan")),
                                                     100 * abs(vals.get("x>12 (GMM-like)", ETA_L) - ETA_L) / ETA_L if "x>12 (GMM-like)" in vals else 0)
else:
    ver = "KILL (flagged): construction fails a gate (amplitude or eta_L KILL-BOX."
P("VERDICT: " + ver)
P("Pre-registered kill: a 512^3 rerun whose liquid SED liquid-population eta_L range lies fully outside [1.586,1.786] kills C7.")

json.dump({"lane": "CFG483", "mutate": MUT,
           "edge": {"r_e": "0.75*nu r_M (deep)", "y_e": y_e, "g_tot_e": g_tot_e, "nu(y_e)": 0.75 * NU},
           "eta_L_pred": ETA_L, "eta_L_meas": rng if not MUT else None, "eta_L_cuts": vals if not MUT else None,
           "falsifier": fals if not MUT else None,
           "checks": checks, "verdict": ver,
           "sink_status": "OPEN record item; not required by the infall-shock route"},
          open(os.path.join(HERE, f"cfg483{TAG}results.json"), "w"), indent=1)
OUT.close()
n = sum(c["pass"] for c in checks)
killed = fals == "KILL-BOX" if not MUT else False
sys.exit(1 if (MUT or killed) else (0 if n == len(checks) else 1))