"""CFG183 attack (e): mock KURVS worlds under each of the three laws. usage: python CFG183_null_e.py SEED   (183 or 184). Exit 0.
N = 10,000 per (world, family). Mock truth = real ten-disc baryons, sigma_out, errors, anchor (+0.092 dex z=0 offset added to g)."""
import os, sys, json, math, copy
import numpy as np
import CFG183_common as C
from CFG183_common import M, pr
from multiprocessing import Pool

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 183
N = int(os.environ.get("CFG183_N", "10000"))
WORLDS = {"W1": ("T", 0.0, 1.0), "W2": ("flat", 1.0, 2.14), "W3": ("rival", 1.0, 0.65), "W4": ("T", 1.0, 4.3), "W5": ("flat", 0.4, 0.67), "W6": ("rival", 1.03, 0.67)}
FAMS = ("ideal", "N1", "ideal+sc", "N1+sc")   # +sc = POST-HOC variant (added after seeing the frozen families): 0.12 dex intrinsic per-disc scatter in log g
OFFSET = 0.092
S, AS, K = C.load("inc_star_deg")
LAW = {"flat": C.make_law("flat"), "rival": C.make_law("rival"), "T": C.make_law("T")}
Cbase = M.corr(S, C.spec_s(1.0))[0]          # C for s = 1 (linear in s)
A0 = M.A0["canonical"]
GRID = np.exp(np.linspace(math.log(0.05), math.log(30.0), 40))
Rm = S.R * M.KPC / 1e6

def make_mock(rng, law, s_true, mu_true, fam, noise=True):
    n = len(S.z)
    dlogM = rng.normal(0, S.mass_err, n) if noise else np.zeros(n)
    St = copy.copy(S); St.logM = S.logM + dlogM
    base = fam.split("+")[0]
    mu = np.full(n, mu_true) if base == "ideal" else mu_true * 10 ** (0.3 * rng.normal(size=n))
    gb = M.gbar(St, mu, 0.0)
    f = LAW[law](S.z)
    g = M.gpred(gb, A0 * f) * 10 ** OFFSET
    if noise and fam.endswith("+sc"):
        g = g * 10 ** (0.12 * rng.normal(size=n))
    Vc2 = g * Rm
    if base == "ideal":
        alpha_mult = np.ones(n)
    else:
        alpha_mult = np.exp(rng.normal(0, 0.4, n)) * math.exp(rng.normal(0, 0.2))
    Cm = s_true * Cbase * alpha_mult
    V2 = np.maximum(Vc2 - Cm, 0.0025 * Vc2)
    floored = float(np.mean(Vc2 - Cm < 0.0025 * Vc2))
    V = np.sqrt(V2)
    if noise:
        itrue = S.inc + rng.normal(0, S.einc, n)
        V = V * np.sin(np.clip(itrue, 0.05, 1.55)) / np.sin(S.inc) + rng.normal(0, S.eV, n)
    Sm = copy.copy(S); Sm.V = V
    return Sm, floored

def analyse_mock(Sm):
    out = {}
    z = lambda t: t[0] / t[1]
    for s in (0.0, 1.0):
        c = C.cell(Sm, AS, s, 0.67, None)
        out["zf%d" % s] = z(c["flat"]); out["zr%d" % s] = z(c["H"])
    cf = C.cell(Sm, AS, 1.0, C.CEIL, None)
    out["excl_f"] = z(cf["flat"]) > 1.0; out["excl_r"] = z(cf["H"]) > 1.0
    with C.law_ctx(LAW["T"]):
        for s in (0.0, 1.0):
            out["zt%d" % s] = z(C.cell(Sm, AS, s, 0.67, None)["H"])
        out["excl_t"] = z(C.cell(Sm, AS, 1.0, C.CEIL, None)["H"]) > 1.0
        d = np.array([C.cell(Sm, AS, 0.0, m, None)["H"][0] for m in GRID])
    out["dt0"] = C.cell(Sm, AS, 0.0, 0.67, LAW["T"])["H"][0]
    # T break-even at P0 (sign change of D' on the grid; D' decreasing in mu)
    if d[0] < 0: be = 0.0
    elif d[-1] > 0: be = np.inf
    else:
        i = int(np.argmax(d < 0)); t = d[i - 1] / (d[i - 1] - d[i]); be = math.exp(math.log(GRID[i - 1]) + t * (math.log(GRID[i]) - math.log(GRID[i - 1])))
    out["be0"] = be
    return out

def job(args):
    wn, fam, seed = args
    law, s_true, mu_true = WORLDS[wn]
    rng = np.random.default_rng([seed, int(wn[1:]), FAMS.index(fam)])
    rows = []; fl = []
    for k in range(N):
        Sm, f = make_mock(rng, law, s_true, mu_true, fam)
        rows.append(analyse_mock(Sm)); fl.append(f)
    keys = rows[0].keys()
    arr = {k: np.array([r[k] for r in rows], float) for k in keys}
    O = (np.abs(arr["zt0"]) <= 1.5) & (arr["zf0"] <= -2) & (arr["zr0"] <= -3.5)
    res = dict(world=wn, fam=fam, seed=seed, law=law, s_true=s_true, mu_true=mu_true, N=N,
               mean=dict(zt0=float(arr["zt0"].mean()), zf0=float(arr["zf0"].mean()), zr0=float(arr["zr0"].mean()), zt1=float(arr["zt1"].mean()), zf1=float(arr["zf1"].mean()), zr1=float(arr["zr1"].mean())),
               P_O=float(O.mean()), P_excl_T_s1=float(arr["excl_t"].mean()), P_excl_flat_s1=float(arr["excl_f"].mean()), P_excl_rival_s1=float(arr["excl_r"].mean()),
               P_T_be0_in=float(np.mean((arr["be0"] >= 0.6) & (arr["be0"] <= 1.69))), floored=float(np.mean(fl)))
    for s in (0, 1):
        for L, k in (("flat", "zf%d"), ("rival", "zr%d"), ("T", "zt%d")):
            res["P_fit_%s_s%d" % (L, s)] = float(np.mean(np.abs(arr[k % s]) < 2))
    return res

def control_noiseless():
    rng = np.random.default_rng(0); out = []
    for wn, (law, s_true, mu_true) in WORLDS.items():
        Sm, f = make_mock(rng, law, s_true, mu_true, "ideal", noise=False)
        sp = C.spec_s(s_true)
        if law == "T":
            d = C.cell(Sm, AS, s_true, mu_true, LAW["T"])["H"]
        else:
            c = C.cell(Sm, AS, s_true, mu_true, None); d = c["flat"] if law == "flat" else c["H"]
        out.append((wn, law, s_true, mu_true, d[0], f))
    return out

if __name__ == "__main__":
    pr("CFG183 (e) mocks; seed %d, N=%d per (world,family); repo=<repo>" % (SEED, N))
    pr("E-C1 noiseless mock: analysing at the TRUE (law, s, mu) must return D' ~ 0 (line |D'| < 0.02):")
    ctl = control_noiseless(); okc = True
    for wn, law, s, mu, d, f in ctl:
        pr("   %s %-5s s=%.2f mu=%.2f  D'=%+.4f  floored-fraction %.2f  %s" % (wn, law, s, mu, d, f, "ok" if abs(d) < 0.02 else "MISS")); okc &= abs(d) < 0.02
    jobs = [(w, f, SEED) for w in WORLDS for f in FAMS]
    with Pool(min(12, len(jobs))) as p:
        R = p.map(job, jobs)
    pr("E-C1 all within 0.02: %s" % okc)
    pr("results (mean z at mu=0.67 for flat/rival/T at P0 and s=1; P(O) = observed P0 pattern {|z_T|<=1.5, z_flat<=-2, z_rival<=-3.5}):")
    for r in R:
        m = r["mean"]
        pr("  %s %-5s %-5s truth(s=%.2f,mu=%.2f) | P0 z: flat %+.2f rival %+.2f T %+.2f | s=1 z: flat %+.2f rival %+.2f T %+.2f | P(O)=%.3f | P(T excl s=1)=%.3f P(flat excl)=%.3f P(rival excl)=%.3f | P(T mu_be(P0) in [0.6,1.69])=%.3f | fits(|z|<2) P0 f/r/T %.2f/%.2f/%.2f  s=1 f/r/T %.2f/%.2f/%.2f | floored %.2f" % (
            r["world"], r["law"], r["fam"], r["s_true"], r["mu_true"], m["zf0"], m["zr0"], m["zt0"], m["zf1"], m["zr1"], m["zt1"], r["P_O"], r["P_excl_T_s1"], r["P_excl_flat_s1"], r["P_excl_rival_s1"], r["P_T_be0_in"],
            r["P_fit_flat_s0"], r["P_fit_rival_s0"], r["P_fit_T_s0"], r["P_fit_flat_s1"], r["P_fit_rival_s1"], r["P_fit_T_s1"], r["floored"]))
    get = {(r["world"], r["fam"]): r for r in R}
    pr("frozen readings:")
    for fam in FAMS:
        pr("   [family %s%s]" % (fam, "  POST-HOC, not frozen" if fam.endswith("+sc") else "  frozen"))
        for other in ("W2", "W3", "W5", "W6"):
            dP = get[("W1", fam)]["P_O"] - get[(other, fam)]["P_O"]
            lab = "IDENTIFIES" if abs(dP) > 0.20 else ("DEGENERATE" if abs(dP) < 0.10 else "WEAK")
            pr("   %-5s P(O|W1)-P(O|%s) = %+.3f -> %s %s" % (fam, other, dP, lab, "(pattern points to T)" if dP > 0.2 else ("(pattern points the other way)" if dP < -0.2 else "")))
    for fam in FAMS:
        a, b = get[("W4", fam)]["P_excl_T_s1"], get[("W1", fam)]["P_excl_T_s1"]
        pr("   %-5s s=1 exclusion: P(T excl | W4) = %.3f, P(T excl | W1) = %.3f -> %s" % (fam, a, b, "INFORMATIVE" if (a > 0.5 and b < 0.05) else "NOT informative by the frozen line (>0.5 and <0.05)"))
    json.dump(dict(seed=SEED, N=N, control=[list(x) for x in ctl], results=R), open(os.path.join(C.HERE, "CFG183_null_e_results_seed%d.json" % SEED), "w"), indent=1)
