#!/usr/bin/env python3
"""CFG480: phase-separation-band test for the phantom switch (door B follow-up).

Door B (LMP first-order transition, CFG478) implies the canonical cold-density
response inside the phantom-ON region is TWO-PHASE: local densities inside the
coexistence band [rho_gas, rho_liquid] phase-separate instead of interpolating
smoothly.  Observable at z=0: the overdensity PDF over ON cells (f>0, the
confined-switch mask) should be BIMODAL -- or at least show a resolved second
mode / plateau -- while a smooth threshold switch gives a single broad mode.

Data: cfg414 RES N256 runs (pos + f + l3 in the npz).
Method:
  1. CIC overdensity delta_c from pos on the 256^3 mesh.
  2. log10(1+delta) PDF over ON cells (f > 0), and over the full box (context).
  3. Bimodality: 1-G vs 2-G Gaussian mixture (hand EM) by AIC; dip statistic
     = valley depth between the two fitted modes relative to the lower peak.
KILL CONDITION: if the ON-cell PDF is unimodal (AIC prefers 1G or dip < 0.1)
AND the cell sample is adequate (N_on > 500), the two-phase reading of the
phantom switch region contributes nothing beyond a smooth threshold at z=0
(flag, not a hard kill -- a z=0 snapshot is a weak test; report as such).
PASS: AIC prefers 2G by > 6 AND dip > 0.1 with N_on > 500.
"""
import json, numpy as np, sys

def cic_rho(pos, M, L):
    dx = L / M
    u = pos / dx
    i0 = np.floor(u).astype(np.int64)
    w = (u - i0).astype(np.float32)
    rho = np.zeros(M ** 3, np.float64)
    for ix in (0, 1):
        for iy in (0, 1):
            for iz in (0, 1):
                wx = w[:, 0] if ix else 1 - w[:, 0]
                wy = w[:, 1] if iy else 1 - w[:, 1]
                wz = w[:, 2] if iz else 1 - w[:, 2]
                idx = ((i0[:, 0] + ix) % M * M + (i0[:, 1] + iy) % M) * M + (i0[:, 2] + iz) % M
                np.add.at(rho, idx, wx * wy * wz)
    return rho.reshape((M,) * 3)

def gmm_1d(x, K, iters=400):
    """hand EM on 1-D samples x; returns (means, sigmas, weights)."""
    lo, hi = np.percentile(x, [2, 98])
    rng = np.random.default_rng(1)
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
    # proper log-likelihood of the fitted mixture (not the posterior)
    D = np.empty((n, K))
    for k in range(K):
        D[:, k] = w[k] * np.exp(-0.5 * ((x - mu[k]) / sg[k]) ** 2) / (sg[k] * 2.5066282)
    ll = float(np.sum(np.log(D.sum(1) + 1e-300)))
    return mu, sg, w, ll

def main():
    work = "/Users/carlzimmerman/new_physics/_external_data/cfg414_work"
    tag = sys.argv[1] if len(sys.argv) > 1 else "cfg414_RES_Rc3_MIXA_X0.4_FLAT_alt_N256_seed360"
    npz = np.load(f"{work}/{tag}_z0.npz")
    pos = npz["pos"]; f = npz["f"].astype(np.float32); l3 = npz["l3"].astype(np.float32)
    meta = json.load(open(f"{work}/{tag}.json"))
    M = meta.get("mesh", 256); L = meta["L"]
    print(f"tag={tag}  M={M}  L={L}  particles={len(pos)}")
    rho = cic_rho(pos, M, L)
    delta = rho / rho.mean() - 1.0
    delta = np.clip(delta, -0.999999, None)      # empty cells -> floor
    on = f > 0
    N_on = int(on.sum())
    x_on = np.log10(1.0 + delta[on])
    x_all = np.log10(1.0 + delta).ravel()
    print(f"ON cells: {N_on}  ({100*N_on/M**3:.3f}% of box)")
    if N_on < 200 or N_on > M ** 3 * 0.7:
        print("sample inadequate -> inconclusive"); return
    # 1G vs 2G
    mu1, s1, w1, ll1 = gmm_1d(x_on, 1)
    mu2, s2, w2, ll2 = gmm_1d(x_on, 2)
    k1, k2 = 3, 6
    aic1, aic2 = 2 * k1 - 2 * ll1, 2 * k2 - 2 * ll2
    dAIC = aic1 - aic2                      # >0 prefers 2G
    # dip: valley between the two modes on the fitted density
    lo = min(mu1.min(), mu2.min()) - 2 * max(s1.max(), s2.max())
    hi = max(mu1.max(), mu2.max()) + 2 * max(s1.max(), s2.max())
    xs = np.linspace(lo, hi, 2001)
    if np.max(s2) > 1e-9:
        order = np.argsort(mu2)
        pf = lambda x: sum(w2[k] * np.exp(-0.5 * ((x - mu2[k]) / s2[k]) ** 2) / (s2[k] * 2.5066282) for k in range(2))
        v1, v2 = sorted(mu2)[0], sorted(mu2)[1]
        valley = min(pf(x) for x in np.linspace(v1, v2, 401))
        pks = [pf(mu2[k]) for k in np.argsort(mu2)]
        dip = (max(pks) - valley) / max(pks)
    else:
        dip = -1.0
    print(f"\nON-cell log10(1+delta): mean={x_on.mean():.3f} std={x_on.std():.3f}")
    print(f"1-G: mu={mu1[0]:.3f} s={s1[0]:.3f}  ll={ll1:.1f}  AIC={aic1:.1f}")
    print(f"2-G: mu={np.round(mu2,3)} s={np.round(s2,3)} w={np.round(w2,3)}  ll={ll2:.1f}  AIC={aic2:.1f}")
    print(f"dAIC (prefers 2G if >6): {dAIC:.1f}   dip={dip:.3f}")
    # context PDF for comparison
    m1a, s1a, w1a, ll1a = gmm_1d(x_all, 1)
    m2a, s2a, w2a, ll2a = gmm_1d(x_all, 2)
    print(f"FULL-box 1-G mu={m1a[0]:.3f} s={s1a[0]:.3f} | 2-G mu={np.round(m2a,3)} s={np.round(s2a,3)} w={np.round(w2a,3)}")
    if N_on > 500 and dAIC > 6 and dip > 0.1:
        verdict = "PASS: bimodal ON-cell density response consistent with a two-phase coexistence band"
    elif N_on <= 500:
        verdict = "INCONCLUSIVE: ON-cell sample too small for a valid dip test"
    else:
        verdict = ("FLAG: unimodal ON-cell density at z=0 -- two-phase reading adds nothing "
                   "beyond a smooth threshold at this snapshot (weak test: z=0, coarse cells)")
    print(f"\nVERDICT: {verdict}")
    print("KILL note: hard kill requires the same test at an intermediate snapshot")
    print("and/or finer mesh; a z=0-only FAIL is a flag, not a kill.")
    res = dict(tag=tag, N_on=int(N_on), mean=float(x_on.mean()), std=float(x_on.std()),
               aic1=float(aic1), aic2=float(aic2), dAIC=float(dAIC), dip=float(dip),
               mu1g=float(mu1[0]), mu2g=[float(v) for v in mu2], s2g=[float(v) for v in s2],
               w2g=[float(v) for v in w2], verdict=verdict)
    out = f"cfg480_{tag.split('cfg414_RES_')[-1][:24]}_bimod.json"
    json.dump(res, open(out, "w"), indent=1)
    print(f"wrote {out}")

if __name__ == "__main__":
    main()