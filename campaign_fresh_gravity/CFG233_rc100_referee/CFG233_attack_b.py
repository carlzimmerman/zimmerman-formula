"""CFG233 attack (b): flat-truth and rival-truth mocks passed through an authors'-style f_DM inference with a mis-specified gas scaling.
env SEED (233 default, or 234). N = 4000 mocks per (world, cell)."""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CFG233_common import *

SEED = int(os.environ.get("SEED", "233"))
N = int(os.environ.get("NMOCK", "4000"))
tag = "" if SEED == 233 else f"_seed{SEED}"
t0 = start("CFG233_attack_b" + tag)
d = load_rc100(); z = d["z"]; n = len(z); zmed = np.median(z); dz = z - zmed
rc = load_rc41()
sigM = float(np.median([0.5 * (float(r["logMbar_lo"]) + float(r["logMbar_hi"])) for r in rc]))
sigV = math.log10(1.05)
# G1 gas model (same fit as attack a)
m41, _, _, rc_ = rc41_match(d)
idx = {r["id"].replace("_", " "): r for r in rc_}
rr = [idx[nm] for nm in d["name"] if nm in idx]; zz = np.array([float(d["z"][i]) for i, nm in enumerate(d["name"]) if nm in idx])
lmu = np.array([float(r["logMgas"]) - float(r["logMstar_SED"]) for r in rr])
cb, *_ = np.linalg.lstsq(np.vstack([zz, np.ones(len(zz))]).T, lmu, rcond=None)
mu = 10 ** (cb[1] + cb[0] * z)
print(f"seed {SEED}, N {N}; sigma_M (RC41 median) {sigM:.3f}; sigma_V {sigV:.4f} dex; G1: log10 mu = {cb[1]:+.3f} + {cb[0]:+.3f} z")
gobs0 = d["gobs"]; Re = d["Re"]
gb_true = {T: invert_gbar(gobs0, a0_of(T, z), nu_mono) for T in ("flat", "rival")}
df_obs, dr_obs = delta_pair(d["D"], d["gbar"], z)
obs = (ts(z, df_obs), ts(z, dr_obs))
def rsd(x): return 1.4826 * np.median(np.abs(x - np.median(x)))
obs_scatter = rsd(df_obs)
print(f"observed slopes {obs[0]:+.4f} {obs[1]:+.4f}; observed robust SD of delta_flat {obs_scatter:.4f}")
FLOOR = 0.01


def make(T, kfac, B, rng, sig_int, sigM_=sigM, floor=True, tau_only=False):
    e_int = rng.normal(0, sig_int, (B, n)); e_V = rng.normal(0, sigV, (B, n)); e_M = rng.normal(0, sigM_, (B, n))
    gobs_true = gobs0[None] * 10 ** e_int
    gobs_meas = gobs_true * 10 ** (2 * e_V)
    gb_as = gb_true[T][None] * kfac[None] * 10 ** e_M
    f = 1 - gb_as / gobs_meas
    if floor:
        nfl = (f < FLOOR).sum(1).mean()
        f = np.clip(f, FLOOR, 0.99)
    else:
        nfl = (f <= 0).sum(1).mean(); f = np.clip(f, 1e-4, 0.99)
    f = np.round(f, 2)
    f = np.clip(f, 0.01 if floor else 0.0001, 0.99)
    V = np.round(np.sqrt(gobs_meas * Re[None] * KPC) / 1e3)
    go = (V * 1e3) ** 2 / (Re[None] * KPC)
    gb = (1 - f) * go
    D = 1 / (1 - f)
    zb = np.broadcast_to(z, (B, n))
    a = delta_of(D, gb, zb, "flat"); b = delta_of(D, gb, zb, "rival")
    sf = ts_batch(zb, a); sr = ts_batch(zb, b)
    return sf, sr, float(nfl), np.array([rsd(x) for x in a[:50]]).mean()


def calibrate():
    lo, hi = 0.0, 0.5
    for _ in range(14):
        mid = 0.5 * (lo + hi)
        rng = np.random.default_rng(SEED + 1000)
        _, _, _, sc = make("flat", np.ones(n), 200, rng, mid)
        if sc < obs_scatter: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)


sig_int = calibrate()
print(f"calibrated intrinsic scatter of log D: {sig_int:.4f} dex (declared calibration; alt 0.10 reported)")


def kgas(c, t):
    return (1 + mu) / (1 + c * mu * 10 ** (t * dz))


def summarize(sf, sr):
    P = np.vstack([sf, sr]); m = P.mean(1); C = np.cov(P)
    return m, C


cs = [0.25, 0.5, 1.0, 2.0, 4.0]; tl = [-0.30, -0.15, 0.0, 0.15, 0.30]
out = {}
rng = np.random.default_rng(SEED)
tt = time.time()
for c in cs:
    for t in tl:
        row = {}
        for T in ("flat", "rival"):
            sf, sr, nfl, _ = make(T, kgas(c, t), N, rng, sig_int)
            m, C = summarize(sf, sr)
            row[T] = dict(mean=list(m), sd=[math.sqrt(C[0, 0]), math.sqrt(C[1, 1])], cov=C.tolist(), p_flat_le_obs=float((sf <= obs[0]).mean()),
                          p_rival_le_obs=float((sr <= obs[1]).mean()), box=float(((abs(sf - obs[0]) < 0.02) & (abs(sr - obs[1]) < 0.02)).mean()),
                          nfloor=nfl, med_flat=float(np.median(sf)))
        # Gaussian 2D LR at the observed pair
        def logpdf(T):
            m = np.array(row[T]["mean"]); C = np.array(row[T]["cov"]); x = np.array(obs) - m
            return -0.5 * x @ np.linalg.solve(C, x) - 0.5 * np.log(np.linalg.det(C))
        row["LR_gauss"] = float(np.exp(logpdf("rival") - logpdf("flat")))
        row["LR_box"] = float((row["rival"]["box"] + 1 / N) / (row["flat"]["box"] + 1 / N))
        out[f"c{c}/t{t}"] = row
        print(f"c={c:4} t={t:+.2f}: flat-truth slopes {row['flat']['mean'][0]:+.3f}/{row['flat']['mean'][1]:+.3f} (sd {row['flat']['sd'][0]:.3f}) P(flat<=obs) {row['flat']['p_flat_le_obs']:.3f} | rival-truth {row['rival']['mean'][0]:+.3f}/{row['rival']['mean'][1]:+.3f} P(flat<=obs) {row['rival']['p_flat_le_obs']:.3f} | LR gauss {row['LR_gauss']:.2f} box {row['LR_box']:.2f} | floored rows/mock {row['flat']['nfloor']:.1f}/{row['rival']['nfloor']:.1f}")
print("grid time", round(time.time() - tt, 1), "s")

# summary rules
r0 = out["c1.0/t0.0"]
sup = r0["flat"]["p_flat_le_obs"] >= 0.03 and r0["rival"]["p_flat_le_obs"] < 0.003
print(f"\nc=1,t=0: P(flat-truth flat slope <= {obs[0]:+.3f}) = {r0['flat']['p_flat_le_obs']:.3f}; P(rival-truth ...) = {r0['rival']['p_flat_le_obs']:.4f}; rule 'deficit slope unremarkable in a flat world' (>=0.03 and rival <0.003): {'SUPPORTED' if sup else 'NOT SUPPORTED'}")
band = [(c, t) for c in (0.5, 1.0, 2.0) for t in (-0.15, 0.0, 0.15)]
lrs = {f"c{c}/t{t}": (out[f"c{c}/t{t}"]["LR_gauss"], out[f"c{c}/t{t}"]["LR_box"]) for c, t in band}
worst = max(v[0] for v in lrs.values())
print("plausible-band LR (rival over flat; gauss, box):", {k: (round(a, 2), round(b, 2)) for k, (a, b) in lrs.items()})
print(f"max plausible-band Gaussian LR = {worst:.2f}; frozen fail line: any cell with LR >= 1/3 -> headline 'rival disfavoured' {'FAILS as a discriminating statement' if worst >= 1/3 else 'holds'}")
nfail = sum(v[0] >= 1 / 3 for v in lrs.values())
print(f"cells with LR >= 1/3: {nfail}/9")
# break-even (c,t): rival-truth median flat slope == obs flat slope, along t for each c
be = {}
for c in cs:
    xs = np.array(tl); ys = np.array([out[f"c{c}/t{t}"]["rival"]["med_flat"] for t in tl]) - obs[0]
    cross = None
    for i in range(len(xs) - 1):
        if ys[i] * ys[i + 1] < 0:
            cross = float(xs[i] - ys[i] * (xs[i + 1] - xs[i]) / (ys[i + 1] - ys[i])); break
    be[c] = cross
print("rival-truth mock median flat slope crosses the observed value at t =", be, "(inside plausible band |t|<=0.15 and c in [0.5,2]?", {c: (v is not None and abs(v) <= 0.15 and 0.5 <= c <= 2) for c, v in be.items()}, ")")

# variants at c=1, t=0
var = {}
for name, kw in (("sig_int_0.10", dict(sig_int=0.10)), ("sigM_0.20", dict(sig_int=sig_int, sigM_=0.20)), ("no_floor", dict(sig_int=sig_int, floor=False))):
    row = {}
    for T in ("flat", "rival"):
        sf, sr, nfl, _ = make(T, kgas(1.0, 0.0), N, rng, **kw)
        row[T] = dict(mean=[float(sf.mean()), float(sr.mean())], sd=[float(sf.std()), float(sr.std())], p_flat_le_obs=float((sf <= obs[0]).mean()), nfloor=nfl)
    var[name] = row
    print(f"variant {name} (c=1,t=0): flat-truth mean slopes {row['flat']['mean'][0]:+.3f}/{row['flat']['mean'][1]:+.3f} P(flat<=obs) {row['flat']['p_flat_le_obs']:.3f}; rival-truth {row['rival']['mean'][0]:+.3f}/{row['rival']['mean'][1]:+.3f} P {row['rival']['p_flat_le_obs']:.3f}")
# POST-FREEZE rows for the CFG217 question: baryon-mass tilt worlds
print("\nPOST-FREEZE (labelled): total baryon-mass tilt tau_total (dex over the z range; assumed/true = 10^(tau dz)) in the two worlds, c=1 otherwise")
pf = {}
for tot in (0.0, 0.15, 0.20, 0.26, 0.33):
    tau = tot / (z.max() - z.min())
    row = {}
    for T in ("flat", "rival"):
        sf, sr, nfl, _ = make(T, 10 ** (tau * dz), N, rng, sig_int)
        m, C = summarize(sf, sr)
        row[T] = dict(mean=list(m), sd=[math.sqrt(C[0, 0]), math.sqrt(C[1, 1])], cov=C.tolist(), p_flat_le_obs=float((sf <= obs[0]).mean()), p_rival_le_obs=float((sr <= obs[1]).mean()),
                      box=float(((abs(sf - obs[0]) < 0.02) & (abs(sr - obs[1]) < 0.02)).mean()))
    def lp(T):
        m = np.array(row[T]["mean"]); C = np.array(row[T]["cov"]); x = np.array(obs) - m
        return -0.5 * x @ np.linalg.solve(C, x) - 0.5 * np.log(np.linalg.det(C))
    row["LR_gauss"] = float(np.exp(lp("rival") - lp("flat")))
    pf[tot] = row
    print(f"  tau_total {tot:.2f}: rival-truth mean slopes {row['rival']['mean'][0]:+.3f}/{row['rival']['mean'][1]:+.3f} (obs {obs[0]:+.3f}/{obs[1]:+.3f}) box-frac {row['rival']['box']:.3f}; flat-truth mean {row['flat']['mean'][0]:+.3f}/{row['flat']['mean'][1]:+.3f} box-frac {row['flat']['box']:.3f}; LR(rival/flat) {row['LR_gauss']:.2f}")
# POST-FREEZE marginalised likelihood ratio over a Gaussian prior on the total baryon-mass tilt (labelled; the frozen rule is the cell rule above)
print("\nPOST-FREEZE (labelled): marginal LR (rival over flat) with tau_total ~ N(0, s_tau) shared by both worlds")
taus = np.arange(-0.40, 0.601, 0.05)
LL = {"flat": [], "rival": []}
for tot in taus:
    tau = tot / (z.max() - z.min())
    for T in ("flat", "rival"):
        sf, sr, nfl, _ = make(T, 10 ** (tau * dz), N, rng, sig_int)
        m, C = summarize(sf, sr); x = np.array(obs) - m
        LL[T].append(float(np.exp(-0.5 * x @ np.linalg.solve(C, x)) / (2 * np.pi * math.sqrt(np.linalg.det(C)))))
mlr = {}
for st in (0.05, 0.10, 0.20, 0.40):
    w = np.exp(-0.5 * (taus / st) ** 2); w /= w.sum()
    Lf = float((w * np.array(LL["flat"])).sum()); Lr = float((w * np.array(LL["rival"])).sum())
    mlr[st] = Lr / Lf
    print(f"  prior sd {st:.2f} dex: marginal LR(rival/flat) = {Lr/Lf:.3g}")
best = {T: float(taus[int(np.argmax(LL[T]))]) for T in LL}
print("  best-fit tau_total (max likelihood over the grid): flat world", best["flat"], "; rival world", best["rival"], "; max L rival/flat =", max(LL["rival"]) / max(LL["flat"]))
pf["marginal_LR"] = mlr; pf["tau_grid"] = list(taus); pf["LL"] = LL
savejson("CFG233_attack_b" + tag, dict(seed=SEED, N=N, sig_int=sig_int, sigM=sigM, obs=obs, grid=out, be=be, variants=var, postfreeze=pf, lrs=lrs))
print("done")
