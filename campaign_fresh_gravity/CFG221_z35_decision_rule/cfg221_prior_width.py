#!/usr/bin/env python3
"""CFG221 ADDENDUM 3 (frozen 5398e74b9 before any operating-characteristics table was read): the prior-width sweep and the C2 diagnostic.
(1) The noise-free control C2 of cfg221_decision_rule.py failed (6 of 12): here, for the frozen sigma and for each swept sigma, the per-(truth, N) verdict and the status of each law in
each of the four cells for the noise-free mock (no measurement noise, no extra scatter, true offset 0), to show WHICH cell breaks it.
(2) The sweep: the same rule, mocks and controls with sigma scaled by s in {1 (the frozen widths, for reference), 0.5, 0.33} in both the rule and the PRIOR draws, REAL scenario, true offsets
c in {0, PRIOR}, N in {13, 20, 36, 50}, both truths, K = 100 mocks, seed 221, B = 500.  Reports P(correct)/P(wrong), FEASIBLE (P(correct) >= 0.8 for both truths at c = 0),
FALSE-SEPARATION-CONTROLLED (wrong <= 0.094 at c = 0 and PRIOR) and sigma_required = the largest tested scale with FEASIBLE at some N <= 50 and false separation controlled.
Run:  python3 campaign_fresh_gravity/CFG221_z35_decision_rule/cfg221_prior_width.py        (a few minutes on 16 cores)
"""
import os, sys, json, math, time
sys.dont_write_bytecode = True
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg221_decision_rule as M                      # the frozen rule's functions; its top-level definitions only (its driver sits under __main__)

SCALES = (1.0, 0.5, 0.33)
NS = (13, 20, 36, 50)
K_MOCK, NB = M.K_MOCK, M.NB


def sweep_cell(task):
    s, truth, c, N, i = task
    M.SIGMA = M.np.array([0.30, 0.30, 0.40]) * s                  # gen_mock reads the module global at call time
    rng = np.random.default_rng(np.random.SeedSequence([221, 5000 + i]))
    cnt = {"LO": 0, "HI": 0, "NONE": 0}
    for _ in range(K_MOCK):
        v, _, _ = M.rule(M.gen_mock(M.BASE, N, truth, c, M.SCEN["REAL"], rng), "FLAT", "H(z)", NB, rng, sigma=M.SIGMA)
        cnt[v] += 1
    return task, cnt


if __name__ == "__main__":
    out = []

    def P(s=""):
        print(s, flush=True); out.append(s)

    P(__doc__.split("Run:")[0].strip())
    t0 = time.time()
    # ---------------------------------------------------------------- (1) the noise-free diagnostic
    P("\n(1) NOISE-FREE MOCK (no measurement noise, no extra scatter, true offset 0), statuses (flat / rival) per cell [primary, mono-alt, P2-can, P2-alt] and the verdict, by sigma scale")
    for s in SCALES:
        sig = np.array([0.30, 0.30, 0.40]) * s
        M.SIGMA = sig
        rng = np.random.default_rng(np.random.SeedSequence([221, 999]))
        ok = 0
        P(f"  sigma scale {s} (sigma_dust {0.30 * s:.2f} dex):")
        for truth, want in (("FLAT", "LO"), ("H(z)", "HI")):
            for N in M.NGRID:
                mock = M.gen_mock(M.BASE, N, truth, 0.0, 0.0, rng, noise=False)
                v, res, med = M.rule(mock, "FLAT", "H(z)", NB, rng, sigma=sig)
                ok += v == want
                P(f"    truth {truth:5s} N = {N:2d}: verdict {v:4s} " + "  ".join(f"{res[(c, 'FLAT')][0]}/{res[(c, 'H(z)')][0]}" for c in M.CELLS) + f"   rival CI upper by cell " + " ".join(f"{med[(c, 'H(z)')][1]:+.2f}" for c in M.CELLS)
                  + "; flat CI [" + " ".join(f"{med[(c, 'FLAT')][0]:+.2f},{med[(c, 'FLAT')][1]:+.2f}" for c in M.CELLS[:2]) + " ...]")
        P(f"    -> correct separation {ok}/12")
    # ---------------------------------------------------------------- (2) the sweep
    import multiprocessing as mp
    tasks, i = [], 0
    for s in SCALES:
        for truth in ("FLAT", "H(z)"):
            for c in (0.0, "PRIOR"):
                for N in NS:
                    tasks.append((s, truth, c, N, i)); i += 1
    P(f"\n(2) SWEEP: {len(tasks)} cells x {K_MOCK} mocks (REAL; the true offset 0 or drawn from the same scaled prior)")
    with mp.get_context("spawn").Pool(processes=min(15, mp.cpu_count())) as pool:
        results = pool.map(sweep_cell, tasks, chunksize=1)
    R = {(t[0], t[1], str(t[2]), t[3]): cnt for t, cnt in results}
    lim = 0.05 + 2 * math.sqrt(0.05 * 0.95 / K_MOCK)

    def rt(s, truth, c, N):
        cnt = R[(s, truth, str(c), N)]
        return (cnt["LO"] if truth == "FLAT" else cnt["HI"]) / K_MOCK, (cnt["HI"] if truth == "FLAT" else cnt["LO"]) / K_MOCK

    sig_req = None
    for s in SCALES:
        P(f"\n  sigma scale {s} (sigma_dust = sigma_CO = {0.30 * s:.2f}, sigma_[CII] = {0.40 * s:.2f} dex): P(correct)/P(wrong) at N = " + " ".join(f"{N:>9d}" for N in NS))
        for truth in ("FLAT", "H(z)"):
            for c in (0.0, "PRIOR"):
                P(f"    {truth:5s} c = {str(c):6s}  " + " ".join(f"{rt(s, truth, c, N)[0]:4.2f}/{rt(s, truth, c, N)[1]:4.2f}" for N in NS))
        feas = [N for N in NS if min(rt(s, "FLAT", 0.0, N)[0], rt(s, "H(z)", 0.0, N)[0]) >= 0.8]
        ctl = max(rt(s, t, c, N)[1] for t in ("FLAT", "H(z)") for c in (0.0, "PRIOR") for N in NS) <= lim
        best = max(min(rt(s, "FLAT", 0.0, N)[0], rt(s, "H(z)", 0.0, N)[0]) for N in NS)
        P(f"    FEASIBLE (P(correct) >= 0.8 for both truths at c = 0): " + (f"yes, N_feasible = {feas[0]}" if feas else f"no (best min power {best:.2f})") + f";  false separation {'CONTROLLED' if ctl else 'NOT controlled'} (line {lim:.3f})")
        if feas and ctl and (sig_req is None or s > sig_req):
            sig_req = s
    P("\n  sigma_required (the largest tested scale with FEASIBLE at some N <= 50 and false separation controlled): " + (f"scale {sig_req} (sigma_dust = sigma_CO = {0.30 * sig_req:.2f} dex)" if sig_req is not None else "none of the tested widths"))
    P(f"\n{time.time() - t0:.0f} s")
    open(os.path.join(HERE, "cfg221_prior_width.out"), "w").write("\n".join(out) + "\n")
    json.dump({"|".join(map(str, k)): v for k, v in R.items()}, open(os.path.join(HERE, "cfg221_prior_width_results.json"), "w"), indent=1)
