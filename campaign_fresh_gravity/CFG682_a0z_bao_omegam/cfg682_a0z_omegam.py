"""CFG682 (criteria 2de123ae6): a0(z*)/a0(0) + raw BAO (+SN shape) -> Omega_m without the CMB, under the owner's tracking law
a0 ∝ sqrt(rho_DE). Reuses CFG681's data, X(z) model and chi2 functions verbatim. MUTATE=1: BAO replaced by its own X≡1 fit."""
import os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); MUT = os.environ.get("MUTATE") == "1"
SRC = os.path.join(HERE, "..", "CFG681_bao_raw_geometry", "cfg681_bao.py")
g = {"__file__": SRC, "__name__": "cfg681"}; os.environ.pop("MUTATE", None)
exec(open(SRC).read().split("def sig_equiv")[0], g)                      # data + Efun/Igrid/bao_chi2/sn_chi2/fit (no tests run)
NODES, bao_chi2, sn_chi2, fit, Igrid, Efun, zg = g["NODES"], g["bao_chi2"], g["sn_chi2"], g["fit"], g["Igrid"], g["Efun"], g["zg"]
data = None
if MUT:
    b = fit(["bao"], fixX=True); om = b.x[0]; _, q = bao_chi2(om, np.ones(5)); I = Igrid(om, np.ones(5))
    data = [(nm, z, q*np.interp(z, zg, I), sdm, q/Efun(om, np.ones(5), np.array([z]))[0], sdh, r) for (nm, z, dm, sdm, dh, sdh, r) in g["ANISO"]]
    zb_, dv, sdv = g["BGS"]; g["BGS"] = (zb_, q*(zb_*np.interp(zb_, zg, I)**2/Efun(om, np.ones(5), np.array([zb_]))[0])**(1/3), sdv)
    MUT_OM = float(om)
OMS = np.round(np.arange(0.24, 0.36 + 1e-9, 0.0025), 4); ZS = [1.0, 1.2, 1.5, 2.33]
def wvec(z): return np.array([np.interp(z, NODES, np.r_[0.0, np.eye(5)[i]]) for i in range(5)])   # X(z) = 1*w0 + sum w_i X_i
def chi_fixed(which, om, xn):
    c = 0.0
    if "bao" in which: c += bao_chi2(om, xn, data)[0]
    if "sn" in which: c += sn_chi2(om, xn)
    return c
def hessian(fun, x, h=0.01):
    n = len(x); H = np.zeros((n, n)); f0 = fun(x)
    for i in range(n):
        for j in range(i, n):
            e_i, e_j = np.eye(n)[i]*h, np.eye(n)[j]*h
            H[i, j] = H[j, i] = (fun(x+e_i+e_j) - fun(x+e_i-e_j) - fun(x-e_i+e_j) + fun(x-e_i-e_j))/(4*h*h)
    return H
res = {"mutate": MUT}
for tag, which in [("BAO", ["bao"]), ("BAO+SN", ["bao", "sn"])]:
    rows = []; prev = None
    for om in OMS:
        cands = [fit(which, om_fix=om, data=data, start=s) for s in ([prev] if prev is not None else []) + [np.ones(5), np.linspace(1, 1.5, 5)]]
        b = min(cands, key=lambda r: r.fun); xn = b.x; prev = xn
        H = hessian(lambda x: chi_fixed(which, om, x), xn); cov = 2*np.linalg.pinv(H)
        xs = {str(z): (1.0*(z == 0) + float(np.interp(z, NODES, np.r_[1.0, xn])), float(np.sqrt(max(wvec(z)@cov@wvec(z), 0)))) for z in ZS}
        rows.append(dict(om=float(om), chi2=float(b.fun), X=xs, nodes=xn.tolist()))
    chi = np.array([r["chi2"] for r in rows]); res[tag] = dict(rows=rows)
    print(f"\n=== {tag}  MUTATE={MUT}   χ² range over Ωm grid: {chi.min():.2f} .. {chi.max():.2f}")
    for r in rows[::4]:
        print(f"  Ωm={r['om']:.4f} χ²={r['chi2']:.2f}  " + "  ".join(f"√X({z})={np.sqrt(max(r['X'][z][0], 0)):.3f}(σX {r['X'][z][1]:.2f})" for z in ["1.0", "1.5", "2.33"]))
    # ---- P2 inversion ----
    inv = {}
    for z in ZS:
        X = np.array([r["X"][str(z)][0] for r in rows]); sX = np.array([r["X"][str(z)][1] for r in rows])
        lsq = np.where(X > 0, 0.5*np.log10(np.maximum(X, 1e-12)), -np.inf); slsq = np.where(X > 0, 0.5*sX/(np.maximum(X, 1e-12)*np.log(10)), np.inf)
        prior = np.exp(-0.5*(chi - chi.min()))
        out = {}
        for e in [0.02, 0.03, 0.05, 0.075, 0.10, 0.15, 0.20, 0.30]:
            s = np.sqrt(e**2 + slsq**2); L = np.where(np.isfinite(lsq), np.exp(-0.5*(lsq/s)**2)/s, 0.0)   # r = 1 (flat a0)
            P = prior*L
            if P.sum() == 0: out[str(e)] = None; continue
            P = P/P.sum(); m = (P*OMS).sum(); sd = np.sqrt((P*(OMS - m)**2).sum()); cdf = np.cumsum(P)
            out[str(e)] = dict(mean=float(m), sd=float(sd), lo68=float(np.interp(0.16, cdf, OMS)), hi68=float(np.interp(0.84, cdf, OMS)),
                              z_planck=float((m - 0.3153)/np.hypot(sd, 0.0073)))
        es = [float(k) for k, v in out.items() if v]; sds = [out[str(k)]["sd"] for k in es]
        estar = float(np.interp(0.0073, sds, es)) if min(sds) <= 0.0073 <= max(sds) else (None if min(sds) > 0.0073 else ">0.30")
        inv[str(z)] = dict(by_e=out, e_star=estar)
        print(f"  z*={z}: flat-a0 Ωm by e: " + "  ".join(f"e={k}: {v['mean']:.4f}±{v['sd']:.4f}" for k, v in out.items() if v) + f"   e* (σ=0.0073) = {estar}")
    res[tag]["inversion_flat_a0"] = inv
# ---- P3 record samples (effective e from committed numbers; see README) ----
P3 = {"KURVS-CDFS z~1.5 (CFG140/141/160; gas unmeasured, pressure-support model sets the verdict)": (1.5, 0.30, "lower bound on e"),
      "z~1.2 multi-tracer gas set (CFG224: gas K 0.128 dex, stars ~0.1 dex, deep-MOND leverage 1)": (1.2, float(np.hypot(0.128, 0.10)), "deep-MOND best case"),
      "RC100 / CRISTAL (CFG223: g_bar/a0 1.1-4.4, leverage 2.5-4.8, 0.05 dex baryons)": (2.33, 0.05*2.5, "optimistic: 0.05 dex baryons; nearest node z 2.33")}
res["P3"] = {}
print("\n=== P3 record samples (BAO+SN inversion, flat a0)")
for name, (z, e, note) in P3.items():
    inv = res["BAO+SN"]["inversion_flat_a0"][str(z)]["by_e"]; ks = sorted(float(k) for k, v in inv.items() if v)
    sd = float(np.interp(e, ks, [inv[str(k)]["sd"] for k in ks])); estar = res["BAO+SN"]["inversion_flat_a0"][str(z)]["e_star"]
    grade = "REACHES CMB PRECISION" if (isinstance(estar, float) and e <= estar) else ("INFORMATIVE" if sd <= 0.03 else "NOT INFORMATIVE")
    res["P3"][name] = dict(z=z, e=e, note=note, sigma_om=sd, grade=grade); print(f"  {name}: e≈{e:.3f} dex ({note}) → σ(Ωm) ≈ {sd:.4f} → {grade}")
if MUT: print(f"\nMUTATE check: X≡1 mock Ωm = {MUT_OM:.4f}; flat-a0 inversion (BAO, z*=2.33, e=0.02) = {res['BAO']['inversion_flat_a0']['2.33']['by_e']['0.02']['mean']:.4f}")
json.dump(res, open(os.path.join(HERE, "cfg682_results" + ("_MUTATE" if MUT else "") + ".json"), "w"), indent=1)
