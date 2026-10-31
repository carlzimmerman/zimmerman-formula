#!/usr/bin/env python3
"""KN1_kids_native_halos (FROZEN_CRITERIA.md): X53's harness with ZN1's native shape in place of the core rule. One run:
    KN1_MASS=em1|am1 KN1_NORM=tot|fc1 KN1_SNAP=0.25|0.00 KN1_RX=1 KN1_TAG=name python3 kn1_kids.py
    python3 kn1_kids.py --k1    # FC1's rule as a table reproduces FC1's KiDS numbers
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, sys
import numpy as np
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
os.environ.pop("X53_MUTATE", None)
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); K1 = "--k1" in sys.argv; TAG = "k1" if K1 else os.environ["KN1_TAG"]
X53D = os.path.join(REB, "X53_outer_lensing_law_vs_halos"); SRC = os.path.join(X53D, "x53_outer_lensing.py"); src = open(SRC).read(); CE = json.load(open(os.path.join(REB, "CE1_converged_eta_grade", "ce1_results.json")))["eta"]; FC = (lambda om, ob: (om - ob) / om)(0.2976016, 0.0223081 / 0.6856427 ** 2); EV = [FC * CE[str(e)]["med"] for e in (12, 13, 14)]
def rep(a, b):
    global src
    assert src.count(a) == 1, (a[:70], src.count(a)); src = src.replace(a, b)
B_S = 'def B(x):\n    x = np.asarray(x, float)\n    return 4 * (np.arcsinh(x) - x / np.sqrt(1 + x * x))\n'
rep("def B(x):\n    x = np.asarray(x, float); return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)\n", B_S)
rep("    return 4.0 / (3.0 * B1) * cf ** 1.25\n", "    return 4.0 / (3.0 * B1) * cf ** 1.25 * B1 / float(B(1.0))\n")
rep("(St / r0t) * r0t ** 3 / ((r + r0t) * (r * r + r0t * r0t))", "(St / r0t) * r0t ** 3 / (r * r + r0t * r0t) ** 1.5")
rep("def eta_of(M, cfmode):\n", "def _eta_of_x53(M, cfmode):\n")
NEW = f'''_EL = np.array([12.0, 13.0, 14.0]); _EV = np.array({EV!r})
def eta_of(M, cfmode):
    if cfmode != "cf4": return _eta_of_x53(M, cfmode)
    return float(np.interp(math.log10(M), _EL, _EV))
'''
rep(B_S, NEW + B_S)
DEF = f'''
KN1 = dict(on=True, k1={K1!r}, mass=os.environ.get("KN1_MASS", "em1"), norm="fc1" if {K1!r} else os.environ.get("KN1_NORM", "tot"), snap=os.environ.get("KN1_SNAP", "0.25"), rx=float(os.environ.get("KN1_RX", "1")), n=0, below=0, fc={FC!r}, T=[], X=None)
def kn1_k1_table():
    bg_ = BG["A_c2b_refit"]; rhoc_ = 2.775e11 * bg_["h"] ** 2 / 1e18; Xg_ = np.geomspace(1e-3, 40.0, 500); KN1["X"] = np.log(Xg_); T_ = []
    for l_ in np.arange(7.5, 15.5, 0.02):
        M2_ = 10.0 ** l_; R2_ = (3 * M2_ / (4 * math.pi * 200 * rhoc_)) ** (1 / 3); Sg_ = max(SIGA0["canonical"], eta_of(M2_, "cf4") * sigma_coll(M2_)); r0_ = solve_r0(M2_, R2_, Sg_); T_.append((float(l_), np.log(math.pi * Sg_ * r0_ ** 2 * B(np.minimum(Xg_, 1.0) * R2_ / r0_) / M2_), 40.0))
    KN1["T"] = T_
if not KN1["k1"]:
    _J = json.load(open(os.path.join({REB!r}, "ZN1_zooms_to_z0", "zn1_shapes.json"))); KN1["X"] = np.log(np.array(_J["x"])); KN1["T"] = sorted(((_J[m_][KN1["snap"]]["lgM"], np.array(_J[m_][KN1["snap"]]["lnm"]), _J[m_][KN1["snap"]]["x_edge"]) for m_ in ("1e12", "1e13", "1e14")), key=lambda t_: t_[0])
    if KN1["mass"] == "am1": _A = json.load(open(os.path.join({REB!r}, "AM1_native_abundance_match", "am1_results.json")))["curve"]; KN1["A"] = (np.array(_A["lMb"]), np.array(_A["lM200"]))
def kn1_lm(lb, bg):
    return float(np.interp(lb, *KN1["A"])) if KN1["mass"] == "am1" else bg["a"] + bg["b"] * (lb - 10.0)
def kn1_shape(lg):
    if KN1["k1"] and not KN1["T"]: kn1_k1_table()
    T_ = KN1["T"]; KN1["n"] += 1
    if lg <= T_[0][0]: KN1["below"] += 1; return T_[0][1], T_[0][2]
    if lg >= T_[-1][0]: return T_[-1][1], T_[-1][2]
    k_ = next(i_ for i_ in range(len(T_) - 1) if T_[i_][0] <= lg <= T_[i_ + 1][0]); w_ = (lg - T_[k_][0]) / (T_[k_ + 1][0] - T_[k_][0]); return (1 - w_) * T_[k_][1] + w_ * T_[k_ + 1][1], min(T_[k_][2], T_[k_ + 1][2])
def kn1_mass(Mc, bg, r, zs):
    Ez2 = 1.0 if zs is None else OM_NAT * (1 + zs) ** 3 + 1 - OM_NAT; rhoc = 2.775e11 * bg["h"] ** 2 * Ez2 / 1e18; fc_ = KN1["fc"]; Mt_ = Mc / fc_; M_, R_ = (fc_ * Mt_, (3 * Mt_ / (4 * math.pi * 200 * rhoc)) ** (1 / 3)) if KN1["norm"] == "tot" else (Mc, (3 * Mc / (4 * math.pi * 200 * rhoc)) ** (1 / 3))
    ln_, xe_ = kn1_shape(math.log10(Mc if KN1["k1"] else Mt_)); x_ = np.minimum(np.asarray(r, float) / (R_ * KN1["rx"]), xe_); lx_ = np.log(np.maximum(x_, 1e-300)); return M_ * np.exp(np.where(lx_ >= KN1["X"][0], np.interp(lx_, KN1["X"], ln_), ln_[0] + 2 * (lx_ - KN1["X"][0]))), R_
'''
rep("def halo_setup(foot, logMbrel, cfg_h):", DEF + "\ndef halo_setup(foot, logMbrel, cfg_h):")
rep('''    M200, R200, r0, Sig, above = halo_setup(foot, math.log10(Ms + Mc), cfg_h)
    rcut = 100 * R200 if MUT else R200
''', '''    if KN1["on"]:
        bg_ = BG[cfg_h["bg"]]; lc_ = kn1_lm(math.log10(Ms + Mc), bg_); Mh_, Rr_ = kn1_mass(10 ** lc_, bg_, RGRID_PC, None if KN1["k1"] else float(KN1["snap"])); return Mb + Mh_, (10 ** lc_, Rr_, 0.0, True)
    M200, R200, r0, Sig, above = halo_setup(foot, math.log10(Ms + Mc), cfg_h)
    rcut = 100 * R200 if MUT else R200
''')
rep('os.path.join(HERE, f"x53_outer_lensing_results{SFX}.json")', repr(os.path.join(HERE, f"kn1_results_{TAG}.json")))
rep('os.path.join(HERE, f"x53_outer_lensing{SFX}.out")', repr(os.path.join(HERE, f"kn1_{TAG}.out")))
ns = {"__file__": SRC, "__name__": "__main__"}; sys.argv = [SRC]
try: exec(compile(src, SRC, "exec"), ns)
except SystemExit: pass
R = json.load(open(os.path.join(HERE, f"kn1_results_{TAG}.json"))); L = []
def row(RR, lab): return "; ".join(f"[{f}] {g}: dchi2 {RR['footings'][f][g]['dchi2_H2H_minus_L2H']:+.1f}, H2H {RR['footings'][f][g]['H2H']['chi2']:.1f}, L2H {RR['footings'][f][g]['L2H']['chi2']:.1f}, b {[round(v, 2) for v in RR['footings'][f][g]['H2H']['b']]}" for f in ("canonical", "alt") for g in ("primary", "all"))
if K1:
    base = json.load(open(os.path.join(REB, "FC1_cold_share_native_eta", "x79_rule", "x79_kids_results_native.json")))["footings"]["canonical"]; Rk = R["footings"]["canonical"]; da = abs(Rk["all"]["H2H"]["chi2"] - base["all"]["H2H"]["chi2"]); dp = abs(Rk["primary"]["H2H"]["chi2"] - base["primary"]["H2H"]["chi2"]); dl = abs(Rk["all"]["L2H"]["chi2"] - base["all"]["L2H"]["chi2"]); ok = da <= 1.0; L.append(f"K1 FC1's rule as a table through this path, canonical: H2H all {Rk['all']['H2H']['chi2']:.3f} vs {base['all']['H2H']['chi2']:.3f} (|d| {da:.3f}, limit 1.0); primary |d| {dp:.3f}; law arm |d| {dl:.1e}: {'PASS' if ok else 'FAIL'}"); open(os.path.join(HERE, "kn1_k1.out"), "w").write("\n".join(L) + "\n")
print("\n".join(L)) if L else None
KN = ns["KN1"]; out = dict(tag=TAG, mass=KN["mass"], norm=KN["norm"], snap=KN["snap"], rx=KN["rx"], below=KN["below"], n=KN["n"], footings={f: {g: dict(dchi2=R["footings"][f][g]["dchi2_H2H_minus_L2H"], H2H=R["footings"][f][g]["H2H"]["chi2"], L2H=R["footings"][f][g]["L2H"]["chi2"], b=R["footings"][f][g]["H2H"]["b"], per_bin=R["footings"][f][g]["per_bin_dchi2_2h"]) for g in ("primary", "all")} for f in ("canonical", "alt")}, verdict={f: R["footings"][f]["verdict"] for f in ("canonical", "alt")})
json.dump(out, open(os.path.join(HERE, f"kn1_grade_{TAG}.json"), "w"), indent=1, default=float); print(f"KN1 {TAG}: {row(R, TAG)}; verdict {out['verdict']}; below the 1e12 tag {KN['below']} of {KN['n']}")
