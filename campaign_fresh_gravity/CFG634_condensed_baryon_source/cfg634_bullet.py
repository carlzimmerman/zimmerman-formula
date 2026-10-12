#!/usr/bin/env python3
"""CFG634 T4 (FROZEN_CRITERIA.md, 1fea20013): static Bullet check for H-CB, the condensed-baryon source. No merger grid is run.

Progenitors: CFG625's Progenitor625 (variants BASE, B1 primary, B2, B3; M200 1.5e15 main / 1.5e14 sub with the cool-core cloud),
imported read-only. Condensed = the stellar component rho_s; hot = ICM grid gas + cool-core cloud.
  H-CB settled phantom: the round-rule phantom of the stars alone (truncated at r_t as the progenitor does).
  Reservoir: R0 (case L), RI (cold(<r) = max(settled, 5.364 M_b(<r))), RN (supply 5.364 M_b minus settled, NFW c = 4 in r200; CFG629).
(a) gas-tied share of the dark mass inside 250 kpc; (b) Clowe+06 Table 2 aperture convergence contrast (galaxy minus plasma,
100 kpc apertures at the measured positions; measured aperture baryons; dark components centred on the BCGs; Sigma_crit from CFG4 H5);
(c) main-cluster projected M(<250 kpc) / Paraficz+16 (PROVISIONAL, recalled; CFG625's constants).
MUTATE: M1 hot restored to the source reproduces CFG625 static (R0, B1) and CFG629 (RN, BASE).
Run from the repository root:  OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG634_condensed_baryon_source/cfg634_bullet.py
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import io, math, json, time, contextlib
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
sys.path.insert(0, LANES); sys.path.insert(0, os.path.join(LANES, "CFG625_merger_baryon_inputs"))
try:
    os.nice(10)
except OSError:
    pass
with contextlib.redirect_stdout(io.StringIO()):
    import cfg625_lib as L625                                                # noqa: E402  (read-only)
import CFG4_common as C4                                                     # noqa: E402
from cfg599_lib import phantom_mass, cumtrapz_sph                            # noqa: E402
LOG, CHK, RES = [], {}, {"lane": "CFG634", "script": "cfg634_bullet", "criteria": "1fea20013"}
COLD = 5.364                       # CFG629 / CFG597 literal supply constant
FOOTS = ("can", "alt")
VARS = ("BASE", "B1", "B2", "B3")


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


P(__doc__.split("Run from")[0].strip())
J4 = json.load(open(os.path.join(LANES, "CFG4_clusters_results.json")))["numbers"]["H5"]
SIGCR = J4["Sigma_crit_Msun_kpc2"]; AP = math.pi * 100.0 ** 2
BT = os.path.join(REPO, "opus_48_extended_research", "reviews", "bullet", "bullet_data_table.py")
with contextlib.redirect_stdout(io.StringIO()):
    BNS, _ = C4.exec_slices(BT, [(None, None)], name="bullet_readonly")
KAS = BNS["KPC_PER_ARCSEC"]
TAB = {}
for lab, r_, d_, mx, emx, ms, ems, kb, ekb in BNS["TABLE2"]:
    TAB[lab] = dict(ra=15 * (r_[0] + r_[1] / 60 + r_[2] / 3600), dec=-(abs(d_[0]) + d_[1] / 60 + d_[2] / 3600), MX=mx * 1e12, Ms=ms * 1e12, kb=kb, ekb=ekb)
ra0, de0 = TAB["Main cluster BCG"]["ra"], TAB["Main cluster BCG"]["dec"]
for v in TAB.values():
    v["x"] = (v["ra"] - ra0) * math.cos(math.radians(de0)) * 3600 * KAS; v["y"] = (v["dec"] - de0) * 3600 * KAS
POS = {k: np.array([v["x"], v["y"]]) for k, v in TAB.items()}
P(f"  positions (kpc, main BCG at 0): " + "; ".join(f"{k} ({v[0]:+.0f}, {v[1]:+.0f})" for k, v in POS.items()))
DK_OBS = {g: (TAB[f"{n} BCG"]["kb"] - TAB[f"{n} plasma"]["kb"], math.hypot(TAB[f"{n} BCG"]["ekb"], TAB[f"{n} plasma"]["ekb"]))
          for g, n in (("main", "Main cluster"), ("sub", "Subcluster"))}


def m_nfw(x):
    return np.log1p(x) - x / (1 + x)


def dark_components(p, src, res, conc=4.0):
    """returns (rho_settled, rho_reservoir, Mset_tot, Mres_tot) on p.r; src: cond | all | none."""
    r = p.r
    Ms_r = {"cond": p.Ms, "all": p.Mbar, "none": 0 * p.Mbar}[src]
    if src == "all":
        rho_set = p.rho_ph.copy(); Mset = p.Mph.copy(); Mt = p.Mph_tot
    else:
        Mph = phantom_mass(r, Ms_r, p.a0) if src == "cond" else 0 * r
        Mt = float(np.interp(p.rt, r, Mph))
        Mset = np.where(r < p.rt, Mph, Mt)
        rho_set = np.gradient(Mset, r) / (4 * math.pi * np.maximum(r, 1e-3) ** 2); rho_set[r >= p.rt] = 0.0
    if res == "R0":
        return rho_set, 0 * r, Mt, 0.0
    if res == "RI":
        Mc = np.maximum(Mset, COLD * p.Mbar)
        rho_c = np.gradient(Mc, r) / (4 * math.pi * np.maximum(r, 1e-3) ** 2)
        rho_res = np.maximum(rho_c - rho_set, 0.0)
        return rho_set, rho_res, Mt, float(cumtrapz_sph(r, rho_res)[-1])
    supply = COLD * p.Mb; Mu = max(supply - Mt, 0.0)
    rs = p.r200 / conc
    nfw = np.where(r < p.r200, 1 / (np.maximum(r, 1e-3) / rs * (1 + r / rs) ** 2), 0.0)
    Mn = np.r_[0, np.cumsum(0.5 * (4 * np.pi * r[1:] ** 2 * nfw[1:] + 4 * np.pi * r[:-1] ** 2 * nfw[:-1]) * np.diff(r))]
    return rho_set, Mu * nfw / Mn[-1], Mt, Mu


def proj629(r, rho, R):
    f = 4 * np.pi * r ** 2 * rho; M = np.r_[0, np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(r))]
    k = r > R; rr = r[k]; w = 1 - np.sqrt(1 - (R / rr) ** 2)
    return float(np.interp(R, r, M) + np.trapz(f[k] * w, rr))


ZG = np.concatenate([[0.0], np.geomspace(1e-2, 8000.0, 2500)])
RG = np.concatenate([[0.0], np.geomspace(0.5, 3000.0, 400)])


def sigma_of(r, rho):
    lr = np.log(np.maximum(r, 1e-3))
    S = np.empty(len(RG))
    for i, R in enumerate(RG):
        rr = np.sqrt(R ** 2 + ZG ** 2)
        S[i] = 2 * np.trapz(np.interp(np.log(np.maximum(rr, 1e-3)), lr, rho, right=0.0), ZG)
    return S


SS = np.linspace(0, 100.0, 61); PH = np.linspace(0, 2 * math.pi, 97)[:-1]
SSg, PHg = np.meshgrid(SS, PH, indexing="ij")


def ap_mass(S, centre, ap_c):
    x = ap_c[0] + SSg * np.cos(PHg) - centre[0]; y = ap_c[1] + SSg * np.sin(PHg) - centre[1]
    s = np.interp(np.hypot(x, y), RG, S)
    return float(np.trapz(np.mean(s, axis=1) * 2 * math.pi * SS, SS))


# control: aperture integrator on a Plummer sphere centred in the aperture vs analytic projected mass
pl_r = np.concatenate([[0.0], np.geomspace(0.5, 8000, 4000)]); pl = L625.plummer_rho(pl_r, 1e13, 80.0)
c_ap = ap_mass(sigma_of(pl_r, pl), np.zeros(2), np.zeros(2)); c_an = 1e13 * 100 ** 2 / (100 ** 2 + 80 ** 2)
check("C-T4 aperture integrator vs analytic Plummer projected mass (1e-3)", abs(c_ap / c_an - 1) < 1e-3, f"{c_ap:.4e} vs {c_an:.4e}")

PRO = {}
for var in VARS:
    for ft in FOOTS:
        PRO[(var, ft, "main")] = L625.Progenitor625(1.5e15, ft, cloud=False, variant=var)
        PRO[(var, ft, "sub")] = L625.Progenitor625(1.5e14, ft, cloud=True, variant=var)

# (a) invariance of the H-CB phantom under the hot gas, and B's gas-tied share
import copy
inv, sens = 0.0, 0.0
for (var, ft, role), p in PRO.items():
    q = copy.copy(p); q.Mbar = p.Mbar + p.Mg; q.Mg = 2 * p.Mg            # hot gas doubled in the baryon field
    q.Mph = phantom_mass(p.r, q.Mbar, p.a0); q.Mph_tot = float(np.interp(p.rt, p.r, q.Mph))
    q.rho_ph = np.gradient(q.Mph, p.r) / (4 * math.pi * np.maximum(p.r, 1e-3) ** 2)
    inv = max(inv, float(np.max(np.abs(dark_components(p, "cond", "R0")[0] - dark_components(q, "cond", "R0")[0]))))
    sens = max(sens, float(np.max(np.abs(dark_components(p, "all", "R0")[0] - dark_components(q, "all", "R0")[0]))))
check("T4a H-CB settled phantom is unchanged when the hot gas is doubled (B's changes: code path has teeth)", inv <= 1e-12 and sens > 0,
      f"H-CB max |d rho| {inv:.1e}; B max |d rho| {sens:.2e}")
SHARE = {}
for (var, ft, role), p in PRO.items():
    Mall = p.Mph; Mst = np.where(p.r < p.rt, phantom_mass(p.r, p.Ms, p.a0), np.interp(p.rt, p.r, phantom_mass(p.r, p.Ms, p.a0)))
    rs_ = np.gradient(Mst, p.r) / (4 * math.pi * np.maximum(p.r, 1e-3) ** 2); rs_[p.r >= p.rt] = 0
    sh = 1 - L625.proj_mass(p.r, rs_, 250.0) / L625.proj_mass(p.r, p.rho_ph, 250.0)
    SHARE[f"{var}_{ft}_{role}"] = dict(B_gas_tied_share_250=float(sh), HCB_gas_tied_share_250=0.0)
P("  (a) B's gas-tied share of the settled phantom inside 250 kpc (H-CB: 0 by construction): "
  + "; ".join(f"{k} {v['B_gas_tied_share_250']:.2f}" for k, v in SHARE.items() if k.startswith("B1")))

# (b) + (c)
T4 = {}
CASES = [("HCB", "cond"), ("B_alpha0", "all"), ("M2", "none")]
for var in VARS:
    for ft in FOOTS:
        for tag, srcm in CASES:
            for res in ("R0", "RI", "RN"):
                key = f"{var}|{ft}|{tag}|{res}"
                comp = {}
                for role in ("main", "sub"):
                    p = PRO[(var, ft, role)]
                    rs_, rr_, Mt, Mu = dark_components(p, srcm, res)
                    comp[role] = dict(p=p, rho_d=rs_ + rr_, Mset=Mt, Mres=Mu)
                SD = {role: sigma_of(comp[role]["p"].r, comp[role]["rho_d"]) for role in comp}
                cen = {"main": POS["Main cluster BCG"], "sub": POS["Subcluster BCG"]}
                kap = {}
                for lab in TAB:
                    Md = sum(ap_mass(SD[role], cen[role], POS[lab]) for role in SD)
                    kap[lab] = (TAB[lab]["MX"] + TAB[lab]["Ms"] + Md) / (SIGCR * AP)
                dk = {"main": kap["Main cluster BCG"] - kap["Main cluster plasma"], "sub": kap["Subcluster BCG"] - kap["Subcluster plasma"]}
                zz = {g: (dk[g] - DK_OBS[g][0]) / DK_OBS[g][1] for g in dk}
                core = {}
                for role in ("main", "sub"):
                    p = comp[role]["p"]
                    bar = p.rho_g + p.rho_cc + p.rho_s
                    tot = L625.proj_mass(p.r, bar, 250.0) + L625.proj_mass(p.r, comp[role]["rho_d"], 250.0)
                    core[role] = dict(proj250=tot, ratio_P16=tot / L625.P16_M250[role][0], ratio_629proj=(proj629(p.r, bar, 250) + proj629(p.r, comp[role]["rho_d"], 250)) / (2.5e14 if role == "main" else 2.0e14),
                                      Mset=comp[role]["Mset"], Mres=comp[role]["Mres"])
                lab_b = "PASS" if all(abs(zz[g]) <= 2 and dk[g] > 0 for g in dk) else ("FAIL" if any(abs(zz[g]) >= 3 for g in dk) else "TENSION")
                T4[key] = dict(dkappa=dk, z=zz, label=lab_b, core=core)
                if var == "B1" or (tag == "B_alpha0" and var == "BASE"):
                    P(f"  {key:24s} dkappa main {dk['main']:+.3f} (obs {DK_OBS['main'][0]:+.2f}+-{DK_OBS['main'][1]:.2f}, z {zz['main']:+.2f}), "
                      f"sub {dk['sub']:+.3f} (obs {DK_OBS['sub'][0]:+.2f}+-{DK_OBS['sub'][1]:.2f}, z {zz['sub']:+.2f}) -> {lab_b} | "
                      f"M(<250)/P16 main {core['main']['ratio_P16']:.2f}, sub {core['sub']['ratio_P16']:.2f} | settled main {core['main']['Mset']:.2e}, reservoir {core['main']['Mres']:.2e}")
# B at alpha = infinity proxy: gas-sourced part of B's phantom centred on the plasma (reported only)
for ft in FOOTS:
    comp = {}
    for role in ("main", "sub"):
        p = PRO[("B1", ft, role)]
        rs_, _, _, _ = dark_components(p, "cond", "R0")
        comp[role] = (sigma_of(p.r, rs_), sigma_of(p.r, np.maximum(p.rho_ph - rs_, 0)))
    cen = {"main": POS["Main cluster BCG"], "sub": POS["Subcluster BCG"]}; pcen = {"main": POS["Main cluster plasma"], "sub": POS["Subcluster plasma"]}
    kap = {lab: (TAB[lab]["MX"] + TAB[lab]["Ms"] + sum(ap_mass(comp[r_][0], cen[r_], POS[lab]) + ap_mass(comp[r_][1], pcen[r_], POS[lab]) for r_ in comp)) / (SIGCR * AP) for lab in TAB}
    dk = {"main": kap["Main cluster BCG"] - kap["Main cluster plasma"], "sub": kap["Subcluster BCG"] - kap["Subcluster plasma"]}
    T4[f"B1|{ft}|B_alphaInf_proxy|R0"] = dict(dkappa=dk, z={g: (dk[g] - DK_OBS[g][0]) / DK_OBS[g][1] for g in dk})
    P(f"  B1|{ft}|B_alphaInf_proxy|R0 (reported only): dkappa main {dk['main']:+.3f}, sub {dk['sub']:+.3f}")

J625 = json.load(open(os.path.join(LANES, "CFG625_merger_baryon_inputs", "cfg625_static_results.json")))["masses_t0"]
J629 = json.load(open(os.path.join(LANES, "CFG629_cluster_supply_check", "cfg629_supply_results.json")))
m1a = max(abs(T4[f"B1|{ft}|B_alpha0|R0"]["core"][role]["ratio_P16"] - J625[f"B1_{ft}_{role}"]["ratio_to_P16"]) for ft in FOOTS for role in ("main", "sub"))
check("M1-T4a hot restored (B source, R0) reproduces CFG625 static B1 M(<250)/P16 (1e-6)", m1a < 1e-6, f"max diff {m1a:.1e}")
m1b = max(abs(T4[f"BASE|{ft}|B_alpha0|RN"]["core"][role]["ratio_629proj"] - J629[f"{ft}_{role}"]["proj250_with_unsettled_over_lensing"]) for ft in FOOTS for role in ("main", "sub"))
check("M1-T4b hot restored (B source, RN, BASE) reproduces CFG629 (1e-6)", m1b < 1e-6, f"max diff {m1b:.1e}")

lab4 = {res: {ft: T4[f"B1|{ft}|HCB|{res}"]["label"] for ft in FOOTS} for res in ("R0", "RI", "RN")}
RES.update(T4=T4, gas_tied_share=SHARE, dkappa_obs=DK_OBS, positions={k: v.tolist() for k, v in POS.items()}, HCB_labels_B1=lab4,
           variant_labels={f"{var}|{ft}|HCB|{res}": T4[f"{var}|{ft}|HCB|{res}"]["label"] for var in VARS for ft in FOOTS for res in ("R0", "RI", "RN")})
P(f"  T4(b) H-CB labels (B1): {lab4}")
P("  T4(b) H-CB labels, all variants: " + "; ".join(f"{k} {v}" for k, v in RES["variant_labels"].items()))
RES["checks"] = CHK; RES["elapsed_s"] = round(time.time() - T0, 1)
nf = sum(1 for c in CHK.values() if not c["ok"])
P(f"\n{len(CHK) - nf}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
json.dump(C4.jclean(RES), open(os.path.join(HERE, "cfg634_bullet_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg634_bullet.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nf else 0)
