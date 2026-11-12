#!/usr/bin/env python3
"""SS4 (FROZEN_CRITERIA.md f3effad98c): variant K's linear growth. A three-fluid ODE (baryons, half 1, half 2), the record's QX3
iter2 Jeans form generalised: after onset each pressured half i obeys
    delta_i'' + (2 + dlnH) delta_i' = (3/2) sum_j Omega_j delta_j - (c_s,i k / (a H))^2 delta_i,
c_s2 = v_stiff (field), c_s1 = R_c1 H sqrt(1.5 Omega_m) / pi (k_J1 = pi a / R_c1, R_c1 physical). The background is unchanged
(no conversion). Outputs: sigma8, S8 and the CS gate (|S8_K/S8_ref - 1| <= 5.9 %), P(k) ratios at k 0.3 / 1 / 3 h/Mpc at
z 0.3 / 0.5, fsigma8 (CE2, fine grid), forest (z > onset: unchanged), 7(b) reading, KA-K3 (c_s -> 0 gives R = 1).
    SS1_FOOT=<f> SS4_V=K|Kform|MK2 python3 ss4_cosmo.py   -> parts/vcosmo_<V>_<f>.json
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json, math, io, contextlib
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SS1 = os.path.join(REPO, "closure_2026_11_09", "SS1_self_shielded_conversion"); sys.path.insert(0, SS1); sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import numpy as np
FOOT = os.environ.get("SS1_FOOT", "canonical"); V = os.environ.get("SS4_V", "K")
_a = sys.argv; sys.argv = ["ss4.py", "none", V]
with contextlib.redirect_stdout(io.StringIO()):
    import ss4 as S4
sys.argv = _a
src = open(os.path.join(SS1, "ss1_cosmo.py")).read(); cut = src.index("# ================================================================== run")
ns = {"__file__": os.path.join(SS1, "ss1_cosmo.py"), "__name__": "ss1c_ss4"}; a_ = sys.argv; sys.argv = ["ss1_cosmo.py"]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:cut], "ss1c", "exec"), ns)
sys.argv = a_
p = S4.vparK(V, FOOT); F = p["F"]; M = ns["M"]; OD, OB = ns["OD"], ns["OB"]; REFBG = ns["REFBG"]; KG, ZG = ns["KG"], ns["ZG"]; hh = F["h"]
ZF = np.linspace(0.0, 1.2, 241); EP = np.concatenate([ZG, ZF])
z = REFBG["z"]; lna_t = np.log(1 / (1 + z)); o = np.argsort(lna_t); lna_t = lna_t[o]; lnH = np.log(REFBG["H"][o]); dlnH = np.gradient(lnH, lna_t)
def solve(on, scale=1.0):
    ai = 1 / 3401.0; adec = 1 / 1091.0; nk = len(KG); grid = np.unique(np.concatenate([np.linspace(math.log(ai), 0.0, 6001), np.log(1 / (1 + EP))])); keys = set(float(x) for x in np.log(1 / (1 + EP)))
    y = np.zeros((nk, 6)); y[:, 0] = ai; y[:, 1] = ai; y[:, 4] = ai; y[:, 5] = ai; rec = {}; I6 = np.eye(6)[None, :, :]
    for n in range(len(grid) - 1):
        h_ = grid[n + 1] - grid[n]; lm = 0.5 * (grid[n] + grid[n + 1]); a = math.exp(lm); zz = 1 / a - 1
        Hk = math.exp(np.interp(lm, lna_t, lnH)); E2 = Hk ** 2 / 100.0 ** 2; dl = float(np.interp(lm, lna_t, dlnH))
        Oh = 0.5 * OD * a ** -3 / E2; Ob = OB * a ** -3 / E2; Om = 2 * Oh + Ob
        p1 = np.zeros(nk); p2 = np.zeros(nk)
        if on and zz < p["z_dec"]:
            cs1 = scale * (p["rc1"] / 1000.0) * Hk * math.sqrt(1.5 * Om) / math.pi; cs2 = scale * p["v_stiff"]
            p1 = (cs1 * KG / (a * Hk)) ** 2; p2 = (cs2 * KG / (a * Hk)) ** 2
        A = np.zeros((nk, 6, 6))
        for i, pr in ((0, p1), (4, p2)):                                       # halves: rows (0,1) half 1, (4,5) half 2
            A[:, i, i + 1] = 1; A[:, i + 1, 0] += 1.5 * Oh; A[:, i + 1, 4] += 1.5 * Oh; A[:, i + 1, i] -= pr; A[:, i + 1, i + 1] = -(2 + dl)
            if a > adec: A[:, i + 1, 2] += 1.5 * Ob
        if a > adec: A[:, 2, 3] = 1; A[:, 3, 0] = 1.5 * Oh; A[:, 3, 4] = 1.5 * Oh; A[:, 3, 2] = 1.5 * Ob; A[:, 3, 3] = -(2 + dl)
        y = np.linalg.solve(I6 - 0.5 * h_ * A, ((I6 + 0.5 * h_ * A) @ y[:, :, None]))[:, :, 0]
        if float(grid[n + 1]) in keys: rec[float(grid[n + 1])] = y.copy()
    out = np.array([OB * rec[k][:, 2] + 0.5 * OD * (rec[k][:, 0] + rec[k][:, 4]) for k in (float(x) for x in np.log(1 / (1 + EP)))]).T
    return out[:, :len(ZG)], out[:, len(ZG):]
(o1, f1), (o0, f0) = solve(True), solve(False); Rr = o1 / o0; RF_ = f1 / f0
(k1, _), _ = solve(True, scale=0.0), None; ka3 = float(np.max(np.abs(k1 / o0 - 1)))
R8 = 8.0 / hh; lk = np.log(KG); W8 = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3; w2k3 = W8(KG * R8) ** 2 * KG ** 3 / (2 * np.pi ** 2)
PrefF = np.array([[M.pk_lin(k_, z_) for z_ in ZF] for k_ in KG]); s8F = lambda RR: np.sqrt(np.trapz(PrefF * RR ** 2 * w2k3[:, None], lk, axis=0))
lnaF = np.log(1 / (1 + ZF)); sK, sR = s8F(RF_), s8F(np.ones_like(RF_)); rrF = np.gradient(sK, lnaF) / np.gradient(sR, lnaF)
rows = []
for (tb, zb, r1, p1_, m1, r2, p2_, m2) in ns["DESI"]:
    e1, e2 = 0.5 * (p1_ + m1), 0.5 * (p2_ + m2); x = float(np.interp(zb, ZF, rrF)); rows.append(dict(bin=tb, z=zb, Rf=x, in_sf=bool(abs(x - r1) <= 2 * e1), in_sfb=bool(abs(x - r2) <= 2 * e2), s8dir=bool(x <= 1.001)))
fs_pass = all(r["in_sf"] and r["in_sfb"] and r["s8dir"] for r in rows)
s8_ref = float(M.sigma8()); s8r = float(sK[0] / sR[0]); Om0 = (OB + OD) / hh ** 2; S8 = s8_ref * s8r * math.sqrt(Om0 / 0.3); S8ref = s8_ref * math.sqrt(Om0 / 0.3)
cs_ok = abs(S8 / S8ref - 1) <= 2 * 0.0225 / 0.759
pk = {f"z {zz} k {kh} h/Mpc": float(np.interp(math.log(kh * hh), lk, RF_[:, int(np.argmin(abs(ZF - zz)))] ** 2)) for zz in (0.3, 0.5) for kh in (0.3, 1.0, 3.0)}
Sx = ns["limber4_bg"](REFBG, Rr); cl, _ = ns["Q3"]["best_amp_chi2"](ns["X0"] * Sx); FD = ns["forest_setup"](); fr = ns["forest_eval"](FD, REFBG, Rr)
out = dict(variant=V, footing=FOOT, criteria=S4.CRIT, z_dec=p["z_dec"], rc1_kpc=p["rc1"], v_stiff=p["v_stiff"], KA_K3_max_dev=ka3, KA_K3_pass=bool(ka3 < 1e-6),
           cs1_today_kms=(p["rc1"] / 1000.0) * 100 * hh * math.sqrt(1.5 * Om0) / math.pi,
           G6=dict(status="PASS", note="no conversion: background identical to the reference"), sigma8=s8_ref * s8r, sigma8_ref=s8_ref, sigma8_ratio_z0=s8r, S8=S8, S8_ref=S8ref,
           CS=dict(status="PASS" if cs_ok else "FAIL", S8_change=S8 / S8ref - 1, line=2 * 0.0225 / 0.759, Pk_ratio=pk),
           fs8=dict(rows=rows, pass_=bool(fs_pass)), forest=fr, G8=dict(status="PASS" if (fs_pass and fr["status"] == "PASS") else "FAIL"),
           lensing_reading=dict(chi2=float(cl), status="NO VERDICT (no validated method)"), F_conv_today=0.0, lambda_today_Mpc=0.0)
def clean(x):
    if isinstance(x, dict): return {str(k): clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [clean(v) for v in x]
    if isinstance(x, (np.floating, np.integer)): return x.item()
    if isinstance(x, np.bool_): return bool(x)
    return x
json.dump(clean(out), open(os.path.join(HERE, "parts", f"vcosmo_{V}_{FOOT}.json"), "w"), indent=1)
print(f"[{FOOT}] {V}: KA-K3 dev {ka3:.1e}; c_s1 today {out['cs1_today_kms']:.1f} km/s; sigma8 {out['sigma8']:.3f} (ratio {s8r:.3f}) S8 {S8:.3f} (ref {S8ref:.3f}, change {S8/S8ref-1:+.1%}) -> CS {out['CS']['status']}; "
      f"P ratio " + " ".join(f"{k} {v:.3f}" for k, v in pk.items()) + f"; Rf " + " ".join(f"{r['bin']} {r['Rf']:.3f}" for r in rows) + f" -> gate 8 {out['G8']['status']}; lensing reading {cl:.2f}; forest {fr['dchi2']:.3f}", flush=True)
