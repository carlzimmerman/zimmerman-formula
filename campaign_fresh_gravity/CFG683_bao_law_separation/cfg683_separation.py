"""CFG683 (criteria 2c54af75e): raw BAO (+SN shape) predictions of both a0(z) laws, CMB-free, and the a0 precision that separates them.
tracking: a0(z)/a0(0) = sqrt X(z); rival: a0(z)/a0(0) = E(z). CFG681 data/model verbatim; CFG682 grid. MUTATE=1: CFG681 M1 mock."""
import os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); MUT = os.environ.get("MUTATE") == "1"
SRC = os.path.join(HERE, "..", "CFG681_bao_raw_geometry", "cfg681_bao.py"); os.environ.pop("MUTATE", None)
g = {"__file__": SRC, "__name__": "cfg681"}; exec(open(SRC).read().split("def sig_equiv")[0], g)
NODES, bao_chi2, sn_chi2, fit, Igrid, Efun, zg, OMR = g["NODES"], g["bao_chi2"], g["sn_chi2"], g["fit"], g["Igrid"], g["Efun"], g["zg"], g["OMR"]
data = None
if MUT:
    b = fit(["bao"], fixX=True); om0 = b.x[0]; _, q = bao_chi2(om0, np.ones(5)); I = Igrid(om0, np.ones(5))
    data = [(nm, z, q*np.interp(z, zg, I), sdm, q/Efun(om0, np.ones(5), np.array([z]))[0], sdh, r) for (nm, z, dm, sdm, dh, sdh, r) in g["ANISO"]]
    zb_, dv, sdv = g["BGS"]; g["BGS"] = (zb_, q*(zb_*np.interp(zb_, zg, I)**2/Efun(om0, np.ones(5), np.array([zb_]))[0])**(1/3), sdv)
r682 = json.load(open(os.path.join(HERE, "..", "CFG682_a0z_bao_omegam", "cfg682_results" + ("_MUTATE" if MUT else "") + ".json")))
ZS = [1.0, 1.2, 1.5, 2.33]; L10 = np.log(10)
def wvec(z): return np.array([np.interp(z, NODES, np.r_[0.0, np.eye(5)[i]]) for i in range(5)])
def chi_fixed(which, om, xn):
    return (bao_chi2(om, xn, data)[0] if "bao" in which else 0) + (sn_chi2(om, xn) if "sn" in which else 0)
def hessian(fun, x, h=0.01):
    n = len(x); H = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            ei, ej = np.eye(n)[i]*h, np.eye(n)[j]*h
            H[i, j] = H[j, i] = (fun(x+ei+ej) - fun(x+ei-ej) - fun(x-ei+ej) + fun(x-ei-ej))/(4*h*h)
    return H
res = {"mutate": MUT}
for tag, which in [("BAO+SN", ["bao", "sn"]), ("BAO", ["bao"])]:
    rows = r682[tag]["rows"]; chi = np.array([r["chi2"] for r in rows]); keep = chi <= chi.min() + 1.0
    pred = {str(z): dict(E=[], X=[]) for z in ZS}
    for r, k in zip(rows, keep):
        if not k: continue
        om, xn = r["om"], np.array(r["nodes"]); cov = 2*np.linalg.pinv(hessian(lambda x: chi_fixed(which, om, x), xn))
        for z in ZS:
            w = wvec(z); X = float(np.interp(z, NODES, np.r_[1.0, xn])); sX = float(np.sqrt(max(w@cov@w, 0)))
            E = float(Efun(om, xn, np.array([z]))[0]); sE = (1 - om - OMR)*sX/(2*E)           # dE/dX(z) at fixed Ω_m
            pred[str(z)]["E"].append((np.log10(E), sE/(E*L10))); pred[str(z)]["X"].append((0.5*np.log10(X) if X > 0 else -np.inf, 0.5*sX/(X*L10) if X > 0 else np.inf, X, sX))
    out = {}
    print(f"\n=== {tag}  MUTATE={MUT}  ({keep.sum()} Ωm grid points within Δχ² ≤ 1: {rows[np.argmax(keep)]['om']:.4f}–{rows[len(keep)-1-np.argmax(keep[::-1])]['om']:.4f})")
    for z in ZS:
        E = np.array(pred[str(z)]["E"]); Xr = pred[str(z)]["X"]
        Ehi = (E[:, 0] + E[:, 1]).max(); Elo = (E[:, 0] - E[:, 1]).min()
        Xlin_hi = max(x[2] + x[3] for x in Xr); Xlin_lo = min(x[2] - x[3] for x in Xr)
        sq_hi = 0.5*np.log10(Xlin_hi); sq_lo = 0.5*np.log10(Xlin_lo) if Xlin_lo > 0 else -np.inf
        gap = Elo - sq_hi                                     # closest edges (dex); rival above tracking
        sE = float(np.median(E[:, 1])); sXl = float(np.median([x[1] for x in Xr if np.isfinite(x[1])]))
        def S(e): return gap/np.sqrt(e**2 + sE**2 + sXl**2) if gap > 0 else 0.0
        es = np.linspace(0.01, 1.0, 1000); ok = [e for e in es if S(e) >= 3]; e3 = float(max(ok)) if ok else None
        out[str(z)] = dict(rival_E_band=[float(10**Elo), float(10**Ehi)], tracking_band=[float(np.sqrt(max(Xlin_lo, 0))), float(np.sqrt(Xlin_hi))],
                           gap_dex=float(gap), e_3sigma=e3, S_at={str(e): float(S(e)) for e in (0.05, 0.10, 0.125, 0.16, 0.20, 0.30, 0.40, 0.70)})
        print(f"  z*={z}: rival a0∝H(z): {10**Elo:.3f}–{10**Ehi:.3f}   tracking √X: {np.sqrt(max(Xlin_lo,0)):.3f}–{np.sqrt(Xlin_hi):.3f}   "
              f"closest gap {gap:+.3f} dex   e for 3σ: {e3 if e3 is None else round(e3, 3)}   S(e=0.16)={S(0.16):.2f}  S(e=0.30)={S(0.30):.2f}")
    res[tag] = out
if MUT:
    I = Igrid(om0, np.ones(5)); chk = {str(z): float(Efun(om0, np.ones(5), np.array([z]))[0]) for z in ZS}
    print("\nMUTATE: X≡1 fit E(z*) =", {k: round(v, 4) for k, v in chk.items()}, " (rival band must contain these)")
    res["mutate_E_true"] = chk
P3 = {"KURVS-CDFS z~1.5 (gas unmeasured)": (1.5, 0.30), "z~1.2 multi-tracer (deep-MOND best case)": (1.2, 0.162),
      "RC100/CRISTAL optimistic (0.05 dex baryons)": (2.33, 0.125), "RC100/CRISTAL realistic (±0.15 dex baryons)": (2.33, 0.40)}
res["P3"] = {}
print("\n=== P3 (BAO+SN bands)")
for n, (z, e) in P3.items():
    o = res["BAO+SN"][str(z)]; gap = o["gap_dex"]
    sE_s = None
    S = np.interp(e, [0.05, 0.10, 0.125, 0.16, 0.20, 0.30, 0.40, 0.70], [o["S_at"][k] for k in ["0.05", "0.1", "0.125", "0.16", "0.2", "0.3", "0.4", "0.7"]])
    gr = "DECIDES THE FORK" if S >= 3 else ("LEANS" if S >= 2 else "CANNOT")
    res["P3"][n] = dict(z=z, e=e, S=float(S), grade=gr); print(f"  {n}: e={e} dex → S = {S:.2f} → {gr}")
json.dump(res, open(os.path.join(HERE, "cfg683_results" + ("_MUTATE" if MUT else "") + ".json"), "w"), indent=1)
