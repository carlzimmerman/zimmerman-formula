#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR8 (2/4) -- THE ORDER PARAMETER WITH ITS RADIAL MODE: HOW LIGHT MUST THE RADIAL MODE BE FOR THE FIELD TO PASS THROUGH
SHELL CROSSING?

WHY.  L374's condensate is a phase-only field: its dust density is slaved to the phase (rho = 2 P''(X0)(X - X0)), it has
  no amplitude that can pass through zero, and it fails at the first crossing.  L374's MUTATE -- a linear complex field
  with the same D and eps (Gross-Pitaevskii-Poisson) -- passes for W <= 1e-3.  The owner of L374 and the V0 writer (DF1,
  real_research/dark_fluid_2026/FL1_order_parameter.py, uncommitted) read both as limits of ONE superfluid order
  parameter Phi = sqrt(n) e^{i theta}: the condensate is its phase-only (Thomas-Fermi) limit, GP its full form.  What sets
  which limit applies is the order parameter's RADIAL (amplitude) mode.

THE RADIAL MASS.  For a complex scalar about its rotating state T = Omega t, R = R0 (the lead track's covariant clock,
  real_research/closure_push_2026_09_26/covariant_clock/RESULT.md section 3), the radial mode has mass mu^2 = V''(R0) -
  Omega^2 and the soft branch is omega_-^2 = (mu^2/A) k^2 + (16 Omega^4/A^3) k^4 + ..., A = mu^2 + 4 Omega^2.  Its
  non-relativistic limit (mu << Omega) is Bogoliubov's omega^2 = c_s^2 k^2 + D^2 k^4 with D = 1/(2 Omega) = hbar/2m and
  c_s = mu D (checked symbolically below, S1).  So at fixed de Broglie length (fixed D) the radial mass is
      m_r = mu = c_s / D = 1 / xi   (xi = the healing length),   W = c_s^2 / v0^2 = (m_r D / v0)^2,
  and a scan of L374's warmth W at fixed lambda IS a scan of m_r.  In L374's units (L = v0 = 1): m_r = 4 pi sqrt(W) /
  lambda (an inverse length); m_r v0 t_sc = 2 sqrt(W) L / lambda; the healing rate omega_h = c_s m_r = W v0^2 / D gives
  omega_h t_sc = 2 W L / lambda.  Heavy radial mode (m_r -> infinity at fixed D): the amplitude is slaved (Thomas-Fermi),
  the field is a pressure-supported phase-only fluid.  Light radial mode: the amplitude is free to go to zero.

THE TEST.  L374's problem, grid and pass rule; the wave form of the order parameter (Gross-Pitaevskii-Poisson, gamma = 2)
  scanned in W at lambda = L/100 and L/200, free-streaming and self-gravitating, plus its gamma = 3 version (a |psi|^6
  self-interaction: the order-parameter form of the P ~ X^{3/2} index).  nx = 2048 (checked against 4096 in C1).

PRE-DECLARED (before any run of this script).
  R1 [the radial-mass window]: the gamma = 2 order parameter tracks the collisionless answer (L374's rule) at every
     W <= 1e-3 and fails at every W >= 3e-2, in both tests at every lambda scanned.  (L374's MUTATE bracket: W = 1e-3
     tracked, W = 1e-2 failed free streaming by 6.4-6.6% and tracked with gravity.)  The largest tracking W on the scan
     (W_c) is reported per lambda with its m_r, m_r v0 t_sc and omega_h t_sc.
  R2 [the index does not matter when the radial mode is light]: the gamma = 3 order parameter tracks at W = 1e-3 in both
     tests (and is reported at W = 0.1).
CHECKS
  S1 SYMBOLIC: the gyroscopic soft branch's k^2 and k^4 coefficients at mu << Omega are mu^2/(4 Omega^2) and 1/(4 Omega^2):
     c_s = mu D exactly at leading order.
  C0 IMPORT: this lane's wave() reproduces L374's imported schrodinger() at the same grid (M between them <= 1e-12).
  C1 POSITIVE CONTROL AND RESOLUTION: Schroedinger-Poisson (W = 0, m_r = 0) tracks after crossing at both lambda in both
     tests, and nx = 2048 agrees with nx = 4096 to |dM| <= 2e-3 at every checkpoint (free, L/100).
  C2 UNITARITY: the wave field's norm is conserved to 1e-10 in every run (mass conservation of the split-step scheme).
  R1, R2 as above.
  W  (post hoc, NOT pre-declared: added after the first run of this script falsified R2) the gamma = 3 order parameter
     at W = 1e-4 and 1e-5, and the self-interaction energy at the densest caustic point, h(rho_peak) / (v0^2 / 2).
MUTATE=1 makes the radial mode heavy: every W on the scan is multiplied by 100.  R1 and R2 must FAIL (rc = 1).

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR8_order_parameter_scan.py
Single-threaded; about 3-4 minutes.
"""
import os, sys, json, math, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import XR8_common as C                                            # noqa: E402

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR8_order_parameter_scan" + ("_MUTATE" if MUTATE else "")
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR8-2", "mutate": MUTATE, "checks": {}, "numbers": {}}
NX = 2048
LAM1, LAM2 = C.L / 100, C.L / 200
WF = 100.0 if MUTATE else 1.0                                     # MUTATE: heavy radial mode


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 116); P(t); P("=" * 116)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the radial mode is made heavy -- every W on the scan x 100 ***")
P(f"\n  L374 source sha256 {C.l374_sha256()[:16]}...")
OUT["numbers"]["l374_sha256"] = C.l374_sha256()

# ------------------------------------------------------------------------------------------------ S1 symbolic
banner("S1  the radial mass of the order parameter and the non-relativistic sound speed")
k, mu, Om = sp.symbols("k mu Omega", positive=True)
A = mu ** 2 + 4 * Om ** 2
wm2 = k ** 2 + A / 2 - sp.sqrt(A ** 2 + 16 * Om ** 2 * k ** 2) / 2
ser = sp.series(wm2, k, 0, 5).removeO()
c2k, c4k = sp.simplify(ser.coeff(k, 2)), sp.simplify(ser.coeff(k, 4))
lead_c2 = sp.series(c2k, mu, 0, 3).removeO(); lead_c4 = sp.limit(c4k, mu, 0)
Dsym = 1 / (2 * Om)
s1 = sp.simplify(lead_c2 - (mu * Dsym) ** 2) == 0 and sp.simplify(lead_c4 - Dsym ** 2) == 0
check("S1 SYMBOLIC: the gyroscopic soft branch gives c_s^2 = mu^2/(4 Omega^2) and D^2 = 1/(4 Omega^2) at mu << Omega, so c_s = mu D "
      "(the radial mass is the inverse healing length at fixed D)",
      f"k^2 coeff {c2k} -> {lead_c2}; k^4 coeff {c4k} -> {lead_c4}", s1)

# ------------------------------------------------------------------------------------------------ targets and SP
G = C.Grid(NX)
NB = {"free": C.nbody_cold("free", NX, 400000), "gravity": C.nbody_cold("gravity", NX, 50000)}
TSC = {"free": C.TSC, "gravity": C.TSC_GRAV_L374}
POST = {te: [t for t in C.TCHK[te] if t > TSC[te]] for te in NB}
SP = {(te, lam): C.wave(te, lam, 0.0, NX, node_every=0, record_min=False) for te in NB for lam in (LAM1, LAM2)}
SPM = {kk: {t: G.misplaced(v["rs"][t], NB[kk[0]]["rs"][t]) for t in C.TCHK[kk[0]]} for kk, v in SP.items()}
P(f"  targets + SP done   [{time.time() - T0:.0f}s]")

# ------------------------------------------------------------------------------------------------ the scan
SCAN = []
SCAN += [("g2", "free", LAM1, W) for W in (1e-4, 3e-4, 1e-3, 2e-3, 3e-3, 5e-3, 1e-2, 3e-2, 1e-1)]
SCAN += [("g2", "free", LAM2, W) for W in (1e-3, 3e-3, 5e-3, 1e-2, 3e-2)]
SCAN += [("g2", "gravity", LAM1, W) for W in (1e-3, 1e-2, 3e-2)]
SCAN += [("g2", "gravity", LAM2, W) for W in (1e-3, 1e-2, 3e-2)]
SCAN += [("g3", "free", LAM1, W) for W in (1e-3, 1e-1)] + [("g3", "gravity", LAM1, 1e-3)]
# POST HOC (added after this script's first run falsified R2; reported, not load-bearing): the gamma = 3 order parameter
# at lower W, to locate where its |psi|^6 interaction becomes negligible at the caustics' densities
POSTHOC = [("g3", "free", LAM1, W) for W in (1e-4, 1e-5)] + [("g3", "gravity", LAM1, W) for W in (1e-4, 1e-5)]
SCAN += POSTHOC
R, NORM = {}, {}
for c in SCAN:
    kind, te, lam, W = c
    r = C.wave(te, lam, W * WF, NX, gamma=3 if kind == "g3" else 2, node_every=0, record_min=False)
    NORM[c] = abs(float(np.sum(np.abs(r["psi"]) ** 2)) * G.dx / (C.RHOB * C.L) - 1)
    R[c] = r
P(f"  {len(SCAN)} order-parameter cells done   [{time.time() - T0:.0f}s]")


def mr(W, lam):
    D = C.D_of(lam); cs = math.sqrt(W) * C.V0
    return dict(m_r=cs / D, xi=D / cs if cs > 0 else float("inf"), m_r_v0_tsc=cs / D * C.V0 * C.TSC,
                omega_h_tsc=cs * cs / D * C.TSC)


banner("MISPLACED MASS of the order parameter vs the collisionless answer, by radial mass")
TAB, OK = {}, {}
for c in SCAN:
    kind, te, lam, W = c; r = R[c]; Weff = W * WF
    M = {t: G.misplaced(r["rs"][t], NB[te]["rs"][t]) for t in C.TCHK[te]}
    ok = C.tracks(M, SPM[(te, lam)], POST[te], check_energy=False)
    OK[c] = ok
    q = mr(Weff, lam)
    hmax = (Weff * r["rho_max"] if kind == "g2" else 0.5 * Weff * r["rho_max"] ** 2) * C.V0 ** 2   # h(rho_max), rho_bar = 1
    TAB[f"{kind}|{te}|L/{round(C.L / lam)}|W={Weff:g}"] = dict(M={f"{t:.4f}": v for t, v in M.items()}, tracks=ok, **q,
                                                                norm_err=NORM[c], rho_max=r["rho_max"],
                                                                h_max_over_half_v0sq=hmax / (0.5 * C.V0 ** 2),
                                                                post_hoc=c in POSTHOC)
    P(f"    {'gamma=3' if kind == 'g3' else 'gamma=2'} {te:8s} L/{round(C.L / lam)} W={Weff:<7g} (m_r = {q['m_r']:7.1f}/L, "
      f"xi = L/{1 / q['xi']:.0f}, m_r v0 t_sc = {q['m_r_v0_tsc']:6.2f}, omega_h t_sc = {q['omega_h_tsc']:6.3f}): "
      + ", ".join(f"{t / TSC[te]:.2f}tsc {v:.4f}" for t, v in M.items() if t in POST[te])
      + f" | peak rho {r['rho_max']:.0f}, h(peak) / (v0^2/2) = {hmax / (0.5 * C.V0 ** 2):.3g}" + (" | TRACKS" if ok else " | fails")
      + (" [post hoc]" if c in POSTHOC else ""))
OUT["numbers"]["table"] = TAB

# ------------------------------------------------------------------------------------------------ checks
banner("CHECKS")
if not MUTATE:
    a = C.L374.schrodinger("free", LAM1, 0.0, NX)
    d = max(G.misplaced(a["rs"][t], SP[("free", LAM1)]["rs"][t]) for t in C.TCHK["free"])
    check("C0 IMPORT: this lane's wave() reproduces L374's imported schrodinger() at the same grid", f"max M between them {d:.1e}",
          d <= 1e-12)
    G4 = C.Grid(2 * NX); NB4 = C.nbody_cold("free", 2 * NX, 400000)
    sp4 = C.wave("free", LAM1, 0.0, 2 * NX, node_every=0, record_min=False)
    dM = {t: abs(G4.misplaced(sp4["rs"][t], NB4["rs"][t]) - SPM[("free", LAM1)][t]) for t in C.TCHK["free"]}
    c1 = {f"{te}|L/{round(C.L / lam)}": max(SPM[(te, lam)][t] for t in POST[te]) for te in NB for lam in (LAM1, LAM2)}
    check("C1 POSITIVE CONTROL AND RESOLUTION: Schroedinger-Poisson (m_r = 0) tracks after crossing (M <= 0.05) at both lambda in "
          "both tests, and nx = 2048 agrees with 4096 to |dM| <= 2e-3 (free, L/100)",
          f"max post-crossing M {({kk: round(v, 4) for kk, v in c1.items()})}; |dM| 2048 vs 4096 max {max(dM.values()):.1e}",
          all(v <= C.M_TOL for v in c1.values()) and max(dM.values()) <= 2e-3)
check("C2 UNITARITY: the wave field's norm is conserved to 1e-10 in every run", f"max |norm - 1| {max(NORM.values()):.1e}",
      max(NORM.values()) <= 1e-10)

banner("R1  THE RADIAL-MASS WINDOW (set before any run)")
r1, wc = [], {}
for lam in (LAM1, LAM2):
    for te in ("free", "gravity"):
        cells = sorted([c for c in SCAN if c[0] == "g2" and c[1] == te and c[2] == lam], key=lambda c: c[3])
        if not cells:
            continue
        light = [OK[c] for c in cells if c[3] <= 1e-3]
        heavy = [not OK[c] for c in cells if c[3] >= 3e-2]
        r1 += light + heavy
        track_W = [c[3] * WF for c in cells if OK[c]]
        wc[f"{te}|L/{round(C.L / lam)}"] = max(track_W) if track_W else None
        P(f"    {te:8s} L/{round(C.L / lam)}: tracks at W = {[f'{w:g}' for w in track_W]}; fails at "
          f"{[f'{c[3] * WF:g}' for c in cells if not OK[c]]}")
WC = {kk: (dict(W_c=v, **mr(v, LAM1 if kk.endswith('100') else LAM2)) if v else None) for kk, v in wc.items()}
check("R1: the gamma = 2 order parameter tracks at every W <= 1e-3 and fails at every W >= 3e-2 (both tests, every lambda scanned)",
      {kk: (f"W_c = {v['W_c']:g}: m_r = {v['m_r']:.1f}/L, xi = L/{1 / v['xi']:.0f}, m_r v0 t_sc = {v['m_r_v0_tsc']:.2f}, "
            f"omega_h t_sc = {v['omega_h_tsc']:.3f}") if v else "nothing tracks" for kk, v in WC.items()},
      all(r1) and len(r1) > 0,
      reading=("the radial mode must be light: W = (m_r D / v0)^2 below a few e-3, i.e. healing length xi = 1/m_r >~ lambda / "
               "(4 pi sqrt(W_c)) -- the self-interaction energy far below the streams' kinetic energy") if (all(r1) and r1) else
      "the window's pre-declared edges do not hold in this run -- see the table")
OUT["numbers"]["W_c"] = WC
g3 = [OK[c] for c in SCAN if c[0] == "g3" and c[3] == 1e-3]
r2ok = all(g3) and len(g3) == 2
check("R2: the gamma = 3 order parameter (|psi|^6, the P ~ X^{3/2} index) tracks at W = 1e-3 in both tests",
      {f"{c[1]}|W={c[3] * WF:g}": OK[c] for c in SCAN if c[0] == "g3" and c not in POSTHOC}, r2ok,
      reading=("when the radial mode is light the index is irrelevant; at W = 0.1 both indices are pressure-dominated fluids")
      if r2ok else ("FALSIFIED: at the same sound speed at rho_bar the gamma = 3 order parameter does not track -- the index "
                    "matters (see the post-hoc item below)"))

ph = {f"{c[1]}|W={c[3] * WF:g}": dict(tracks=OK[c], h_peak=TAB[f"g3|{c[1]}|L/100|W={c[3] * WF:g}"]["h_max_over_half_v0sq"])
      for c in POSTHOC}
hg2 = max([v["h_max_over_half_v0sq"] for k_, v in TAB.items() if k_.startswith("g2") and v["tracks"]], default=float("nan"))
check("W (post hoc, after R2 failed; not load-bearing): the gamma = 3 order parameter at lower W, and the self-interaction "
      "energy at the densest caustic point, h(rho_peak), against the streams' kinetic energy v0^2/2",
      f"gamma = 3: {({k_: (('tracks' if v['tracks'] else 'fails') + ', h_peak/(v0^2/2) = ' + format(v['h_peak'], '.3g')) for k_, v in ph.items()})}; "
      f"largest h_peak/(v0^2/2) among tracking gamma = 2 cells {hg2:.3g}", True, load_bearing=False,
      reading="gamma = 3 needs W ~ 100x below gamma = 2's (free <= 1e-4, self-gravitating <= 1e-5, against 5e-3 / 1e-2): its "
              "|psi|^6 interaction grows as rho^2 where streams pile up.  In free streaming both indices change verdict near "
              "h(rho_peak) ~ 0.2-0.6 of v0^2/2; with gravity they do not share one threshold, so no single number (W at "
              "rho_bar or h at the caustic peak) is index-independent in this scan")
OUT["numbers"]["post_hoc_gamma3"] = ph

banner("VERDICT")
n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["runtime_s"] = len(CH), n_fail, round(time.time() - T0, 1)
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1,
          default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
P(f"  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {SLUG}_results.json   "
  f"[{time.time() - T0:.0f}s]")
P(f"rc={0 if n_fail == 0 else 1}")
sys.exit(0 if n_fail == 0 else 1)
