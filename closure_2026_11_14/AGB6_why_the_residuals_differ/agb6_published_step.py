"""AGB6 extension (written after the plan's chain was run and its step 6 was seen to carry slope; same rule).

Step 6 of the chain, raw Pantheon+ magnitudes -> published ones (m_b_corr), is broken into its parts. First the
construction of m_b_corr is recovered from the release itself: m_b_corr - mB + biasCor_m_b is regressed on x1, c and
the low-mass flag over the whole release. Then, on the chain's supernovae and with the chain's fit:
   P    mB, stretch and colour coefficients free
   Pc   mB + alpha x1 - beta c with the release's coefficients, nothing else
   Pcb  Pc - biasCor_m_b            (the release's bias correction, which is computed per host-mass group)
   Pb   m_b_corr                    (as published)
Writes agb6_published_step.json; log to agb6_published_step.out."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = ["agb6_chain.py"]; sys.path.insert(0, HERE)
import numpy as np
import agb6_chain as C

log = lambda s: print(s, flush=True); out = {}
f = os.path.join(C.D4.PP, "PantheonPlusSH0ES.dat"); hdr = open(f).readline().split(); raw = np.genfromtxt(f, skip_header=1, dtype=str)
g = lambda n: raw[:, hdr.index(n)].astype(float)
mB, mc, x1, c, bc, lm, z, ids = g("mB"), g("m_b_corr"), g("x1"), g("c"), g("biasCor_m_b"), g("HOST_LOGMASS"), g("zHD"), g("IDSURVEY").astype(int)
k = (z > 0.01) & (lm > 5)
for lab, kk in (("whole release, z > 0.01", k), ("SDSS rows", k & (ids == 1))):
    X = np.column_stack([np.ones(kk.sum()), x1[kk], c[kk], (lm[kk] < 10) - 0.5]); y = (mc - mB + bc)[kk]; b = np.linalg.lstsq(X, y, rcond=None)[0]; r = y - X@b
    X2 = np.column_stack([np.ones(kk.sum()), x1[kk], c[kk]]); y2 = (mc - mB)[kk]; b2 = np.linalg.lstsq(X2, y2, rcond=None)[0]
    log(f"{lab} (n {kk.sum()}): m_b_corr - mB + biasCor = {b[0]:+.4f} + {b[1]:.4f} x1 + ({b[2]:.4f}) c + ({b[3]:+.4f}) x (low-mass - 1/2); rms {r.std():.4f} mag."
        f" Mean biasCor: low-mass {bc[kk][lm[kk] < 10].mean():+.4f}, high-mass {bc[kk][lm[kk] >= 10].mean():+.4f}")
    out[lab] = dict(alpha=float(b[1]), beta=float(-b[2]), step=float(b[3]), rms=float(r.std()), bias_low=float(bc[kk][lm[kk] < 10].mean()), bias_high=float(bc[kk][lm[kk] >= 10].mean()))
al, be = out["whole release, z > 0.01"]["alpha"], out["whole release, z > 0.01"]["beta"]

d = C.assemble(); pos = {q: i for i, q in enumerate(raw[:, hdr.index("CID")][ids == 1])}; ix = np.array([pos[q] for q in d["cid"]]); bias = bc[ids == 1][ix]
assert np.allclose(mB[ids == 1][ix], d["mB"])
mf = C.mu_fid(d["z"], d["zh"]); S = {"P": (d["mB"] - mf, [d["x1p"], d["cp"]]), "Pc": (d["mB"] + al*d["x1p"] - be*d["cp"] - mf, []),
                                    "Pcb": (d["mB"] + al*d["x1p"] - be*d["cp"] - bias - mf, []), "Pb": (d["mcorr"] - mf, [])}
n = len(d["age"]); idx0 = np.arange(n); e = np.quantile(d["z"], np.linspace(0, 1, 9)); b = np.clip(np.searchsorted(e, d["z"], side="right") - 1, 0, 7)
rng = np.random.default_rng(C.SEED); boots = [rng.integers(0, n, n) for _ in range(400)]
for wl, w in (("claim's weights", 1/(d["shr"]**2 + 0.01)), ("equal weights", np.ones(n))):
    for step in (False, True):
        A = {q: C.amp(y, ex, d, idx0, w, step, b) for q, (y, ex) in S.items()}; Bt = {q: np.array([C.amp(y, ex, d, i, w, step, b) for i in boots]) for q, (y, ex) in S.items()}
        key = f"{wl}, {'step' if step else 'nostep'}"; out[key] = dict(A={q: [float(A[q]), float(Bt[q].std(ddof=1))] for q in S}, steps={})
        log(f"{wl}, n {n}, {'mass step free' if step else 'no mass step'}: " + "  ".join(f"{q} {A[q]:+.3f} +- {Bt[q].std(ddof=1):.3f}" for q in S))
        for a, cc in (("P", "Pc"), ("Pc", "Pcb"), ("Pcb", "Pb"), ("P", "Pb")):
            dv = A[a] - A[cc]; sd = float((Bt[a] - Bt[cc]).std(ddof=1)); out[key]["steps"][f"{a}->{cc}"] = dict(change=float(dv), sd=sd, carries=bool(abs(dv) >= 2*sd))
            log(f"      step {a:3s} -> {cc:3s}: change {dv:+.3f} +- {sd:.3f} ({dv/sd:+.1f} sigma)  {'CARRIES SLOPE' if abs(dv) >= 2*sd else 'does not'}")
# what the bias correction looks like against host age on these supernovae
low = d["mass"] < 10; B = np.zeros((n, 8)); B[np.arange(n), b] = 1.0
def line(v, idx, extra=None):
    cols = [B[idx][:, B[idx].sum(0) > 0]] + ([] if extra is None else [extra[idx]]) + [d["age"][idx]]; return np.linalg.lstsq(np.column_stack(cols), v[idx], rcond=None)[0][-1]
s0 = line(bias, idx0); sd = np.std([line(bias, i) for i in boots], ddof=1); s1 = line(bias, idx0, low - 0.5); sd1 = np.std([line(bias, i, low - 0.5) for i in boots], ddof=1)
log(f"the release's bias correction on these supernovae: mean {bias[low].mean():+.4f} in low-mass hosts, {bias[~low].mean():+.4f} in the others;"
    f" trend with host age {s0:+.5f} +- {sd:.5f} mag/Gyr ({s0/C.SLOPE:+.3f} in units of the published slope); with a mass step taken out {s1:+.5f} +- {sd1:.5f} ({s1/C.SLOPE:+.3f})")
out["bias_vs_age"] = dict(slope=float(s0), sd=float(sd), slope_with_step=float(s1), sd_with_step=float(sd1), mean_low=float(bias[low].mean()), mean_high=float(bias[~low].mean()))
json.dump(out, open(os.path.join(HERE, "agb6_published_step.json"), "w"), indent=1, default=float); log("wrote agb6_published_step.json")
