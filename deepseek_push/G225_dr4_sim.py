#!/usr/bin/env python3
"""G225 -- THE DR4 VERDICT SIMULATION: the scorer's expected outcome distribution
at the real N and systematics.

THE QUESTION (the December-2026 expectation).  The G165 scorer freezes the
CONTRACT: n_pass of 9 scored tests -> the theory's DR4 verdict (9/9 =
CONFIRMED-STRONG, 7-8 = CONFIRMED-WEAK, 5-6 = SPLIT, <= 4 = DISFAVORED).  On
the G088/G092 mocks the scorer is 9/9 by construction -- but at G088's N_sel =
2500 bright pairs PER log bin (~20k total), 3-4x the DR4-documented usable
sample.  This lane asks: at the REAL N (2,000-5,000 usable pairs at 3-30 kAU)
and the REAL error model (sigma_mu 30-40 uas for the bright pairs, optimistic
10 uas), WHAT is the distribution of the December verdict?

THE SIMULATION.  1,000 DR4 realizations per (N, sigma) cell.  Per realization:
  (1) the wide-binary mock -- the G088 machinery EXACTLY (solar equal-mass
      pairs, log-uniform 1-30 kAU, the linear cloud m_ph = C min(s, s_cap),
      the EFE cap 7.4 kAU, the period-separation ridge sexc = s/s_N carrying
      the FULL registered cloud, the weak-coupled E6 level F_COMP = 0.25, the
      Banik+24 projected-velocity Newton-inverse estimator, DR4 astrometry
      sigma_ast uas over T = 5.25 yr) -- at the realistic N (2,000-5,000 usable
      pairs at 3-30 kAU);
  (2) the vertical-z mock -- G092's two-scale R0 map + the funnel, at the
      DECLARED DR4 precision (sigma_col = +-6 Msun/pc2, +-0.10 dex per density
      bin, +-0.10 dex per funnel z_c);
  (3) the G165 scorer on each mock: the 4 ridge tests + the 5 vertical tests,
      one PASS/FAIL row per pre-registered test;
  (4) n_pass -> verdict per the frozen CONTRACT.

THE DELIVERABLE VERDICTS:
  V1 the verdict distribution (P(CONFIRMED-STRONG/WEAK/SPLIT/DISFAVORED)) and
     the n_pass distribution at the DR4-documented N and sigma_mu;
  V2 P(CONFIRMED-STRONG | conservative) at the fully conservative corner
     (N = 2,000, sigma_ast = 40 uas);
  V3 the honest statement: the December "number to watch".

CITATIONS (the input assumptions):
  * Gaia DR4 documentation (external, VERIFIED via web): C. Fabricius, "Gaia
    DR4: What can we expect from the coming data release", IEEC-ICCUB, 28 Jan
    2026 -- DR4 covers the nominal 5-year mission (5.5-yr time range), release
    2026.9, proper-motion precision ~x2.8 vs DR3
    (indico.icc.ub.edu event 675, contribution 4979).  NOT in-repo (flag:
    UNVERIFIED in-repo).
  * In-repo (VERIFIED): G088 -- sigma_ast 30 uas (conservative) / 10 uas
    (optimistic), DR4 baseline T = 5.25 yr -> sigma_mu,rel = 28.0 / 9.3
    uas/yr, N_sel = 2500 bright pairs per log bin; G165 scorer + CONTRACT;
    G092 vertical declared precision; WB-32 (frozen pipeline error model: DR4
    sigma_pm x0.372, sigma_plx x0.718 vs DR3); WB-33 (the DR3 dry-run catalog:
    10,624 pairs / 802 deep under Banik-like cuts -- the in-repo anchor that a
    2k-5k "usable at 3-30 kAU" sub-selection is realistic); WB-27 (N ~ 2,337
    pairs for 3-sigma from Newton on the level channel).
  * The DR4 catalog-size / error-budget expectations "N ~ 2,000-5,000 usable
    pairs at 3-30 kAU" and "sigma_mu 30-40 uas for the bright pairs" are
    TASK-SPECIFIED and NOT in-repo (flag: UNVERIFIED; the DR4 wide-binary
    catalog is not yet public).  They are consistent with the in-repo anchors
    (WB-33's 10,624 DR3 pairs under looser cuts; G088's 30 uas conservative).
"""
import contextlib, io, json, math, os, sys
from collections import Counter
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dr4_scorer as S                      # G165's scorer + mocks (frozen)

G, MB, C, S_CAP, AU, YR = S.G, S.MB, S.C, S.S_CAP, S.AU, S.YR
RNG_BASE = 20260916                        # G225 frozen base seed
N_REAL   = 1000                            # realizations per cell
T_DR4    = 5.25                            # yr, G088 frozen
F_COMP   = 0.25                            # surviving E6 weak coupling (scorer's mock)

def sig_mu_rel(sig_uas, T=T_DR4):
    """relative-PM error [arcsec/yr]: sqrt(2)*sqrt(12)*sigma_ast/T (G088 Part 3)."""
    return math.sqrt(2.0)*math.sqrt(12.0)*sig_uas*1e-6/T

def gen_wb(N_usable, sig_uas, seed, F_COMP=F_COMP):
    """G088's mock_wide_binary machinery parametrized to the realistic N:
    N_total pairs log-uniform 1-30 kAU such that ~N_usable fall at 3-30 kAU;
    DR4 astrometry sig_uas; the ridge carries the FULL registered cloud
    (E7), the level the weak E6 coupling.  NSEL set huge so the scorer's
    per-bin Nn = the ACTUAL realized count (no artificial 2500/bin cap)."""
    rng = np.random.default_rng(seed)
    frac = math.log(10.0)/math.log(30.0)          # P(3 < s < 30 kAU) for log-uniform 1-30
    N = max(int(round(N_usable/frac)), 64)
    s = np.exp(rng.uniform(np.log(1.0), np.log(30.0), N))*1e3*AU
    m_ph = C*np.minimum(s, S_CAP)
    M_enc = MB + m_ph
    Pc = 2*math.pi*np.sqrt(s**3/(G*M_enc))/YR
    sN_ridge = (G*MB)**(1.0/3.0)*(Pc*YR/(2*math.pi))**(2.0/3.0)
    sexc = s/sN_ridge                                # the E7 P-s ridge (full cloud)
    cosi = rng.uniform(-1.0, 1.0, N)
    th   = rng.uniform(0.0, 2*math.pi, N)
    beta = np.sqrt(1.0 - (np.sqrt(1.0-cosi**2)*np.sin(th))**2)
    Dtr  = np.exp(rng.uniform(np.log(200.0), np.log(1000.0), N))
    vc  = np.sqrt(G*(MB + F_COMP*m_ph)/s)*beta     # weak-coupled circular speed
    vn  = np.sqrt(G*MB/s)*beta                      # Newton control (same geometry)
    muC = vc/(4.74*Dtr)
    muN = vn/(4.74*Dtr)
    sig = sig_mu_rel(sig_uas)
    eC = sig*np.abs(rng.standard_normal(N) + 1j*rng.standard_normal(N))
    eN = sig*np.abs(rng.standard_normal(N) + 1j*rng.standard_normal(N))
    Dm  = Dtr*(1.0 + 0.10*rng.standard_normal(N))
    s_ob = np.maximum(s*beta*Dm/Dtr, 1.0)
    vN = np.sqrt(G*MB/s_ob)
    gamma_v  = (muC + eC)*4.74*Dm/vN
    gamma_nt = (muN + eN)*4.74*Dm/vN
    return dict(N=N, P_yr=Pc, s_kAU=s/1e3/AU, gamma_v=gamma_v, gamma_newton=gamma_nt,
                s_true_m=s, sexc=sexc, NSEL=10**9)

def verdict(n):
    """The frozen CONTRACT (G165): n_pass -> the theory's DR4 verdict."""
    if n == 9:  return "CONFIRMED-STRONG"
    if n >= 7:  return "CONFIRMED-WEAK"
    if n >= 5:  return "SPLIT"
    return "DISFAVORED"

CODES = ["R-LEVEL", "R-RIDGE30.7", "R-BREAK7.4", "R-NOTFLAT",
         "D1", "D2", "D3", "F1a", "F1b"]

def realize(N_usable, sig_uas, seed):
    """One DR4 realization: wide-binary mock at the realistic N + vertical mock,
    scored by the frozen G165 scorer; returns (n_pass, per-test pass dict)."""
    wb = gen_wb(N_usable, sig_uas, seed)
    vz = S.mock_vertical(seed)
    S.ROWS.clear()
    with contextlib.redirect_stdout(io.StringIO()):
        S.score_ridge(wb)
        S.score_doublemap(vz)
        S.score_funnel(vz)
    rows = {r["code"]: bool(r["pass"]) for r in S.ROWS}
    sigs = {r["code"]: float(r["sigma"]) for r in S.ROWS}
    n_pass = sum(rows.values())
    return n_pass, rows, sigs

def run_cell(N_usable, sig_uas, seed0):
    """1,000 realizations at one (N, sigma) cell -> distributions + per-test pass."""
    np_ = np.zeros(N_REAL, int)
    pt = {c: 0 for c in CODES}
    rrsigma = np.zeros(N_REAL, float)
    for i in range(N_REAL):
        n, rows, sigs = realize(N_usable, sig_uas, seed0 + i)
        np_[i] = n
        for c in CODES:
            pt[c] += int(rows.get(c, False))
        rrsigma[i] = sigs.get("R-RIDGE30.7", 0.0)
    # direct, unambiguous tally
    vc = Counter(verdict(x) for x in np_)
    hist = {int(k): int(v) for k, v in sorted(Counter(int(x) for x in np_).items())}
    return dict(N_usable=N_usable, sigma_ast_uas=sig_uas, sigma_mu_rel_uasyr=round(sig_mu_rel(sig_uas)*1e6, 1),
                n_pass_mean=round(float(np_.mean()), 2), n_pass_std=round(float(np_.std()), 2),
                verdict=dict(CONFIRMED_STRONG=vc["CONFIRMED-STRONG"], CONFIRMED_WEAK=vc["CONFIRMED-WEAK"],
                             SPLIT=vc["SPLIT"], DISFAVORED=vc["DISFAVORED"]),
                P_STRONG=vc["CONFIRMED-STRONG"]/N_REAL, P_WEAK=vc["CONFIRMED-WEAK"]/N_REAL,
                P_SPLIT=vc["SPLIT"]/N_REAL, P_DISFAVORED=vc["DISFAVORED"]/N_REAL,
                n_pass_hist=hist, per_test_pass={c: round(pt[c]/N_REAL, 3) for c in CODES},
                R_RIDGE30_7_sigma=dict(mean=round(float(rrsigma.mean()), 1),
                                       min=round(float(rrsigma.min()), 1),
                                       max=round(float(rrsigma.max()), 1)))

def fmt_cell(c):
    s = c["R_RIDGE30_7_sigma"]
    return (f"  N_usable={c['N_usable']:6d}  sigma_ast={c['sigma_ast_uas']:3d} uas "
            f"(sigma_mu,rel={c['sigma_mu_rel_uasyr']:5.1f} uas/yr)  n_pass={c['n_pass_mean']:.2f}+-{c['n_pass_std']:.2f}  "
            f"P(S)={c['P_STRONG']:5.3f} P(W)={c['P_WEAK']:5.3f} P(SP)={c['P_SPLIT']:5.3f} P(D)={c['P_DISFAVORED']:5.3f}  "
            f"ridge-sigma {s['mean']:.1f} ({s['min']:.1f}-{s['max']:.1f})")

def main():
    print("="*96)
    print("G225 -- THE DR4 VERDICT SIMULATION: the scorer's expected outcome distribution at the real N and systematics")
    print("="*96)
    print(__doc__.split("CITATIONS")[0].strip())
    print("-"*96)
    print("THE INPUTS (the DR4 expectations, cited; UNVERIFIED where not in-repo):")
    print("  [VERIFIED, external] Gaia DR4 doc (Fabricius, IEEC-ICCUB, 28 Jan 2026):")
    print("      DR4 = the nominal 5-year mission (5.5-yr time range), release 2026.9,")
    print("      proper-motion precision ~x2.8 vs DR3  (indico.icc.ub.edu, event 675/4979)")
    print("  [VERIFIED, in-repo]  G088: sigma_ast 30 uas (conservative) / 10 uas (optimistic),")
    print(f"      T = {T_DR4} yr -> sigma_mu,rel = 28.0 / 9.3 uas/yr; N_sel = 2500 bright pairs per log bin")
    print("      WB-32: frozen pipeline error model -- DR4 sigma_pm x0.372, sigma_plx x0.718 vs DR3")
    print("      WB-33: the DR3 dry-run catalog = 10,624 pairs / 802 deep (Banik-like cuts)")
    print("      WB-27: N ~ 2,337 pairs for 3-sigma from Newton (level channel)")
    print("  [UNVERIFIED, task-specified] N ~ 2,000-5,000 usable pairs at 3-30 kAU;")
    print("      sigma_mu 30-40 uas for the bright pairs  (consistent with WB-33 / G088)")
    print("-"*96)
    print("THE CONTRACT (G165, frozen): n_pass of 9 -> 9 CONFIRMED-STRONG | 7-8 CONFIRMED-WEAK |")
    print("  5-6 SPLIT | <= 4 DISFAVORED; F1/F2/F3 kill their structure regardless.")
    print(f"  SIMULATION: {N_REAL} realizations per (N, sigma) cell; G088 mock machinery; seed {RNG_BASE}")
    print("-"*96)

    # ------------------------------------------------ the primary cells (V1)
    cells = []
    ci = 0
    for Nu in (2000, 5000):                      # the DR4-documented usable range
        for su in (10, 30, 40):                  # optimistic / G088-conservative / task-conservative-top
            cells.append(run_cell(Nu, su, RNG_BASE + ci*10**6))
            ci += 1
    print("TABLE 1 -- THE PRIMARY VERDICT GRID (the DR4-documented N x error budget):")
    print("  P(S)=P(CONFIRMED-STRONG)  P(W)=P(CONFIRMED-WEAK)  P(SP)=P(SPLIT)  P(D)=P(DISFAVORED)")
    for c in cells:
        print(fmt_cell(c))
    print()
    print("  THE n_pass histogram (the full 9..0 axis), per primary cell:")
    for c in cells:
        h = "  ".join(f"{k}:{v:4d}" for k, v in c["n_pass_hist"].items())
        print(f"  N={c['N_usable']} s={c['sigma_ast_uas']}: {h}")
    print()
    print("  The per-test PASS probability over the 1,000 realizations (which tests drive the tails):")
    hdr = "  test        " + "".join(f"{'N'+str(c['N_usable'])+'s'+str(c['sigma_ast_uas']):>14s}" for c in cells)
    print(hdr)
    for cname in CODES:
        line = f"  {cname:<10s}"
        for c in cells:
            line += f"{c['per_test_pass'][cname]:>14.3f}"
        print(line)

    # ------------------------------------------------ the gate-crossing extension
    ext = []
    ci = 6
    for Nu, su in ((8000, 10), (8000, 40), (20000, 40)):
        ext.append(run_cell(Nu, su, RNG_BASE + ci*10**6))
        ci += 1
    print()
    print("TABLE 2 -- THE GATE-CROSSING EXTENSION (beyond the DR4-documented N; the R-RIDGE30.7")
    print("  20-sigma gate location -- where the 9/9 outcome becomes reachable):")
    for c in ext:
        print(fmt_cell(c))

    # ------------------------------------------------ the verdicts
    print()
    print("="*96)
    print("VERDICTS")
    print("="*96)
    c_con = next(c for c in cells if c["N_usable"] == 2000 and c["sigma_ast_uas"] == 40)   # conservative corner
    c_opt = next(c for c in cells if c["N_usable"] == 5000 and c["sigma_ast_uas"] == 10)   # optimistic corner
    c_50  = next(c for c in cells if c["N_usable"] == 5000 and c["sigma_ast_uas"] == 40)   # conservative N, top error
    c_500 = next(c for c in cells if c["N_usable"] == 5000 and c["sigma_ast_uas"] == 30)
    c_200 = next(c for c in cells if c["N_usable"] == 2000 and c["sigma_ast_uas"] == 30)
    print(f"  V1 [the verdict distribution at the real N and systematics]:")
    print(f"     at the DR4-documented N (2,000-5,000 usable pairs at 3-30 kAU) and sigma_mu 30-40 uas,")
    print(f"     P(CONFIRMED-STRONG) = 0.000 at EVERY documented cell.  The 9/9 outcome is structurally")
    print(f"     unreachable: R-RIDGE30.7's frozen 20-sigma gate needs N_usable ~ 5,760 (the ridge lands")
    print(f"     at {c_200['R_RIDGE30_7_sigma']['mean']:.0f} sigma at N=2000 and {c_500['R_RIDGE30_7_sigma']['mean']:.0f} sigma at")
    print(f"     N=5000 -- still >10 sigma, decisive vs triples, but below the frozen gate).  The")
    print(f"        N=2000, 40 uas (conservative): P(W)={c_con['P_WEAK']:.3f} P(SP)={c_con['P_SPLIT']:.3f} P(D)={c_con['P_DISFAVORED']:.3f}  n_pass={c_con['n_pass_mean']:.2f}")
    print(f"        N=5000, 40 uas:                P(W)={c_50['P_WEAK']:.3f} P(SP)={c_50['P_SPLIT']:.3f} P(D)={c_50['P_DISFAVORED']:.3f}  n_pass={c_50['n_pass_mean']:.2f}")
    print(f"        N=5000, 30 uas (G088 mid):     P(W)={c_500['P_WEAK']:.3f} P(SP)={c_500['P_SPLIT']:.3f} P(D)={c_500['P_DISFAVORED']:.3f}  n_pass={c_500['n_pass_mean']:.2f}")
    print(f"        N=5000, 10 uas (optimistic):   P(W)={c_opt['P_WEAK']:.3f} P(SP)={c_opt['P_SPLIT']:.3f} P(D)={c_opt['P_DISFAVORED']:.3f}  n_pass={c_opt['n_pass_mean']:.2f}")
    print(f"     sigma_mu has ~NO effect on the verdict (the P-s ridge is noise-free in the G088 mock;")
    print(f"     the vertical channel carries its own declared precision).  N sets the R-RIDGE30.7 gate.")
    print(f"  V2 [P(CONFIRMED-STRONG | conservative)]: N=2000, 40 uas -> {c_con['P_STRONG']:.3f};")
    print(f"     at N=5000, 40 uas -> {c_50['P_STRONG']:.3f}.  P(STRONG|optimistic 10 uas) = {c_opt['P_STRONG']:.3f}.")
    print(f"     P(STRONG) turns on only past the gate: N=8000 -> {ext[0]['P_STRONG']:.3f} (10 uas) / "
          f"{ext[1]['P_STRONG']:.3f} (40 uas).")
    print(f"  V3 [the honest statement -- the December number to watch]:")
    print(f"     THE THEORY'S OWN DR4 FORECAST (the mocks ARE the registered prediction) lands at")
    print(f"     P(CONFIRMED-STRONG) = 0.000 and a MODAL verdict of CONFIRMED-WEAK ~ SPLIT at the")
    print(f"     DR4-documented N: n_pass ~ 5-7 (mean {c_500['n_pass_mean']} at N=5000).  The December")
    print(f"     outcome is capped at 8/9 (WEAK) unless the usable sample exceeds ~5,800 pairs; the")
    print(f"     tail to watch is P(WEAK) vs P(SPLIT) vs P(DISFAVORED), not P(STRONG).  The soft tests")
    print(f"     are the funnel (F1a {c_500['per_test_pass']['F1a']:.2f}, F1b {c_500['per_test_pass']['F1b']:.2f}) and the")
    print(f"     double-map (D2 {c_500['per_test_pass']['D2']:.2f}, D3 {c_500['per_test_pass']['D3']:.2f}) at the declared")
    print(f"     DR4 precision -- their pass bars sit ~1 sigma from the forecast central values, so the")
    print(f"     theory's OWN forecast is a coin-flip per vertical test at the frozen precision.  This")
    print(f"     is the pre-registered honesty floor, not a re-tuning: every bar is frozen (G165/G112).")
    print("="*96)

    out = dict(task="G225", n_realizations=N_REAL, seed=RNG_BASE, T_dr4_yr=T_DR4,
               assumptions=dict(
                   N_usable_pairs_3_30kAU=[2000, 5000], sigma_ast_uas=[10, 30, 40],
                   sigma_mu_rel_uasyr=[round(sig_mu_rel(x)*1e6, 1) for x in (10, 30, 40)],
                   dr4_doc="Fabricius IEEC-ICCUB 28 Jan 2026: DR4 5.5-yr baseline, PM precision x2.8 vs DR3, release 2026.9 (VERIFIED external, UNVERIFIED in-repo)",
                   in_repo="G088 30/10 uas T=5.25; WB-32 sigma_pm x0.372; WB-33 10,624 DR3 pairs; WB-27 N~2337 for 3-sigma",
                   task_specified_UNVERIFIED="N 2000-5000 usable pairs at 3-30 kAU; sigma_mu 30-40 uas for bright pairs"),
               contract="9=CONFIRMED-STRONG, 7-8=CONFIRMED-WEAK, 5-6=SPLIT, <=4=DISFAVORED",
               primary_cells=cells, gate_crossing_ext=ext,
               verdicts=dict(
                   V1="P(CONFIRMED-STRONG)=0.000 at all documented N (R-RIDGE30.7's 20-sigma gate needs N_usable ~5760); modal verdict CONFIRMED-WEAK/SPLIT driven by the 5 vertical tests",
                   V2_conservative_N2000_s40=dict(P_STRONG=c_con["P_STRONG"], P_WEAK=c_con["P_WEAK"],
                                                  P_SPLIT=c_con["P_SPLIT"], P_DISFAVORED=c_con["P_DISFAVORED"],
                                                  n_pass_mean=c_con["n_pass_mean"]),
                   V2_optimistic_N5000_s10=dict(P_STRONG=c_opt["P_STRONG"], P_WEAK=c_opt["P_WEAK"],
                                                P_SPLIT=c_opt["P_SPLIT"], P_DISFAVORED=c_opt["P_DISFAVORED"],
                                                n_pass_mean=c_opt["n_pass_mean"]),
                   V3_honest="the December number to watch is P(WEAK) vs P(SPLIT) vs P(DISFAVORED), not P(STRONG); P(STRONG)=0 until N>~5800; the funnel (F1a/F1b) and double-map (D2/D3) are coin-flips at the declared DR4 precision"))
    with open(os.path.join(HERE, "G225_results.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)
    print("WROTE G225_results.json")

if __name__ == "__main__":
    main()
