#!/usr/bin/env python3
"""CFG495 Step 2: the drawdown prediction for KiDS isolated lenses (CFG377/CFG413 conventions), both footings, never pooled.

Reads ONLY the lens catalogue (M_gal, z, log M*) and the KiDS pair weights WW (needed to pair-average a model into the 15 g_bar bins,
exactly as CFG377 does). The shear signal (WG) is NOT read here. The frozen two-halo template comes from the S0 control (cfg495_sim.py env term).

Outputs: cfg495_predict.out, cfg495_predict_results.json; per-group tables ../../../_external_data/cfg495_work/cfg495_pred_tables.npz
"""
import os, sys, json, math, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cfg495_lenslib as LL

REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
OUTW = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg495_work"))
LOG = []
def P(s=""):
    print(s, flush=True); LOG.append(str(s))
T0 = time.time()
np.set_printoptions(linewidth=200, precision=4, suppress=True)

lens = np.load(os.path.join(DATA, "lr_lenses.npz"))
z = lens["z"].astype(float); Mgal = lens["Mgal"].astype(float); logMs = lens["logM"].astype(float)
WW = np.load(os.path.join(DATA, "cfg110_perlens.npz"))["WW"]
nL = len(z)
lmg = np.log10(Mgal)
key = np.floor(lmg / 0.01).astype(np.int64) * 1000 + np.floor(z / 0.03).astype(np.int64)     # CFG377 grouping
_, gi, cnt = np.unique(key, return_inverse=True, return_counts=True); gi = gi.ravel()
GM = 10 ** (np.bincount(gi, weights=lmg) / cnt); GZ = np.bincount(gi, weights=z) / cnt; GS = np.bincount(gi, weights=logMs) / cnt
NG = len(cnt)
P(f"CFG495 Step 2: {nL} lenses, {NG} groups (CFG377 grouping); f_b {LL.FB:.5f}; a0 canonical {LL.A0_SI['canonical']:.4e} / alt {LL.A0_SI['alt']:.4e}")

# ---------------------------------------------------------------- frozen two-halo template from the S0 controls (both seeds)
env = []
for k in ("N512_s360_can", "N512_s359_can"):
    p = os.path.join(OUTW, f"cfg495_sim_{k}.json")
    env.append(json.load(open(p))["env"])
RBE = np.array(json.load(open(os.path.join(OUTW, "cfg495_sim_N512_s360_can.json")))["RB_ENV"]); RCE = np.sqrt(RBE[1:] * RBE[:-1])
TPL = {iso: LL.env_template(env, iso) for iso in ("iso1", "iso05", "all")}
for iso, (lM, tab) in TPL.items():
    P(f"  2h template [{iso}]: log M_ta classes [Msun/h] {np.round(lM, 2).tolist()}")
    for i in range(len(lM)):
        ok = np.isfinite(tab[i])
        P(f"     {lM[i]:.2f}: DS_out(R_com = 0.8/1/2/4 Mpc/h) = {np.interp(np.log([0.8, 1, 2, 4]), np.log(RCE[ok]), tab[i][ok]).round(3).tolist()} h Msun/pc^2"
          f"  ({(~ok).sum()} empty lattice bins dropped)")

def pstack(tab, mask=None):
    mask = np.ones(nL, bool) if mask is None else mask
    out = np.zeros(15)
    for k in range(15):
        w = np.bincount(gi[mask], weights=WW[mask, k], minlength=NG)
        out[k] = (w @ tab[:, k]) / w.sum()
    return out
gcen = np.sqrt(LL.GEDGE_K[:-1] * LL.GEDGE_K[1:])
Rm = (WW * np.sqrt(LL.G_MPC * Mgal[:, None] / gcen[None, :])).sum(0) / WW.sum(0)
P("  pair-weighted mean R [Mpc]: " + str(np.round(Rm, 3)))

# ---------------------------------------------------------------- per-group tables
TAB = {}
VARS2H = [("iso05", "D2"), ("iso1", "D2"), ("all", "D2"), ("iso05", "D1"), ("iso05", "D0")]
t = time.time()
for foot in ("canonical", "alt"):
    T = {n: np.zeros((NG, 15)) for n in ("lcdm", "nodd", "prop", "shell")}
    meta = {n: np.zeros(NG) for n in ("rta", "Mta", "fret", "redge", "q", "qsh", "Me", "M200")}
    for g in range(NG):
        v, m = LL.esd_vectors(GM[g], GZ[g], GS[g], foot)
        for n in T: T[n][g] = v[n]
        for n in meta: meta[n][g] = m[n]
    TAB[foot] = dict(**T, **{"meta_" + n: meta[n] for n in meta})
    P(f"  [{foot}] tables {time.time() - t:.0f}s; median q {np.nanmedian(meta['q']):.3f}, x_edge {np.nanmedian(meta['redge'] / meta['rta']):.3f}, "
      f"f_ret {np.nanmedian(meta['fret']):.3f}, r_ta {np.nanmedian(meta['rta']):.3f} Mpc; shell overdraw (q_sh > 1) in {np.mean(meta['qsh'] > 1):.2%} of groups; "
      f"edge capped at r_ta in {np.mean(meta['redge'] >= meta['rta'] * (1 - 1e-9)):.2%}")
T2 = {}
for iso, zf in VARS2H:
    lM, tab = TPL[iso]
    T2[f"{iso}_{zf}"] = np.array([LL.finish(LL.two_halo_fn(math.log10(TAB['canonical']['meta_Mta'][g] * LL.H), GZ[g], lM, RCE, tab, zf), GM[g]) for g in range(NG)])
TT = np.array([LL.finish(lambda R: R ** -0.8 * 1e12, GM[g]) for g in range(NG)])     # CFG377's R^-0.8 shape (reported only)
# halo-mass sensitivity tables (M200 x 10^+-0.2; the 2h term is kept at the nominal mass)
for dl in (-0.2, 0.2):
    for foot in ("canonical", "alt"):
        T = {n: np.zeros((NG, 15)) for n in ("lcdm", "nodd", "prop", "shell")}
        for g in range(NG):
            v, m = LL.esd_vectors(GM[g], GZ[g], GS[g], foot, dlogM=dl)
            for n in T: T[n][g] = v[n]
        for n in T: TAB[foot][f"{n}_dlogM{dl:+.1f}"] = T[n]
    P(f"  halo-mass shift {dl:+.1f} dex tables done ({time.time() - t:.0f}s)")
np.savez_compressed(os.path.join(OUTW, "cfg495_pred_tables.npz"), gi=gi, GM=GM, GZ=GZ, GS=GS, TT=TT,
                    **{f"{f}_{n}": TAB[f][n] for f in TAB for n in TAB[f]}, **{f"2h_{k}": v for k, v in T2.items()})

# ---------------------------------------------------------------- stacked predictions
RES = dict(Rm=Rm.tolist(), n_groups=NG)
for foot in ("canonical", "alt"):
    S = {n: pstack(TAB[foot][n]) for n in ("lcdm", "nodd", "prop", "shell")}
    S2 = {k: pstack(v) for k, v in T2.items()}
    St = pstack(TT)
    A_equiv = float(np.sum(S2["iso05_D2"][Rm > 0.5] * St[Rm > 0.5]) / np.sum(St[Rm > 0.5] ** 2))
    RES[foot] = dict(**{n: S[n].tolist() for n in S}, two_halo={k: v.tolist() for k, v in S2.items()}, tmpl_R08=St.tolist(), A_equiv_R08=A_equiv,
                     frac_prop_of_nodd=(S["prop"] / (S["nodd"] + S2["iso05_D2"])).tolist(), frac_shell_of_nodd=(S["shell"] / (S["nodd"] + S2["iso05_D2"])).tolist())
    P(f"\n== [{foot}] stacked 15-bin predictions [Msun/pc^2] (frozen 2h = iso05, D(z)^2)")
    P("  R [Mpc]        : " + str(np.round(Rm, 3)))
    P("  LCDM 1h        : " + str(np.round(S["lcdm"], 3)))
    P("  F no drawdown  : " + str(np.round(S["nodd"], 3)))
    P("  drawdown PROP  : " + str(np.round(S["prop"], 3)))
    P("  drawdown SHELL : " + str(np.round(S["shell"], 3)))
    P("  2h frozen      : " + str(np.round(S2["iso05_D2"], 3)))
    P("  PROP / (F_nodd + 2h): " + str(np.round(RES[foot]["frac_prop_of_nodd"], 3)))
    P(f"  frozen 2h expressed as CFG377's R^-0.8 amplitude (bins R > 0.5 Mpc): A_equiv = {A_equiv:.3f}  (CFG413/486 free fits: 0.95-1.57)")

# ---------------------------------------------------------------- typical lens masses (log M* 10.5-11), physical radii
P("\n== typical lenses (z = 0.3; M_gal = M* x 10^0.08, the median catalogue ratio): Delta Sigma at R = 0.1/0.3/0.6/1/2 Mpc [Msun/pc^2]")
RQ = np.array([0.1, 0.3, 0.6, 1.0, 2.0]); TYP = {}
for lMs in (10.5, 10.75, 11.0):
    for foot in ("canonical", "alt"):
        v, m = LL.esd_vectors(10 ** (lMs + 0.08), 0.3, lMs, foot, extra_R=RQ)
        lM, tab = TPL["iso05"]
        two = LL.two_halo_fn(math.log10(m["Mta"] * LL.H), 0.3, lM, RCE, tab, "D2")(RQ) * 1e-12
        TYP[f"{lMs}|{foot}"] = dict(rta=m["rta"], redge=m["redge"], x_edge=m["redge"] / m["rta"], q=m["q"], qsh=m["qsh"], fret=m["fret"], Me=m["Me"], Mta=m["Mta"],
                                    lcdm=v["R_lcdm"].tolist(), nodd=v["R_nodd"].tolist(), prop=v["R_prop"].tolist(), shell=v["R_shell"].tolist(), two_halo=two.tolist())
        P(f"  log M* {lMs:5.2f} [{foot:9s}] r_ta {m['rta']:.3f} Mpc, r_edge {m['redge']:.3f} (x {m['redge'] / m['rta']:.2f}), f_ret {m['fret']:.3f}, "
          f"M_e/M_ta {m['Me'] / m['Mta']:.3f}, q {m['q']:.3f}, q_sh {m['qsh']:.2f}")
        P(f"      LCDM {np.round(v['R_lcdm'], 3)}  F_nodd {np.round(v['R_nodd'], 3)}  PROP {np.round(v['R_prop'], 3)}  SHELL {np.round(v['R_shell'], 3)}  2h {np.round(two, 3)}")
RES["typical"] = TYP
P(f"\nelapsed {time.time() - T0:.0f}s")
json.dump(RES, open(os.path.join(HERE, "cfg495_predict_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg495_predict.out"), "w").write("\n".join(LOG) + "\n")
