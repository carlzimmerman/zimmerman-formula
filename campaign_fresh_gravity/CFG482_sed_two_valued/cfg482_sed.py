#!/usr/bin/env python3
"""CFG482: the decisive two-valued SED test for door B (runs on a fresh npz
with the s_ph/s_c dump from the patched CFG414 engine).

Door B / CFG481 say: the phantom switch is a FIRST-ORDER coexistence, so the
local SED x = s_ph - s_c inside ON cells (f > 0.5) must be TWO-VALUED:
  - a "gas" population at x << 0 (phantom starved, excess clamped at 0), and
  - a "liquid" population pinned at x ~ 0^+ (marginal activation -- the
    Maxwell line of the exact operator).
The smooth-threshold alternative gives ONE broad population straddling 0.

Pre-registered diagnostics (KILL if ALL fail on adequate samples):
  D1  bimodality of x inside ON cells  (2-G over 1-G by AIC: need dAIC > 6)
  D2  marginal pile-up: fraction of ON cells with 0 <= x < sigma_x/10 must
      EXCEED 1.2x the smooth-Gaussian expectation centred at x=0
  D3  the excess mass e = f*max(x,0) vs x relation: the liquid phase sits
      AT the threshold: mode(x | x>=0) within sigma_x/10 of 0
  D4  inside-cover x distribution vs outside-cover (control): the band
      signature must be STRONGER in covers (the confined switch region)
PASS verdict if D1+D2 (or D3+D2) hold with N_on > 2000.
"""
import json, numpy as np, sys

def gmm_1d(x, K, iters=300, seed=2):
    rng = np.random.default_rng(seed)
    lo, hi = np.percentile(x, [2, 98])
    mu = np.linspace(lo, hi, K)
    sg = np.full(K, (hi - lo) / (2 * K))
    w = np.full(K, 1.0 / K)
    n = len(x)
    R = np.zeros((n, K))
    for _ in range(iters):
        for k in range(K):
            R[:, k] = w[k] * np.exp(-0.5 * ((x - mu[k]) / sg[k]) ** 2) / (sg[k] * 2.5066282)
        R /= R.sum(1, keepdims=True) + 1e-300
        nk = R.sum(0)
        mu = (R * x[:, None]).sum(0) / nk
        sg = np.sqrt((R * (x[:, None] - mu) ** 2).sum(0) / nk) + 1e-6
        w = nk / n
    D = np.empty((n, K))
    for k in range(K):
        D[:, k] = w[k] * np.exp(-0.5 * ((x - mu[k]) / sg[k]) ** 2) / (sg[k] * 2.5066282)
    ll = float(np.sum(np.log(D.sum(1) + 1e-300)))
    return mu, sg, w, ll

def main():
    work = "/Users/carlzimmerman/new_physics/_external_data/cfg414_work"
    tag = sys.argv[1] if len(sys.argv) > 1 else "cfg414_RES_Rc3_MIXA_X0.4_FLAT_alt_N256_seed360"
    z = np.load(f"{work}/{tag}_z0.npz")
    if "sph" not in z.files or "sc" not in z.files:
        print("npz has no sph/sc fields -- need a rerun with the patched engine."); return
    f = z["f"].astype(np.float32); l3 = z["l3"].astype(np.float32)
    sph = z["sph"].astype(np.float32); sc = z["sc"].astype(np.float32)
    x = (sph - sc).astype(np.float32)
    on = f > 0.5
    N_on = int(on.sum())
    print(f"tag={tag}  ON cells={N_on}  mean f={f.mean():.4f}")
    if N_on < 2000:
        print("sample inadequate -> inconclusive"); return
    sx = x[on]; sxv = sx.ravel()
    sig = float(sx.std())
    mu1, s1, w1, ll1 = gmm_1d(sxv, 1)
    mu2, s2, w2, ll2 = gmm_1d(sxv, 2)
    dAIC = (2 * 3 - 2 * ll1) - (2 * 6 - 2 * ll2)
    # D2: marginal pile-up
    band = (sx >= 0) & (sx < sig / 10)
    frac_band = float(band.mean())
    gauss_at0 = 1.0 / (np.sqrt(2 * np.pi) * sig) * (sig / 10)   # smooth expectation
    pile = frac_band / gauss_at0
    # D3: mode of the x>=0 population
    posx = sx[sx >= 0]
    h, be = np.histogram(posx, bins=60, range=(0, sig))
    mode_pos = float(be[np.argmax(h)] + (be[1] - be[0]) / 2)
    # D4: covers vs outside (inside = knots)
    knot = on & (l3 >= 0); fil = on & (l3 < 0)
    sigk = float(x[knot].std()) if knot.sum() > 100 else np.nan
    pk = float((x[knot] >= 0).mean()) if knot.sum() > 100 else np.nan
    print(f"\nD1 bimodality:   1-G AIC={2*3-2*ll1:.0f}  2-G AIC={2*6-2*ll2:.0f}  dAIC={dAIC:.1f}")
    print(f"                 2-G mu={np.round(mu2,3)} s={np.round(s2,3)} w={np.round(w2,3)}")
    print(f"D2 marginal pile-up: P(0<=x<sig/10)={frac_band:.4f}  smooth-expectation={gauss_at0:.4f}  ratio={pile:.2f}")
    print(f"D3 mode of x>=0 population: {mode_pos:.4f}  (0 = Maxwell marginalisation)  sig={sig:.4f}")
    print(f"D4 cover knots: sigma={sigk:.4f}  P(x>=0)={pk:.4f}  (vs ON-all {float((sx>=0).mean()):.4f})")
    d1 = dAIC > 6
    d2 = pile > 1.2
    d3 = mode_pos < sig / 10
    if (d1 and d2) or (d3 and d2):
        verdict = ("PASS: two-valued SED response in the phantom-ON region "
                   "(bimodal + Maxwell marginalisation) -- door B's first-order "
                   "switch reads directly in the data")
    else:
        verdict = ("KILL (flagged): no two-valued SED response at z=0 -- the "
                   "first-order reading does not survive the switch-variable test")
    print(f"\nVERDICT: {verdict}")
    print("(z=0 snapshot; intermediate-snapshot confirmation remains the stronger test)")
    json.dump(dict(tag=tag, N_on=int(N_on), sig=float(sig), dAIC=float(dAIC),
                   pile=float(pile), mode_pos=float(mode_pos), d1=d1, d2=d2, d3=d3,
                   verdict=verdict), open("cfg482_sed_two_valued.json", "w"), indent=1)

if __name__ == "__main__":
    main()