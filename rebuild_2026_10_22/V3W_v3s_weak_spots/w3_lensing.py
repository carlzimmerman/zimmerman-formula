#!/usr/bin/env python3
"""V3W W3: v3s's galaxy lensing-to-dynamical mass ratio against the repo's galaxy-galaxy lensing data.

Criteria: FROZEN_CRITERIA.md (37c16dcbaa).
D1: KiDS-1000 isolated lenses (Brouwer+21 Fig. 3, released covariance) through F2's machinery, executed read-only as X53 does.
D2: GH1's 9,049 G09 centrals (KiDS-1000, 50-300 kpc), recomputed from GH1's work file gh1_esd.npz (outside the repo).
Satellites (X75) are reported with GH1's method systematic, not graded.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 w3_lensing.py      (V3W_MUTATE=1: lensing sees Newtonian baryons only)
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing; nothing here says the data favour the framework.
"""
import os, sys
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import io, json, math, time, contextlib
import numpy as np
from scipy import stats

T0 = time.time()
MUT = os.environ.get("V3W_MUTATE") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REB = os.path.dirname(HERE)
REPO = os.path.dirname(REB)
OUT, CHK = [], {}
RES = {"lane": "V3W_v3s_weak_spots", "part": "W3", "criteria": "37c16dcbaa", "mutate": MUT}
np.seterr(all="ignore")


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def T(s):
    print(f"  [{s}; {time.time() - T0:.0f}s]", file=sys.stderr, flush=True)


def check(name, ok, detail):
    CHK[name] = bool(ok); RES.setdefault("checks", {})[name] = dict(ok=bool(ok), detail=str(detail))
    P(f"{name} {'PASS' if ok else 'FAIL'} {detail}")


# ============================================================ F2 machinery (read-only: sections 1 and 4), as X53
F2SRC = os.path.join(REB, "F2_outer_lensing", "f2_outer_lensing.py")
TF = open(F2SRC).read()
s1 = TF[:TF.index("# ============================================================================ 2. K0")]
s4 = TF[TF.index("# ============================================================================ 4. lens inventory"):
        TF.index("# ============================================================================ 5. Track A")]
NF = {"__file__": F2SRC, "__name__": "f2_ro"}
argv0 = sys.argv; sys.argv = [F2SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(s1 + "\n" + s4, F2SRC, "exec"), NF)
sys.argv = argv0
AQ, C, Y = NF["AQ"], NF["C"], NF["Y"]
IDX_ALL, IDX_PRIM = NF["IDX_ALL"], NF["IDX_PRIM"]
data_native, stack_model, sel_of = NF["data_native"], NF["stack_model"], NF["sel_of"]
FOOTS = ("canonical", "alt")
H_NAT = 0.679
CENTRAL0 = dict(h=H_NAT, dMs=0.0, dcold=0.0, fhot=0.5, ye="zero", pz=1.0)          # X53's (L) configuration
Rn, Yn, FN = data_native(H_NAT); Cn = C * FN * FN
X53 = json.load(open(os.path.join(REB, "X53_outer_lensing_law_vs_halos", "x53_outer_lensing_results.json")))
nu_law = AQ.nu_simple
P("V3W W3  galaxy lensing = dynamics: amplitude A = Delta Sigma_obs / Delta Sigma_law (= M_lens / M_dyn,law)" + ("  [MUTATE: lensing sees Newtonian baryons]" if MUT else ""))
P(f"  F2 machinery loaded read-only; native factor {FN:.4f}")
T("F2 loaded")


def gls(y, m, Cm):
    Ci = np.linalg.inv(Cm)
    F = float(m @ Ci @ m); A = float(m @ Ci @ y) / F
    r = y - A * m; x2 = float(r @ Ci @ r); n = len(y)
    s = 1 / math.sqrt(F); sc = max(1.0, math.sqrt(x2 / (n - 1)))
    return dict(A=A, s_stat=s, scale=sc, s_scaled=s * sc, chi2=x2, n=n, p=float(stats.chi2.sf(x2, n - 1)),
                chi2_at_A1=float((y - m) @ Ci @ (y - m)))


# ============================================================ D1: KiDS-1000 isolated lenses
D1 = {}
for foot in FOOTS:
    AQ.nu_simple = nu_law
    mL = stack_model(foot, Rn, CENTRAL0)
    if foot == FOOTS[0] or True:
        ref = np.array(X53["footings"][foot]["profiles"]["L"])
        k1 = float(np.max(np.abs(mL / ref - 1)))
        RES.setdefault("K1", {})[foot] = k1
    if MUT:
        AQ.nu_simple = lambda y: np.ones_like(np.asarray(y, float))
        mL = stack_model(foot, Rn, CENTRAL0)
        AQ.nu_simple = nu_law
    out = {}
    for lab, idx in (("primary", IDX_PRIM), ("all", IDX_ALL)):
        s = sel_of(idx)
        out[lab] = gls(Yn.ravel()[s], mL.ravel()[s], Cn[np.ix_(s, s)])
    # systematics (frozen): M* +-0.2 dex, cold gas +-0.2 dex, primary range
    sysA = {}
    for nm, cfg in (("Ms-0.2", dict(CENTRAL0, dMs=-0.2)), ("Ms+0.2", dict(CENTRAL0, dMs=0.2)),
                    ("cold-0.2", dict(CENTRAL0, dcold=-0.2)), ("cold+0.2", dict(CENTRAL0, dcold=0.2))):
        if MUT:
            AQ.nu_simple = lambda y: np.ones_like(np.asarray(y, float))
        mm = stack_model(foot, Rn, cfg)
        AQ.nu_simple = nu_law
        s = sel_of(IDX_PRIM)
        sysA[nm] = gls(Yn.ravel()[s], mm.ravel()[s], Cn[np.ix_(s, s)])["A"]
    s_sys = math.sqrt((0.5 * (sysA["Ms+0.2"] - sysA["Ms-0.2"])) ** 2 + (0.5 * (sysA["cold+0.2"] - sysA["cold-0.2"])) ** 2)
    pr = out["primary"]
    s_tot = math.sqrt(pr["s_scaled"] ** 2 + s_sys ** 2)
    z = (pr["A"] - 1) / s_tot
    D1[foot] = dict(fits=out, sys_A=sysA, s_sys=s_sys, s_tot=s_tot, z=z)
    P(f"  D1 [{foot}] primary R<=0.31 Mpc: A = {pr['A']:.4f} +- {pr['s_stat']:.4f} stat (x{pr['scale']:.2f} -> {pr['s_scaled']:.4f}) +- {s_sys:.4f} sys "
      f"= +- {s_tot:.4f}; (A-1)/sigma = {z:+.2f}; chi2_min {pr['chi2']:.1f}/{pr['n'] - 1} (p {pr['p']:.1e}); chi2 at A=1 {pr['chi2_at_A1']:.1f}")
    P(f"     systematics A: " + ", ".join(f"{k} {v:.4f}" for k, v in sysA.items()))
    a_ = out["all"]
    P(f"     all radii (reported): A = {a_['A']:.4f} +- {a_['s_scaled']:.4f} (scaled); chi2_min {a_['chi2']:.1f}/{a_['n'] - 1}")
    T(f"D1 {foot}")
RES["D1"] = D1
k1max = max(RES["K1"].values())
check("W3-K1", k1max <= 1e-9, f"law stack reproduces X53's committed (L) profiles: max rel {k1max:.1e} (<= 1e-9)")

# ============================================================ D2: GH1 matched hosts
GH1J = json.load(open(os.path.join(REB, "GH1_matched_lensing_satellites", "gh1_results.json")))
NPZ = os.path.join(os.path.dirname(REPO), "_external_data", "gh1_work", "gh1_esd.npz")
d = np.load(NPZ)
L_ = (d["WG"], d["WX"], d["WW"], d["NN"]); R_ = (d["rWG"], d["rWX"], d["rWW"], d["rNN"])
pg, pr_, hbin = d["pg"], d["pr"], d["hbin"]
NPATCH = 30
RC = np.array(GH1J["radii_kpc"]); GR = np.array(GH1J["graded_mask"])


def esd(sel_l, sel_r, comp=0):                                   # GH1's estimator, line for line
    out = []
    for b in range(4):
        ml, mr = sel_l & (hbin == b), sel_r
        out.append(L_[comp][ml].sum(0) / L_[2][ml].sum(0) - R_[comp][mr].sum(0) / R_[2][mr].sum(0))
    return np.array(out)


def cov(Jk, mask):
    v = Jk[:, :, mask].reshape(NPATCH, -1); m = v.mean(0)
    return (NPATCH - 1) / NPATCH * (v - m).T @ (v - m)


allL, allR = np.ones(len(hbin), bool), np.ones(len(pr_), bool)
DS = esd(allL, allR, 0)
k2 = float(np.max(np.abs(DS / np.array(GH1J["DS"]) - 1)))
check("W3-K2", k2 <= 1e-12, f"GH1 Delta Sigma recomputed from gh1_esd.npz equals GH1's committed DS: max rel {k2:.1e} (<= 1e-12)")
JK = np.array([esd(pg != p, pr_ != p, 0) for p in range(NPATCH)])
Cg = cov(JK, GR); npts = int(GR.sum()) * 4
hart = (NPATCH - npts - 2) / (NPATCH - 1)
Cg_h = Cg / hart                                                   # Hartlap: inverse scaled by hart <=> covariance / hart
k2b = float(np.max(np.abs(np.sqrt(np.diag(Cg)).reshape(4, -1) / np.array(GH1J["err"]) - 1)))
check("W3-K2b", k2b <= 1e-12, f"jackknife errors equal GH1's committed err: max rel {k2b:.1e}")
yv = np.concatenate([DS[b, GR] for b in range(4)])
D2 = {}
for foot in FOOTS:
    mLg = np.concatenate([np.array(GH1J["footings"][foot]["pred_L"][b]) for b in range(4)])
    if MUT:                                                       # Newtonian-baryon lensing: scale by the D1 Newt/L ratio per bin at matched radii
        ratio = []
        for b in range(4):
            rN = np.array(X53["footings"][foot]["profiles"]["Newt"][b]) / np.array(X53["footings"][foot]["profiles"]["L"][b])
            Rx = np.array(X53["footings"][foot]["profiles"]["R"][b]) * 1e3
            ratio.append(np.interp(np.log(RC[GR]), np.log(Rx), rN))
        mLg = mLg * np.concatenate(ratio)
    g = gls(yv, mLg, Cg_h)
    s_tot = math.sqrt(g["s_scaled"] ** 2 + 0.0)
    z_lo = (g["A"] - 1) / s_tot
    z_pz = (g["A"] * 1.10 - 1) / s_tot                              # one-sided photo-z allowance: true A up to 10 % higher
    zD2 = z_lo if g["A"] > 1 else (0.0 if 1.10 * g["A"] >= 1 else z_pz)      # true A in [A, 1.1 A] (photo-z dilution, one-sided)
    D2[foot] = dict(fit=g, s_tot=s_tot, z=z_lo, z_photoz=z_pz, z_used=zD2, chi2_L_GH1=GH1J["footings"][foot]["chi2_L"])
    P(f"  D2 [{foot}] GH1 matched hosts 50-300 kpc: A = {g['A']:.4f} +- {g['s_stat']:.4f} (x{g['scale']:.2f} -> {g['s_scaled']:.4f}); "
      f"(A-1)/sigma = {z_lo:+.2f} ({z_pz:+.2f} with +10 % photo-z); chi2 at A=1 {g['chi2_at_A1']:.1f} (GH1 recorded law {GH1J['footings'][foot]['chi2_L']:.1f}); "
      f"chi2_min {g['chi2']:.1f}/{g['n'] - 1}")
    RES.setdefault("K3", {})[foot] = abs(g["chi2_at_A1"] / GH1J["footings"][foot]["chi2_L"] - 1)
RES["D2"] = D2
if not MUT:
    k3 = max(RES["K3"].values())
    check("W3-K3", k3 <= 1e-9, f"chi2 of the law at A = 1 reproduces GH1's recorded chi2_L: max rel {k3:.1e} (<= 1e-9)")

# ============================================================ satellites (reported, not graded)
X75 = json.load(open(os.path.join(REB, "X75_satellite_kinematics_mass_gap", "x75_satkin_results.json")))
sig = np.array(X75["measured"]["pair"]["sigma"]); sige = np.array(X75["measured"]["pair"]["err"])
SAT = {}
for foot in FOOTS:
    law = np.array(X75["footings"][foot]["law_pred"])
    Ad = (sig / law) ** 2; sAd = 2 * Ad * sige / sig
    w = 1 / sAd ** 2; Am = float(np.sum(w * Ad) / np.sum(w)); sAm = float(1 / math.sqrt(np.sum(w)))
    SAT[foot] = dict(A_dyn_per_bin=Ad.tolist(), err=sAd.tolist(), A_dyn_mean=Am, err_mean=sAm,
                     GH1_Delta_lens=GH1J["footings"][foot]["D"], GH1_Delta_sat=GH1J["footings"][foot]["D_sat"],
                     method_systematic_dex=GH1J["footings"][foot]["D_sat"] - GH1J["footings"][foot]["D"])
    P(f"  satellites [{foot}] (not graded): A_dyn = (sigma/sigma_law)^2 per bin " + ", ".join(f"{a:.2f}+-{e:.2f}" for a, e in zip(Ad, sAd)) +
      f"; weighted {Am:.2f}+-{sAm:.2f}. GH1 matched hosts: lensing Delta {GH1J['footings'][foot]['D']:+.2f}, satellites {GH1J['footings'][foot]['D_sat']:+.2f} "
      f"-> satellite method systematic {SAT[foot]['method_systematic_dex']:+.2f} dex in M200")
RES["satellites"] = SAT

# ============================================================ predicted ratio (W1's Psi equation at galaxy scale)
cl = 2.99792458e8; KPC = 3.0857e19
PRED = {}
for foot, A0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    ag = A0 / cl ** 2
    PRED[foot] = {f"{R:g}kpc": 2 * ag * R * KPC * (1 + abs(math.log(3000 / R))) for R in (30, 100, 310, 2600)}
    P(f"  predicted |M_lens/M_dyn - 1| (bound, W1 Psi-equation with the a0-cap source, cutoff 3 Mpc): " + ", ".join(f"{k} {v:.1e}" for k, v in PRED[foot].items()))
RES["predicted_ratio_bound"] = PRED

# ============================================================ labels
labels = {}
for foot in FOOTS:
    z1 = D1[foot]["z"]; z2 = D2[foot]["z_used"]
    okc = all(CHK.values())
    if not okc:
        labels[foot] = "UNDECIDED (a W3 check failed)"
    elif abs(z1) <= 2 and abs(z2) <= 2:
        labels[foot] = f"PASS: A_D1 = {D1[foot]['fits']['primary']['A']:.3f} +- {D1[foot]['s_tot']:.3f} ({z1:+.1f} sigma), A_D2 = {D2[foot]['fit']['A']:.3f} +- {D2[foot]['s_tot']:.3f} ({z2:+.1f} sigma)"
    elif abs(z1) > 2 or abs(z2) > 3:
        labels[foot] = f"FAIL: A_D1 = {D1[foot]['fits']['primary']['A']:.3f} +- {D1[foot]['s_tot']:.3f} ({z1:+.1f} sigma), A_D2 = {D2[foot]['fit']['A']:.3f} +- {D2[foot]['s_tot']:.3f} ({z2:+.1f} sigma)"
    else:
        labels[foot] = f"UNDECIDED: D1 {z1:+.1f} sigma passes, D2 {z2:+.1f} sigma between 2 and 3"
    P(f"W3 [{foot}]: {labels[foot]}")
RES["labels"] = labels
if MUT:
    bite = all(labels[f].startswith("FAIL") for f in FOOTS)
    check("W3-MUTATE-bites", not bite, f"Newtonian-baryon lensing gives a FAIL label in both footings: {bite} "
          f"(D1 {D1['canonical']['z']:+.2f} / {D1['alt']['z']:+.2f} sigma_tot, D2 {D2['canonical']['z_used']:+.2f} / {D2['alt']['z_used']:+.2f}); the twin must fail this. "
          f"First MUTATE execution tested D1 alone (> 2 sigma) and did not trip: D1's frozen sigma_tot scales with A")
n_ok = sum(CHK.values())
P(f"\nW3 COMPLETE: {n_ok}/{len(CHK)} checks PASS")


def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)): return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    return o


json.dump(clean(RES), open(os.path.join(HERE, f"w3_lensing{TAG}.json"), "w"), indent=1, sort_keys=True)
open(os.path.join(HERE, f"w3_lensing{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if n_ok == len(CHK) else 1)
