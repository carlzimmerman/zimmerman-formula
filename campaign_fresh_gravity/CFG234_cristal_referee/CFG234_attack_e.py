"""CFG234 attack (e): power of a 3-sigma one-sided rival exclusion (flat-truth mocks) on the independent route; CFG218's 'about 13' check;
post-freeze extension to N = 6 (dust-detected CRISTAL) and N = 8. env SEED (234 default; run at 234 and 235). N_mock = 2000, B = 300. Reports; exit 0."""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CFG234_common import *

SEED = int(os.environ.get("SEED", "234"))
t = start(f"CFG234_attack_e_seed{SEED}")
NMOCK, BB = 2000, 300
NGRID = [6, 8, 9, 11, 13, 15, 17, 20, 25, 30, 40, 60]
df = load_cristal(); d12 = df.loc[ID12]; d9 = df.loc[ROUTE9]; d6 = df.loc[DETECTED6]
d8 = df.loc[[i for i in ROUTE9 if i != "23b"]]
R = {}
t0 = time.time()


def route_sample(d):
    rf = route_factor(d)
    _, _, yf = cell(d, gbar_mul=rf, route="recompute"); _, _, yr = cell(d, rival=True, gbar_mul=rf, route="recompute")
    dlf = cell(d, gbar_mul=rf, route="recompute")[0]
    return yf, yr, dlf


samples = {}
yf, yr, dlf = route_sample(d9); samples["route9"] = (yf, yr, dlf)
yf, yr, dlf = route_sample(d6); samples["route6_detected"] = (yf, yr, dlf)
yf, yr, dlf = route_sample(d8); samples["route8_no23b"] = (yf, yr, dlf)
dl12, _, yf12 = cell(d12); _, _, yr12 = cell(d12, rival=True); samples["fit12"] = (yf12, yr12, dl12)
for k, (yf, yr, dlf) in samples.items():
    S = float(np.median(np.log10(nu_mono(yr) / nu_mono(yf))))
    print(f"sample {k}: n={len(yf)}; observed delta_flat median {np.median(dlf):+.3f}, MAD-sigma {mad_sigma(dlf):.3f}, std {np.std(dlf, ddof=1):.3f}; signal S (median rival-vs-flat separation at own g_bar,z) {S:.4f}")
    R[f"sample_{k}"] = dict(n=len(yf), s_mad=mad_sigma(dlf), s_std=float(np.std(dlf, ddof=1)), S=S)

# ---------------- e1: the CFG218 arithmetic (hypothesis: band 0.226 is a 95 % (1.96 sigma) width at n = 9, sigma_n = sigma_9 sqrt(9/n), 3 sigma_n = S)
print("\n== e1: CFG218 arithmetic under the HYPOTHESIS that its statistical band is a 1.96-sigma width, scaling 1/sqrt(n) ==")
sig9 = 0.226 / 1.96
e1 = {}
for nm, S in (("S_CFG218 (0.288, route 9)", 0.288), ("S route9 (mine)", R["sample_route9"]["S"]), ("S detected-6 (mine)", R["sample_route6_detected"]["S"]), ("S route8 no 23b (mine)", R["sample_route8_no23b"]["S"])):
    n3 = 9 * (3 * sig9 / S) ** 2
    n3s = 9 * (3 * sig9 / (S - 0.038)) ** 2
    e1[nm] = dict(n_3sigma=n3, n_3sigma_with_Ssys_0p038=n3s)
    print(f"  {nm}: S = {S:.3f}: n for 3 sigma = {n3:.1f}; after subtracting CFG218's S_sys 0.038: {n3s:.1f}")
for n in (6, 8, 9, 13):
    print(f"  at n = {n}: sigma_n = {sig9 * np.sqrt(9 / n):.3f}; S/sigma_n (S = 0.288) = {0.288 / (sig9 * np.sqrt(9 / n)):.2f}; (S = detected-6 {R['sample_route6_detected']['S']:.3f}) = {R['sample_route6_detected']['S'] / (sig9 * np.sqrt(9 / n)):.2f}")
R["e1"] = e1

# ---------------- e2: mocks
print(f"\n== e2: flat-truth mocks, seed {SEED}, N_mock {NMOCK}, B {BB}: power = P(median delta_rival / sd_boot < -3) ==")
rng = np.random.default_rng(SEED)


def power_curve(key, s, bias, truth="flat", sys_sd=0.0):
    yf, yr, _ = samples[key]
    out = {}
    for n in NGRID:
        dlf, dlr = mock_deltas(rng, yf, yr, truth, n, NMOCK, s, bias)
        med, sd, lo, hi = boot_med_batch(dlr, BB, rng)
        z = med / np.sqrt(sd ** 2 + sys_sd ** 2)
        out[n] = dict(power=float(np.mean(z < -3)), med_mean=float(np.mean(med)), sd_mean=float(np.mean(sd)), frac_ci_under=float(np.mean(hi < 0)))
    return out


def nq(curve, thr):
    ns = sorted(curve)
    for a, b in zip(ns[:-1], ns[1:]):
        pa, pb = curve[a]["power"], curve[b]["power"]
        if curve[a]["power"] >= thr: return a
        if pa < thr <= pb: return float(a + (thr - pa) / (pb - pa) * (b - a))
    return ns[0] if curve[ns[0]]["power"] >= thr else None


def show(tag, curve):
    print(f"  {tag}: " + " ".join(f"n{n}:{curve[n]['power']:.2f}" for n in NGRID) + f" | n_50 = {nq(curve, .5)}, n_80 = {nq(curve, .8)}")


e2 = {}
S9 = R["sample_route9"];
# frozen variants: sample route9 with route scatter s (MAD); bias grid; and fit-route s
for bias in (0.0, 0.044, -0.044, 0.10, -0.10, 0.20, -0.20):
    c = power_curve("route9", S9["s_mad"], bias); e2[f"route9|s_mad|b={bias}"] = c; show(f"route9 s={S9['s_mad']:.3f} b={bias:+.3f}", c)
for bias in (0.0, 0.044):
    c = power_curve("route9", R["sample_fit12"]["s_mad"], bias); e2[f"route9|s_fit12|b={bias}"] = c; show(f"route9 s(fit12)={R['sample_fit12']['s_mad']:.3f} b={bias:+.3f}", c)
    c = power_curve("route9", S9["s_std"], bias); e2[f"route9|s_std|b={bias}"] = c; show(f"[extra, not frozen] route9 s(std)={S9['s_std']:.3f} b={bias:+.3f}", c)
for bias in (0.0, 0.044, -0.044):
    c = power_curve("fit12", R["sample_fit12"]["s_mad"], bias); e2[f"fit12|s_mad|b={bias}"] = c; show(f"fit12 s={R['sample_fit12']['s_mad']:.3f} b={bias:+.3f}", c)
# post-freeze extension: strict class A CRISTAL (detected-6), and 8 without 23b
for key in ("route6_detected", "route8_no23b"):
    for bias in (0.0, 0.044, -0.044):
        c = power_curve(key, R[f"sample_{key}"]["s_mad"], bias); e2[f"{key}|s_mad|b={bias}"] = c; show(f"[post-freeze] {key} s={R[f'sample_{key}']['s_mad']:.3f} b={bias:+.3f}", c)
R["e2"] = e2

# analytic normal-approximation cross-check
print("\n  analytic cross-check n_norm = (3 * 1.2533 * s / (S_eff))^2, S_eff = S - b (rival median expected -S + b):")
for key in ("route9", "route6_detected", "route8_no23b", "fit12"):
    S = R[f"sample_{key}"]["S"]; s = R[f"sample_{key}"]["s_mad"]
    for b in (0.0, 0.044, 0.10):
        print(f"    {key}: s {s:.3f}, S {S:.3f}, b {b:+.3f}: n_norm = {(3 * 1.2533 * s / (S - b)) ** 2:.1f}")

# ---------------- e3: with an irreducible systematic sigma_sys
print("\n== e3: with sigma_sys not shrinking with n (z_tot = median / sqrt(sd^2 + sigma_sys^2)); route9, s = MAD, b = +0.044 ==")
e3 = {}
for nm, ss in (("CFG218 S_sys 0.038", 0.038), ("b2 half-range hold/rival 0.156", 0.156), ("b2 half-range recompute/rival 0.211", 0.211)):
    c = power_curve("route9", S9["s_mad"], 0.044, sys_sd=ss); e3[nm] = c; show(f"sigma_sys = {ss} ({nm})", c)
    print(f"     cap at n -> infinity: S / sigma_sys = {S9['S'] / ss:.2f} (S route9 = {S9['S']:.3f}; S - b = {S9['S'] - 0.044:.3f} -> {(S9['S'] - 0.044) / ss:.2f})")
R["e3"] = e3

# ---------------- e4: false-positive rate under rival truth
print("\n== e4: rival-truth mocks: P(rival excluded at 3 sigma) (must be < 1 %) ==")
e4 = {}
for key in ("route9", "route6_detected"):
    c = power_curve(key, R[f"sample_{key}"]["s_mad"], 0.0, truth="rival"); e4[key] = c
    print(f"  {key}: " + " ".join(f"n{n}:{c[n]['power']:.3f}" for n in NGRID) + f" | max {max(v['power'] for v in c.values()):.3f}")
R["e4"] = e4
e4_ok = all(max(v["power"] for v in c.values()) < 0.01 for c in e4.values())
print("e4 control:", "PASS" if e4_ok else "FAIL")
print(f"\nrun time {time.time() - t0:.0f} s")
savejson(f"CFG234_attack_e_seed{SEED}", R)
sys.exit(0)
