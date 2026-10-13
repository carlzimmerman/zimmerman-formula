"""CFG687 (criteria 12cb826e8): raw KiDS-1000 shear stacked around eRASS1 clusters vs the law from their X-ray gas.
Reuses CFG686 RUN3's setup verbatim (estimator esd(), BAO-raw distances, nu_mono/A0, sigma_proj, SIS self-test) by exec.
argv[1] = cached KiDS columns. MUTATE=M1 (cross shear), M2 (random-minus-random)."""
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); MUT = os.environ.get("MUTATE", "")
SRC = os.path.join(LANES, "CFG686_cluster_shear_vs_law", "cfg686_shear.py")
os.environ.pop("MUTATE", None); g = {"__file__": SRC, "__name__": "cfg686"}; sys.argv = [SRC, sys.argv[1]]
exec(open(SRC).read().split("# ---- measure ----")[0], g)                    # prints CFG686 cluster count + SIS self-test
esd, DM, nu_mono, A0, RC, MPC, G, MSUN, KG, sigma_proj = (g[k] for k in ("esd", "DM", "nu_mono", "A0", "RC", "MPC", "G", "MSUN", "KG_PER_MSUN_PC2", "sigma_proj"))
RGRID = g["RGRID"]
# ---- eRASS1 clusters ----
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(LANES, "..", "..", "_external_data", "cfg687_inputs", "erass1_main.tsv"))]
CL = []
for r in rows:
    try: ra, de, z, mg, R5 = float(r[1]), float(r[2]), float(r[3]), float(r[5]), float(r[8])
    except Exception: continue
    inN = 125 <= ra <= 240 and -6 <= de <= 5; inS = (ra >= 325 or ra <= 60) and -37 <= de <= -25
    if (inN or inS) and 0.05 <= z <= 0.5 and mg > 0 and R5 > 0: CL.append(dict(name=r[0].strip(), ra=ra, dec=de, z=z, Mgas500=mg*1e11, R500=R5/1e3))
print(f"eRASS1 candidates in KiDS boxes: {len(CL)}", flush=True)
def law(cl, a0, beta=2/3, rcf=0.15, fs=0.20):
    r = RGRID; rc = rcf*cl["R500"]; shape = (1 + (r/rc)**2)**(-1.5*beta); shape[r > 3.0] = 0
    dm = 4*np.pi*(r*MPC)**2*shape; M = np.r_[0, np.cumsum(0.5*(dm[1:] + dm[:-1])*np.diff(r*MPC))]
    Mg = M*(cl["Mgas500"]*MSUN/np.interp(cl["R500"], r, M)); Mb = Mg*(1 + fs); gb = G*Mb/(r*MPC)**2
    gL = gb*nu_mono(gb/a0) if a0 > 0 else gb; ML = gL*(r*MPC)**2/G; rhoL = np.gradient(ML, r*MPC)/(4*np.pi*(r*MPC)**2)
    Sig = np.array([sigma_proj(rhoL, r, R) for R in RC])
    M2 = np.array([np.interp(R, r, ML) + np.trapz(4*np.pi*(r[r > R]*MPC)**2*rhoL[r > R]*(1 - np.sqrt(1 - (R/r[r > R])**2)), r[r > R]*MPC) for R in RC])
    return (M2/(np.pi*(RC*MPC)**2) - Sig)/KG
BR = [(b, rc, fs) for b in (0.6, 2/3, 0.8) for rc in (0.10, 0.15, 0.20) for fs in (0.10, 0.20, 0.30)]
rng = np.random.default_rng(687); out = []
for i, cl in enumerate(CL):
    m = esd(cl["ra"], cl["dec"], cl["z"], cross=(MUT == "M1"))
    if m is None or m[3] < 200: continue
    rnd = []
    for _ in range(10):
        a = rng.uniform(0, 2*np.pi); s = rng.uniform(1, 3)
        rr = esd((cl["ra"] + s*np.cos(a)/np.cos(np.radians(cl["dec"]))) % 360, cl["dec"] + s*np.sin(a), cl["z"], cross=(MUT == "M1"))
        if rr is not None and rr[3] > 0.5*m[3]: rnd.append(rr[0])
        if len(rnd) >= 6: break
    if len(rnd) < 5: continue
    rnd = np.nan_to_num(np.array(rnd))
    d = (rnd[:3].mean(0) - rnd[3:].mean(0)) if MUT == "M2" else np.nan_to_num(m[0]) - rnd.mean(0)
    pred = {f"{f}|b{b:.2f}|rc{rc:.2f}|f{fs:.2f}": law(cl, a0, b, rc, fs).tolist() for f, a0 in A0.items() for (b, rc, fs) in BR}
    out.append(dict(cl, n_src=m[3], dsig=d.tolist(), err=np.nan_to_num(m[1], nan=1e9).tolist(), pred=pred, newton=law(cl, 0.0).tolist()))
    if len(out) % 50 == 0: print(f"  measured {len(out)} clusters (of {i+1} tried)", flush=True)
print(f"clusters used: {len(out)}", flush=True)
# ---- stack, jackknife over 30 RA-ordered equal-count patches ----
D = np.array([o["dsig"] for o in out]); E = np.array([o["err"] for o in out]); W = np.where(E > 0, 1/E**2, 0)
order = np.argsort([o["ra"] for o in out]); patch = np.empty(len(out), int); patch[order] = np.arange(len(out))*30//len(out)
BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}
def A_of(sel, P):
    return {b: (W[sel][:, j]*D[sel][:, j]).sum()/(W[sel][:, j]*P[sel][:, j]).sum() for b, j in BANDS.items()}
def jk(fun):
    full = fun(np.ones(len(out), bool)); reps = [fun(patch != p) for p in range(30)]
    return {k: (float(full[k]), float(np.sqrt(29/30*np.sum((np.array([r[k] for r in reps]) - np.mean([r[k] for r in reps]))**2)))) for k in full}
res = {"mutate": MUT, "n": len(out)}; summ = {}
for key in list(out[0]["pred"].keys()) + ["newton"]:
    P = np.array([o["pred"][key] if key != "newton" else o["newton"] for o in out]); summ[key] = jk(lambda s, P=P: A_of(s, P))
res["A"] = summ
stack = jk(lambda s: {f"b{j}": (W[s][:, j]*D[s][:, j]).sum()/W[s][:, j].sum() for j in range(8)})
res["stack"] = stack
print("\nSTACK ΔΣ (M☉/pc²) R =", np.round(RC, 2).tolist()); print("  ", [f"{stack[f'b{j}'][0]:.1f}±{stack[f'b{j}'][1]:.1f}" for j in range(8)])
PK = "canonical|b0.67|rc0.15|f0.20"; PA = "alt|b0.67|rc0.15|f0.20"
for k in (PK, PA, "newton"): print(f"  A[{k}]: " + "  ".join(f"{b} {v[0]:.2f}±{v[1]:.2f}" for b, v in summ[k].items()))
def verdict(k):
    z = {b: (summ[k][b][0] - 1)/summ[k][b][1] for b in ("MID", "OUTER")}
    if min(z.values()) <= -2: return "LAW OVERPREDICTS"
    if z["OUTER"] >= 2: return "EXTENDED EXCESS"
    if z["MID"] >= 2: return "CORE EXCESS"
    return "LAW SUFFICES"
res["T1"] = {f: verdict(f"{f}|b0.67|rc0.15|f0.20") for f in A0}
br = [verdict(k) for k in summ if k != "newton"]; res["T1_brackets"] = {v: br.count(v) for v in set(br)}
print("\nT1 VERDICT:", res["T1"], " brackets:", res["T1_brackets"])
# ---- T2 mass scaling across Mgas500 terciles ----
mg = np.array([o["Mgas500"] for o in out]); q = np.quantile(mg, [0, 1/3, 2/3, 1]); tid = np.clip(np.digitize(mg, q[1:-1]), 0, 2)
def outer_stack(sel, arr):
    j = BANDS["OUTER"]; return (W[sel][:, j]*arr[sel][:, j]).sum()/W[sel][:, j].sum()
def slope(sel, arr):
    xs, ys = [], []
    for t in range(3):
        s = sel & (tid == t); v = outer_stack(s, arr)
        if v <= 0: return np.nan
        xs.append(np.log10(np.median(mg[s]))); ys.append(np.log10(v))
    return np.polyfit(xs, ys, 1)[0]
PL = np.array([o["pred"][PK] for o in out]); PN = np.array([o["newton"] for o in out])
s_obs = jk(lambda s: {"s": slope(s, D)}); s_law = slope(np.ones(len(out), bool), PL); s_N = slope(np.ones(len(out), bool), PN)
so, se = s_obs["s"]
T2 = "FOLLOWS THE LAW" if (abs(so - s_law) < 2*se and abs(so - s_N) >= 2*se) else ("FOLLOWS NEWTON" if (abs(so - s_N) < 2*se and abs(so - s_law) >= 2*se) else "NOT DECIDED")
res["T2"] = dict(s_obs=so, s_err=se, s_law=float(s_law), s_newton=float(s_N), tercile_Mgas_median=[float(np.median(mg[tid == t])) for t in range(3)], verdict=T2)
print(f"T2 mass scaling: s_obs = {so:.2f} ± {se:.2f}   s_law = {s_law:.2f}   s_Newton = {s_N:.2f}   → {T2}")
c686 = json.load(open(os.path.join(LANES, "CFG686_cluster_shear_vs_law", "cfg686_results.json")))["A"]["canonical|b+0.0|f0.20"]["OUTER"] if not MUT else None
if c686: z = (summ[PK]["OUTER"][0] - c686[0])/np.hypot(summ[PK]["OUTER"][1], c686[1]); res["consistency_CFG686"] = float(z); print(f"Consistency with CFG686 OUTER: {z:+.2f}σ")
if not MUT:   # per-cluster arrays for the post-hoc T2 diagnostic (cfg687_posthoc_t2.py)
    np.savez_compressed(os.path.join(HERE, "cfg687_percluster.npz"), D=D, E=E, PL=PL, PN=PN, mg=mg, z=np.array([o["z"] for o in out]),
                        ra=np.array([o["ra"] for o in out]), dec=np.array([o["dec"] for o in out]), R500=np.array([o["R500"] for o in out]))
json.dump(res, open(os.path.join(HERE, "cfg687_results" + (f"_MUTATE_{MUT}" if MUT else "") + ".json"), "w"), indent=1, default=float)
