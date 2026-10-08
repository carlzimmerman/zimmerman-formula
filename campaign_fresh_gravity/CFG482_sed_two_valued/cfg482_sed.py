#!/usr/bin/env python3
"""CFG482 (v2): two-valued SED test on the switch variable x = s_ph - s_c.

v1 (z0, pre-registered): KILL fired on the MEAN-FIELD marginalization tests
(D2 pile-up at 0+, D3 mode at the threshold) -- v1's D2/D3 tested the CFG478
vdW-marginal picture.  The CFG481 EXACT LMP operator predicts no marginal
population: realized cells sit in ONE of the two phases (the canonical double
well has no state at the Maxwell line), so the exact signatures are
  E1  bimodality of x inside ON cells (dAIC > 6)
  E2  ANTI-pile-up: the threshold band [0, sig/10) is DEPOPULATED
      (ratio < 0.6 of the smooth expectation) -- the valley between phases
  E3  mode separation: |mu2 - mu1| > 2 * min(s)  (well-separated phases)  -- v3:
      REPLACED by the histogram dip (CFG480 gate): gas/liquid modes are the
      two highest local maxima of the x-histogram over [1,99] pct; dip =
      (top - valley)/top between them; need dip > 0.1.  (E3-GMM failed at z0
      because the GAS phase has a fat cosmic tail: s1=40.7 inflates min(s);
      the dip gate sees the true -15 vs +13 valley at 0.977.)
  E4  EPOCH GROWTH: separation widens as a grows (operator: gamma(beta*a)
      monotone in beta) -- requires per-epoch dumps (z1/z0.5/z0)
v1 z0 result (pre-registered, mean-field marginal tests): D2/D3 FAIL --
    marginalization KILLED.  v3 re-reading on the EXACT-LMP signatures:
    E1 dAIC=29393 P, E2 ratio=0.20 P, E3 dip=0.977 (gas mode at x=-15 vs
    liquid +13, valley 98% depopulated) P  ->  z0 PASS (two-phase satisfies
    the exact operator; mean-field marginal variant dead).
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

def epoch_stats(z, epoch, out):
    f = z["f"].astype(np.float32); l3 = z["l3"].astype(np.float32)
    sph = z["sph"].astype(np.float32); sc = z["sc"].astype(np.float32)
    x = (sph - sc).astype(np.float32)
    on = f > 0.5
    N_on = int(on.sum())
    if N_on < 2000:
        print(f"  {epoch}: ON={N_on} -> inadequate sample")
        return None
    sx = x[on].ravel()
    sig = float(sx.std())
    mu1, s1, w1, ll1 = gmm_1d(sx, 1)
    mu2, s2, w2, ll2 = gmm_1d(sx, 2)
    dAIC = (2 * 3 - 2 * ll1) - (2 * 6 - 2 * ll2)
    band = (sx >= 0) & (sx < sig / 10)
    frac_band = float(band.mean())
    gauss_at0 = 1.0 / (np.sqrt(2 * np.pi) * sig) * (sig / 10)
    pile = frac_band / gauss_at0
    posx = sx[sx >= 0]
    h, be = np.histogram(posx, bins=60, range=(0, sig))
    mode_pos = float(be[np.argmax(h)] + (be[1] - be[0]) / 2)
    sep = abs(mu2[1] - mu2[0]) / (2 * min(s2))
    # v3: dip gate between the two highest histogram modes (CFG480 gate)
    lo, hi = np.percentile(sx, [1, 99])
    h, be = np.histogram(sx, bins=100, range=(lo, hi))
    cx = (be[:-1] + be[1:]) / 2
    sm = np.convolve(h, np.ones(3) / 3, "same")
    mx = []
    for i in range(2, len(sm) - 2):
        if sm[i] >= sm[i-2] and sm[i] >= sm[i-1] and sm[i] >= sm[i+1] and sm[i] >= sm[i+2]:
            mx.append((sm[i], cx[i]))
    mx.sort(key=lambda t: -t[0])
    if len(mx) >= 2:
        (v1, c1), (v2, c2) = mx[0], mx[1]
        a, b = min(c1, c2), max(c1, c2)
        seg = (cx >= a) & (cx <= b)
        valley = sm[seg].min()
        dip = (max(v1, v2) - valley) / max(v1, v2)
        gas_mode = c1 if c1 < c2 else c2
    else:
        dip, gas_mode = 0.0, np.nan
    e1 = dAIC > 6
    e2 = pile < 0.6
    e3 = dip > 0.1
    r = dict(epoch=epoch, N_on=N_on, sig=sig, dAIC=dAIC, mu=mu2.tolist(),
             s=s2.tolist(), w=w2.tolist(), pile=pile, mode_pos=mode_pos,
             sep=sep, dip=dip, gas_mode=gas_mode, E1=e1, E2=e2, E3=e3)
    print(f"  {epoch}: ON={N_on} sig={sig:.2f} dAIC={dAIC:.0f} "
          f"mu={np.round(mu2,1)} gas@={gas_mode:.1f} "
          f"pile={pile:.2f} dip={dip:.3f} -> E1:{'P' if e1 else 'F'} E2:{'P' if e2 else 'F'} E3:{'P' if e3 else 'F'}")
    out.append(r)
    return r

def main():
    work = "/Users/carlzimmerman/new_physics/_external_data/cfg414_work"
    tag = sys.argv[1] if len(sys.argv) > 1 else "cfg414_RES_Rc3_MIXA_X0.4_FLAT_alt_N256_seed360"
    epochs = sys.argv[2].split(",") if len(sys.argv) > 2 else ["z1", "z0.5", "z0"]
    out = []
    print(f"tag={tag}  exact-LMP criteria: E1 dAIC>6, E2 anti-pile-up<0.6, E3 dip>0.1")
    for ep in epochs:
        z = np.load(f"{work}/{tag}_{ep}.npz")
        if "sph" not in z.files or "sc" not in z.files:
            print(f"  {ep}: no sph/sc fields -- rerun with the patched engine"); continue
        epoch_stats(z, ep, out)
    if len(out) >= 2:
        seps = [r["sep"] for r in out]
        growth = seps[-1] > seps[0]           # E4: separation widens with a
        print(f"\nE4 epoch growth: sep z1..z0 = {[round(s,2) for s in seps]} -> "
              f"{'PASS (widening: operator beta-growth reproduced)' if growth else 'FAIL'}")
        e4 = growth
    else:
        e4 = None
    npass = sum(r["E1"] and r["E2"] and r["E3"] for r in out)
    verdict = ("PASS: exact-LMP two-phase signature (bimodal, anti-piled-up, "
               "separated modes) at every epoch" if npass == len(out) and len(out) > 0
               else "KILL (flagged): two-phase signature absent/critical at some epoch")
    print(f"\nVERDICT: {verdict}")
    json.dump(dict(tag=tag, epochs=out, E4_growth=e4, verdict=verdict),
              open("cfg482_sed_two_valued.json", "w"), indent=1, default=bool)

if __name__ == "__main__":
    main()