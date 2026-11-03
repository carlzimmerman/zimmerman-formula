"""NP1 candidate loader for RQ3: a frozen Gaussian-process rule, g = law(g_b, a0) 10^m(leaves), leaves as SY1's g_of_Q computes them, one fit per footing chosen by the a0 passed in.
Reads gb, gg, r, a0 only; never a label. Non-finite leaves or H return NaN, so RQ3 reads NOT COMPUTABLE. A description of data, not a theory; no action. kappa = 1/2 FITTED."""
import os, sys
import numpy as np
sys.dont_write_bytecode = True
_H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(_H), "SY1_free_constant_law_search"))
import sy1_leaves as _L
A0F = dict(canonical=9.360324825027975e-11, alt=1.1312e-10)
def load(stem):
    return {k: dict(np.load(os.path.join(_H, "rules", f"{stem}_{k}.npz"))) for k in A0F}
def _m(R, F, chunk=2000):
    out = np.full(len(F), np.nan); ok = np.all(np.isfinite(F), 1); Z = (F[ok] - R["mu"]) / R["sd"]; ell = R["ell"]; v = np.empty(len(Z)); B = R["Z"] / ell
    for i in range(0, len(Z), chunk):
        A = Z[i:i + chunk] / ell; d = (A * A).sum(1)[:, None] + (B * B).sum(1)[None, :] - 2 * A @ B.T; v[i:i + chunk] = (float(R["sf2"]) * np.exp(-0.5 * np.maximum(d, 0))) @ R["alpha"]
    out[ok] = v; return out
def g_of_Q(RS, Q):
    gb = np.asarray(Q["gb"], float); a = float(Q["a0"]); R = RS[min(A0F, key=lambda k: abs(np.log(a / A0F[k])))]; arm = str(R["arm"])
    pos = gb > 0; safe = np.where(pos, gb, 1.0); y = safe / _L.A0C
    with np.errstate(all="ignore"): f = np.clip(np.asarray(Q["gg"], float) / safe, 0.0, 1.0)
    r = np.broadcast_to(np.asarray(Q["r"], float), gb.shape); ell = r * _L.A0C / _L.CL ** 2; f = np.broadcast_to(f, gb.shape)
    with np.errstate(all="ignore"):
        cols = [np.log10(y), np.log10(ell), f]
        if arm == "L5": s = _L.slope(gb, r); D = _L.D_leaf(y, s, ell); cols += [s, np.arcsinh(D)]
        F = np.column_stack([np.ravel(c) for c in cols]); H = (10 ** _m(R, F)).reshape(gb.shape)
    bad = pos & (~np.isfinite(H) | (H <= 0)); v = np.where(pos, _L.wrap(3, safe, a, np.where(pos & np.isfinite(H), H, 1.0)), gb)
    return np.where(bad, np.nan, v)
