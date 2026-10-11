#!/usr/bin/env python3
"""CFG624 G5 (FROZEN_CRITERIA.md 803cef306): raw KiDS-1000 + DES Y3 xi+- against the NO-COLD-ENERGY PM gravitating field.
CFG592's native machinery (surveys, published scale cuts, covariance, Hankel transforms, nuisance priors, NLA IA, the support rule and
the fit) is executed read-only; this lane re-implements only the projection with general (Om, Ok, OL): lensing prefactor
1.5 Om (H0/c)^2 f_K(chi)/a on the gravitating overdensity relative to the mean matter (here: baryon) density, f_K in the lensing
efficiency, in the Limber measure and in k = (l + 1/2)/f_K(chi), and the model's own linear growth for z > 1 and for the NLA term.
M-G5a: with the CFG592 engine background (Om 0.3138, flat) and CFG530's LR L100 N512 held-boost spectra, this code must reproduce
CFG592's chi2_F (KiDS / DES) within 0.01.  No HMcode, BAHAMAS, mass function or S0 ratio enters any verdict.
Run from the repository root:  nice -n 10 python3 campaign_fresh_gravity/CFG624_no_cold_energy/cfg624_shear.py
kappa = 1/2 FITTED; footings never pooled; no particle species; not theory closed."""
import os, sys, json, math, glob, time, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.optimize import minimize
from scipy.integrate import quad
from scipy.stats import chi2 as CH

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
D592 = os.path.join(LANES, "CFG592_cosmic_shear_likelihood")
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg624_work"))
T0 = time.time(); LOG = []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


P(__doc__.split("Run from")[0].strip())
src = open(os.path.join(D592, "cfg592_native.py")).read()
m1 = "# ------------------------------------------------------------------ feedback context"
assert src.count(m1) == 1
NS = {"__file__": os.path.join(D592, "cfg592_native.py"), "__name__": "cfg592_native_ro"}
os.environ.pop("CFG592_MUTATE", None)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index(m1)], "cfg592_native_ro", "exec"), NS)
SURV, ZG, AG, _wz, LN = NS["SURV"], NS["ZG"], NS["AG"], NS["_wz"], NS["LN"]
nuis_spec, subset, C1RHO = NS["nuis_spec"], NS["subset"], NS["C1RHO"]
CKM = 2997.92458                                                             # c/H0 in Mpc/h


class Model:
    """a background + growth + node spectra (z = 0, 0.5, 1) + low-k linear shape."""
    def __init__(self, Om, Ok, OL, nodes, k, k_lo, k_hi, plin_shape, label):
        self.Om, self.Ok, self.OL, self.label = Om, Ok, OL, label
        Ez = lambda z: math.sqrt(Om * (1 + z) ** 3 + Ok * (1 + z) ** 2 + OL)
        self.chi = np.array([quad(lambda x: 1 / Ez(x), 0, z)[0] for z in ZG]) * CKM
        self.dchidz = CKM / np.array([Ez(z) for z in ZG])
        self.fK = self.fk(self.chi)
        E = lambda a: math.sqrt(Om / a ** 3 + Ok / a ** 2 + OL)
        g = lambda x: quad(lambda u: 1.0 / (u * E(u)) ** 3, 0, x)[0] * E(x)
        g1 = g(1.0); self.D = lambda a: g(a) / g1
        self.DZG = np.array([self.D(a) for a in AG]); self.D1 = self.D(0.5)
        self.nodes, self.k, self.k_lo, self.k_hi, self.plin = nodes, np.asarray(k), k_lo, k_hi, plin_shape

    def fk(self, x):
        if self.Ok > 1e-12:
            s = math.sqrt(self.Ok) / CKM; return np.sinh(s * x) / s
        return np.asarray(x, float)

    def node_P(self, pb, kq):
        kb = self.k; m = kb <= self.k_hi * 1.0000001; kb_, pb_ = kb[m], np.asarray(pb)[m]
        lp = np.interp(np.log(np.clip(kq, self.k_lo, self.k_hi)), np.log(kb_), np.log(pb_))
        sel = kb_ >= self.k_hi / 2; s = np.polyfit(np.log(kb_[sel]), np.log(pb_[sel]), 1)[0]
        p_hi = np.exp(np.interp(np.log(self.k_hi), np.log(kb_), np.log(pb_)))
        low = self.plin(kq) * (pb_[0] / self.plin(np.array([kb_[0]]))[0])
        return np.where(kq < self.k_lo, low, np.where(kq > self.k_hi, p_hi * (kq / self.k_hi) ** s, np.exp(lp)))

    def Pmat(self):
        KK = (LN[:, None] + 0.5) / self.fK[None, :]
        lnP = np.array([np.log(self.node_P(self.nodes[z], KK)) for z in (0.0, 0.5, 1.0)])
        Pm = np.empty_like(KK); NZ = np.array([0.0, 0.5, 1.0])
        for j, z in enumerate(ZG):
            if z <= 1.0:
                i = 0 if z <= 0.5 else 1; w = (z - NZ[i]) / 0.5
                Pm[:, j] = np.exp(lnP[i, :, j] + w * (lnP[i + 1, :, j] - lnP[i, :, j]))
            else:
                Pm[:, j] = np.exp(lnP[2, :, j]) * (self.DZG[j] / self.D1) ** 2
        return Pm, KK

    def kernels(self, S, dz):
        fK = self.fK; chi = self.chi
        dif = chi[None, :] - chi[:, None]
        KLEN = np.where(dif > 0, self.fk(np.maximum(dif, 0.0)) / fK[None, :], 0.0) * _wz[None, :]
        pref = 1.5 * self.Om * (1 / CKM) ** 2 * fK / AG
        q, I = [], []
        for n, s in zip(S["nz"], dz):
            nn = np.interp(ZG - s, S["zmid"], n, left=0.0, right=0.0); nn = nn / np.trapz(nn, ZG)
            q.append(pref * (KLEN @ nn)); I.append(nn / self.dchidz)
        return np.array(q), np.array(I), self.dchidz * _wz / fK ** 2

    def C_ell(self, S, par, Pm):
        q, I, wchi = self.kernels(S, par["dz"])
        F = -C1RHO * self.Om / self.DZG * (((1 + ZG) / 1.62) ** par.get("eta", 0.0))
        PW = Pm * wchi[None, :]; Ig = I * F[None, :]
        GG = np.einsum("lj,aj,bj->abl", PW, q, q); A = par["A"]
        if A != 0.0:
            GI = np.einsum("lj,aj,bj->abl", PW, q, Ig); II = np.einsum("lj,aj,bj->abl", PW, Ig, Ig)
            Cab = GG + A * (GI + GI.transpose(1, 0, 2)) + A * A * II
        else:
            Cab = GG
        return np.array([Cab[a - 1, b - 1] for a, b in S["pairs"]])

    def theory(self, S, D, par, Pm):
        Cp = self.C_ell(S, par, Pm); XP = Cp @ S["Hp"].T; XM = Cp @ S["Hm"].T
        t = np.where(D["isp"], XP[D["ip"], D["ia"]], XM[D["ip"], D["ia"]])
        if "m" in par:
            t = t * (1 + par["m"][D["b1"]]) * (1 + par["m"][D["b2"]])
        return t

    def fit(self, S, D, Pm, ia=True):
        x0, lo, hi, unpack, prior = nuis_spec(S, 1.0, ia)
        def f(x):
            r = D["d"] - self.theory(S, D, unpack(x), Pm); return float(r @ D["Cinv"] @ r) + prior(x)
        starts = [x0] + ([np.r_[x0[:-2], -0.5, 0.0] if S["name"] == "DES" else np.r_[x0[:-1], -0.5]] if ia else [])
        best = None
        for xs in starts:
            r = minimize(f, xs, method="L-BFGS-B", bounds=[(a, b) for a, b in zip(lo, hi)], options=dict(maxiter=400, ftol=1e-12, gtol=1e-8))
            if best is None or r.fun < best.fun:
                best = r
        par = unpack(best.x); t = self.theory(S, D, par, Pm); r_ = D["d"] - t
        return dict(chi2=float(best.fun), chi2_data=float(r_ @ D["Cinv"] @ r_), A_IA=float(par["A"]), model_over_data_median=float(np.median(t / D["d"])))

    def support(self, S, Pm, KK):
        x0, _, _, unpack, _ = nuis_spec(S, 1.0, False); par = unpack(x0)
        q, I, wchi = self.kernels(S, par["dz"])
        inside = (KK >= self.k_lo) & (KK <= self.k_hi); PW = Pm * wchi[None, :]
        tot = np.einsum("lj,aj,bj->abl", PW, q, q); ins = np.einsum("lj,aj,bj->abl", PW * inside, q, q)
        Ct = np.array([tot[a - 1, b - 1] for a, b in S["pairs"]]); Ci = np.array([ins[a - 1, b - 1] for a, b in S["pairs"]])
        fp = (Ci @ S["Ap"].T) / (Ct @ S["Ap"].T); fm = (Ci @ S["Am"].T) / (Ct @ S["Am"].T)
        return np.where(S["isp_all"], fp[S["ip_all"], S["ia_all"]], fm[S["ip_all"], S["ia_all"]])


def score(model, extra_all=True):
    Pm, KK = model.Pmat(); out = {}
    for sn, S in SURV.items():
        f = model.support(S, Pm, KK); keep = S["pubkeep"] & (f >= 0.9); D = subset(S, keep); r = dict(N_kept=D["N"], N_published=int(S["pubkeep"].sum()))
        if D["N"] >= 10:
            ft = model.fit(S, D, Pm); r.update(fit=ft, p=float(CH.sf(ft["chi2_data"], D["N"])), keep=keep)
        if extra_all:
            Da = subset(S, S["pubkeep"]); fa = model.fit(S, Da, Pm)
            r["EXTRAPOLATED_all_points"] = dict(N=Da["N"], fit=fa, p=float(CH.sf(fa["chi2_data"], Da["N"])))
        out[sn] = r
    return out


# ------------------------------------------------------------------ M-G5a: the projection code in the CFG592 limit
P("\n== M-G5a control: CFG530 LR L100 N512 (held boost) through this lane's projection with CFG592's background")
J592 = json.load(open(os.path.join(D592, "cfg592_native_results.json")))["runs"]
REF = {}; CTL = {}
for name in ("530_LRcan_L100_N512", "530_LRalt_L100_N512"):
    run = NS["load_run"](name)
    nodes = {z: run["nodes"][z][0] * run["B"] for z in (0.0, 0.5, 1.0)}
    Om_e = NS["Om"]
    mB = Model(Om_e, 0.0, 1.0 - Om_e, nodes, run["k"], run["k_lo"], run["k_hi"], NS["P_lin0"], name)
    PmB, KKB = mB.Pmat(); REF[name] = {}
    for sn, S in SURV.items():
        PS0 = NS["Pmat"](run, "S0"); fsup = NS["support_mask"](S, run, PS0); keep = S["pubkeep"] & (fsup >= 0.9); D = subset(S, keep)
        ft = mB.fit(S, D, PmB); ref = J592[name]["surveys"][sn]["fits"]["IA"]["F"]["chi2"]
        REF[name][sn] = dict(chi2_this=ft["chi2"], chi2_cfg592=ref, N=D["N"], keep=keep, p_F=J592[name]["surveys"][sn]["p_F"], model=mB, Pm=PmB)
        P(f"  {name} {sn}: N {D['N']}; chi2_F this code {ft['chi2']:.3f} vs CFG592 {ref:.3f}")
mg5a = all(abs(v["chi2_this"] - v["chi2_cfg592"]) <= 0.01 for d in REF.values() for v in d.values())
P(f"  [{'PASS' if mg5a else 'FAIL'}] M-G5a projection code reproduces CFG592 chi2_F within 0.01")

# ------------------------------------------------------------------ NCE runs
camb_t = np.load(os.path.join(WORK, "cfg624_camb_pk.npz"))
kc, p0c = camb_t["kh"], camb_t["pk"][int(np.argmin(camb_t["z"]))]
plin_nce = lambda k: np.exp(np.interp(np.log(np.maximum(k, 1e-4)), np.log(kc), np.log(p0c)))
RES = dict(lane="CFG624", script="cfg624_shear", criteria="803cef306", M_G5a=dict(ok=bool(mg5a), rows={n: {s: {k: v for k, v in x.items() if k in ("chi2_this", "chi2_cfg592", "N")}
                                                                                          for s, x in d.items()} for n, d in REF.items()}), runs={})
for fn in sorted(glob.glob(os.path.join(WORK, "cfg624_*_N*_L100_*.json"))):
    if fn.endswith(".partial.json"):
        continue
    r = json.load(open(fn)); sn_ = r["snap"]
    if not all(k in sn_ for k in ("z0", "z0.5", "z1")):
        continue
    bg = r["background"]; N = r["np"]; L = r["L"]
    nodes = {0.0: np.array(sn_["z0"]["P_grav"]), 0.5: np.array(sn_["z0.5"]["P_grav"]), 1.0: np.array(sn_["z1"]["P_grav"])}
    k = np.array(sn_["z0"]["k_grav"])
    name = f"{r['switch']}_{r['foot']}_N{N}"
    m = Model(bg["Om"], bg["Ok"], bg["OL"], nodes, k, float(k[0]), math.pi * N / (4 * L), plin_nce, name)
    sc = score(m)
    info = dict(switch=r["switch"], foot=r["foot"], N=N, L=L, k_lo=float(k[0]), k_hi=math.pi * N / (4 * L),
                sigma8_part={z: sn_[z]["sigma8"] for z in ("zi", "z1", "z0.5", "z0")}, sigma8_grav={z: sn_[z]["sigma8_grav"] for z in ("zi", "z1", "z0.5", "z0")},
                fsw_vol={z: sn_[z]["fsw_vol"] for z in ("zi", "z1", "z0.5", "z0")}, runtime_s=r.get("runtime_s"), surveys={})
    for s_, v in sc.items():
        row = {kk: vv for kk, vv in v.items() if kk != "keep"}
        if "fit" in v and r["switch"] != "S0":                           # B on the NCE kept set (only where B's own support covers it)
            bname = "530_LRcan_L100_N512" if r["foot"] == "canonical" else "530_LRalt_L100_N512"
            br = REF[bname][s_]; inter = v["keep"] & br["keep"]
            if inter.sum() >= 10:
                D = subset(SURV[s_], inter)
                row["B_on_intersection"] = dict(N=int(inter.sum()), chi2_B=br["model"].fit(SURV[s_], D, br["Pm"])["chi2"], chi2_NCE=m.fit(SURV[s_], D, m.Pmat()[0])["chi2"])
        info["surveys"][s_] = row
    ps = [info["surveys"][s_]["p"] for s_ in SURV if "p" in info["surveys"][s_]]
    info["class"] = "NOT DIAGNOSTIC" if not ps else ("FAIL" if min(ps) < 0.001 else ("PASS" if min(ps) >= 0.01 else "TENSION"))
    RES["runs"][name] = info
    P(f"\n  {name} ({'NCE-S law in bound regions' if r['switch'] == 'T1' else 'NCE-E law everywhere' if r['switch'] == 'S1' else 'a0 -> 0 MUTATE'}): "
      f"sigma8 part/grav z0 {info['sigma8_part']['z0']:.4f}/{info['sigma8_grav']['z0']:.4f}; fsw_vol z0 {info['fsw_vol']['z0']:.4f}; k {info['k_lo']:.3f}-{info['k_hi']:.2f}")
    for s_, v in info["surveys"].items():
        ex = v["EXTRAPOLATED_all_points"]
        line = f"    {s_}: N_kept {v['N_kept']}"
        if "fit" in v:
            line += f", chi2 {v['fit']['chi2']:.1f} (data part {v['fit']['chi2_data']:.1f}, p {v['p']:.2e}), model/data median {v['fit']['model_over_data_median']:.3f}"
        if "B_on_intersection" in v:
            bi = v["B_on_intersection"]; line += f"; on the B-supported intersection (N {bi['N']}): chi2 NCE {bi['chi2_NCE']:.1f} vs B {bi['chi2_B']:.1f}"
        line += f" | EXTRAPOLATED all {ex['N']} points: chi2 {ex['fit']['chi2']:.1f} (p {ex['p']:.1e}), model/data median {ex['fit']['model_over_data_median']:.3f}"
        P(line)
    P(f"    class (frozen rule): {info['class']}")
RES["elapsed_s"] = round(time.time() - T0, 1)
json.dump(RES, open(os.path.join(HERE, "cfg624_shear_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg624_shear.out"), "w").write("\n".join(LOG) + "\n")
P(f"\ndone {RES['elapsed_s']} s")
