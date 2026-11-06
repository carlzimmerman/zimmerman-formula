#!/usr/bin/env python3
"""QX7 iter_1 (criteria d9d76d87a2): stiffness switched by potential depth read through AC2q's X = s^2/(2N^2).
    python3 qx7_iter1.py            # graded: qx7_iter1.json / .out
    python3 qx7_iter1.py --mutate   # MUTATE A (t = 1e-7) and B (flipped switch): qx7_iter1_MUTATE.*
Depth key at a galaxy = local depth (QX5 key a) + large-scale Phi (Gaussian, sigma from CLASS linear P(k) of QX3 iter2's
worst-corner background, A_s rescaled to its fitted value). kappa = 1/2 FITTED; not theory closed. 1 thread."""
import os, sys, json, math
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.stats import norm
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../../.."))
MUT = "--mutate" in sys.argv; TAG = "qx7_iter1_MUTATE" if MUT else "qx7_iter1"; OUT = []
def P(s): print(s, flush=True); OUT.append(s)

# ---- QX5 machinery (samples, key a), reused by executing its source up to its class loop (as QX6 does) ----
Q5 = os.path.join(REPO, "closure_2026_11_06", "QX5_cluster_terms", "qx5.py")
src = open(Q5).read(); cut = src.index("DIR = dict(")
argv0, sys.argv = sys.argv, [Q5]; os.environ.pop("QX5_GCUT", None)
NS = {"__file__": Q5, "__name__": "qx5_reused"}
exec(compile(src[:cut], Q5, "exec"), NS); sys.argv = argv0
G, C, A0, SP, tables, phi_from = (NS[k] for k in ("G", "C", "A0", "SP", "tables", "phi_from"))

# ---- background and sigma_Phi (QX3 iter2 helpers) ----
sys.path.insert(0, os.path.join(REPO, "closure_2026_11_06", "QX3_cmb_growth", "iter2_kq_dust"))
cwd = os.getcwd(); os.chdir(os.path.join(REPO, "closure_2026_11_06", "QX3_cmb_growth", "iter2_kq_dust"))
import iter2 as I2
os.chdir(cwd)
it2 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX3_cmb_growth", "iter2_kq_dust", "iter2.json")))
W = max(it2["G1"], key=lambda r: r["chi2_min"])
ob, od, H0, ns, As = W["omega_b"], W["omega_d_best"], W["H0"], W["n_s"], W["A_s_implied"]
h = H0 / 100; Om = (ob + od) / h ** 2; CKMS = 2.99792458e5; H0c = H0 / CKMS     # 1/Mpc
M = I2.run_class(ob, od, H0, ns, pk=True)
def sigma_phi(kmin, kmax=10.0, n=4000):
    lk = np.linspace(math.log(kmin), math.log(kmax), n); k = np.exp(lk)
    Pk = np.array([M.pk(float(x), 0.0) for x in k]) * (As / I2.AS0)       # Mpc^3, rescaled to the fitted amplitude
    D2d = k ** 3 * Pk / (2 * np.pi ** 2); D2phi = (1.5 * Om * H0c ** 2) ** 2 * D2d / k ** 4
    return float(math.sqrt(np.trapz(D2phi, lk))), float(math.sqrt(np.interp(math.log(0.01), lk, D2phi)))
SIG = {}
for lab_, km in (("kmin_H0", H0c), ("kmin_10H0", 10 * H0c)):
    s, per = sigma_phi(km); SIG[lab_] = s
P(f"QX7 iter1 {TAG}: background omega_b {ob} omega_d {od:.4f} H0 {H0} n_s {ns} A_s {As:.3e}; Omega_m {Om:.3f}")
P(f"  sigma_Phi(z=0): k_min = H0/c -> {SIG['kmin_H0']:.3e}; k_min = 10 H0/c -> {SIG['kmin_10H0']:.3e}; Delta_Phi per ln k at k=0.01/Mpc {per:.3e}")
# known answer: Poisson normalisation check, Delta^2_Phi = (9/25) Delta^2_R T^2 g^2 on large scales; report ratio at k = 1e-3
kk = 1e-3; Pk = M.pk(kk, 0.0) * (As / I2.AS0); D2phi = (1.5 * Om * H0c ** 2) ** 2 * kk ** 3 * Pk / (2 * np.pi ** 2) / kk ** 4
D2R = As * (kk / 0.05) ** (ns - 1); ratio = D2phi / ((9 / 25) * D2R)
P(f"  K1 (large-scale Phi vs (3/5)^2 Delta_R^2): ratio {ratio:.3f} at k = 1e-3/Mpc (expected T^2 g^2 ~ 0.5-0.8 with the late vacuum term)")

RES = dict(tag=TAG, criteria="d9d76d87a2", background=dict(omega_b=ob, omega_d=od, H0=H0, n_s=ns, A_s=As),
           sigma_phi=SIG, K1_ratio=float(ratio), note="kappa = 1/2 FITTED; not theory closed")

def sparc_keys(a0):
    ks = []
    for g in SP:
        r, V = g["R"], g["V"]; gobs = V ** 2 / r; Mb_last = g["vb2"][-1] * r[-1] / G
        ks.append(max(phi_from(r, gobs, i, Mb_last, a0) / C ** 2 for i in range(len(r))))
    return np.array(ks)

def cold_frac(t, kloc, sig, shape, flipped=False):
    # x = -Phi_LSS ~ N(0, sig); depth = kloc + x (wells positive)
    if shape == "one":
        p = 1 - norm.cdf((t - kloc) / sig)
    else:
        p = 1 - (norm.cdf((t - kloc) / sig) - norm.cdf((-t - kloc) / sig))
    if flipped: p = 1 - p
    return float(p.mean())

for f, a0 in A0.items():
    TX = tables("a", a0, False)["X"]; kx = np.array([x["k"] for x in TX]); kgal = sparc_keys(a0)
    tC1 = float(kx.min()); RES[f] = dict(XCOP_key_min=tC1, XCOP_key_max=float(kx.max()), SPARC_key_max=float(kgal.max()),
                                         SPARC_key_median=float(np.median(kgal)), n_SPARC=int(len(kgal)), cases={})
    P(f"[{f}] X-COP keys {kx.min():.3e}-{kx.max():.3e} (C1: t <= {tC1:.3e}); SPARC per-galaxy max key median {np.median(kgal):.3e}, max {kgal.max():.3e} ({len(kgal)} galaxies)")
    win_all = True
    for kl, sig in SIG.items():
        for shape in ("one", "two"):
            if not MUT:
                fr = cold_frac(tC1, kgal, sig, shape); ok = fr <= 0.05
                # largest cold fraction-safe threshold: smallest t with fraction <= 0.05
                ts = np.geomspace(1e-7, 1e-2, 2001); frs = np.array([cold_frac(t, kgal, sig, shape) for t in ts])
                tmin = float(ts[np.argmax(frs <= 0.05)]) if (frs <= 0.05).any() else None
                RES[f]["cases"][f"{kl}|{shape}"] = dict(cold_fraction_at_tC1=fr, C2_pass_at_tC1=bool(ok), t_needed_for_C2=tmin, window=bool(ok))
                P(f"   {kl:10s} {shape}-sided: galaxies cold at t = t_C1: {fr:.3f} (line 0.05) -> {'window' if ok else 'NO window'}; C2 needs t >= {tmin:.3e} vs t_C1 {tC1:.3e} ({(tmin or float('nan')) / tC1:.2f}x)")
                if kl == "kmin_10H0" and shape == "one": RES[f]["generous_window"] = bool(ok)
                win_all &= ok
            else:
                frA = cold_frac(1e-7, kgal, sig, shape); biteA = frA > 0.5
                # MUTATE B: flipped switch; C1 flipped = all X-COP cold = all X-COP keys < t (deterministic part)
                ts = np.geomspace(1e-7, 1e-3, 401); c1f = [bool((kx < t).all()) for t in ts]
                biteB = not any(c1f)
                c2f_at_c1 = [cold_frac(t, kgal, sig, shape, flipped=True) for t, c in zip(ts, c1f) if c]
                RES[f]["cases"][f"{kl}|{shape}"] = dict(A_cold_fraction_t1e7=frA, A_bites=bool(biteA), B_C1_flipped_satisfiable=bool(any(c1f)),
                                                         B_bites_as_frozen=bool(biteB), B_window_flipped=bool(any(x <= 0.05 for x in c2f_at_c1)))
                P(f"   {kl:10s} {shape}: MUTATE A cold fraction at t=1e-7 {frA:.3f} -> {'BITES' if biteA else 'NO BITE'}; "
                  f"MUTATE B (flipped): C1 satisfiable {any(c1f)} -> {'BITES' if biteB else 'DOES NOT BITE as frozen'}; flipped full window {any(x <= 0.05 for x in c2f_at_c1)}")
    if not MUT:
        # frozen window definition: a t satisfying C1 and C2 for each k_min and each switch shape
        RES[f]["window_all_cases"] = bool(win_all)
        RES[f]["label"] = "PASS this stage (window)" if win_all else ("FAIL (no window: large-scale Phi dominates the depth key)"
                          + ("; generous case alone has a knife-edge window" if RES[f]["generous_window"] else ""))
        P(f"   LABEL [{f}]: {RES[f]['label']}")

# white dwarf / neutron star capture bound (reported): mass within the star's own radius at the cosmic mean dust density
rho_d0 = od / h ** 2 * 3 * (H0 * 1e3 / 3.0857e22) ** 2 / (8 * math.pi * G)
for nm, R_m, Mst in (("white dwarf", 7e6, 0.6), ("neutron star", 1.2e4, 1.4)):
    md = 4 / 3 * math.pi * R_m ** 3 * rho_d0 / 1.989e30
    RES.setdefault("compact", {})[nm] = dict(M_dust_within_R_Msun=md, fraction=md / Mst)
    P(f"  {nm}: dust within R at rho_d0 {rho_d0:.2e} kg/m^3 = {md:.2e} Msun ({md / Mst:.1e} of the star): not graded")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
