"""AGB1R Part A: BAO + supernovae, flat w0-wa, no CMB. One mode per process; writes agb1r_A_<mode>.json.
Modes: full, des_only, rand197, bao_overlap (frozen); tmplW_full, tmplW_des_only, legacy_offset (reported only)."""
import os, sys, time
import numpy as np
from scipy.interpolate import CubicSpline
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agb1r_common import (load_des, sample_keep, SN, BAO, PartA, build_template, fit_A, a_profile, intervals,
                          w1_word, w2_word, w3_word, dump, HERE)

MODE = sys.argv[1]
GRID = [round(-1.0 + 0.1*i, 1) for i in range(41)]
t0 = time.time()
logf = open(os.path.join(HERE, f"agb1r_A_{MODE}.out"), "w")
def log(s=""):
    print(s, flush=True); logf.write(s + "\n"); logf.flush()

D = load_des()
sample = {"tmplW_full": "full", "tmplW_des_only": "des_only", "legacy_offset": "full"}.get(MODE, MODE)
keep = sample_keep(D, sample)
kind = "W" if MODE.startswith("tmplW") else "S"
TT = build_template(kind)
T = TT["spline"](D["zhd"][keep])
sn = SN(D, keep, T)
bao = BAO("overlap" if MODE == "bao_overlap" else "all")
model = PartA(sn, bao)
log(f"AGB1R Part A, mode {MODE}: {len(keep)} supernovae, {len(bao.bins)} BAO D_M/D_H bins + BGS, template T_{kind}")
out = dict(mode=MODE, sample=sample, n_sn=len(keep), template=kind, bao_bins=[b[0] for b in bao.bins] + ["BGS"])
if MODE == "rand197":
    dropped = np.setdiff1d(np.arange(len(D["zhd"])), keep)
    out["rand197_dropped_cid_first10"] = D["cid"][dropped][:10].tolist()
    out["rand197_dropped_positions"] = dropped.tolist()


def fmt(r):
    s = (f"Om {r['Om']:.4f}  w0 {r['w0']:+.4f}  wa {r['wa']:+.4f}  q0 {r['q0']:+.4f}  A {r['A']:+.4f}  "
         f"chi2 {r['chi2']:.4f} (SN {r['chi2_sn']:.3f}, BAO {r['chi2_bao']:.3f})  min q {r['minq']:+.4f} at z {r['z_minq']:.3f}")
    if r["edge"]: s += "  AT PRIOR EDGE " + ",".join(r["edge"])
    if "constraint_met" in r and not r["constraint_met"]: s += "  CONSTRAINT NOT MET"
    return s


if MODE != "legacy_offset":
    log("A profile (two sweeps):")
    prof = a_profile(model, GRID, log=log)
    # A free: fifth start from the grid minimum
    gmin = min(GRID, key=lambda a: prof[a]["chi2"])
    fr = fit_A(model, None, "free", extra_starts=[(prof[gmin]["Om"], prof[gmin]["w0"], prof[gmin]["wa"])])
    log(f"A free: {fmt(fr)}")
    chis = np.array([prof[a]["chi2"] for a in GRID])
    # KA: spline through the grid only
    sp = CubicSpline(GRID, chis); fine = np.linspace(GRID[0], GRID[-1], 400001); cf = sp(fine); i = int(np.argmin(cf))
    ka = dict(spline_Amin=float(fine[i]), spline_chi2min=float(cf[i]), A_free=fr["A"], chi2_free=fr["chi2"])
    ka["pass_"] = bool(abs(ka["spline_Amin"] - fr["A"]) <= 0.03 and abs(ka["spline_chi2min"] - fr["chi2"]) <= 0.05)
    log(f"KA: spline min A {ka['spline_Amin']:+.4f} vs A_free {fr['A']:+.4f}; chi2 {ka['spline_chi2min']:.4f} vs "
        f"{fr['chi2']:.4f} -> {'PASS' if ka['pass_'] else 'FAIL'}")
    # the A = 0 and A = 1 forks: refit with the grid point's best fit as fifth start; keep the lower (grid updated)
    forks = {}
    for lab, Af in (("A0", 0.0), ("A1", 1.0)):
        g = prof[Af]
        r = fit_A(model, Af, "free", extra_starts=[(g["Om"], g["w0"], g["wa"])])
        if r["chi2"] > g["chi2"]: r = g
        prof[Af] = r; forks[lab] = r
    forks["Afree"] = fr
    chis = np.array([prof[a]["chi2"] for a in GRID])
    iv, _, _ = intervals(GRID, chis, fr["chi2"], fr["A"])
    # intervals from the grid-only spline with the A-free chi2 as reference
    sp = CubicSpline(GRID, chis); cf = sp(fine)
    ivg = {}
    for L in (1.0, 4.0):
        idx = np.where(cf - fr["chi2"] <= L)[0]
        if len(idx) == 0: ivg[L] = None; continue
        lo = float(fine[idx[0]]) if idx[0] > 0 else None; hi = float(fine[idx[-1]]) if idx[-1] < len(fine) - 1 else None
        ivg[L] = [lo, hi]
    d0 = prof[0.0]["chi2"] - fr["chi2"]; d1 = prof[1.0]["chi2"] - fr["chi2"]
    log(f"best A {fr['A']:+.4f}; dchi2 = 1 interval {ivg[1.0]}; dchi2 = 4 interval {ivg[4.0]} "
        f"(with A-free point in spline: {iv[1.0]}, {iv[4.0]})")
    log(f"dchi2(A = 0) = {d0:.4f};  dchi2(A = 1) = {d1:.4f}")
    out.update(profile={a: prof[a] for a in GRID}, A_free=fr, KA=ka, interval_1=ivg[1.0], interval_4=ivg[4.0],
               interval_1_withfree=iv[1.0], interval_4_withfree=iv[4.0], dchi2_A0=d0, dchi2_A1=d1,
               W1_first=w1_word(d0, d1))
    log(f"first word of W1 on this sample: {out['W1_first']}")
    if kind == "W":
        f023 = fit_A(model, 0.23, "free", extra_starts=[(prof[0.2]["Om"], prof[0.2]["w0"], prof[0.2]["wa"]),
                                                        (prof[0.3]["Om"], prof[0.3]["w0"], prof[0.3]["wa"])])
        out["dchi2_AW_023"] = f023["chi2"] - fr["chi2"]; out["fit_AW_023"] = f023
        log(f"T_W: dchi2(A_W = 0) {d0:.4f}; dchi2(A_W = 0.23) {out['dchi2_AW_023']:.4f}; dchi2(A_W = 1) {d1:.4f}")

    if MODE in ("full", "des_only", "bao_overlap"):
        out["forks"] = {}
        for lab, Af in (("A0", 0.0), ("A1", 1.0), ("Afree", None)):
            b = forks[lab]
            st = [(b["Om"], b["w0"], b["wa"])]
            rq = fit_A(model, Af, "q0", extra_starts=st)
            rn = fit_A(model, Af, "never", extra_starts=st)
            dt = rq["chi2"] - b["chi2"]; dn = rn["chi2"] - b["chi2"]
            rec = dict(best=b, q0zero=rq, never=rn, dchi2_today=dt, dchi2_never=dn,
                       W2=w2_word(b["q0"], dt), W3=w3_word(dn))
            out["forks"][lab] = rec
            log(f"fork {lab}:")
            log(f"  best      {fmt(b)}")
            log(f"  q0 = 0    {fmt(rq)}   dchi2_today {dt:.4f}")
            log(f"  never     {fmt(rn)}   dchi2_never {dn:.4f}")
            log(f"  W2 {rec['W2']};  W3 {rec['W3']}")

else:
    # legacy_offset: a constant step delta on the 197 legacy SNe in place of (and then beside) the age template
    leg = (D["ids"][keep] != 10).astype(float)
    snd = SN(D, keep, leg); md = PartA(snd, bao)
    dfree = fit_A(md, None, "free")
    d0fit = fit_A(md, 0.0, "free", extra_starts=[(dfree["Om"], dfree["w0"], dfree["wa"])])
    log(f"delta free (age template off): best delta {dfree['A']:+.4f} mag  chi2 {dfree['chi2']:.4f};  "
        f"dchi2(delta = 0) {d0fit['chi2'] - dfree['chi2']:.4f}")
    out["delta_only"] = dict(free=dfree, at0=d0fit, dchi2_delta0=d0fit["chi2"] - dfree["chi2"])
    # delta and A both free: profile delta analytically with M by putting the step into the data at fixed delta is not
    # linear-exact, so do it exactly: a two-template linear profile (M, delta, A) via a wrapper SN class.
    class SN2:
        def __init__(s, base, T1, T2):
            s.W = base.W; s.mu = base.mu; s.z = base.z; s.zhel = base.zhel
            X = np.c_[np.ones(len(s.z)), T1, T2]; s.X = X; s.WX = s.W @ X; s.XWX = X.T @ s.WX
        def chi2(s, muth, A=None):
            r = s.mu - muth
            if A is not None: r = r - A*s.X[:, 2]
            Wr = s.W @ r; rWr = float(r @ Wr)
            if A is None:
                v = s.WX.T @ r; sol = np.linalg.solve(s.XWX, v); return rWr - float(v @ sol), float(sol[2]), float(sol[0])
            v = s.WX[:, :2].T @ r; sol = np.linalg.solve(s.XWX[:2, :2], v)
            return rWr - float(v @ sol), float(A), float(sol[0])
    sn2 = SN2(sn, leg, T); m2 = PartA(sn2, bao); m2.nsn = len(keep)
    both = fit_A(m2, None, "free")
    prof2 = {}
    for Af in GRID:
        prof2[Af] = fit_A(m2, Af, "free", extra_starts=[(both["Om"], both["w0"], both["wa"])])
    chis = np.array([prof2[a]["chi2"] for a in GRID])
    sp = CubicSpline(GRID, chis); fine = np.linspace(GRID[0], GRID[-1], 400001); cf = sp(fine)
    ivs = {}
    for L in (1.0, 4.0):
        idx = np.where(cf - both["chi2"] <= L)[0]
        lo = float(fine[idx[0]]) if idx[0] > 0 else None; hi = float(fine[idx[-1]]) if idx[-1] < len(fine) - 1 else None
        ivs[L] = [lo, hi]
    # delta at the joint best fit
    dm = m2.dist.DM(both["Om"], both["w0"], both["wa"])[:len(keep)]
    muth = 5*np.log10((1 + sn.zhel)*dm); r = sn.mu - muth; v = sn2.WX.T @ r; sol = np.linalg.solve(sn2.XWX, v)
    d0b = prof2[0.0]["chi2"] - both["chi2"]; d1b = prof2[1.0]["chi2"] - both["chi2"]
    log(f"delta and A free: best A {both['A']:+.4f} (delta {sol[1]:+.4f} mag) chi2 {both['chi2']:.4f};  "
        f"A interval dchi2=1 {ivs[1.0]}, dchi2=4 {ivs[4.0]};  dchi2(A=0) {d0b:.4f}, dchi2(A=1) {d1b:.4f} (delta free)")
    out["delta_and_A"] = dict(free=both, delta=float(sol[1]), interval_1=ivs[1.0], interval_4=ivs[4.0],
                              dchi2_A0=d0b, dchi2_A1=d1b, profile=prof2)

out["runtime_s"] = time.time() - t0
dump(out, os.path.join(HERE, f"agb1r_A_{MODE}.json"))
log(f"done in {out['runtime_s']:.0f} s")
