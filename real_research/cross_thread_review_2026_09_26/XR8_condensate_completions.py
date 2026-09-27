#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR8 (1/4) -- CAN ANY COMPLETION OF THE CONDENSATE'S SINGLE-VELOCITY FLUID PASS THROUGH SHELL CROSSING?

WHY.  L374 (real_research/condensate_dust_2026/, 4366a5625) showed that the record's ghost-condensate dust -- P(X)
  quadratic about its minimum plus the (box phi)^2 term, i.e. a dispersive gamma = 2 fluid with one velocity per point --
  breaks down at the first stream crossing (cold) or collides like a fluid (warm), and named its untested completions:
  the cubic operator and other completions.  XR8 part B tests them on L374's own problem.  The question for the author
  ("we need to find out what the 'Fluid' is.. which is not particles") is whether ANY phase-only (single-velocity)
  completion of the condensate multistreams.

THE COMPLETIONS (one-dimensional, non-relativistic, weak field; the Hamiltonian form is in XR8_common.fluid):
  (i)   control: L374's condensate itself, run through L374's own imported function.
  (ii)  cubic operators.
        (ii-a) the ghost condensate's spatial cubic (lap pi)(grad pi)^2 (the Galileon-type operator): in ONE dimension it
               is a total derivative (Euler-Lagrange identically zero, sympy), so L374's 1-D test cannot see it; in 2-D
               it is not (Monge-Ampere form).  Scope statement, not a pass.
        (ii-b) the cubic term of P(X) about its minimum, P'''(X - X0)^3: an adiabatic index gamma = 3 (P ~ rho^3, the
               X^{3/2}-type index of the Berezhiani-Khoury superfluid and of a 1-D collisionless gas) in place of 2, at
               the same sound speed at rho_bar and the same k^4 term.
        (ii-c) the X-dependence of the k^4 coefficient, alpha(X) -> the cubic operator delta (lap pi)^2: the k^4
               coefficient becomes beta (1 + b delta_rho), b = +0.5 and -0.5.
  (iii) higher-order dispersion: a k^6 term (gamma6 / 2)(d_x^2 v)^2, (a) ADDED to L374's k^4 with gamma6 = beta
        (lambda/2pi)^2, and (b) REPLACING it (beta = 0) with the same gamma6.
  WHAT IS HELD FIXED (the owner's pitfall d): the de Broglie length lambda = 4 pi D / v0 with D = sqrt(eps beta), as L374;
  eps = W v0^2 / rho_bar; the k^6 length lambda / 2 pi.  So beta = D^2 / eps grows as W falls (L374's C1 effect, which
  bends the large-scale flow as D^2 / W); both W (1e-1 ... 1e-4) and lambda (L/100, L/200) are scanned, and the
  pre-crossing deviation is reported for every cell.

PRE-DECLARED (written before any run of this script; the code tests that preceded it are listed in XR8_README.md).
  R1 [the structural expectation]: NO single-velocity completion tracks the collisionless answer under L374's own pass
     rule (L374 lines 41-44: M <= max(0.05, 2 x SP's M) at every post-crossing checkpoint in BOTH tests, min rho >=
     -0.01 rho_bar, energy to 1%, no breakdown).  Reason: one velocity per point cannot represent three streams; the
     best a single-velocity fluid can do is replace crossing by pressure (collision) or by a density that leaves the
     condensate's domain (rho < 0, below the minimum).  If any cell tracks, R1 FAILS and that is the headline.
CHECKS
  C0 IMPORT: this lane's generalised solver reproduces L374's imported condensate() exactly at the same grid (base
     completion: identical first-negative and breakdown times, smoothed densities to 1e-10).
  C1 CONTROL: L374's committed first-negative / breakdown times (its results JSON) are reproduced at nx = 4096 to
     <= 1e-3 relative (L374's x2 grid and dt/2 agree to 2e-5, so the residual here is resolution), and its W = 0.1
     free-streaming misplacement (21.5% at 3 t_sc) to 1e-3.
  C2 POSITIVE CONTROL: Schroedinger-Poisson at the same D tracks (M <= 0.05, both tests, both lambda).
  C3 NEGATIVE CONTROL: the pressureless fluid follows the exact single-stream central density (20 rho_bar at 0.95 t_sc,
     within 10%) and diverges by 1.05 t_sc (L374's C3).
  C4 NUMERICAL TRUST: every completion run conserves its Hamiltonian to 1% while min rho >= -rho_bar.
  C5 RESOLUTION AND TIME STEP, PER COMPLETION (the owner's pitfall e: the unstable band below the minimum moves with each
     completion): the (free, L/100, W = 1e-3) cell of each new completion at twice the grid and at half the time step
     gives the same verdict, with breakdown / first-negative times within 20% (L374's C5 tolerance; the actual spread is
     printed).
  C5b alpha(X): ill-posedness diagnosed (breakdown time shrinks under refinement) where its Hamiltonian loses positivity.
  C5c TIME STEP, k^6 WITH GRAVITY: a code test showed the k^6 completions breaking spuriously early with gravity at
     W = 1e-4 under L374's step rule (0.29 t_sc; at half the step 1.07-1.37 t_sc, unchanged at a quarter).  They are run at
     half L374's step, and every self-gravitating k^6 cell is re-run at a further half: same verdict, times within 5%.
  C6 SYMBOLIC (ii-a): the 1-D Euler-Lagrange expression of (pi_xx)(pi_x)^2 is identically 0; the 2-D one is not.
  R1 as above.   W (reported): every cell's failure mode (time below the minimum, breakdown time, post-crossing M).
MUTATE=1 replaces every gamma = 2 and gamma = 3 fluid cell at W <= 1e-3 by its WAVE form (Gross-Pitaevskii-Poisson with
  the same D, W and index: the order parameter with its amplitude): some cells then track, and R1 must FAIL (rc = 1).
  Outputs are written with a _MUTATE suffix; the main run is written last.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR8_condensate_completions.py
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
SLUG = "XR8_condensate_completions" + ("_MUTATE" if MUTATE else "")
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR8-1", "mutate": MUTATE, "checks": {}, "numbers": {}}
NX = 2048                                                         # completions; C1/C5 use 4096
NXC = 4096
LAM1, LAM2 = C.L / 100, C.L / 200


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 116); P(t); P("=" * 116)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every gamma = 2 / gamma = 3 cell at W <= 1e-3 is replaced by its wave form (GP-Poisson) ***")
P(f"\n  L374 source sha256 {C.l374_sha256()[:16]}...  (imported: Grid, v_init, S_init, condensate, schrodinger)")
OUT["numbers"]["l374_sha256"] = C.l374_sha256()

# ------------------------------------------------------------------------------------------------ targets and SP
G = C.Grid(NX)
NB = {"free": C.nbody_cold("free", NX, 400000), "gravity": C.nbody_cold("gravity", NX, 50000)}
TSC = {"free": C.TSC, "gravity": C.TSC_GRAV_L374}
POST = {te: [t for t in C.TCHK[te] if t > TSC[te]] for te in NB}
PRE = {te: [t for t in C.TCHK[te] if t < TSC[te]] for te in NB}
# the pass rule's reference: L374's own committed Schroedinger-Poisson M (8192 grid) at the same lambda and time
J374 = json.load(open(os.path.join(C.L374_DIR, "L374_condensate_dust_shell_crossing_results.json")))["numbers"]["table"]
SPM = {}
for te in NB:
    for lam in (LAM1, LAM2):
        row = J374[f"SP|{te}|{lam:.4f}"]
        SPM[(te, lam)] = {t: row[f"{t:.4f}"] for t in C.TCHK[te]}
SP1 = C.wave("free", LAM1, 0.0, NX, node_every=0, record_min=False)      # the in-run positive control (C2)
P(f"  targets + SP done   [{time.time() - T0:.0f}s]")


def score(te, lam, r):
    M = {t: G.misplaced(r["rs"][t], NB[te]["rs"][t]) for t in C.TCHK[te] if t in r["rs"]}
    ok = C.tracks(M, SPM[(te, lam)], POST[te], r.get("min_rho", 0.0), r.get("e_drift", 0.0), r.get("t_break"),
                  check_energy="e_drift" in r)
    return M, ok


def run_cell(kind, te, lam, W, nx=NX, dtfac=1.0):
    """kind: 'base' (L374's own function), 'g3', 'k4k6', 'k6', 'a+', 'a-'.  MUTATE swaps gamma 2/3 cells at W <= 1e-3
    for their wave form."""
    if MUTATE and kind in ("base", "g3") and W <= 1e-3:
        r = C.wave(te, lam, W, nx, gamma=3 if kind == "g3" else 2, node_every=0, record_min=False)
        r["min_rho"], r["t_break"] = 0.0, None
        return r
    if kind == "base":
        return C.L374.condensate(te, lam, W, nx) if dtfac == 1.0 else C.L374.condensate(te, lam, W, nx, dtfac=dtfac)
    if kind == "g3":
        return C.fluid(te, lam, W, nx, eos="g3", dtfac=dtfac)
    if kind == "k4k6":                                           # k^6 completions: half L374's step (see C5c)
        return C.fluid(te, lam, W, nx, disp="k4k6", dtfac=0.5 * dtfac)
    if kind == "k6":
        return C.fluid(te, lam, W, nx, disp="k6", dtfac=0.5 * dtfac)
    if kind in ("a+", "a-"):
        return C.fluid(te, lam, W, nx, b_alpha=0.5 if kind == "a+" else -0.5, dtfac=dtfac)
    raise ValueError(kind)


CELLS = []
for te in ("free", "gravity"):
    CELLS += [("base", te, LAM1, W) for W in (1e-3, 1e-4)]
    CELLS += [("g3", te, LAM1, W) for W in (1e-1, 1e-2, 1e-3, 1e-4)] + [("g3", te, LAM2, 1e-3)]
    CELLS += [("k4k6", te, LAM1, W) for W in (1e-2, 1e-3, 1e-4)] + [("k4k6", te, LAM2, 1e-3)]
    CELLS += [("k6", te, LAM1, W) for W in (1e-2, 1e-3, 1e-4)] + [("k6", te, LAM2, 1e-3)]
    CELLS += [(a_, te, LAM1, W) for a_ in ("a+", "a-") for W in (1e-2, 1e-3)]
CELLS.append(("base", "free", LAM1, 1e-1))
R = {}
for c in CELLS:
    R[c] = run_cell(*c)
P(f"  {len(CELLS)} completion cells done   [{time.time() - T0:.0f}s]")

# ------------------------------------------------------------------------------------------------ table
banner("MISPLACED MASS vs the collisionless answer (L/50 coarse-graining), per completion and cell")
NAMES = {"base": "(i) L374 condensate (control)", "g3": "(ii-b) gamma = 3 (P''' / X^{3/2} index)",
         "a+": "(ii-c) alpha(X): k^4 coefficient x (1 + 0.5 delta)", "a-": "(ii-c) alpha(X): k^4 coefficient x (1 - 0.5 delta)",
         "k4k6": "(iii-a) k^4 + k^6", "k6": "(iii-b) k^6 only"}
TAB, PASS = {}, {}
for c in CELLS:
    kind, te, lam, W = c; r = R[c]
    M, ok = score(te, lam, r)
    tn, tb = r.get("t_neg"), r.get("t_break")
    pre = max([M[t] for t in PRE[te] if t in M], default=float("nan"))
    key = f"{kind}|{te}|L/{round(C.L / lam)}|W={W:g}"
    TAB[key] = dict(M={f"{t:.4f}": v for t, v in M.items()}, pre_M=pre, min_rho=r.get("min_rho"), e_drift=r.get("e_drift"),
                    t_neg_over_tsc=(tn / TSC[te]) if tn else None, t_break_over_tsc=(tb / TSC[te]) if tb else None, tracks=ok)
    PASS[(kind, lam, W, te)] = ok
    P(f"    {NAMES[kind]:48s} {te:8s} L/{round(C.L / lam)} W={W:<7g}: pre-crossing M {pre:.4f}; "
      + ", ".join(f"t={t / TSC[te]:.2f}tsc {v:.4f}" for t, v in M.items() if t in POST[te])
      + (f" | below the minimum at {tn / TSC[te]:.2f} t_sc" if tn else "")
      + (f" | BREAKS DOWN at {tb / TSC[te]:.2f} t_sc" if tb else "")
      + f" | min rho {r.get('min_rho', 0):+.3g}" + (f" | E drift {r['e_drift']:.1e}" if r.get('e_drift') is not None else "")
      + (" | TRACKS" if ok else ""))
OUT["numbers"]["table"] = TAB

# ------------------------------------------------------------------------------------------------ checks
banner("CHECKS")
if not MUTATE:
    a = C.fluid("free", LAM1, 1e-3, NX); b = R[("base", "free", LAM1, 1e-3)]
    dmax = max(float(np.max(np.abs(a["rs"][t] - b["rs"][t]))) for t in a["rs"])
    check("C0 IMPORT: the generalised solver reproduces L374's imported condensate() exactly (base completion, same grid)",
          f"t_neg {a['t_neg']} vs {b['t_neg']}; t_break {a['t_break']} vs {b['t_break']}; max |d rho_s| {dmax:.1e}",
          a["t_neg"] == b["t_neg"] and a["t_break"] == b["t_break"] and dmax <= 1e-10)
    c1 = {}
    for te in ("free", "gravity"):
        for W in (1e-3, 1e-4):
            ref = J374[f"cond|{te}|0.0100|{W:g}"]; r = C.L374.condensate(te, LAM1, W, NXC); r2k = R[("base", te, LAM1, W)]
            c1[f"{te}|W={W:g}"] = dict(t_neg=abs(r["t_neg"] / ref["t_neg"] - 1), t_break=abs(r["t_break"] / ref["t_break"] - 1),
                                        t_break_2048=abs(r2k["t_break"] / ref["t_break"] - 1))
    GC = C.Grid(NXC); NBC = C.nbody_cold("free", NXC, 400000)
    rW = C.L374.condensate("free", LAM1, 1e-1, NXC); tl = C.TCHK["free"][-1]
    m21 = GC.misplaced(rW["rs"][tl], NBC["rs"][tl]); ref21 = J374["cond|free|0.0100|0.1"]["M"][f"{tl:.4f}"]
    check("C1 CONTROL: L374's committed first-negative and breakdown times reproduced to <= 1e-3 relative at nx = 4096, and its "
          "W = 0.1 free-streaming misplacement at 3 t_sc to 1e-3 (the 2048 grid used for the completions is printed too)",
          {k: f"t_neg {v['t_neg']:.1e}, t_break {v['t_break']:.1e} (2048: {v['t_break_2048']:.1e})" for k, v in c1.items()}
          | {"M(W=0.1, 3 t_sc)": f"{m21:.4f} vs L374 {ref21:.4f}"},
          all(max(v["t_neg"], v["t_break"]) <= 1e-3 for v in c1.values()) and abs(m21 - ref21) <= 1e-3)
    OUT["numbers"]["C1"] = dict(rel=c1, M21=m21, M21_ref=ref21)
spm1 = {t: G.misplaced(SP1["rs"][t], NB["free"]["rs"][t]) for t in C.TCHK["free"]}
c2 = {f"{te}|L/{round(C.L / lam)}": max(SPM[(te, lam)][t] for t in POST[te]) for te in NB for lam in (LAM1, LAM2)}
check("C2 POSITIVE CONTROL: Schroedinger-Poisson at the same D tracks after crossing (this run: free, L/100, M <= 0.05); L374's "
      "committed SP misplacement, the pass rule's reference, is below 0.025 everywhere, so the rule's threshold is 0.05",
      f"this run {max(spm1[t] for t in POST['free']):.4f}; L374 max post-crossing SP M {({k: round(v, 4) for k, v in c2.items()})}",
      max(spm1[t] for t in POST["free"]) <= C.M_TOL and all(v <= C.M_TOL / 2 for v in c2.values()))
d0 = C.L374.condensate("free", None, None, NX, pressureless=True)
check("C3 NEGATIVE CONTROL (L374's own pressureless run): central density 20 rho_bar at 0.95 t_sc (10%), then max rho > 50 "
      "rho_bar or breakdown by 1.05 t_sc",
      f"rho_c(0.95 t_sc) {d0['rho_c95']:.3f}; max rho by 1.05 t_sc {d0['rho_max_105']:.1f}; t_break {d0['t_break']}",
      d0["rho_c95"] is not None and abs(d0["rho_c95"] / 20 - 1) < 0.10
      and (d0["rho_max_105"] > 50 or (d0["t_break"] is not None and d0["t_break"] <= 1.05 * C.TSC)))
if not MUTATE:
    c4 = {k: v["e_drift"] for k, v in TAB.items() if v.get("e_drift") is not None}
    c4_ok = {k: v for k, v in c4.items() if not k.startswith(("a+", "a-"))}
    check("C4 NUMERICAL TRUST: every well-posed completion run conserves its Hamiltonian to 1% while min rho >= -rho_bar "
          "(alpha(X) is diagnosed separately in C5b)",
          f"max drift {max(c4_ok.values()):.1e} over {len(c4_ok)} runs", max(c4_ok.values()) <= C.E_TOL)

    def rel(a_, b_):
        if a_ is None and b_ is None:
            return 0.0
        if a_ is None or b_ is None:
            return float("inf")
        return abs(b_ / a_ - 1)
    c5 = {}
    for kind in ("g3", "k4k6", "k6"):
        r1 = R[(kind, "free", LAM1, 1e-3)]
        r2 = run_cell(kind, "free", LAM1, 1e-3, nx=NXC)
        r3 = run_cell(kind, "free", LAM1, 1e-3, dtfac=0.5)
        M3, v3 = score("free", LAM1, r3)
        M2 = {t: GC.misplaced(r2["rs"][t], NBC["rs"][t]) for t in r2["rs"]}
        v2 = C.tracks(M2, SPM[("free", LAM1)], POST["free"], r2["min_rho"], r2["e_drift"], r2["t_break"])
        v1 = PASS[(kind, LAM1, 1e-3, "free")]
        spread = max(rel(r1["t_neg"], r2["t_neg"]), rel(r1["t_neg"], r3["t_neg"]),
                     rel(r1["t_break"], r2["t_break"]), rel(r1["t_break"], r3["t_break"]))
        c5[kind] = dict(verdicts=(v1, v2, v3), t_neg=(r1["t_neg"], r2["t_neg"], r3["t_neg"]),
                        t_break=(r1["t_break"], r2["t_break"], r3["t_break"]), spread=spread)
    check("C5 RESOLUTION AND TIME STEP, per completion (gamma = 3, k^4 + k^6, k^6): the (free, L/100, W = 1e-3) cell at 2x grid "
          "(4096) and at dt/2 gives the same verdict, with first-negative / breakdown times within 20%",
          {k: f"verdicts {v['verdicts']}; t_neg {[None if x is None else round(x / C.TSC, 4) for x in v['t_neg']]} t_sc; "
              f"t_break {[None if x is None else round(x / C.TSC, 4) for x in v['t_break']]} t_sc; max spread {v['spread']:.1e}"
           for k, v in c5.items()},
          all(len(set(v["verdicts"])) == 1 and v["spread"] <= 0.20 for v in c5.values()))
    # C5b: alpha(X) -- a Hamiltonian that loses positivity where |b d_x v| > eps / D is ill-posed: its breakdown time
    # must SHRINK under refinement (growth rate ~ k^2), unlike a converged breakdown.  At W = 1e-2 the initial flow is
    # inside the positive region (|b d_x v| = 3.1 < eps/D = 12.6) and the breakdown must instead converge.
    c5b = {}
    for W in (1e-3, 1e-2):
        ra = R[("a+", "free", LAM1, W)]; rb = run_cell("a+", "free", LAM1, W, nx=NXC)
        c5b[f"W={W:g}"] = dict(tb_2048=ra["t_break"], tb_4096=rb["t_break"], eps_over_D=W / C.D_of(LAM1),
                               b_dxv=0.5 * 2 * np.pi)
    illposed = c5b["W=0.001"]["tb_4096"] is not None and c5b["W=0.001"]["tb_2048"] is not None and \
        c5b["W=0.001"]["tb_4096"] < 0.8 * c5b["W=0.001"]["tb_2048"] and c5b["W=0.001"]["tb_2048"] < 0.1 * C.TSC
    conv = rel(c5b["W=0.01"]["tb_2048"], c5b["W=0.01"]["tb_4096"]) <= 0.20
    check("C5b alpha(X) (the delta (lap pi)^2 cubic): at W = 1e-3 the completion is ILL-POSED on the initial flow (|b d_x v| = "
          "3.1 > eps/D = 1.26: its Hamiltonian loses positivity, breakdown within 0.1 t_sc and earlier on the finer grid); at "
          "W = 1e-2 (eps/D = 12.6) its breakdown converges within 20%",
          {k: f"t_break 2048 {v['tb_2048'] and round(v['tb_2048'] / C.TSC, 4)} t_sc, 4096 {v['tb_4096'] and round(v['tb_4096'] / C.TSC, 4)} "
              f"t_sc; eps/D {v['eps_over_D']:.2f} vs |b d_x v| {v['b_dxv']:.2f}" for k, v in c5b.items()},
          illposed and conv)
    OUT["numbers"]["C5"] = {k: {kk: (list(vv) if isinstance(vv, tuple) else vv) for kk, vv in v.items()} for k, v in c5.items()}
    OUT["numbers"]["C5b"] = c5b
    # C5c: every self-gravitating cell of the k^6 completions (every W and lambda) re-run at half its time step
    c5c, bad = {}, []
    for c in CELLS:
        kind, te, lam, W = c
        if kind not in ("k4k6", "k6") or te != "gravity":
            continue
        r1 = R[c]; rh = run_cell(kind, te, lam, W, dtfac=0.5)
        M1, v1 = score(te, lam, r1); Mh, vh = score(te, lam, rh)
        sp_ = max(rel(r1["t_neg"], rh["t_neg"]), rel(r1["t_break"], rh["t_break"]))
        c5c[f"{kind}|{te}|L/{round(C.L / lam)}|W={W:g}"] = dict(t_neg=(r1["t_neg"], rh["t_neg"]), t_break=(r1["t_break"], rh["t_break"]),
                                                              verdicts=(v1, vh), spread=sp_)
        if v1 != vh or sp_ > 0.05:
            bad.append(f"{kind}|{te}|W={W:g}: spread {sp_:.2e}")
    check("C5c TIME STEP, k^6 COMPLETIONS WITH GRAVITY: every self-gravitating k^4+k^6 and k^6 cell (every W and lambda), run at half "
          "L374's step, re-run at a further half gives the same verdict and first-negative / breakdown times within 5%",
          f"{len(c5c)} cells; max spread {max(v['spread'] for v in c5c.values()):.1e}; outliers {bad or 'none'}", not bad)
    OUT["numbers"]["C5c"] = {k: {kk: (list(vv) if isinstance(vv, tuple) else vv) for kk, vv in v.items()} for k, v in c5c.items()}

# C6 symbolic
x, y, t = sp.symbols("x y t", real=True)


def EL(Lag, f, vars_, maxord=2):
    import itertools
    expr = 0
    derivs = [()]
    for o in range(1, maxord + 1):
        derivs += list(itertools.combinations_with_replacement(vars_, o))
    for d in derivs:
        fd = f if not d else sp.diff(f, *d)
        term = sp.diff(Lag, fd)
        for v in d:
            term = sp.diff(term, v)
        expr += (-1) ** len(d) * term
    return sp.simplify(expr)


pi1 = sp.Function("pi")(x, t); pi2 = sp.Function("pi")(x, y, t)
e1 = EL(sp.diff(pi1, x, 2) * sp.diff(pi1, x) ** 2, pi1, [x, t])
lap = sp.diff(pi2, x, 2) + sp.diff(pi2, y, 2)
e2 = EL(lap * (sp.diff(pi2, x) ** 2 + sp.diff(pi2, y) ** 2), pi2, [x, y, t])
check("C6 SYMBOLIC (ii-a): the ghost condensate's spatial cubic (lap pi)(grad pi)^2 is a total derivative in 1-D (Euler-Lagrange "
      "identically 0) but not in 2-D -- L374's 1-D test cannot see it",
      f"1-D: {e1}; 2-D: {sp.factor(e2)}", e1 == 0 and sp.simplify(e2) != 0,
      reading="the leading Galileon-type cubic needs a 2-D/3-D shell-crossing test; this lane does not run one")
OUT["numbers"]["C6"] = dict(EL_1D=str(e1), EL_2D=str(sp.factor(e2)))

# ------------------------------------------------------------------------------------------------ R1
banner("R1  THE STRUCTURAL EXPECTATION (set before any run): no single-velocity completion tracks")
WIN = []
for kind in NAMES:
    for lam in (LAM1, LAM2):
        for W in sorted({c[3] for c in CELLS if c[0] == kind and c[2] == lam}):
            okf = PASS.get((kind, lam, W, "free")); okg = PASS.get((kind, lam, W, "gravity"))
            if okf is None and okg is None:
                continue
            if okf and okg:
                WIN.append(f"{kind}|L/{round(C.L / lam)}|W={W:g}")
            P(f"    {NAMES[kind]:48s} L/{round(C.L / lam)} W={W:<7g}: free {'tracks' if okf else ('does NOT track' if okf is not None else '-')}, "
              f"self-gravitating {'tracks' if okg else ('does NOT track' if okg is not None else '-')}")
check("R1: no single-velocity completion of the condensate tracks the collisionless answer in both tests (L374's rule)",
      f"tracking cells: {WIN or 'none'}", not WIN,
      reading=("every completion either leaves the condensate's domain (rho < 0, below the minimum, then runs away) or "
               "replaces crossing by pressure; one velocity per point cannot carry three streams") if not WIN else
      "a cell tracks -- see the table")
check("W (reported) the failure modes in the table above", "see above", True, load_bearing=False)
OUT["numbers"]["tracking_cells"] = WIN

banner("VERDICT")
n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["runtime_s"] = len(CH), n_fail, round(time.time() - T0, 1)
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1,
          default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
P(f"  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {SLUG}_results.json   "
  f"[{time.time() - T0:.0f}s]")
P(f"rc={0 if n_fail == 0 else 1}")
sys.exit(0 if n_fail == 0 else 1)
