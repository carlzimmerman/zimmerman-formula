"""NV1 candidate loader for RQ3: a frozen admissible GP rule on (log y, log ell, f, E), g = law(g_b, a0) 10^m. E is looked up from the call's keys by the candidate's
formula (FROZEN_CRITERIA, candidate loader): sample + name (discs, LITTLE THINGS, dwarfs), r500 (X-COP rows), lgMb (groups), the grid's total baryons (lensing, E2), sample (MW, planets).
No E -> NaN -> RQ3 reads NOT COMPUTABLE. Reading name / sample / r500 / host earns RQ3's [LABEL] tag: inherent to a non-local leaf. Leaves as np2_cand (NP2), copied.
A description of data, not a theory; no action. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
import numpy as np
sys.dont_write_bytecode = True
_H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(_H), "SY1_free_constant_law_search"))
import sy1_leaves as _L
A0F = dict(canonical=9.360324825027975e-11, alt=1.1312e-10); EM1 = (11.18, 0.90); G_SI, MSUN = 6.674e-11, 1.989e30
def load(stem, table):
    RS = {k: dict(np.load(os.path.join(_H, "rules", f"{stem}_{k}.npz"))) for k in A0F}; T = json.load(open(os.path.join(_H, "rules", f"{table}.json"))); return RS, T
def _k(A, B, ell, sf2):
    A = A / ell; B = B / ell; d = (A * A).sum(1)[:, None] + (B * B).sum(1)[None, :] - 2 * A @ B.T; return sf2 * np.exp(-0.5 * np.maximum(d, 0))
def _m(R, F, chunk=2000):
    out = np.full(len(F), np.nan); ok = np.all(np.isfinite(F), 1); Z = (F[ok] - R["mu"]) / R["sd"]; ell = R["ell"]; sf2 = float(R["sf2"]); v = np.empty(len(Z))
    Zc, Vc, be = R["Zc"], R["Vc"], R["beta"]; Vl = Vc / ell ** 2
    for i in range(0, len(Z), chunk):
        q = Z[i:i + chunk]; x = _k(q, R["Z"], ell, sf2) @ R["alpha"]
        if len(be): x = x + (_k(q, Zc, ell, sf2) * (q @ Vl.T - (Vl * Zc).sum(1)[None, :])) @ be
        v[i:i + chunk] = x
    out[ok] = v; return out
def _em1(T, lgMb):
    E = EM1[0] + EM1[1] * (np.asarray(lgMb, float) - 10.0)
    mm = T.get("mut_map")
    if mm is not None:   # E-shuffle MUTATE: an on-the-fly E takes the shuffled value of the tabulated system with the nearest original E
        o = np.asarray(mm[0]); s = np.asarray(mm[1]); E = s[np.abs(o[None, :] - np.ravel(E)[:, None]).argmin(1)].reshape(np.shape(E))
    return E
def E_of(T, Q, gb):
    s = Q["sample"]
    if s in ("disc", "dwarf disc", "dwarf"):
        if "name" not in Q: return np.nan
        v = T.get(s, {}).get(str(Q["name"]))
        return np.nan if v is None else float(v)
    if s == "cluster":
        if "r500" not in Q or not T.get("cluster_r500"): return np.nan
        r5 = np.asarray(Q["r500"], float); ref = np.array([x[0] for x in T["cluster_r500"]]); ev = np.array([np.nan if x[1] is None else x[1] for x in T["cluster_r500"]], float)
        j = np.abs(np.log(np.maximum(r5, 1e-300))[..., None] - np.log(ref)).argmin(-1); hit = np.isclose(r5, ref[j], rtol=1e-9, atol=0); return np.where(hit, ev[j], np.nan)
    if s == "group":
        if T.get("group") != "EM1" or "lgMb" not in Q: return np.nan
        return _em1(T, float(Q["lgMb"]))
    if s == "lens":
        if T.get("lens") != "EM1": return np.nan
        r = np.ravel(np.asarray(Q["r"], float)); g = np.ravel(gb); M = g[-1] * r[-1] ** 2 / G_SI / MSUN; return _em1(T, math.log10(M)) if M > 0 else np.nan
    if s in ("MW", "planet"):
        v = T.get(s); return np.nan if v is None else float(v)
    return np.nan
def g_core(R, gb, gg, r, a0, E):
    pos = gb > 0; safe = np.where(pos, gb, 1.0); y = safe / _L.A0C
    with np.errstate(all="ignore"): f = np.clip(np.asarray(gg, float) / safe, 0.0, 1.0)
    r = np.broadcast_to(np.asarray(r, float), gb.shape); ell = r * _L.A0C / _L.CL ** 2; f = np.broadcast_to(f, gb.shape); E = np.broadcast_to(np.asarray(E, float), gb.shape)
    with np.errstate(all="ignore"):
        F = np.column_stack([np.ravel(np.log10(y)), np.ravel(np.log10(ell)), np.ravel(f), np.ravel(E)]); H = (10 ** _m(R, F)).reshape(gb.shape)
    bad = pos & (~np.isfinite(H) | (H <= 0)); v = np.where(pos, _L.wrap(3, safe, a0, np.where(pos & np.isfinite(H), H, 1.0)), gb)
    return np.where(bad, np.nan, v)
def g_of_Q(RT, Q):
    RS, T = RT; gb = np.asarray(Q["gb"], float); a = float(Q["a0"]); R = RS[min(A0F, key=lambda k: abs(np.log(a / A0F[k])))]
    E = E_of(T, Q, gb); return g_core(R, gb, Q["gg"], Q["r"], a, E)
