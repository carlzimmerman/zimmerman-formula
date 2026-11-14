"""AGB6 chain (plan: PLAN.md in this folder). A diagnosis, not a blind test.

Seven sets of residuals for the same supernovae, each fitted the same way (weighted line in host age inside 8
redshift bins; A in units of 0.030 mag/Gyr), and the change of A across each step with its bootstrap error.
Writes agb6_chain.json; log to agb6_chain.out."""
import json, os, sys
for _v in ("VECLIB_MAXIMUM_THREADS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import warnings
import numpy as np
warnings.filterwarnings("ignore", message=".*encountered in matmul")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.environ.get("AGB5_REPO") or os.path.normpath(os.path.join(HERE, "..", ".."))
os.environ.setdefault("AGB5_REPO", REPO)
sys.path.insert(0, os.path.join(REPO, "closure_2026_11_14", "AGB5_claims_own_age_table"))
import agb5_data as D5
D4 = D5.D4
SLOPE = -0.030; ALPHA, BETA = 0.183, 2.91; SEED = 20261122
log = lambda s: print(s, flush=True)


def mu_fid(z, zh, om=0.334):
    zg = np.expm1(np.linspace(0, np.log(2.0), 20001)); e = np.sqrt(om*(1 + zg)**3 + 1 - om)
    dm = np.concatenate([[0.0], np.cumsum(0.5*(1/e[1:] + 1/e[:-1])*np.diff(zg))])
    return 5*np.log10((1 + zh)*np.interp(z, zg, dm))


def sako_blocks():
    lines = open(D4.SAKO).read().split("\n"); hdr = lines[0].split(); rows = [l.split() for l in lines[1:] if l.strip()]
    occ = lambda n: [i for i, x in enumerate(hdr) if x == n]; num = lambda i: np.array([np.nan if r[i] == "\\N" else float(r[i]) for r in rows])
    return dict(cid=np.array([r[0] for r in rows]), x0=num(occ("x0")[0]), x1=num(occ("x1")[0]), c=num(occ("c")[0]), mu_salt=num(occ("mu")[0]), mu_mlcs=num(occ("mu")[1]))


def assemble():
    p = D4.pantheon_sdss(); S = sako_blocks(); pos = {c: i for i, c in enumerate(S["cid"])}
    rows = {}
    for which in (2, 1):                                   # table 1 wins for the shared hosts, as in AGB5
        T = D5.table(which)
        for i, c in enumerate(T["id"]): rows[c] = (T["age"][i], T["hr"][i], T["s_hr"][i], which)
    keep = np.array([(c in rows) and (c in pos) for c in p["cid"]]); cid = p["cid"][keep]; ix = np.array([pos[c] for c in cid])
    d = dict(cid=cid, z=p["z"][keep], zh=p["zh"][keep], mB=p["mB"][keep], x1p=p["x1"][keep], cp=p["c"][keep], mcorr=p["mcorr"][keep], mass=p["lm"][keep],
             age=np.array([rows[c][0] for c in cid]), hr=np.array([rows[c][1] for c in cid]), shr=np.array([rows[c][2] for c in cid]),
             tab=np.array([rows[c][3] for c in cid]), x0s=S["x0"][ix], x1s=S["x1"][ix], cs=S["c"][ix], mus=S["mu_salt"][ix], mum=S["mu_mlcs"][ix])
    ok = np.all([np.isfinite(d[k]) for k in ("age", "hr", "x0s", "x1s", "cs", "mus", "mum", "mB", "x1p", "cp", "mcorr", "mass")], axis=0) & (d["x0s"] > 0)
    return {k: v[ok] for k, v in d.items()}


def sets(d):
    mf = mu_fid(d["z"], d["zh"])
    return {"C": (d["hr"], []), "M": (d["mum"] - mf, []), "S": (d["mus"] - mf, []), "S'": (-2.5*np.log10(d["x0s"]) - mf, [d["x1s"], d["cs"]]),
            "P'": (d["mB"] + ALPHA*d["x1p"] - BETA*d["cp"] - mf, []), "P": (d["mB"] - mf, [d["x1p"], d["cp"]]), "Pb": (d["mcorr"] - mf, [])}


STEPS = [("C", "S"), ("C", "M"), ("S", "S'"), ("S'", "P"), ("S", "P'"), ("P", "Pb"), ("C", "P")]


def amp(y, extra, d, idx, w, step, b):
    B = np.zeros((len(idx), 8)); B[np.arange(len(idx)), b[idx]] = 1.0; B = B[:, B.sum(0) > 0]
    cols = [B] + [e[idx] for e in extra] + ([(d["mass"][idx] < 10) - 0.5] if step else []) + [SLOPE*d["age"][idx]]
    X = np.column_stack(cols); XW = X.T*w[idx]
    return np.linalg.lstsq(XW@X, XW@y[idx], rcond=None)[0][-1]


def chain(d, sel, weights, label, out):
    idx0 = np.where(sel)[0]; n = len(idx0); e = np.quantile(d["z"][idx0], np.linspace(0, 1, 9)); b = np.clip(np.searchsorted(e, d["z"], side="right") - 1, 0, 7)
    w = 1/(d["shr"]**2 + 0.01) if weights == "claim" else np.ones(len(d["z"])); S = sets(d); rng = np.random.default_rng(SEED)
    boots = [idx0[rng.integers(0, n, n)] for _ in range(400)]; res = {}
    for step in (False, True):
        A = {k: amp(y, ex, d, idx0, w, step, b) for k, (y, ex) in S.items()}
        Bt = {k: np.array([amp(y, ex, d, i, w, step, b) for i in boots]) for k, (y, ex) in S.items()}
        tag = "step" if step else "nostep"; res[tag] = dict(A={k: [float(A[k]), float(Bt[k].std(ddof=1))] for k in S}, steps={})
        log(f"{label}, n {n}, {'mass step free' if step else 'no mass step'}: " + "  ".join(f"{k} {A[k]:+.3f} +- {Bt[k].std(ddof=1):.3f}" for k in S))
        for a, c in STEPS:
            dv = A[a] - A[c]; sd = float((Bt[a] - Bt[c]).std(ddof=1)); res[tag]["steps"][f"{a}->{c}"] = dict(change=float(dv), sd=sd, sigma=float(dv/sd), carries=bool(abs(dv) >= 2*sd))
            log(f"      step {a:2s} -> {c:2s}: change {dv:+.3f} +- {sd:.3f} ({dv/sd:+.1f} sigma)  {'CARRIES SLOPE' if abs(dv) >= 2*sd else 'does not'}")
    out[label] = res
    return b, w, S, boots, idx0


def main():
    d = assemble(); out = dict(n=len(d["age"]), n_table1=int((d["tab"] == 1).sum()), n_table2=int((d["tab"] == 2).sum()))
    log(f"AGB6 chain: {out['n']} supernovae in Pantheon+ and in one of the claim's tables with every quantity present ({out['n_table1']} from table 1, {out['n_table2']} from table 2 only)")
    allsel = np.ones(len(d["age"]), bool)
    b, w, S, boots, idx0 = chain(d, allsel, "claim", "all", out)
    chain(d, d["tab"] == 1, "claim", "table 1", out); chain(d, d["tab"] == 2, "claim", "table 2 only", out); chain(d, allsel, "equal", "all, equal weights", out)
    # per-supernova differences of the two light-curve fits against host age
    log("Pantheon+ fit minus the survey's SALT2 fit, per supernova, against host age (line inside the 8 redshift bins; per Gyr):")
    def line(v, idx):
        B = np.zeros((len(idx), 8)); B[np.arange(len(idx)), b[idx]] = 1.0; B = B[:, B.sum(0) > 0]; X = np.column_stack([B, d["age"][idx]])
        return np.linalg.lstsq(X, v[idx], rcond=None)[0][-1]
    out["fit_differences"] = {}
    for nm, v in (("stretch x1", d["x1p"] - d["x1s"]), ("colour c", d["cp"] - d["cs"]), ("peak magnitude", d["mB"] - (-2.5*np.log10(d["x0s"]) + 10.635)),
                  ("modulus at fixed coefficients (P' - S)", S["P'"][0] - S["S"][0]), ("MLCS2k2 minus SALT2 modulus of the survey (M - S)", S["M"][0] - S["S"][0])):
        s0 = line(v, idx0); sd = float(np.std([line(v, i) for i in boots], ddof=1)); out["fit_differences"][nm] = dict(mean=float(v.mean()), rms=float(v.std()), slope_per_gyr=float(s0), sd=sd)
        log(f"   {nm:52s} mean {v.mean():+.4f}  rms {v.std():.4f}  slope {s0:+.5f} +- {sd:.5f} per Gyr ({s0/sd:+.1f} sigma)" + (f"  = {s0/SLOPE:+.3f} in units of the published slope" if "modulus" in nm or "magnitude" in nm else ""))
    # the largest disagreements between C and P
    def resid(y, ex):
        B = np.zeros((len(y), 8)); B[np.arange(len(y)), b] = 1.0; X = np.column_stack([B] + ex); XW = X.T*w; return y - X@np.linalg.lstsq(XW@X, XW@y, rcond=None)[0]
    rC, rP = resid(*S["C"]), resid(*S["P"]); dd = rC - rP; top = np.argsort(-np.abs(dd))[:5]
    log("the five supernovae where the claim's residual and the Pantheon+ residual differ most:")
    for i in top: log(f"   SDSS id {d['cid'][i]:>6s}  z {d['z'][i]:.3f}  host age {d['age'][i]:.1f} Gyr  claim {rC[i]:+.3f}  Pantheon+ {rP[i]:+.3f}  difference {dd[i]:+.3f}  (table {d['tab'][i]})")
    keep = np.ones(len(dd), bool); keep[top] = False; i5 = np.where(keep)[0]
    out["without_top5"] = {k: float(amp(S[k][0], S[k][1], d, i5, w, False, b)) for k in ("C", "P")}; out["top5"] = [dict(cid=str(d["cid"][i]), age=float(d["age"][i]), diff=float(dd[i])) for i in top]
    log(f"   without those five (no mass step): C {out['without_top5']['C']:+.3f}, P {out['without_top5']['P']:+.3f}; rms of the difference over all {dd.std():.3f} mag")
    json.dump(out, open(os.path.join(HERE, "agb6_chain.json"), "w"), indent=1, default=float); log("wrote agb6_chain.json")


if __name__ == "__main__":
    main()
