#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG245 Gate A -- AMOUNT: the supply ceiling, the relaxed state and the selectivity control (frozen criteria section 3).

  A0 (BINDING)  S = the bound cold mass of the passive CFG244 run (frac_bound_all x M_out; read-only JSON), point cores; the target at x = 30 needs
                M_ph = M_b (sqrt(901) - 1) = 29.02 M_b.  PASS iff S/M_ph(<30) >= 0.90 at every mass and every q.  Reported: x_cap, x(S/M_ph = 0.9), cosmic-share cap, budget row.
  A1            relaxed state (Gamma = infinity, M_c = min(M_ph, S)): C within 10% on x in [0.3, x_cap] by construction (P-DECLARED); exponential spheres against C_loc and C_44.
  A2            selectivity: a Verlinde-shaped target (M_V = M_b x) handed to the relaxed operator is reproduced to 1e-12 where supply allows (P-derived impossible).
  A3 (reported) SHMR-halo supply (f_ret from CFG243 README:74; a declared function shape) and the renormalised-amplitude reading.
Run: ZF_REPO=<repo> python3 CFG245_A_supply.py ; MUTATE=MM1|MA1|MA2 python3 CFG245_A_supply.py   (exits 1 when the control bites)
"""
import os, sys, math
sys.dont_write_bytecode = True
import numpy as np
from scipy.special import gammainc
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG245_common as K

MUT = os.environ.get("MUTATE", "").strip()
SLUG = "CFG245_A_supply"
POST = (K.upstream_binding() is not None) and not MUT
if POST:
    SLUG += "_POSTHOC"
R = K.Report(SLUG, MUT or None)
X30 = 30.0
MPH30 = math.sqrt(1 + X30 ** 2) - 1.0
HEXP = {1e9: 2.0, 1e10: 3.0, 1e11: 4.0, 1e12: 5.0}
F_RET = {1e9: 0.104, 1e10: 0.258, 1e11: 0.086, 1e12: 0.002}      # CFG243_turnaround_dust/README.md:74 (committed SHMR retained fractions)


def xcap(S):
    return math.sqrt((S + 1.0) ** 2 - 1.0)


def x_at_ratio(S, rho=0.9):
    return math.sqrt((S / rho + 1.0) ** 2 - 1.0)


def supply_table(create=False, S_override=None):
    tab = {}
    for M in K.MASSES:
        for q in K.QS:
            r = K.point_run(M, q, 20000)
            S = r["diag"]["frac_bound_all"] * r["setup"]["M_out"] / M
            if S_override is not None:
                S = S_override
            tab[(M, q)] = dict(S=S, Mta=r["setup"]["M_ta"] / M, ratio30=(float("inf") if create else S / MPH30), xcap=(float("inf") if create else xcap(S)),
                               x09=(float("inf") if create else x_at_ratio(S)), frac_bound=r["diag"]["frac_bound_all"], M_out_over_Mb=r["setup"]["M_out"] / M)
    return tab


def main():
    R.banner("CFG245 Gate A -- AMOUNT (supply ceiling, relaxed state, selectivity)" + ("  (POST-HOC EXTRA: an upstream gate already bound)" if POST else "") + (f"  (MUTATE {MUT})" if MUT else ""))
    S_over = None
    create = False
    if MUT == "MA2":
        S_over = K.OMEGA_C_OVER_B
    if MUT == "MM1":
        create = True
    if MUT == "MA1":
        create = True        # S = infinity, Gamma = infinity, target := the true C(r) (for a point mass identical to the local-field target)
    base = supply_table()
    tab = supply_table(create=create, S_override=S_over)
    # ---------------------------------------------------------------- controls
    R.banner("CONTROLS")
    ctl = {}
    r1 = [base[k]["Mta"] for k in base]
    ok_a1 = all(abs(v - 23.6) / 23.6 < 0.01 for v in r1)
    ctl["C-A1"] = ok_a1
    R.cell("C-A1 the passive set-up reproduces CFG118's z = 0 turnaround mass 23.6 M_b at every mass (CFG118 README:55) within 1%", "PASS" if ok_a1 else "FAIL",
           f"M_ta/M_b = {min(r1):.3f}-{max(r1):.3f}; S/M_b = {min(base[k]['S'] for k in base):.2f}-{max(base[k]['S'] for k in base):.2f} (bound cold mass incl. the bound shells beyond the turnaround)")
    # ---------------------------------------------------------------- A0
    R.banner("A0 -- supply ceiling: S/M_ph(<30) >= 0.90 at every mass and bracket (BINDING)")
    R.P(f"  target at x = 30: M_ph = M_b (sqrt(901) - 1) = {MPH30:.3f} M_b")
    R.P(f"  {'M_b':>8s} {'q':>5s} {'S/M_b':>8s} {'frac bound':>11s} {'S/M_ph(<30)':>12s} {'x_cap':>7s} {'x(S/Mph=.9)':>12s}")
    for (M, q), v in sorted(tab.items()):
        R.P(f"  {M:8.0e} {q:5.2f} {v['S']:8.3f} {v['frac_bound']:11.5f} {v['ratio30']:12.4f} {v['xcap']:7.2f} {v['x09']:12.2f}")
    minratio = min(v["ratio30"] for v in tab.values())
    a0_ok = all(v["ratio30"] >= 0.90 for v in tab.values())
    minratio_b = min(v["ratio30"] for v in base.values())
    maxratio_b = max(v["ratio30"] for v in base.values())
    a0_base_ok = all(v["ratio30"] >= 0.90 for v in base.values())
    R.P(f"  min ratio = {minratio:.4f}; max = {max(v['ratio30'] for v in tab.values()):.4f}  (line 0.90; frozen hand: 0.78 for S = 22.6 M_b or 0.86 for S = 25)")
    margin_note = (f"KNIFE-EDGE: S/M_ph(<30) = {minratio_b:.4f}-{maxratio_b:.4f} against the line 0.90 (a margin of 0.3-1.4% of the ratio; one shell is 0.0039 M_b = 1.3e-4 of the target); "
                   "the frozen line is applied exactly and the failure is reported as a failure of the frozen line, not as a large shortfall") if (not a0_base_ok and minratio_b > 0.88) else ""
    R.cell("A0 supply ceiling (baseline, passive S)", "PASS" if a0_base_ok else "FAIL (BINDING)", f"min S/M_ph(<30) = {minratio_b:.4f}. " + margin_note)
    R.P(f"  cosmic-share cap (S = 5.36 M_b, CFG131 README:7): x_cap = {xcap(K.OMEGA_C_OVER_B):.2f}; the record's cosmic budget row: Omega_ph = 0.47-0.55 against Omega_c = 0.265 if every galaxy's phantom ran to its turnaround radius (CFG4_README.md:296)")
    # ---------------------------------------------------------------- A1
    R.banner("A1 -- relaxed state (Gamma = infinity), M_c = min(M_ph, S): C within 10% to x_cap (P-DECLARED); beyond x_cap the fluid is exhausted")
    xg = K.XC
    a1 = {}
    for M in K.MASSES:
        S = np.mean([base[(M, q)]["S"] for q in K.QS])
        Mph = K.Mph_point(xg)
        Mc = np.minimum(Mph, S)
        Rr = Mc / Mph
        inside = xg <= xcap(S)
        a1[M] = dict(S=float(S), xcap=xcap(S), ok_to_cap=bool(np.all(np.abs(Rr[inside] - 1) < 1e-12)), R_at_28=float(Rr[-1]), R_at_30=float(min(S, MPH30) / MPH30),
                     dex_at_28=float(K.delta_dex(Mc[-1], Mph[-1], 1.0)), dex_at_30=float(math.log10((1 + min(S, MPH30)) / (1 + MPH30))))
        R.P(f"  M_b = {M:.0e}: S = {S:.2f} M_b, x_cap = {xcap(S):.2f}; R_cum = 1 to machine precision for x <= x_cap ({a1[M]['ok_to_cap']}); R_cum(x = 28.2) = {a1[M]['R_at_28']:.4f} ({a1[M]['dex_at_28']:+.3f} dex in g_tot); R_cum(x = 30) = {a1[M]['R_at_30']:.4f} ({a1[M]['dex_at_30']:+.3f} dex); local C/C_target = 0 beyond x_cap")
    R.cell("A1 relaxed state (point cores)", "PASS as P-DECLARED (selectivity: not a result; the scale is supplied by the target)", "controls: R_cum = 1 for x <= x_cap at every mass")
    # exponential spheres: local-field target vs C_44 cumulative targets from the sims' own exponential-sphere runs
    R.P("  exponential spheres (CFG118 h = 2,3,4,5 kpc): the relaxed fluid at Gamma = infinity builds the LOCAL-FIELD target M_ph,loc(<r) = (nu - 1) M_b(<r); the shared G1 target is the sims' C_44 cumulative mass")
    expo = {}
    for foot in K.FOOTS:
        for M in K.MASSES:
            rr = None
            for r in K.sims()["runs"]:
                sp = r["spec"]
                if sp["kind"] == "main" and sp["geom"] == "exp" and sp["M"] == M and sp["q"] == 0.1 and sp["N"] == 20000:
                    rr = r
            McT = np.array(rr["foot"][foot]["target"]["Mc"])
            hh = HEXP[M] / K.r_M(M, foot)
            Mb_enc = gammainc(3.0, xg / hh)
            y = Mb_enc / xg ** 2
            Mphl = (K.nu_p2(y) - 1.0) * Mb_enc * M
            m = (xg >= 0.3) & (xg <= 30)
            ratio = Mphl[m] / McT[m]
            expo[f"{foot}|{M:.0e}"] = dict(max=float(ratio.max()), min=float(ratio.min()))
        R.P(f"    {foot:10s}: M_ph,loc(<r)/M_target,44(<r) over x in [0.3, 28.2]: " + "  ".join(f"{M:.0e}: {expo[f'{foot}|{M:.0e}']['min']:.3f}-{expo[f'{foot}|{M:.0e}']['max']:.3f}" for M in K.MASSES))
    R.P("    -> the class cannot pass the shared G1 exponential-sphere cell against C_44 even at Gamma = infinity wherever this ratio leaves [0.90, 1.10] (stated, per G0.2)")
    # ---------------------------------------------------------------- A2
    R.banner("A2 -- selectivity: a Verlinde-shaped target handed to the relaxed operator (M_V = M_b x) is reproduced")
    dev = 0.0
    for M in K.MASSES:
        S = np.mean([base[(M, q)]["S"] for q in K.QS])
        MV = xg
        Mc = np.minimum(MV, S)
        inside = xg <= S
        dev = max(dev, float(np.abs(Mc[inside] / MV[inside] - 1).max()))
    R.cell("A2 selectivity: the relaxed state reproduces M_V = M_b x to 1e-12 where supply allows", "PASS (restatement: P-derived impossible)" if dev < 1e-12 else "FAIL", f"max deviation {dev:.2e}")
    # ---------------------------------------------------------------- A3
    R.banner("A3 -- supply sensitivity rows (reported, not binding)")
    shm = {}
    for M in K.MASSES:
        S = K.OMEGA_C_OVER_B / F_RET[M]
        shm[M] = dict(S=S, ratio30=S / MPH30, xcap=xcap(S))
        R.P(f"  SHMR-halo supply (declared function shape, f_ret = {F_RET[M]}): M_b = {M:.0e}: S = {S:.1f} M_b, S/M_ph(<30) = {S/MPH30:.2f}, x_cap = {xcap(S):.1f}"
            + ("  [f_ret = 0.002 at 1e12 is the record's own flagged-absurd Moster inversion]" if M == 1e12 else ""))
    R.P("  renormalised-amplitude reading: a0_eff = [S/M_ph(<R_b)]^2 a0 with R_b = r_ta(z = 0) of the passive run")
    amp = {}
    for foot in K.FOOTS:
        row = []
        for M in K.MASSES:
            r = K.point_run(M, 0.1, 20000)
            xta = r["setup"]["r_ta0"] / K.r_M(M, foot)
            S = base[(M, 0.1)]["S"]
            a = S / (math.sqrt(1 + xta ** 2) - 1.0)
            row.append((xta, a, a ** 2))
        amp[foot] = row
        R.P(f"    {foot:10s}: x_ta = " + ", ".join(f"{r[0]:.0f}" for r in row) + "; S/M_ph(<r_ta) = " + ", ".join(f"{r[1]:.3f}" for r in row) +
            f"; amplitude spread {max(r[1] for r in row)/min(r[1] for r in row):.2f} (a0_eff spread {math.log10(max(r[2] for r in row)/min(r[2] for r in row)):.2f} dex)")
    # ---------------------------------------------------------------- MUTATE
    if MUT:
        if MUT == "MM1":
            # creation form, no cap: A0 flips; mass-conservation cell flips
            created = K.relaxed_Mc(K.passive(1e10, 0.1, "canonical")["Minf"], K.passive(1e10, 0.1, "canonical")["Mph"], 1e99, 0.0, "two", create=True)
            dm = float((created[-1] - K.passive(1e10, 0.1, "canonical")["Minf"][-1]) / 1e10)
            R.P(f"  MUTATE MM1: A0 baseline {'PASS' if a0_base_ok else 'FAIL'} -> creation form {'PASS' if a0_ok else 'FAIL'}; mass created inside D at Gamma = infinity: {dm:+.3f} M_b (baseline 0)")
            bites = (a0_base_ok != a0_ok) and abs(dm) > 1e-6
        elif MUT == "MA1":
            R.P(f"  MUTATE MA1: evaluator fed the true C(r) with S = infinity and Gamma = infinity: A0 baseline {'PASS' if a0_base_ok else 'FAIL'} -> {'PASS' if a0_ok else 'FAIL'}; A1 R_cum = 1 on the whole grid")
            bites = (a0_base_ok != a0_ok)
        elif MUT == "MA2":
            xb = np.mean([base[k]["xcap"] for k in base]); xm = np.mean([tab[k]["xcap"] for k in tab])
            R.P(f"  MUTATE MA2: S = 5.36 M_b: x_cap {xb:.2f} -> {xm:.2f}; A0 {'PASS' if a0_ok else 'FAIL'} (baseline {'PASS' if a0_base_ok else 'FAIL'})")
            bites = abs(xm / xb - 1) > 0.5
        else:
            raise SystemExit(f"MUTATE {MUT} is not a Gate A control")
        R.finish(dict(binding_fail=False, mutate_bites=bool(bites)))
        K.exit_mutate(bites, True)
    binding = not a0_base_ok
    R.numbers = dict(A0={f"{M:.0e}|{q}": v for (M, q), v in base.items()}, min_ratio30=minratio_b, max_ratio30=maxratio_b, A1={f"{M:.0e}": v for M, v in a1.items()},
                     A1_expo={k: v for k, v in expo.items()}, A2_dev=dev, A3_shmr={f"{M:.0e}": v for M, v in shm.items()},
                     A3_amp={f: [dict(x_ta=r[0], ratio=r[1], a0eff=r[2]) for r in v] for f, v in amp.items()}, x_cosmic_cap=xcap(K.OMEGA_C_OVER_B), controls=ctl)
    R.finish(dict(binding_fail=bool(binding), controls_ok=bool(ok_a1), post_hoc=POST, a0_min_ratio=minratio_b))
    return 0


if __name__ == "__main__":
    sys.exit(main())
