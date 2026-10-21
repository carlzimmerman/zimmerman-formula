"""WT-03 POST HOC robustness (written AFTER the frozen run of wt03.py; criteria c9ea722b6; amendment AMENDMENT_A1_POSTHOC.md).
Reported only, NO verdict weight. Reads committed CFG689 JSONs only (result commit 6c064b83a); runs nothing of CFG689.
PH0  reproduce the frozen run's primary eps p_rise (same seed, same APPROX-G) - code-equality check.
PH1  the adjacent correlation rho_adj at which segment 0.7-1.0 stops being RISE_68 (draws + closed-form Gaussian).
PH2  net intervals [0, 0.4] and [0, 0.7] (not in the frozen set), eps, with corr(w0, w_k) in {-0.5, 0, +0.5}.
PH3  calibrate the correlations APPROX-G omitted: corr(w0, w_z) at z = 1.0 / 1.5 / 2.33 and one all-node equicorrelation, each
     fitted to the stored joint quantiles sqrtX_q (16/50/84); then the segment flags under the fitted equicorrelation.
PH4  the same eps segment classifier on CFG689's committed bracket modes (SN swaps, flat, no-recon, cold-mass, theta*).
kappa = 1/2 FITTED; nothing here says the data favour the framework.
"""
import glob, json, math, os
import numpy as np
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
C689 = os.path.normpath(os.path.join(HERE, "..", "..", "campaign_fresh_gravity", "CFG689_native_ruler_bao"))
OUTF = open(os.path.join(HERE, "wt03_posthoc.out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
OMG = 2.4728e-5; KMSMPC_TO_GYR = 3.15576e16/3.0856775814913673e19
T68, T95 = 0.8413, 0.9750; LEV = {"68": T68, "95": T95}; QP = [2.5, 16, 50, 84, 97.5]; SEED = 3031; TOL = 1e-12
OUT = {"note": "POST HOC, reported only, no verdict weight", "criteria": "c9ea722b6"}

def corr_adj(n, r):
    C = np.eye(n)
    for i in range(n - 1): C[i, i + 1] = C[i + 1, i] = r
    return C
def draw(mu, sd, Cr, n, seed=SEED):
    C = Cr*np.outer(sd, sd); L = np.linalg.cholesky(C)
    return mu + np.random.default_rng(seed).standard_normal((n, len(mu)))@L.T
def seg_eps(W):
    Fa, Fb = W[:, :-1], W[:, 1:]; dfd = (Fa > 0) & (Fb > 0); nd = dfd.sum(axis=0)
    pr = (dfd & (Fb < Fa - TOL*np.abs(Fa))).sum(axis=0)/np.maximum(nd, 1)
    pf = (dfd & (Fb > Fa + TOL*np.abs(Fa))).sum(axis=0)/np.maximum(nd, 1)
    return pr, pf, np.mean(np.diff(W, axis=1) < 0, axis=0)
def classify(pr, pf, fn, nodes, netflags):
    out = {}
    for L, tl in LEV.items():
        R, F, D = pr >= tl, pf >= tl, fn >= tl
        netr = any(v[L] == "RISE" for v in netflags.values()); netf = any(v[L] == "FALL" for v in netflags.values())
        cls = "PHANTOM-REQUIRED" if (np.any(R & D) or netr) else ("HEALTHY" if np.any(R & ~D) else ("FALLING" if (np.any(F) or netf) else "NOT DIAGNOSTIC"))
        pairs = [(a, b) for a in range(len(pr)) for b in range(len(pr)) if ((R[a] and F[b]) or (F[a] and R[b])) and nodes[a] >= nodes[b + 1]]
        if pairs:
            a, b = min(pairs, key=lambda ab: nodes[ab[0]] - nodes[ab[1] + 1])
            arrow = f"TURNAROUND {'PEAK' if R[a] else 'TROUGH'} at z {[float(x) for x in nodes if nodes[b+1]-1e-9 <= x <= nodes[a]+1e-9]}"
        else:
            sg = {1 for k in range(len(pr)) if R[k]} | {-1 for k in range(len(pr)) if F[k]} | \
                 {1 for v in netflags.values() if v[L] == "RISE"} | {-1 for v in netflags.values() if v[L] == "FALL"}
            arrow = "FLAT" if not sg else ("RISING-ONLY" if sg == {1} else ("FALLING-ONLY" if sg == {-1} else "MIXED"))
        out[L] = dict(flags=["RISE" if R[k] else ("FALL" if F[k] else "FLAT") for k in range(len(pr))], cls=cls, arrow=arrow)
    return out
def netflags_from(q):
    return {zk: {"68": "RISE" if v[3] < 1 else ("FALL" if v[1] > 1 else "FLAT"),
                 "95": "RISE" if v[4] < 1 else ("FALL" if v[0] > 1 else "FLAT")} for zk, v in q.items()}
def H0_of(d):
    cfg, post = d["cfg"], d["BAO+SN"]["posterior"]
    omnu = cfg["mnu"]/93.14; nrel = 3.044 if cfg["mnu"] == 0 else 3.044*2/3; omr = OMG*(1 + 0.2271*nrel)
    om = post["omega_b"][0] + post["omega_c"][0]*(1 + cfg["f"]) + omnu
    wk = post["omega_k"][0] if "omega_k" in post and cfg.get("freek", False) else 0.0
    return 100*math.sqrt(om + omr + wk + post["node_mean"][0])

D = json.load(open(os.path.join(C689, "cfg689.json"))); B = D["BAO+SN"]
NODES = np.array(D["cfg"]["nodes"]); MU = np.array(B["posterior"]["node_mean"]); SD = np.array(B["posterior"]["node_std"])
ZS = ("1.0", "1.2", "1.5", "2.33"); STQ = {zk: B["P1"][zk]["sqrtX_q"] for zk in ZS}

# PH0
P("=== PH0. code equality with the frozen run ===")
fro = json.load(open(os.path.join(HERE, "wt03_results.json")))
W = draw(MU, SD, corr_adj(6, 0.0), 400_000); pr, pf, fn = seg_eps(W)
dev = max(abs(a - b) for a, b in zip(pr, fro["runs"]["+0.0"]["literal"]["eps"]["p_rise"]))
P(f"  primary rho_adj 0: p_rise {np.round(pr, 5).tolist()}; max |diff| vs wt03_results.json {dev:.1e} -> {'SAME' if dev < 1e-12 else 'DIFFERENT'}")
OUT["PH0_same"] = bool(dev < 1e-12)

# PH1
P("\n=== PH1. rho_adj at which segment 0.7-1.0 stops being RISE_68 (eps, literal) ===")
mu7, mu10, s7, s10 = MU[2], MU[3], SD[2], SD[3]
rho_cf = (s7**2 + s10**2 - (mu10 - mu7)**2)/(2*s7*s10)          # Phi(|d|/sigma_d) = Phi(1)
lo, hi = -0.95, 0.0
for _ in range(30):
    mid = 0.5*(lo + hi); Cp = np.eye(6); Cp[2, 3] = Cp[3, 2] = mid      # only the 0.7/1.0 pair matters for this segment
    Wm = draw(MU, SD, Cp, 400_000); p = seg_eps(Wm)[0][2]
    lo, hi = (lo, mid) if p >= T68 else (mid, hi)
mc = math.sqrt(T68*(1 - T68)/400_000)
P(f"  closed-form Gaussian (no positivity cut): rho_adj* = {rho_cf:+.3f}; draws (positivity cut, N 4e5): rho_adj* = {0.5*(lo+hi):+.3f}; "
  f"Monte-Carlo error on p ~ {mc:.4f}")
P(f"  at rho_adj -0.5 the frozen run had p_rise 0.84149 vs t68 0.8413: within {abs(0.84149 - T68)/mc:.1f} MC sigma of the line (KNIFE-EDGE)")
OUT["PH1"] = dict(rho_closed_form=rho_cf, rho_draws=0.5*(lo + hi), mc_err=mc)

# PH2
P("\n=== PH2. net intervals [0, 0.4] and [0, 0.7] (eps; not in the frozen set) ===")
OUT["PH2"] = {}
for k, zk in ((1, "0.4"), (2, "0.7")):
    for r in (-0.5, 0.0, 0.5):
        Cr = np.eye(6); Cr[0, k] = Cr[k, 0] = r
        Wn = draw(MU, SD, Cr, 400_000); ok = (Wn[:, 0] > 0) & (Wn[:, k] > 0)
        x = np.sqrt(Wn[ok, k]/Wn[ok, 0]); q = np.percentile(x, QP); pfall = float(np.mean(x > 1))
        f68 = "FALL" if q[1] > 1 else ("RISE" if q[3] < 1 else "FLAT"); f95 = "FALL" if q[0] > 1 else ("RISE" if q[4] < 1 else "FLAT")
        OUT["PH2"][f"{zk}:{r:+.1f}"] = dict(q=q.tolist(), P_a0_higher_then=pfall, f68=f68, f95=f95)
        P(f"  a0({zk})/a0(0), corr(w0, w{zk}) {r:+.1f}: median {q[2]:.3f}, 68% [{q[1]:.3f}, {q[3]:.3f}], 95% [{q[0]:.3f}, {q[4]:.3f}]; "
          f"P(a0 higher at z {zk} than today) {pfall:.3f} -> 68% {f68}, 95% {f95}")

# PH3
P("\n=== PH3. calibrate the omitted correlations from the stored joint quantiles (sqrtX_q 16/50/84) ===")
grid = np.round(np.arange(-0.95, 0.951, 0.05), 2); OUT["PH3"] = {}
def sqx(Wd, zz):
    wz = Wd@np.array([np.interp(zz, NODES, np.eye(6)[i]) for i in range(6)])
    X = np.where(Wd[:, 0] > 0, wz/np.where(Wd[:, 0] > 0, Wd[:, 0], 1.0), -1.0)
    return np.percentile(np.sqrt(np.clip(X, 0, None)), QP)
for zk, k in (("1.0", 3), ("1.5", 4), ("2.33", 5)):
    best = None
    for r in grid:
        Cr = np.eye(6); Cr[0, k] = Cr[k, 0] = r
        q = sqx(draw(MU, SD, Cr, 200_000), float(zk)); d = max(abs(q[i] - STQ[zk][i]) for i in (1, 2, 3))
        if best is None or d < best[1]: best = (float(r), d, q[1:4].tolist())
    OUT["PH3"][zk] = dict(best_corr_w0=best[0], max_dev=best[1], q=best[2], stored=STQ[zk][1:4])
    P(f"  corr(w0, w{zk}) best fit {best[0]:+.2f} (max dev {best[1]:.4f}; approx {np.round(best[2], 4).tolist()} vs stored {np.round(STQ[zk][1:4], 4).tolist()})")
bestq = None
for r in np.round(np.arange(-0.15, 0.951, 0.05), 2):
    Cr = np.full((6, 6), r); np.fill_diagonal(Cr, 1.0)
    try: Wq = draw(MU, SD, Cr, 200_000)
    except np.linalg.LinAlgError: continue
    d = max(abs(sqx(Wq, float(zk))[i] - STQ[zk][i]) for zk in ZS for i in (1, 2, 3))
    if bestq is None or d < bestq[1]: bestq = (float(r), d)
P(f"  one all-node equicorrelation fitted to all four z: rho_eq = {bestq[0]:+.2f} (max dev {bestq[1]:.4f}; frozen K1b tolerance 0.03)")
Cr = np.full((6, 6), bestq[0]); np.fill_diagonal(Cr, 1.0)
Wq = draw(MU, SD, Cr, 400_000); pr, pf, fn = seg_eps(Wq); cl = classify(pr, pf, fn, NODES, netflags_from(STQ))
P(f"  segments under rho_eq: p_rise {np.round(pr, 4).tolist()} p_fall {np.round(pf, 4).tolist()} f_NEC {np.round(fn, 4).tolist()}")
P(f"    68%: {cl['68']['flags']} -> {cl['68']['cls']}, arrow {cl['68']['arrow']}; 95%: {cl['95']['flags']} -> {cl['95']['cls']}, arrow {cl['95']['arrow']}")
h0g = H0_of(D)*KMSMPC_TO_GYR; m1 = (Wq[:, 1] - Wq[:, 0])/0.4
rq = np.nanpercentile(np.where(Wq[:, 0] > 0, -0.5*h0g*m1/Wq[:, 0], np.nan), QP)
x7 = np.sqrt(np.clip(Wq[:, 2], 0, None)/Wq[:, 0]); q7 = np.percentile(x7, QP)
P(f"  under rho_eq: today's literal eps rate median {rq[2]:+.4f}/Gyr, 68% [{rq[1]:+.4f}, {rq[3]:+.4f}], 95% [{rq[0]:+.4f}, {rq[4]:+.4f}] "
  f"({rq[2]/h0g:+.3f} H0); a0(0.7)/a0(0) median {q7[2]:.3f}, 68% [{q7[1]:.3f}, {q7[3]:.3f}], 95% [{q7[0]:.3f}, {q7[4]:.3f}]; "
  f"P(a0 max at node) " + ", ".join(f"z {NODES[k]:g}: {np.mean(np.argmax(Wq, axis=1) == k):.3f}" for k in range(6)))
OUT["PH3"]["equicorr"] = dict(rho_eq=bestq[0], max_dev=bestq[1], p_rise=pr.tolist(), p_fall=pf.tolist(), f_NEC=fn.tolist(), cls=cl,
                              rate_today_q_per_Gyr=rq.tolist(), a0_07_over_0_q=q7.tolist())

# PH4
P("\n=== PH4. CFG689 committed bracket modes (eps, literal, APPROX-G; theta* modes T* not folded into canon: K9 failed) ===")
OUT["PH4"] = {}
P("  mode | P2 sigma | segments | p_rise (rho_adj 0) | 68% class/arrow (rho -0.5 / 0 / +0.5) | 95% class/arrow (rho 0) | today r_eps median [68%] /Gyr")
for f in sorted(glob.glob(os.path.join(C689, "cfg689_*.json"))):
    d = json.load(open(f)); b = d.get("BAO+SN")
    if not b or "posterior" not in b or d["mode"].startswith("M"): continue
    if not b["K4"]["ok"]:
        P(f"  {d['mode']}: K4 FAILED in CFG689 (no reading) - skipped"); continue
    nd = np.array(d["cfg"]["nodes"]); mu = np.array(b["posterior"]["node_mean"]); sd = np.array(b["posterior"]["node_std"])
    nf = netflags_from({zk: b["P1"][zk]["sqrtX_q"] for zk in b["P1"]})
    res = {}
    for r in (-0.5, 0.0, 0.5):
        Wb = draw(mu, sd, corr_adj(len(nd), r), 200_000); pr, pf, fn = seg_eps(Wb)
        res[r] = (pr, classify(pr, pf, fn, nd, nf), Wb)
    W0 = res[0.0][2]; h0g = H0_of(d)*KMSMPC_TO_GYR
    m1 = (W0[:, 1] - W0[:, 0])/(nd[1] - nd[0]); rr = np.where(W0[:, 0] > 0, -0.5*h0g*m1/W0[:, 0], np.nan); qr = np.nanpercentile(rr, QP)
    c68 = " / ".join(f"{res[r][1]['68']['cls']}, {res[r][1]['68']['arrow']}" for r in (-0.5, 0.0, 0.5))
    P(f"  {d['mode']:5s} | {b['P2']['sigma_equiv']:.2f} | {[f'{a:g}-{c:g}' for a, c in zip(nd[:-1], nd[1:])]} | {np.round(res[0.0][0], 3).tolist()} | "
      f"{c68} | {res[0.0][1]['95']['cls']}, {res[0.0][1]['95']['arrow']} | {qr[2]:+.4f} [{qr[1]:+.4f}, {qr[3]:+.4f}]")
    OUT["PH4"][d["mode"]] = dict(p2_sigma=b["P2"]["sigma_equiv"], nodes=nd.tolist(), p_rise_rho0=res[0.0][0].tolist(),
                                 cls={f"{r:+.1f}": res[r][1] for r in (-0.5, 0.0, 0.5)}, rate_today_q_per_Gyr=qr.tolist())
json.dump(OUT, open(os.path.join(HERE, "wt03_posthoc.json"), "w"), indent=1, default=lambda o: o.tolist() if isinstance(o, np.ndarray) else float(o))
OUTF.close()
