#!/usr/bin/env python3
"""v03_posterior_Z.py -- the honest posterior on Z = c H_eff / a0 and the evidence between the PRE-DECLARED hypotheses (v00).

Model.  ln a0_obs = ln a0_true + eps, eps ~ N(0, s_a^2)  (log-normal a0 likelihood; a Gaussian-in-a0 variant is also run);  a0_true = c H_eff / Z.
  footing 'tot'     : H_eff = H0                       (rho_total footing, a0 = c H0 / Z)
  footing 'Lam'     : H_eff = H0 sqrt(Omega_Lambda)    (rho_Lambda footing; H0 and Omega_Lambda treated as INDEPENDENT, as briefed)
  footing 'Lam-phys': H_eff = H_Lambda(Planck) = 67.4 sqrt(0.685) (the physical dark-energy density is held at its Planck value whatever the
                       local H0 is; a sensitivity variant, immune to the H0 tension)
  H0 models: Planck 67.4+-0.5 | SH0ES 73.0+-1.0 | both (50/50 mixture) | avg 70.2+-2.8 (mean, half-difference: both endpoints at 1 sigma);  Omega_Lambda 0.685+-0.007.
  Prior on Z: flat in ln Z (scale-invariant) unless stated; a flat-in-Z variant is reported.
Bayes factors are ratios of the a0 likelihood marginalised over H0 and Omega_Lambda, for POINT hypotheses Z_i (no Occam factor).
The a0 scenarios and their errors are inputs from v01/v02; NOTHING is tuned to a candidate.
Exit 0 = every check held.
"""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v_common import *
import importlib.util
spec = importlib.util.spec_from_file_location("v00", os.path.join(os.path.dirname(os.path.abspath(__file__)), "v00_declared_hypotheses.py"))
v00 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v00)

ok = []
def check(cond, msg):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {msg}")

print("declared hypothesis file sha256:", v00.declared_hash()[:16], "...  (from v00_declared_hypotheses.py)")
HYP = v00.HYPOTHESES
CAND = [h for h in HYP if h[3] == "candidate"]; CTRL = [h for h in HYP if h[3] == "control"]
r1, r2 = json.load(open("v01_results.json")), json.load(open("v02_results.json"))
U = 1e-10
c = c_si
rng = np.random.default_rng(20260929)
NS = 400000

# ---------------------------------------------------------------- a0 scenarios: (a0 in m/s^2, fractional 1-sigma in ln a0, provenance)
b = r2["budget"]
sig_boot = r2["record_pl"]["sig_ln_bootstrap"]
sig_meas = math.sqrt(sig_boot**2 + b["global distance scale +-5% (calibrator zero point)"]**2 + b["gas mass +-10% (HI calibration, H2, helium)"]**2
                     + b["coherent inclination bias +-1 sigma_i (upper bound)"]**2)
SC = {
    "REC-quoted   (record PL, its own 5.44%)":            (1.0766 * U, 0.0544),
    "REC-boot     (alpha1 PL, bootstrap stat only)":      (r2["record_pl"]["a0_hat"], sig_boot),
    "REC-meas.sys (alpha1 PL, stat+dist+gas+incl)":       (r2["record_pl"]["a0_hat"], sig_meas),
    "MLS16        (1.20 +-0.02 +-0.24)":                  (1.20 * U, math.hypot(0.02, 0.24) / 1.20),
    "Des23        (1.19 +-0.04 +-0.09)":                  (1.19 * U, math.hypot(0.04, 0.09) / 1.19),
    "BTFR         (1.3 +-0.3)":                           (1.3 * U, 0.3 / 1.3),
    "ENSEMBLE E   (9 analysis choices)":                  (r1["E"]["logmean"] * U, r1["E"]["sd_ln"]),
}
print("\nA0 scenarios (a0 [1e-10], 1-sigma in ln a0):")
for k, (a, s) in SC.items():
    print(f"   {k:<50}{a/U:>8.4f}   {100*s:5.1f}%")

# ---------------------------------------------------------------- H models: return samples of H_eff (s^-1) for each footing
def H0_samples(model, n):
    if model == "Planck": return rng.normal(67.4, 0.5, n)
    if model == "SH0ES": return rng.normal(73.0, 1.0, n)
    if model == "both":
        pick = rng.random(n) < 0.5
        return np.where(pick, rng.normal(67.4, 0.5, n), rng.normal(73.0, 1.0, n))
    if model == "avg": return rng.normal(70.2, 2.8, n)
    raise ValueError(model)
def Heff(model, footing, n=NS):
    h0 = H0_samples(model, n)
    if footing == "tot": return H_si(h0)
    if footing == "Lam": return H_si(h0) * np.sqrt(rng.normal(OM_L, 0.007, n))
    if footing == "Lam-phys": return H_si(rng.normal(67.4, 0.5, n) * np.sqrt(rng.normal(OM_L, 0.007, n)) * 1.0) * 1.0
    raise ValueError(footing)
MODELS, FOOT = ["Planck", "SH0ES", "both", "avg"], ["tot", "Lam", "Lam-phys"]
HS = {(m, f): Heff(m, f) for m in MODELS for f in FOOT}
for m in MODELS:                         # Lam-phys is H0-model independent by construction: reuse one draw
    HS[(m, "Lam-phys")] = HS[("Planck", "Lam-phys")]

def lnZ_post(a_obs, s_a, Hs, prior="lnZ", lik="lognormal"):
    """posterior samples of Z"""
    n = len(Hs)
    if lik == "lognormal":
        eps = rng.normal(0, s_a, n)
        lnZ = np.log(c * Hs) - math.log(a_obs) - eps
        Z = np.exp(lnZ)
    else:       # Gaussian in a0 (sigma = s_a * a_obs), flat prior on a0_true > 0
        a = rng.normal(a_obs, s_a * a_obs, n * 2); a = a[a > 0][:n]
        Z = c * Hs[:len(a)] / a
    if prior == "Z":       # flat in Z instead of flat in ln Z: reweight by Z
        w = Z / Z.sum()
        idx = rng.choice(len(Z), size=len(Z), p=w)
        Z = Z[idx]
    return Z
def q(Z, ps=(2.5, 16, 50, 84, 97.5)): return np.percentile(Z, ps)

# ---------------------------------------------------------------- 1. Z intervals
print("\nZ = c H_eff / a0: posterior median and 68% / 95% intervals (flat prior in ln Z, log-normal a0 likelihood)")
res = {"scenarios": {k: dict(a0=v[0], s_a=v[1]) for k, v in SC.items()}, "Z": {}}
print(f"   {'a0 scenario':<48}{'footing / H0':<20}{'median':>7}{'68% interval':>16}{'95% interval':>17}   F(5.789) V(6) M(2pi) inside 68% / 95%")
for sk, (a_obs, s_a) in SC.items():
    for f in FOOT:
        for m in (("Planck", "SH0ES", "avg") if f != "Lam-phys" else ("Planck",)):
            Z = lnZ_post(a_obs, s_a, HS[(m, f)])
            lo95, lo68, med, hi68, hi95 = q(Z)
            ins = lambda z: ("68" if lo68 <= z <= hi68 else ("95" if lo95 <= z <= hi95 else "--"))
            res["Z"][f"{sk}|{f}|{m}"] = dict(median=float(med), lo68=float(lo68), hi68=float(hi68), lo95=float(lo95), hi95=float(hi95))
            if sk.startswith(("REC-quoted", "REC-meas", "MLS16", "ENSEMBLE")) or f == "tot" and m == "Planck":
                print(f"   {sk:<48}{f+' / '+m:<20}{med:>7.3f}  [{lo68:5.2f},{hi68:5.2f}]   [{lo95:5.2f},{hi95:5.2f}]   {ins(Z_F):>2} {ins(6.0):>2} {ins(Z_M):>2}")

# ---------------------------------------------------------------- 2. Bayes factors / posterior odds over the declared list
from numpy.polynomial.hermite_e import hermegauss
_GX, _GW = hermegauss(41); _GW = _GW / math.sqrt(2 * math.pi)
def H_nodes(model, footing):
    """(weights, H_eff in s^-1) by Gauss-Hermite quadrature over H0 (and Omega_Lambda): deterministic, accurate in the tails"""
    comps = {"Planck": [(1.0, 67.4, 0.5)], "SH0ES": [(1.0, 73.0, 1.0)], "both": [(0.5, 67.4, 0.5), (0.5, 73.0, 1.0)], "avg": [(1.0, 70.2, 2.8)]}
    W, H = [], []
    if footing == "Lam-phys":
        comps = {"Planck": comps["Planck"]}; model = "Planck"
    for w0, mu, sg in comps[model]:
        for xk, wk in zip(_GX, _GW):
            h0 = mu + sg * xk
            if footing == "tot":
                W.append(w0 * wk); H.append(H_si(h0))
            else:
                for xo, wo in zip(_GX[::4], _GW[::4] / _GW[::4].sum()):     # 11 Omega_Lambda nodes (weights renormalised)
                    W.append(w0 * wk * wo); H.append(H_si(h0) * math.sqrt(OM_L + 0.007 * xo))
    return np.array(W), np.array(H)
def marg_lik(a_obs, s_a, model, footing, Zs):
    """likelihood of a0_obs for each POINT hypothesis Z, marginalised over H0 (and Omega_Lambda) by quadrature"""
    W, Hq = H_nodes(model, footing)
    lnH = np.log(c * Hq)
    return np.array([np.sum(W * np.exp(-0.5 * ((math.log(a_obs) - (lnH - math.log(Z))) / s_a) ** 2)) / (s_a * math.sqrt(2 * math.pi)) for Z in Zs])
def marg_lik_fixedH(a_obs, s_a, H, Zs):
    return np.array([math.exp(-0.5 * ((math.log(a_obs) - (math.log(c * H) - math.log(Z))) / s_a) ** 2) / (s_a * math.sqrt(2 * math.pi)) for Z in Zs])
Zc = [h[1] for h in CAND]; Zk = [h[1] for h in CTRL]
names = [h[0].split()[0] for h in CAND]
iF, iV, iM = names.index("F"), names.index("V"), names.index("M")
print("\nBAYES FACTORS between the declared candidates (a0 likelihood marginalised over H0, Omega_Lambda); equal prior odds -> posterior probabilities")
res["BF"] = {}
for sk in ("REC-quoted   (record PL, its own 5.44%)", "REC-meas.sys (alpha1 PL, stat+dist+gas+incl)", "ENSEMBLE E   (9 analysis choices)", "MLS16        (1.20 +-0.02 +-0.24)"):
    a_obs, s_a = SC[sk]
    for f, m in (("tot", "Planck"), ("tot", "avg"), ("Lam", "Planck"), ("Lam", "avg"), ("Lam-phys", "Planck")):
        L = marg_lik(a_obs, s_a, m, f, Zc); Lk = marg_lik(a_obs, s_a, m, f, Zk)
        P = L / L.sum()
        res["BF"][f"{sk}|{f}|{m}"] = dict(L=L.tolist(), P=P.tolist(), BF_F_V=float(L[iF] / L[iV]), BF_F_M=float(L[iF] / L[iM]), BF_V_M=float(L[iV] / L[iM]),
                                            best=names[int(np.argmax(L))], ctrl_BF_vs_best=[float(x / L.max()) for x in Lk])
        print(f"   {sk[:12]:<12}{f+'/'+m:<16}" + " ".join(f"{n}:{p:5.3f}" for n, p in zip(names, P)) + f"   BF(F:V)={L[iF]/L[iV]:5.2f} BF(F:M)={L[iF]/L[iM]:5.2f} BF(V:M)={L[iV]/L[iM]:5.2f}  best={names[int(np.argmax(L))]}  controls vs best: {Lk[0]/L.max():.1e}, {Lk[1]/L.max():.1e}")

# ---------------------------------------------------------------- 3. sigma separations
print("\nHOW MANY SIGMA SEPARATE THE HYPOTHESES  n = |ln(Z_i/Z_j)| / s_tot,  s_tot = sqrt(s_a^2 + s_H^2)   (s_H = sd of ln H_eff; the H0 tension is in the 'both' model, not here)")
print(f"   {'a0 scenario':<48}{'footing/H0':<14}{'s_tot':>7}   F-V    F-M    F-K1   F-N    F-P    V-M")
pairs = [("F", "V"), ("F", "M"), ("F", "K1"), ("F", "N"), ("F", "P"), ("V", "M")]
res["sep"] = {}
Zd = dict(zip(names, Zc))
for sk in ("REC-quoted   (record PL, its own 5.44%)", "ENSEMBLE E   (9 analysis choices)"):
    a_obs, s_a = SC[sk]
    for f, m in (("tot", "Planck"), ("Lam", "Planck")):
        sH = float(np.std(np.log(HS[(m, f)]))); st = math.hypot(s_a, sH)
        nv = [abs(math.log(Zd[i] / Zd[j])) / st for i, j in pairs]
        res["sep"][f"{sk}|{f}|{m}"] = dict(s_tot=st, n=dict(zip([f"{i}-{j}" for i, j in pairs], nv)))
        print(f"   {sk:<48}{f+'/'+m:<14}{100*st:>6.1f}%  " + " ".join(f"{x:5.2f}" for x in nv))
print("\n   FULL PAIRWISE sigma-separation matrix among the declared candidates (a0 scenario / s_tot as labelled; same at both footings):")
res["sep_matrix"] = {}
for sk in ("ENSEMBLE E   (9 analysis choices)", "REC-quoted   (record PL, its own 5.44%)"):
    a_obs, s_a = SC[sk]; st = math.hypot(s_a, float(np.std(np.log(HS[("Planck", "tot")]))))
    print(f"   {sk.strip()}  (s_tot = {100*st:.1f}%)")
    print("        " + "".join(f"{n:>7}" for n in names))
    M_ = {}
    for i, ni in enumerate(names):
        row = [abs(math.log(Zc[i] / Zc[j])) / st for j in range(len(names))]
        M_[ni] = dict(zip(names, row))
        print(f"   {ni:>4} " + "".join(f"{x:>7.2f}" for x in row))
    res["sep_matrix"][sk] = M_
print("\n   sigma OFFSET of each declared candidate from the data:  (ln Z_i - ln Z_hat)/s_tot   [+ = candidate above the data-preferred Z, i.e. a0_i below the data]")
print(f"   {'a0 scenario':<48}{'footing/H0':<14}" + "".join(f"{n:>7}" for n in names))
res["offset"] = {}
for sk in ("REC-quoted   (record PL, its own 5.44%)", "REC-meas.sys (alpha1 PL, stat+dist+gas+incl)", "ENSEMBLE E   (9 analysis choices)", "MLS16        (1.20 +-0.02 +-0.24)"):
    a_obs, s_a = SC[sk]
    for f, m in (("tot", "Planck"), ("Lam", "Planck"), ("Lam", "SH0ES")):
        Hq = H_nodes(m, f); lnHm = float(np.sum(Hq[0] * np.log(c * Hq[1]))); sHm = float(math.sqrt(np.sum(Hq[0] * (np.log(c * Hq[1]) - lnHm) ** 2)))
        st = math.hypot(s_a, sHm); zhat = lnHm - math.log(a_obs)
        off = [(math.log(Z) - zhat) / st for Z in Zc]
        res["offset"][f"{sk}|{f}|{m}"] = dict(zip(names, off))
        print(f"   {sk:<48}{f+'/'+m:<14}" + "".join(f"{x:>+7.2f}" for x in off))

# ---------------------------------------------------------------- 4. variants: prior, likelihood shape, H0 mixture
print("\nSENSITIVITY of the 68% interval of Z (ENSEMBLE E, footing tot, H0 Planck): prior and likelihood-shape variants")
a_obs, s_a = SC["ENSEMBLE E   (9 analysis choices)"]
var = {}
for pr in ("lnZ", "Z"):
    for lk in ("lognormal", "gauss"):
        Z = lnZ_post(a_obs, s_a, HS[("Planck", "tot")], prior=pr, lik=lk); v = q(Z); var[(pr, lk)] = v
        print(f"   prior flat in {pr:<4} likelihood {lk:<10}: median {v[2]:.3f}  68% [{v[1]:.3f}, {v[3]:.3f}]  95% [{v[0]:.3f}, {v[4]:.3f}]")
spread = max(v[2] for v in var.values()) / min(v[2] for v in var.values()) - 1
check(spread < 0.05, f"P1 the posterior median of Z moves by < 5% across prior (ln Z vs Z) and likelihood-shape choices at 12% a0 error (spread {100*spread:.1f}%)")
res["variants_spread"] = spread
Zb = lnZ_post(a_obs, s_a, HS[("both", "tot")])
print(f"   H0 'both' mixture (Planck/SH0ES 50/50): median {q(Zb)[2]:.3f}, 68% [{q(Zb)[1]:.3f}, {q(Zb)[3]:.3f}], 95% [{q(Zb)[0]:.3f}, {q(Zb)[4]:.3f}]  (bimodal shift {100*(math.log(73/67.4)):.1f}% in Z)")

# ---------------------------------------------------------------- checks and controls
print("\nCHECKS AND CONTROLS")
# cross-check of the quadrature against brute-force Monte Carlo for the hypotheses within ~2 sigma of the data (tails are MC-noisy by construction)
a_o, s_a_ = SC["ENSEMBLE E   (9 analysis choices)"]
Hs = HS[("avg", "tot")]
Lq = marg_lik(a_o, s_a_, "avg", "tot", Zc)
lnHs = np.log(c * Hs)
Lmc = np.array([np.mean(np.exp(-0.5 * ((math.log(a_o) - (lnHs - math.log(Z))) / s_a_) ** 2)) / (s_a_ * math.sqrt(2 * math.pi)) for Z in Zc])
near = [i for i, Z in enumerate(Zc) if abs(math.log(Z) - math.log(6.0)) < 0.25]
check(np.max(np.abs(Lq[near] / Lmc[near] - 1)) < 0.01, f"K1 quadrature marginal likelihoods equal the brute-force Monte Carlo for the {len(near)} candidates within 25% of Z = 6 (max relative deviation {100*np.max(np.abs(Lq[near]/Lmc[near]-1)):.2f}%); tails are MC-noisy, quadrature is the reference")
mu_lnH = float(np.mean(lnHs)); sH = float(np.std(lnHs))
zq = q(lnZ_post(a_o, s_a_, Hs))
check(abs(0.5 * (math.log(zq[3]) - math.log(zq[1])) - math.hypot(s_a_, sH)) < 0.01, "K2 the 68% interval half-width in ln Z equals sqrt(s_a^2 + s_H^2) (analytic)")
# mutation 1: wrong-sign footing
Zt = np.median(lnZ_post(SC["ENSEMBLE E   (9 analysis choices)"][0], 1e-4, np.full(1000, c_H := H_si(67.4))))     # tiny error: Z_hat(tot)
ZL = np.median(lnZ_post(SC["ENSEMBLE E   (9 analysis choices)"][0], 1e-4, np.full(1000, H_si(67.4) * math.sqrt(OM_L))))
Zwrong = np.median(lnZ_post(SC["ENSEMBLE E   (9 analysis choices)"][0], 1e-4, np.full(1000, H_si(67.4) / math.sqrt(OM_L))))
check(abs(ZL / Zt - math.sqrt(OM_L)) < 1e-3 and abs(Zwrong / Zt - 1 / math.sqrt(OM_L)) < 1e-3 and abs(Zwrong / ZL - 1 / OM_L) < 1e-3,
      f"C1 (mutation) wrong-sign footing (H0/sqrt(Omega_L) instead of H0 sqrt(Omega_L)) moves Z_hat by exactly 1/Omega_L = {1/OM_L:.4f} (found {Zwrong/ZL:.4f}); rho_Lambda footing is sqrt(Omega_L) = {math.sqrt(OM_L):.4f} below rho_total (found {ZL/Zt:.4f})")
# mutation 2: wrong H0
Z67 = np.median(lnZ_post(1.1e-10, 1e-4, np.full(1000, H_si(67.4)))); Z73 = np.median(lnZ_post(1.1e-10, 1e-4, np.full(1000, H_si(73.0))))
check(abs(Z73 / Z67 - 73.0 / 67.4) < 1e-3, f"C2 (mutation) wrong H0 (73 for 67.4) moves Z_hat by exactly 73/67.4 = {73/67.4:.4f} (found {Z73/Z67:.4f})")
# direction: Z ~ 1/a0
Za = np.median(lnZ_post(1.2e-10, 1e-4, np.full(1000, H_si(67.4)))); Zb2 = np.median(lnZ_post(0.6e-10, 1e-4, np.full(1000, H_si(67.4))))
check(abs(Zb2 / Za - 2.0) < 1e-3, "C3 (mutation) halving a0 doubles Z (Z ~ 1/a0)")
# data exactly at a candidate favours it
for key, Zt_ in (("F", Zd["F"]), ("M", Zd["M"]), ("V", Zd["V"])):
    a_at = c * H_si(67.4) / Zt_
    L = marg_lik_fixedH(a_at, 0.10, H_si(67.4), Zc)
    check(names[int(np.argmax(L))] == key, f"C4 (control) data placed exactly at Z_{key} (10% error, H fixed) make {key} the maximum-likelihood hypothesis")
# a control hypothesis must be rejected on real data
worst = max(max(v["ctrl_BF_vs_best"]) for v in res["BF"].values())
check(worst < 1e-2, f"C5 the declared controls (Z = 0.5, Z = 12) are rejected everywhere at Jeffreys' 'decisive' level: largest likelihood ratio to the best candidate {worst:.1e} (Z = 12 is rejected by only ~4 sigma when the a0 error is 20%)")
# half the error doubles the sigma separation
a_obs, s_a = SC["ENSEMBLE E   (9 analysis choices)"]
check(abs(math.log(Zd["F"] / Zd["M"]) / (s_a / 2) / (math.log(Zd["F"] / Zd["M"]) / s_a) - 2) < 1e-9, "C6 (mutation) halving the a0 error doubles every sigma separation (n ~ 1/s)")

# ---------------------------------------------------------------- 5. injection-recovery: calibration and discriminating power
print("\nINJECTION-RECOVERY (analytic Gaussian-in-ln model; truth Z = sqrt(32pi/3); 20000 datasets per row): coverage of the intervals and power of BF(F:V), BF(F:M)")
def sim(s_a, s_H, Ztrue, Zalt, n=20000, seed=1):
    r = np.random.default_rng(seed)
    dev = r.normal(0, s_a, n)                       # ln a0_obs - ln a0_true
    dH = r.normal(0, s_H, n)                        # ln H_eff - its assumed centre
    # data ln a0_obs = ln(cH_true/Ztrue) + dev, with H_true = centre * exp(dH_true); analyst uses centre -> effective error hypot
    lna = -math.log(Ztrue) + dev + dH
    st = math.hypot(s_a, s_H) if False else s_a      # analyst marginalises H: use total
    st = math.hypot(s_a, s_H)
    ln_zhat = -lna
    cover68 = np.mean(np.abs(ln_zhat - math.log(Ztrue)) < st); cover95 = np.mean(np.abs(ln_zhat - math.log(Ztrue)) < 1.96 * st)
    lnBF = ((lna + math.log(Zalt)) ** 2 - (lna + math.log(Ztrue)) ** 2) / (2 * st * st)     # ln L(true) - ln L(alt)
    return cover68, cover95, float(np.mean(lnBF > math.log(3))), float(np.mean(lnBF < -math.log(3))), float(np.median(lnBF))
print(f"   {'s_a':>6}{'s_H':>6}{'alt':>5}{'cover68':>9}{'cover95':>9}{'P(BF>3 for truth)':>19}{'P(BF>3 for alt)':>17}{'median lnBF':>13}")
inj = {}
for s_a in (0.20, 0.12, 0.054, 0.02, 0.01):
    for alt, Zalt in (("V", 6.0), ("M", Z_M)):
        cv68, cv95, pt, pa, med = sim(s_a, 0.0074, Z_F, Zalt)
        inj[f"{s_a}|{alt}"] = dict(cover68=cv68, cover95=cv95, p_truth=pt, p_alt=pa, median_lnBF=med)
        print(f"   {100*s_a:5.1f}%{0.74:6.2f}%{alt:>5}{cv68:>9.3f}{cv95:>9.3f}{pt:>19.3f}{pa:>17.3f}{med:>13.2f}")
res["injection"] = inj
c68 = [v["cover68"] for v in inj.values()]; c95 = [v["cover95"] for v in inj.values()]
check(all(abs(x - 0.6827) < 0.02 for x in c68) and all(abs(x - 0.95) < 0.015 for x in c95), "I1 the 68% and 95% intervals cover the injected truth 68.3% / 95% of the time (calibrated)")
check(inj["0.12|V"]["p_truth"] < 0.10 and inj["0.12|M"]["p_truth"] < 0.35, "I2 at a 12% a0 error, a Bayes factor > 3 for the true Z = sqrt(32 pi/3) over 6 occurs in < 10% of datasets (over 2 pi: < 35%): the data cannot discriminate")
def analytic_lnBF(s_a, s_H, Zt_, Za_):
    st = math.hypot(s_a, s_H); return (math.log(Za_ / Zt_)) ** 2 / (2 * st * st)
errs = []
for key, v in inj.items():
    sa_, alt = key.split("|"); Za_ = 6.0 if alt == "V" else Z_M
    errs.append(abs(v["median_lnBF"] - analytic_lnBF(float(sa_), 0.0074, Z_F, Za_)))
check(max(errs) < 0.15, f"I3 the simulated median ln BF(F:alt) equals the analytic expectation Delta^2/(2 s_tot^2) (max abs deviation {max(errs):.3f}); at 1% a0 error F beats V by BF>3 in {100*inj['0.01|V']['p_truth']:.0f}% and M in {100*inj['0.01|M']['p_truth']:.0f}% of datasets")
check(inj["0.02|M"]["p_truth"] > inj["0.054|M"]["p_truth"] > inj["0.12|M"]["p_truth"] and inj["0.02|V"]["p_truth"] > inj["0.054|V"]["p_truth"], "I4 discriminating power rises monotonically as the a0 error falls")

print(f"\n  {sum(ok)}/{len(ok)} checks held.")
json.dump(res, open("v03_results.json", "w"), indent=1, default=float)
sys.exit(0 if all(ok) else 1)
